"""
Library Finder Skill

Finds Python libraries on PyPI that are good candidates for skill generation
via library_skill_generator. Queries PyPI API and scores candidates on
relevance, maintenance, popularity, and API quality signals.
"""

import datetime as dt
import logging
import os
import time
from typing import Any, Dict, List, Optional
from urllib.parse import quote

import httpx

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.normpath(os.path.join(CURRENT_DIR, "..", "..", "..", ".."))
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
REGISTRY_DB_PATH = os.path.join(DATA_DIR, "skill_registry.db")

_session_cache: Dict[str, Any] = {}
_cache_ttl = 300


class PyPIFinder:
    """PyPI library finder with scoring capabilities."""

    POPULAR_KEYWORDS = {
        "data": ["pandas", "numpy", "dask", "polars", "pyspark", "modin", "vaex"],
        "validation": [
            "pydantic",
            "jsonschema",
            "cerberus",
            "voluptuous",
            "marshmallow",
            "attrs",
            "cattrs",
            "email-validator",
        ],
        "api": ["fastapi", "flask", "django", "bottle", "tornado", "starlette", "hug"],
        "http": ["requests", "httpx", "aiohttp", "urllib3", "httplib2", "pycurl"],
        "ml": [
            "scikit-learn",
            "tensorflow",
            "pytorch",
            "keras",
            "xgboost",
            "lightgbm",
            "catboost",
            "transformers",
        ],
        "nlp": [
            "nltk",
            "spacy",
            "transformers",
            "huggingface-hub",
            "textblob",
            "gensim",
            "flair",
        ],
        "database": [
            "sqlalchemy",
            "psycopg2",
            "pymongo",
            "redis",
            "sqlite3",
            "asyncpg",
            "aiomysql",
        ],
        "testing": [
            "pytest",
            "unittest",
            "nose2",
            "tox",
            "mock",
            "pytest-asyncio",
            "hypothesis",
        ],
        "logging": ["logging", "loguru", "structlog", "colorlog"],
        "config": [
            "pyyaml",
            "toml",
            "python-dotenv",
            "configparser",
            "hydra",
            "omegaconf",
        ],
        "serialization": [
            "json",
            "msgpack",
            "protobuf",
            "orjson",
            "ujson",
            "pickle",
            "cbor2",
        ],
        "time": [
            "datetime",
            "arrow",
            "python-dateutil",
            "pytz",
            "zoneinfo",
            "pendulum",
        ],
        "async": ["asyncio", "aiohttp", "httpx", "uvicorn", "celery", "taskiq"],
        "web": [
            "beautifulsoup4",
            "selenium",
            "playwright",
            "scrapy",
            "lxml",
            "requests-html",
        ],
        "cli": ["click", "typer", "argparse", "docopt", "fire", "cement"],
        "image": ["Pillow", "opencv-python", "scikit-image", "imageio", "wand"],
        "excel": ["openpyxl", "xlsxwriter", "xlrd", "xlwt", "pandas", "pyexcel"],
        "pdf": ["pypdf", "pdfplumber", "pikepdf", "PyPDF2", "reportlab"],
        "docx": ["python-docx", "docxtpl", "python-docx2txt"],
        "auth": [
            "pyjwt",
            "passlib",
            "bcrypt",
            "cryptography",
            "python-jose",
            "authlib",
        ],
        "security": ["safety", "bandit", "pip-audit", "snyk", "OWASP"],
    }

    def __init__(self, timeout: int = 10, max_retries: int = 3):
        self.timeout = timeout
        self.max_retries = max_retries
        self.base_url = "https://pypi.org/pypi"
        self.stats_url = "https://pypistats.org/api/packages"
        self.search_url = "https://pypi.org/search"

    async def search_libraries(
        self, query: str, limit: int = 10, exclude: Optional[List[str]] = None
    ) -> List[Dict[str, Any]]:
        """
        Search PyPI for libraries matching the query.
        Uses curated keyword lists for popular packages, then fetches details.
        """
        exclude = exclude or []
        results = []
        query_lower = query.lower()
        query_terms = set(query_lower.split())

        candidate_names = set()
        keyword_matches = set()

        # Check curated keywords for matches - prioritize these
        for key, packages in self.POPULAR_KEYWORDS.items():
            if key in query_lower:
                keyword_matches.update(packages)
            for term in query_terms:
                if term in key:
                    keyword_matches.update(packages)

        # Add keyword matches first
        candidate_names.update(keyword_matches)

        # Also search by term matching in package names from simple API
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            simple_api_url = "https://pypi.org/simple/"

            try:
                response = await self._fetch_with_retry(
                    client,
                    simple_api_url,
                    {"Accept": "application/vnd.pypi.simple.v1+json"},
                )

                if response.status_code == 200:
                    all_packages = response.json().get("projects", [])

                    for p in all_packages:
                        if not isinstance(p, dict):
                            continue
                        name = p.get("name", "")
                        if not name or name in exclude or name in keyword_matches:
                            continue

                        name_lower = name.lower()
                        if any(term in name_lower for term in query_terms):
                            candidate_names.add(name)

            except Exception as e:
                logger.error("Search error: {}".format(e))

        candidate_names = [n for n in candidate_names if n not in exclude]

        # Prioritize keyword matches (keep original order), then add others sorted by length
        keyword_list = [n for n in candidate_names if n in keyword_matches]
        other_list = sorted(
            [n for n in candidate_names if n not in keyword_matches],
            key=lambda x: (len(x), x),
        )

        candidate_names = keyword_list + other_list
        candidate_names = candidate_names[: limit * 3]

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            for pkg_name in candidate_names:
                try:
                    details = await self._fetch_package_details(client, pkg_name)
                    if details:
                        results.append(details)
                        if len(results) >= limit:
                            break
                except Exception as e:
                    logger.debug("Error fetching {}: {}".format(pkg_name, e))
                    continue

        return results[:limit]

    async def _fetch_with_retry(
        self,
        client: httpx.AsyncClient,
        url: str,
        headers: Optional[Dict[str, str]] = None,
        retry_count: int = 0,
    ) -> httpx.Response:
        """Fetch URL with exponential backoff retry."""
        try:
            response = await client.get(url, headers=headers)
            if response.status_code == 429 and retry_count < self.max_retries:
                wait_time = (2**retry_count) * 0.5
                time.sleep(wait_time)
                return await self._fetch_with_retry(
                    client, url, headers, retry_count + 1
                )
            return response
        except httpx.TimeoutException:
            if retry_count < self.max_retries:
                wait_time = (2**retry_count) * 0.5
                time.sleep(wait_time)
                return await self._fetch_with_retry(
                    client, url, headers, retry_count + 1
                )
            raise

    async def _fetch_package_details(
        self, client: httpx.AsyncClient, package_name: str
    ) -> Optional[Dict[str, Any]]:
        """Fetch detailed package information from PyPI."""
        url = "{}/{}/json".format(self.base_url, package_name)

        try:
            response = await self._fetch_with_retry(client, url)
            if response.status_code == 200:
                data = response.json()
                info = data.get("info", {})
                return {
                    "name": info.get("name", package_name),
                    "description": info.get("summary", "")
                    or info.get("description", ""),
                    "version": info.get("version", "unknown"),
                    "homepage": info.get("home_page", ""),
                    "docs_url": info.get("docs_url", ""),
                    "project_urls": info.get("project_urls", {}),
                    "requires_python": info.get("requires_python", ""),
                    "latest_release_date": info.get("release_date"),
                    "data": data,
                }
        except Exception as e:
            logger.debug("Error fetching details for {}: {}".format(package_name, e))

        return None

    async def get_download_stats(
        self, client: httpx.AsyncClient, package_name: str
    ) -> int:
        """Get monthly download count from pypistats."""
        url = "{}/{}/recent".format(self.stats_url, package_name)

        try:
            response = await self._fetch_with_retry(client, url)
            if response.status_code == 200:
                data = response.json()
                downloads = data.get("views", [{}])[0].get("downloads", 0)
                return downloads
        except Exception:
            pass

        return 0


