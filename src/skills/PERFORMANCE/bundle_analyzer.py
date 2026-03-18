"""
Bundle Analyzer: Dependency bundle analysis skill

This module provides dependency bundle analysis capabilities:
- Parse package.json, requirements.txt, go.mod files
- Analyze dependencies (size, version, duplicates)
- Detect bloat (unused, outdated, large packages)
- Suggest lighter alternatives
- Generate bundle health summary
"""

import json
import re
from typing import Dict, List, Any, Optional
from dataclasses import dataclass


PACKAGE_SIZES = {
    "moment": {"size": "67KB", "category": "date"},
    "lodash": {"size": "70KB", "category": "utility"},
    "underscore": {"size": "6KB", "category": "utility"},
    "ramda": {"size": "42KB", "category": "utility"},
    "axios": {"size": "18KB", "category": "http"},
    "request": {"size": "17KB", "category": "http"},
    "got": {"size": "12KB", "category": "http"},
    "node-fetch": {"size": "7KB", "category": "http"},
    "react": {"size": "130KB", "category": "framework"},
    "vue": {"size": "90KB", "category": "framework"},
    "angular": {"size": "2MB", "category": "framework"},
    "@angular/core": {"size": "1.5MB", "category": "framework"},
    "jquery": {"size": "87KB", "category": "dom"},
    "bootstrap": {"size": "150KB", "category": "ui"},
    "material-ui": {"size": "450KB", "category": "ui"},
    "@mui/material": {"size": "450KB", "category": "ui"},
    "antd": {"size": "2MB", "category": "ui"},
    "chart.js": {"size": "250KB", "category": "chart"},
    "d3": {"size": "300KB", "category": "chart"},
    "three": {"size": "600KB", "category": "3d"},
    "phaser": {"size": "5MB", "category": "game"},
    "express": {"size": "210KB", "category": "server"},
    "fastify": {"size": "75KB", "category": "server"},
    "koa": {"size": "110KB", "category": "server"},
    "mongoose": {"size": "350KB", "category": "orm"},
    "typeorm": {"size": "450KB", "category": "orm"},
    "prisma": {"size": "15MB", "category": "orm"},
    "sequelize": {"size": "400KB", "category": "orm"},
    "webpack": {"size": "2MB", "category": "bundler"},
    "vite": {"size": "200KB", "category": "bundler"},
    "rollup": {"size": "400KB", "category": "bundler"},
    "ts-node": {"size": "180KB", "category": "runtime"},
    "jest": {"size": "10MB", "category": "testing"},
    "mocha": {"size": "1MB", "category": "testing"},
    "typescript": {"size": "70MB", "category": "language"},
    "babel": {"size": "15MB", "category": "transpiler"},
    "prettier": {"size": "25MB", "category": "formatter"},
    "eslint": {"size": "15MB", "category": "linter"},
    "tslint": {"size": "8MB", "category": "linter"},
    "graphql": {"size": "3KB", "category": "api"},
    "apollo-server": {"size": "1MB", "category": "api"},
    "rxjs": {"size": "1MB", "category": "reactive"},
    "socket.io": {"size": "400KB", "category": "realtime"},
    "ws": {"size": "35KB", "category": "realtime"},
    "redis": {"size": "100KB", "category": "cache"},
    "ioredis": {"size": "150KB", "category": "cache"},
    "passport": {"size": "100KB", "category": "auth"},
    "bcrypt": {"size": "100KB", "category": "auth"},
    "jsonwebtoken": {"size": "30KB", "category": "auth"},
    "sharp": {"size": "20MB", "category": "image"},
    "imagemin": {"size": "500KB", "category": "image"},
    "pdfkit": {"size": "5MB", "category": "pdf"},
    "puppeteer": {"size": "300MB", "category": "browser"},
    "playwright": {"size": "400MB", "category": "browser"},
    "selenium-webdriver": {"size": "50MB", "category": "browser"},
    "better-sqlite3": {"size": "2MB", "category": "database"},
    "pg": {"size": "500KB", "category": "database"},
    "mysql2": {"size": "1MB", "category": "database"},
    "mongodb": {"size": "400KB", "category": "database"},
    "lodash-es": {"size": "70KB", "category": "utility"},
    "date-fns": {"size": "25KB", "category": "date"},
    "dayjs": {"size": "7KB", "category": "date"},
    "clsx": {"size": "1KB", "category": "utility"},
    "classnames": {"size": "6KB", "category": "utility"},
    "zustand": {"size": "15KB", "category": "state"},
    "recoil": {"size": "150KB", "category": "state"},
    "jotai": {"size": "25KB", "category": "state"},
    "immer": {"size": "20KB", "category": "state"},
    "valtio": {"size": "10KB", "category": "state"},
    "helmet": {"size": "50KB", "category": "security"},
    "cors": {"size": "30KB", "category": "security"},
    "express-rate-limit": {"size": "40KB", "category": "security"},
    "joi": {"size": "200KB", "category": "validation"},
    "zod": {"size": "50KB", "category": "validation"},
    "yup": {"size": "100KB", "category": "validation"},
    "ajv": {"size": "100KB", "category": "validation"},
    "glob": {"size": "100KB", "category": "filesystem"},
    "fs-extra": {"size": "20KB", "category": "filesystem"},
    "chokidar": {"size": "100KB", "category": "filesystem"},
    "dotenv": {"size": "10KB", "category": "config"},
    "config": {"size": "30KB", "category": "config"},
    "winston": {"size": "100KB", "category": "logging"},
    "pino": {"size": "50KB", "category": "logging"},
    "morgan": {"size": "20KB", "category": "logging"},
    "compression": {"size": "15KB", "category": "middleware"},
    "multer": {"size": "50KB", "category": "upload"},
    "uuid": {"size": "15KB", "category": "utility"},
    "validator": {"size": "200KB", "category": "validation"},
    "slugify": {"size": "5KB", "category": "utility"},
    "qrcode": {"size": "200KB", "category": "utility"},
    "nodemailer": {"size": "200KB", "category": "email"},
    "sendgrid": {"size": "50KB", "category": "email"},
    "stripe": {"size": "30KB", "category": "payment"},
    "paypal-rest-sdk": {"size": "50KB", "category": "payment"},
    "aws-sdk": {"size": "150MB", "category": "cloud"},
    "@aws-sdk/client-s3": {"size": "5MB", "category": "cloud"},
    "firebase": {"size": "1MB", "category": "cloud"},
    "@google-cloud/storage": {"size": "5MB", "category": "cloud"},
    "twilio": {"size": "30KB", "category": "sms"},
    "nexmo": {"size": "50KB", "category": "sms"},
    "snyk": {"size": "100KB", "category": "security"},
    "sentry": {"size": "300KB", "category": "monitoring"},
    "newrelic": {"size": "1MB", "category": "monitoring"},
    "datadog-metrics": {"size": "50KB", "category": "monitoring"},
    "prom-client": {"size": "50KB", "category": "monitoring"},
    "swagger-ui-express": {"size": "50KB", "category": "documentation"},
    "openapi-types": {"size": "5KB", "category": "documentation"},
    "jsdoc": {"size": "15MB", "category": "documentation"},
    "typedoc": {"size": "30MB", "category": "documentation"},
}

ALTERNATIVES = {
    "moment": {
        "替代": "dayjs (7KB) or date-fns (25KB)",
        "reason": "Day.js is a minimalist alternative with a Moment.js compatible API",
    },
    "lodash": {
        "替代": "lodash-es (tree-shakeable) or native methods",
        "reason": "lodash-es enables tree-shaking, native methods reduce bundle size",
    },
    "underscore": {
        "替代": "lodash-es or native methods",
        "reason": "Lodash is more actively maintained and has better TypeScript support",
    },
    "ramda": {
        "替代": "lodash-es or fp-ts",
        "reason": "Smaller footprint with better TypeScript support available",
    },
    "axios": {
        "替代": "fetch (native) or got (12KB) or ky (12KB)",
        "reason": "Native fetch reduces dependencies, got/ky offer modern API",
    },
    "request": {
        "替代": "axios, got, or native fetch",
        "reason": "Request is deprecated; got offers similar API with better performance",
    },
    "jquery": {
        "替代": "native DOM APIs or cash (12KB)",
        "reason": "Modern browsers have excellent native DOM support",
    },
    "bootstrap": {
        "替代": "Tailwind CSS (80KB) or CSS modules",
        "reason": "Tailwind offers more flexibility and smaller bundle sizes",
    },
    "material-ui": {
        "替代": "@mui/material (same, but lighter core) or Radix UI + Tailwind",
        "reason": "Radix provides unstyled primitives for smaller bundles",
    },
    "antd": {
        "替代": "Chakra UI or Mantine",
        "reason": "Chakra/Mantine are more lightweight and customizable",
    },
    "chart.js": {
        "替代": "Chart.js (with only needed charts) or Recharts (React) or ApexCharts",
        "reason": "Chart.js allows tree-shaking of unused chart types",
    },
    "d3": {
        "替代": "specific D3 modules or Chart.js",
        "reason": "Import only needed D3 modules to reduce bundle size",
    },
    "three": {
        "替代": "three-lite or @react-three/fiber",
        "reason": "Three.js has many alternatives optimized for bundle size",
    },
    "phaser": {
        "替代": "PixiJS (250KB) or Kaboom.js (50KB)",
        "reason": "PixiJS is a renderer, Kaboom is much lighter for simple games",
    },
    "express": {
        "替代": "fastify (75KB) or koa (110KB) or hono (15KB)",
        "reason": "Fastify offers better performance and built-in TypeScript support",
    },
    "mongoose": {
        "替代": "mongodb driver + custom schemas or Prisma (light client)",
        "reason": "MongoDB driver is lighter, Prisma offers better DX",
    },
    "prisma": {
        "替代": "Drizzle ORM or Kysely",
        "reason": "Drizzle is much lighter and has better performance",
    },
    "webpack": {
        "替代": "Vite (200KB) or Rollup (400KB) or esbuild (10MB dev)",
        "reason": "Vite offers faster dev experience with Rollup for production",
    },
    "typescript": {
        "替代": "tsc (use only for type checking) or swc (10x faster)",
        "reason": "swc is written in Rust and compiles 10x faster than tsc",
    },
    "babel": {
        "替代": "swc or esbuild",
        "reason": "swc is written in Rust and significantly faster",
    },
    "jest": {
        "替代": "Vitest (shares Vite) or Vitest + happy-dom (faster)",
        "reason": "Vitest is Jest-compatible but much faster using Vite",
    },
    "mocha": {
        "替代": "Jest or Vitest or AVA (parallel)",
        "reason": "Jest/Vitest offer better DX with parallel execution",
    },
    "prettier": {
        "替代": "dprint (faster, Rust) or Biome",
        "reason": "dprint is significantly faster and has similar configuration",
    },
    "eslint": {
        "替代": "Biome (faster, Rust) or oxlint",
        "reason": "Biome is 20-30x faster and integrates formatting",
    },
    "graphql": {
        "替代": "graphql-yoga (lighter) or urql",
        "reason": "graphql-yoga is modular and lighter than Apollo Server",
    },
    "apollo-server": {
        "替代": "graphql-yoga or Hono + GraphQL",
        "reason": "graphql-yoga offers similar features with smaller footprint",
    },
    "rxjs": {
        "替代": "native observables or just- functions",
        "reason": "Full RxJS is large; native observables or lighter libs often suffice",
    },
    "socket.io": {
        "替代": "ws (35KB) + WebSocket fallback",
        "reason": "ws is lighter, Socket.io adds overhead for features you may not need",
    },
    "passport": {
        "替代": "lucia-auth or next-auth (for specific frameworks)",
        "reason": "Modern auth solutions offer better DX and security",
    },
    "bcrypt": {
        "替代": "argon2 or bcryptjs (if bcrypt required)",
        "reason": "argon2 is the winner of PHC competition",
    },
    "sharp": {
        "替代": "jimp (pure JS, slower) or libvips via WASM",
        "reason": "jimp avoids native dependencies but is slower",
    },
    "puppeteer": {
        "替代": "playwright or @sparticuz/chromium",
        "reason": "Playwright is faster, lighter, and supports multiple browsers",
    },
    "playwright": {
        "替代": "Happy DOM + jsdom for unit tests",
        "reason": "For non-browser testing, JSDOM/HappyDOM are much lighter",
    },
    "better-sqlite3": {
        "替代": "sql.js (WASM) or lowdb (JSON)",
        "reason": "sql.js avoids native compilation, lowdb for simple needs",
    },
    "sequelize": {
        "替代": "Prisma, Drizzle, or TypeORM",
        "reason": "Modern ORMs offer better TypeScript support and performance",
    },
    "date-fns": {
        "替代": "dayjs (7KB)",
        "reason": "Day.js is smaller and has a Moment-compatible API",
    },
    "recoil": {
        "替代": "Zustand, Jotai, or Valtio",
        "reason": "Zustand/Jotai are significantly smaller and faster",
    },
    "immer": {
        "替代": "Immer (keep) or use native spread (simpler)",
        "reason": "Immer is already optimized; consider if you need it at all",
    },
    "joi": {
        "替代": "zod (50KB) or superstruct",
        "reason": "Zod has better TypeScript inference and smaller bundle",
    },
    "yup": {
        "替代": "zod or joi",
        "reason": "Zod offers better TypeScript integration",
    },
    "ajv": {
        "替代": "zod (runtime) or quicktype (compile-time)",
        "reason": "Zod provides validation + TypeScript types",
    },
    "glob": {
        "替代": "fast-glob or node:fs.glob (Node 22+)",
        "reason": "fast-glob is faster and lighter",
    },
    "fs-extra": {
        "替代": "native fs + promises or node:fs (Node 10+)",
        "reason": "Native fs covers most use cases now",
    },
    "winston": {
        "替代": "pino (50KB) or console (minimal)",
        "reason": "Pino is significantly faster and lighter",
    },
    "morgan": {
        "替代": "pino-http",
        "reason": "pino-http integrates better with pino for logging",
    },
    "compression": {
        "替代": "native compression (Node 16+) or brotli",
        "reason": "Node has built-in compression support now",
    },
    "multer": {
        "替代": "formidable or native multipart",
        "reason": "formidable is lighter and faster",
    },
    "validator": {
        "替代": "zod + custom validators or validate-it",
        "reason": "Zod handles validation with TypeScript inference",
    },
    "nodemailer": {
        "替代": "resend (API) or sendgrid (API)",
        "reason": "API-based email services offer better deliverability",
    },
    "aws-sdk": {
        "替代": "@aws-sdk/client-* (modular) or @aws-sdk/lib-dynamodb",
        "reason": "Modular SDK reduces bundle size significantly",
    },
    "firebase": {
        "替代": "specific Firebase SDKs or Supabase",
        "reason": "Import only needed Firebase services",
    },
    "sentry": {
        "替代": "otel (OpenTelemetry) or self-hosted solution",
        "reason": "OpenTelemetry is vendor-neutral and increasingly standard",
    },
    "swagger-ui-express": {
        "替代": "scalar or Stoplight Elements",
        "reason": "Modern alternatives offer better UI and performance",
    },
    "jsdoc": {
        "替代": "TypeDoc (for TS) or VitePress (docs site)",
        "reason": "TypeDoc generates better docs for TypeScript projects",
    },
}