class LibraryScorer:
    """Scores libraries based on quality signals."""

    WEIGHTS = {
        "relevance": 0.4,
        "maintenance": 0.3,
        "popularity": 0.2,
        "api_quality": 0.1,
    }

    def __init__(self, query: str):
        self.query = query.lower()
        self.query_terms = set(self.query.split())

    def calculate_relevance(self, package: Dict[str, Any]) -> float:
        """Calculate relevance score based on query matching."""
        name = package.get("name", "").lower()
        description = (package.get("description") or "").lower()

        score = 0.0

        if self.query in name:
            score += 1.0
        elif any(term in name for term in self.query_terms):
            score += 0.5

        if self.query in description:
            score += 0.5

        description_words = set(description.split())
        matches = len(self.query_terms & description_words)
        if matches > 0:
            score += min(matches / len(self.query_terms), 0.5)

        return min(score, 1.0)

    def calculate_maintenance(self, package: Dict[str, Any]) -> float:
        """Calculate maintenance score based on update recency."""
        release_date_str = package.get("latest_release_date")

        if not release_date_str:
            urls = package.get("project_urls", {})
            if isinstance(urls, dict):
                for url in urls.values():
                    if "github.com" in url or "gitlab.com" in url:
                        return 0.3

            data = package.get("data", {})
            releases = data.get("releases", {})
            if releases:
                latest = list(releases.keys())[-1]
                try:
                    release_date = dt.datetime.fromisoformat(
                        latest.replace("Z", "+00:00")
                    )
                    age_months = (
                        dt.datetime.now(dt.timezone.utc) - release_date
                    ).days / 30
                    if age_months <= 12:
                        return 1.0
                    elif age_months <= 24:
                        return 0.5
                except Exception:
                    pass
            return 0.1

        try:
            release_date = dt.datetime.fromisoformat(
                release_date_str.replace("Z", "+00:00")
            )
            age_months = (dt.datetime.now(dt.timezone.utc) - release_date).days / 30

            if age_months <= 12:
                return 1.0
            elif age_months <= 24:
                return 0.5
            else:
                return 0.1
        except Exception:
            return 0.1

    def calculate_popularity(self, downloads: int) -> float:
        """Calculate popularity score based on download count."""
        if downloads > 1_000_000:
            return 1.0
        elif downloads > 100_000:
            return 0.7
        elif downloads > 10_000:
            return 0.4
        elif downloads > 1_000:
            return 0.2
        else:
            return 0.1

    def calculate_api_quality(self, package: Dict[str, Any]) -> float:
        """Calculate API quality score based on documentation presence."""
        score = 0.0

        homepage = package.get("homepage", "")
        docs_url = package.get("docs_url", "")
        project_urls = package.get("project_urls", {})

        if docs_url:
            score += 0.5
        elif homepage and (
            "docs" in homepage.lower() or "readthedocs" in homepage.lower()
        ):
            score += 0.5
        elif homepage:
            score += 0.2

        if isinstance(project_urls, dict):
            source_urls = [
                v
                for k, v in project_urls.items()
                if "github" in k.lower() or "source" in k.lower()
            ]
            if source_urls:
                score += 0.3
            elif homepage and ("github.com" in homepage or "gitlab.com" in homepage):
                score += 0.3

        requires_python = package.get("requires_python", "")
        if requires_python:
            if "3.12" in requires_python or "3.13" in requires_python:
                score += 0.2

        return min(score, 1.0)

    def score_package(
        self, package: Dict[str, Any], downloads: int = 0
    ) -> Dict[str, Any]:
        """Calculate composite score for a package."""
        relevance = self.calculate_relevance(package)
        maintenance = self.calculate_maintenance(package)
        popularity = self.calculate_popularity(downloads)
        api_quality = self.calculate_api_quality(package)

        composite = (
            relevance * self.WEIGHTS["relevance"]
            + maintenance * self.WEIGHTS["maintenance"]
            + popularity * self.WEIGHTS["popularity"]
            + api_quality * self.WEIGHTS["api_quality"]
        )

        return {
            "score": round(composite, 3),
            "signals": {
                "relevance": round(relevance, 3),
                "maintenance": round(maintenance, 3),
                "popularity": round(popularity, 3),
                "api_quality": round(api_quality, 3),
            },
        }