HEAVY_PACKAGES = {
    "angular": "2MB",
    "@angular/core": "1.5MB",
    "antd": "2MB",
    "phaser": "5MB",
    "prisma": "15MB",
    "webpack": "2MB",
    "jest": "10MB",
    "typescript": "70MB",
    "babel": "15MB",
    "prettier": "25MB",
    "eslint": "15MB",
    "tslint": "8MB",
    "typedoc": "30MB",
    "aws-sdk": "150MB",
    "puppeteer": "300MB",
    "playwright": "400MB",
    "selenium-webdriver": "50MB",
}


@dataclass
class DependencyInfo:
    name: str
    version: str
    size: Optional[str] = None
    category: Optional[str] = None
    is_heavy: bool = False


def bundle_analyzer(bundle_file: str, options: dict) -> dict:
    """
    Analyze dependency bundle and provide optimization recommendations.

    Args:
        bundle_file: Content of package.json, requirements.txt, or go.mod
        options: Configuration options including:
            - language: "javascript", "python", or "go" (auto-detected if not specified)
            - strictness: "strict", "moderate", or "relaxed" (default: "moderate")

    Returns:
        Dictionary with analysis results containing:
            - status: "success" or "error"
            - dependencies: All dependencies with versions
            - duplicates: Duplicate dependencies
            - bloat: Potential bloat (unused, large)
            - alternatives: Lighter alternatives
            - summary: Bundle health summary
    """
    try:
        options = _normalize_options(options)
        language = options.get("language", "auto")
        strictness = options.get("strictness", "moderate")

        bundle_type = _detect_bundle_type(bundle_file, language)

        if bundle_type == "unknown":
            return {
                "status": "error",
                "error": "Unable to detect bundle type. Provide valid package.json, requirements.txt, or go.mod content.",
            }

        dependencies = _parse_dependencies(bundle_file, bundle_type)

        duplicates = _find_duplicates(dependencies)

        bloat = _detect_bloat(dependencies, strictness)

        alternatives = _suggest_alternatives(bloat)

        summary = _generate_summary(dependencies, duplicates, bloat, alternatives)

        return {
            "status": "success",
            "bundle_type": bundle_type,
            "dependencies": dependencies,
            "duplicates": duplicates,
            "bloat": bloat,
            "alternatives": alternatives,
            "summary": summary,
        }

    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "message": "Failed to analyze bundle",
        }


def _normalize_options(options: dict) -> dict:
    defaults = {
        "language": "auto",
        "strictness": "moderate",
    }
    return {**defaults, **options}


def _detect_bundle_type(content: str, language: str) -> str:
    if language != "auto":
        return language

    content = content.strip()

    if content.startswith("{"):
        try:
            json.loads(content)
            return "javascript"
        except json.JSONDecodeError:
            pass

    if "{" in content and '"dependencies"' in content:
        return "javascript"

    if re.match(r"^[\w-]+\s*[<>=~!]", content, re.MULTILINE):
        return "python"

    if content.startswith("module "):
        return "go"

    if "go.mod" in content.lower() or "require (" in content:
        return "go"

    if content.count("\n") < 50 and all(
        re.match(r"^[\w-]+\s*[-._\w]+$", line)
        for line in content.split("\n")
        if line and not line.startswith("#")
    ):
        return "python"

    return "unknown"


def _parse_dependencies(content: str, bundle_type: str) -> List[Dict]:
    dependencies = []

    if bundle_type == "javascript":
        dependencies = _parse_package_json(content)
    elif bundle_type == "python":
        dependencies = _parse_requirements_txt(content)
    elif bundle_type == "go":
        dependencies = _parse_go_mod(content)

    return dependencies


def _parse_package_json(content: str) -> List[Dict]:
    try:
        pkg = json.loads(content)
    except json.JSONDecodeError:
        return []

    deps = {}

    if "dependencies" in pkg:
        deps.update(pkg["dependencies"])

    if "devDependencies" in pkg:
        deps.update(pkg["devDependencies"])

    if "peerDependencies" in pkg:
        deps.update(pkg["peerDependencies"])

    if "optionalDependencies" in pkg:
        deps.update(pkg["optionalDependencies"])

    result = []
    for name, version in deps.items():
        pkg_info = PACKAGE_SIZES.get(name.lower(), {})
        size = pkg_info.get("size")
        category = pkg_info.get("category")

        result.append(
            {
                "name": name,
                "version": version,
                "size": size,
                "category": category,
                "is_heavy": name.lower() in HEAVY_PACKAGES
                or (size and ("MB" in size and float(size.replace("MB", "")) > 10)),
            }
        )

    return result