def register_skill() -> Dict[str, Any]:
    """Register this skill in the skill registry."""
    import sqlite3
    import json

    conn = sqlite3.connect(REGISTRY_DB_PATH)
    cursor = conn.cursor()

    skill_id = "library_finder"
    domain = "skill_management"
    name = "Library Finder"
    module_path = "library_finder"
    entry_function = "invoke"
    description = "Finds Python libraries on PyPI for skill generation"
    dependencies = json.dumps(["httpx", "aiohttp"])

    cursor.execute(
        """
        INSERT OR REPLACE INTO skills 
        (skill_id, name, domain, module_path, entry_function, description, dependencies)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """,
        (
            skill_id,
            name,
            domain,
            module_path,
            entry_function,
            description,
            dependencies,
        ),
    )

    conn.commit()
    conn.close()

    return {"status": "registered", "skill_id": skill_id}


async def invoke(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Find Python libraries on PyPI that are good candidates for skill generation.

    Args:
        payload: Dict containing:
            - query: str — domain name or task description
            - limit: int (optional, default 10) — max results
            - min_score: float (optional, default 0.5) — minimum quality score
            - exclude: list (optional) — library names to skip

    Returns:
        Dict with result containing candidates list and metadata
    """
    query = payload.get("query", "")
    limit = payload.get("limit", 10)
    min_score = payload.get("min_score", 0.5)
    exclude = payload.get("exclude", [])

    if not query:
        return {
            "result": {"candidates": [], "error": "Query is required"},
            "metadata": {"timestamp": dt.datetime.now().isoformat(), "query": query},
        }

    cache_key = "{}:{}".format(query, limit)
    if cache_key in _session_cache:
        cached = _session_cache[cache_key]
        if time.time() - cached.get("_cached_at", 0) < _cache_ttl:
            return cached

    finder = PyPIFinder(timeout=10)
    scorer = LibraryScorer(query)

    candidates = []

    try:
        packages = await finder.search_libraries(query, limit * 2, exclude)

        async with httpx.AsyncClient(timeout=10) as client:
            for package in packages:
                try:
                    downloads = await finder.get_download_stats(client, package["name"])
                    scoring = scorer.score_package(package, downloads)

                    if scoring["score"] >= min_score:
                        candidate = {
                            "name": package["name"],
                            "description": package.get("description", "")[:200],
                            "version": package["version"],
                            "score": scoring["score"],
                            "signals": scoring["signals"],
                            "install_cmd": "pip install {}".format(package["name"]),
                            "pypi_url": "https://pypi.org/project/{}".format(
                                package["name"]
                            ),
                        }
                        candidates.append(candidate)
                except Exception as e:
                    logger.debug("Error scoring package: {}".format(e))
                    continue

    except Exception as e:
        logger.error("Library finder error: {}".format(e))
        return {
            "result": {"candidates": [], "error": str(e)},
            "metadata": {
                "timestamp": dt.datetime.now().isoformat(),
                "query": query,
                "total_found": 0,
                "returned_count": 0,
            },
        }

    candidates.sort(key=lambda x: x["score"], reverse=True)
    candidates = candidates[:limit]

    result = {
        "result": {"candidates": candidates},
        "metadata": {
            "timestamp": dt.datetime.now().isoformat(),
            "query": query,
            "total_found": len(candidates),
            "returned_count": len(candidates),
        },
    }

    _session_cache[cache_key] = result
    result["_cached_at"] = time.time()

    return result


if __name__ == "__main__":
    import asyncio

    async def test():
        result = await invoke({"query": "data validation", "limit": 5})
        print(result)

    asyncio.run(test())