def _parse_requirements_txt(content: str) -> List[Dict]:
    deps = []

    for line in content.split("\n"):
        line = line.strip()

        if not line or line.startswith("#") or line.startswith("-"):
            continue

        match = re.match(r"^([a-zA-Z0-9_-]+)\s*([<>=~!.\w]+)?", line)
        if match:
            name = match.group(1).lower()
            version = match.group(2) or "any"

            deps.append(
                {
                    "name": name,
                    "version": version,
                    "size": None,
                    "category": None,
                    "is_heavy": False,
                }
            )

    return deps


def _parse_go_mod(content: str) -> List[Dict]:
    deps = []

    in_require_block = False

    for line in content.split("\n"):
        line = line.strip()

        if line.startswith("require ("):
            in_require_block = True
            continue

        if in_require_block and line == ")":
            in_require_block = False
            continue

        if in_require_block or line.startswith("require "):
            if line.startswith("require "):
                line = line[8:].strip()

            match = re.match(r"([^\s]+)\s+v?([0-9.\w-]+)", line)
            if match:
                name = match.group(1)
                version = "v" + match.group(2)

                deps.append(
                    {
                        "name": name,
                        "version": version,
                        "size": None,
                        "category": None,
                        "is_heavy": False,
                    }
                )

    return deps


def _find_duplicates(dependencies: List[Dict]) -> List[Dict]:
    name_count = {}

    for dep in dependencies:
        name = dep["name"].lower()
        name_count[name] = name_count.get(name, 0) + 1

    duplicates = []
    for name, count in name_count.items():
        if count > 1:
            matching_deps = [d for d in dependencies if d["name"].lower() == name]
            duplicates.append(
                {
                    "name": name,
                    "count": count,
                    "versions": list(set(d["version"] for d in matching_deps)),
                    "locations": [d.get("location", "unknown") for d in matching_deps],
                }
            )

    return duplicates


def _detect_bloat(dependencies: List[Dict], strictness: str) -> List[Dict]:
    bloat = []
    thresholds = {
        "strict": {"size_mb": 0.5, "outdated_months": 6},
        "moderate": {"size_mb": 1, "outdated_months": 12},
        "relaxed": {"size_mb": 2, "outdated_months": 24},
    }

    threshold = thresholds.get(strictness, thresholds["moderate"])

    for dep in dependencies:
        name = dep["name"].lower()
        size = dep.get("size", "")

        is_bloat = False
        bloat_type = []
        recommendation = ""

        if size and "KB" in size:
            kb_size = float(size.replace("KB", ""))
            if kb_size > threshold["size_mb"] * 1000:
                is_bloat = True
                bloat_type.append("large")
                recommendation = f"Consider a lighter alternative (current: {size})"

        if size and "MB" in size:
            mb_size = float(size.replace("MB", ""))
            if mb_size > threshold["size_mb"]:
                is_bloat = True
                bloat_type.append("large")
                recommendation = f"Consider a lighter alternative (current: {size})"

        if dep.get("is_heavy"):
            is_bloat = True
            bloat_type.append("heavy")
            if not recommendation:
                recommendation = f"This is a heavy package. Consider alternatives (known size: {size or 'unknown'})"

        if name in HEAVY_PACKAGES:
            is_bloat = True
            bloat_type.append("known_heavy")
            if not recommendation:
                recommendation = f"Known heavy package. Consider {ALTERNATIVES.get(name, 'lighter alternatives')}"

        if is_bloat:
            bloat.append(
                {
                    "name": dep["name"],
                    "version": dep["version"],
                    "size": size,
                    "category": dep.get("category"),
                    "bloat_type": bloat_type,
                    "severity": "high"
                    if "heavy" in bloat_type or "large" in bloat_type
                    else "medium",
                    "recommendation": recommendation,
                }
            )

    bloat.sort(key=lambda x: {"high": 0, "medium": 1, "low": 2}.get(x["severity"], 2))

    return bloat


def _suggest_alternatives(bloat: List[Dict]) -> List[Dict]:
    alternatives = []

    for item in bloat:
        name = item["name"].lower()
        if name in ALTERNATIVES:
            alt = ALTERNATIVES[name]
            alternatives.append(
                {
                    "current_package": item["name"],
                    "suggested": list(alt.values())[0],
                    "reason": list(alt.values())[1],
                    "severity": item["severity"],
                }
            )

    return alternatives


def _generate_summary(
    dependencies: List[Dict],
    duplicates: List[Dict],
    bloat: List[Dict],
    alternatives: List[Dict],
) -> Dict:
    total_deps = len(dependencies)
    heavy_count = sum(1 for d in dependencies if d.get("is_heavy"))
    bloat_count = len(bloat)
    dup_count = len(duplicates)
    alt_count = len(alternatives)

    score = 100
    score -= min(50, dup_count * 10)
    score -= min(30, bloat_count * 5)
    score -= min(20, heavy_count * 3)
    score = max(0, score)

    if score >= 80:
        health = "excellent"
    elif score >= 60:
        health = "good"
    elif score >= 40:
        health = "fair"
    else:
        health = "poor"

    recommendations = []

    if dup_count > 0:
        recommendations.append(f"Remove {dup_count} duplicate dependency(ies)")

    if bloat_count > 0:
        recommendations.append(f"Address {bloat_count} bloat package(s)")

    if alt_count > 0:
        recommendations.append(f"Consider {alt_count} lighter alternative(s)")

    if not recommendations:
        recommendations.append("Bundle looks healthy - no immediate action required")

    return {
        "total_dependencies": total_deps,
        "heavy_packages": heavy_count,
        "bloat_packages": bloat_count,
        "duplicate_groups": dup_count,
        "alternative_suggestions": alt_count,
        "health_score": score,
        "health_status": health,
        "recommendations": recommendations,
    }


def invoke(payload: dict) -> dict:
    """
    Main entry point for MCP skill invocation.

    Expected payload format:
    {
        "bundle_file": "{ \"dependencies\": {...} }",
        "options": {
            "language": "javascript" | "python" | "go" | "auto",
            "strictness": "strict" | "moderate" | "relaxed"
        },
        "generate_report": false  // optional, generates text report
    }
    """
    bundle_file = payload.get("bundle_file", "")

    if not bundle_file:
        return {"status": "error", "error": "No bundle file content provided"}

    options = payload.get("options", {})
    result = bundle_analyzer(bundle_file, options)

    if payload.get("generate_report", False):
        result["report"] = generate_report(result)

    return {"result": result}


def generate_report(analysis: dict) -> str:
    """Generate human-readable bundle analysis report."""
    if analysis.get("status") != "success":
        return f"Error: {analysis.get('error', 'Unknown error')}"

    lines = []
    lines.append("=" * 60)
    lines.append("BUNDLE ANALYSIS REPORT")
    lines.append("=" * 60)

    bundle_type = analysis.get("bundle_type", "unknown")
    lines.append(f"Bundle Type: {bundle_type}")

    summary = analysis.get("summary", {})
    lines.append(
        f"\nHealth Score: {summary.get('health_score', 0)}/100 ({summary.get('health_status', 'unknown')})"
    )
    lines.append(f"Total Dependencies: {summary.get('total_dependencies', 0)}")
    lines.append(f"Heavy Packages: {summary.get('heavy_packages', 0)}")
    lines.append(f"Bloat Packages: {summary.get('bloat_packages', 0)}")
    lines.append(f"Duplicates: {summary.get('duplicate_groups', 0)}")
    lines.append(f"Alternatives: {summary.get('alternative_suggestions', 0)}")

    dependencies = analysis.get("dependencies", [])
    if dependencies:
        lines.append(f"\nDEPENDENCIES ({len(dependencies)}):")
        lines.append("-" * 40)
        for dep in dependencies[:20]:
            size_str = f" [{dep.get('size', '?')}]" if dep.get("size") else ""
            heavy_str = " ⚠" if dep.get("is_heavy") else ""
            lines.append(f"  {dep['name']}@{dep['version']}{size_str}{heavy_str}")
        if len(dependencies) > 20:
            lines.append(f"  ... and {len(dependencies) - 20} more")

    duplicates = analysis.get("duplicates", [])
    if duplicates:
        lines.append(f"\nDUPLICATES ({len(duplicates)}):")
        lines.append("-" * 40)
        for dup in duplicates:
            lines.append(
                f"  {dup['name']}: {dup['count']} occurrences, versions: {', '.join(dup['versions'])}"
            )

    bloat = analysis.get("bloat", [])
    if bloat:
        lines.append(f"\nBLOAT DETECTED ({len(bloat)}):")
        lines.append("-" * 40)
        for item in bloat[:10]:
            severity = f"[{item['severity'].upper()}]"
            size_str = f" ({item.get('size', '?')})" if item.get("size") else ""
            lines.append(f"  {severity} {item['name']}{size_str}")
            lines.append(f"    Type: {', '.join(item.get('bloat_type', []))}")
            lines.append(f"    Fix: {item.get('recommendation', 'N/A')}")
        if len(bloat) > 10:
            lines.append(f"  ... and {len(bloat) - 10} more")

    alternatives = analysis.get("alternatives", [])
    if alternatives:
        lines.append(f"\nALTERNATIVES ({len(alternatives)}):")
        lines.append("-" * 40)
        for alt in alternatives[:10]:
            lines.append(f"  {alt['current_package']} → {alt['suggested']}")
            lines.append(f"    Reason: {alt['reason']}")

    recommendations = summary.get("recommendations", [])
    if recommendations:
        lines.append(f"\nRECOMMENDATIONS:")
        lines.append("-" * 40)
        for rec in recommendations:
            lines.append(f"  • {rec}")

    return "\n".join(lines)


def register_skill():
    """Return skill metadata for MCP registration."""
    return {
        "name": "bundle-analyzer",
        "description": "Analyze dependency bundles from package.json, requirements.txt, or go.mod - detects duplicates, bloat, heavy packages, and suggests lighter alternatives",
        "version": "1.0.0",
        "domain": "PERFORMANCE",
        "capabilities": [
            "Parse package.json for JavaScript/Node.js dependencies",
            "Parse requirements.txt for Python dependencies",
            "Parse go.mod for Go dependencies",
            "Detect duplicate dependencies",
            "Identify bloat and heavy packages",
            "Suggest lighter package alternatives",
            "Calculate bundle health score",
            "Generate comprehensive analysis reports",
        ],
        "options": {
            "language": "Bundle type: javascript, python, go, or auto (default: auto)",
            "strictness": "Analysis strictness: strict, moderate, or relaxed (default: moderate)",
        },
    }


if __name__ == "__main__":
    test_package_json = json.dumps(
        {
            "dependencies": {
                "react": "^18.2.0",
                "lodash": "^4.17.21",
                "moment": "^2.29.4",
                "axios": "^1.3.0",
                "express": "^4.18.2",
                "mongoose": "^7.0.0",
                "jsonwebtoken": "^9.0.0",
                "bcrypt": "^5.1.0",
                "cors": "^2.8.5",
                "helmet": "^6.0.0",
            },
            "devDependencies": {
                "jest": "^29.5.0",
                "typescript": "^5.0.0",
                "eslint": "^8.40.0",
                "prettier": "^2.8.0",
            },
        },
        indent=2,
    )

    print("=" * 60)
    print("Testing Bundle Analyzer")
    print("=" * 60)

    result = bundle_analyzer(
        test_package_json, {"language": "javascript", "strictness": "moderate"}
    )
    print(json.dumps(result, indent=2))

    print("\n" + "=" * 60)
    print("Generated Report:")
    print("=" * 60)
    print(generate_report(result))
