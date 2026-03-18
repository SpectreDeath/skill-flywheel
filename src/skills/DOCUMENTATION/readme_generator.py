"""
README Generator Skill

Generates comprehensive README files for various project types:
- Analyzes project structure
- Detects project type (Python, JS, Go, etc.)
- Extracts dependencies, entry points, and configuration
- Generates installation, usage, and other sections
- Formats output as Markdown with badges
"""

import os
import re
import json
from typing import Dict, List, Any, Optional
from pathlib import Path
from dataclasses import dataclass, field


SUPPORTED_LANGUAGES = {
    "python": {
        "files": ["setup.py", "pyproject.toml", "requirements.txt", "Pipfile"],
        "entry_points": ["__main__.py", "main.py", "app.py", "cli.py"],
        "config": ["pyproject.toml", "setup.cfg", ".flake8", "pytest.ini", "mypy.ini"],
        "badge": "https://img.shields.io/badge/Python-3.x-blue",
        "color": "blue",
    },
    "javascript": {
        "files": ["package.json"],
        "entry_points": ["index.js", "main.js", "app.js", "server.js"],
        "config": ["package.json", ".eslintrc", "webpack.config.js", "vite.config.js"],
        "badge": "https://img.shields.io/badge/JavaScript-F7DF1E",
        "color": "yellow",
    },
    "typescript": {
        "files": ["package.json", "tsconfig.json"],
        "entry_points": ["index.ts", "main.ts", "app.ts"],
        "config": ["tsconfig.json", ".eslintrc", "jest.config.ts"],
        "badge": "https://img.shields.io/badge/TypeScript-3178C6",
        "color": "3178C6",
    },
    "go": {
        "files": ["go.mod", "go.sum"],
        "entry_points": ["main.go", "cmd/main.go"],
        "config": ["go.mod", ".golangci.yml", "Makefile"],
        "badge": "https://img.shields.io/badge/Go-00ADD8",
        "color": "00ADD8",
    },
    "rust": {
        "files": ["Cargo.toml", "Cargo.lock"],
        "entry_points": ["src/main.rs", "src/lib.rs"],
        "config": ["Cargo.toml", "rustfmt.toml", ".clippy.toml"],
        "badge": "https://img.shields.io/badge/Rust-DEA584",
        "color": "DEA584",
    },
    "java": {
        "files": ["pom.xml", "build.gradle", "build.gradle.kts"],
        "entry_points": ["src/main/java"],
        "config": ["pom.xml", "build.gradle", "settings.gradle"],
        "badge": "https://img.shields.io/badge/Java-ED8B00",
        "color": "ED8B00",
    },
    "csharp": {
        "files": ["*.csproj", "*.sln"],
        "entry_points": ["Program.cs", "Main.cs"],
        "config": ["*.csproj", "appsettings.json"],
        "badge": "https://img.shields.io/badge/C%23-512BD4",
        "color": "512BD4",
    },
    "ruby": {
        "files": ["Gemfile", "*.gemspec"],
        "entry_points": ["main.rb", "app.rb"],
        "config": ["Gemfile", ".ruby-version", "Rakefile"],
        "badge": "https://img.shields.io/badge/Ruby-CC342D",
        "color": "CC342D",
    },
    "php": {
        "files": ["composer.json", "index.php"],
        "entry_points": ["index.php", "app.php"],
        "config": ["composer.json", "phpunit.xml"],
        "badge": "https://img.shields.io/badge/PHP-777BB4",
        "color": "777BB4",
    },
    "swift": {
        "files": ["Package.swift", "*.xcodeproj"],
        "entry_points": ["Sources/main.swift"],
        "config": ["Package.swift", "project.yml"],
        "badge": "https://img.shields.io/badge/Swift-FA7343",
        "color": "FA7343",
    },
    "kotlin": {
        "files": ["build.gradle.kts", "pom.xml"],
        "entry_points": ["src/main/kotlin"],
        "config": ["build.gradle.kts", "settings.gradle.kts"],
        "badge": "https://img.shields.io/badge/Kotlin-7F52FF",
        "color": "7F52FF",
    },
}


@dataclass
class ProjectInfo:
    name: str = ""
    description: str = ""
    language: str = ""
    version: str = ""
    author: str = ""
    license: str = ""
    homepage: str = ""
    repository: str = ""
    dependencies: List[str] = field(default_factory=list)
    dev_dependencies: List[str] = field(default_factory=list)
    entry_points: List[str] = field(default_factory=list)
    has_tests: bool = False
    has_docker: bool = False
    has_github_actions: bool = False
    has_readme: bool = False
    has_license: bool = False
    has_contributing: bool = False
    has_changelog: bool = False
    package_managers: List[str] = field(default_factory=list)
    frameworks: List[str] = field(default_factory=list)
    config_files: List[str] = field(default_factory=list)


def analyze_project_structure(project_path: str) -> ProjectInfo:
    """Analyze the project structure and extract relevant information."""
    info = ProjectInfo()

    path = Path(project_path)
    if not path.exists():
        return info

    if path.is_file():
        path = path.parent

    files = [f.name for f in path.iterdir() if f.is_file()]
    dirs = [d.name for d in path.iterdir() if d.is_dir()]

    info.name = path.name

    for lang, config in SUPPORTED_LANGUAGES.items():
        for file_pattern in config["files"]:
            if "*" in file_pattern:
                if any(f.endswith(file_pattern.replace("*", "")) for f in files):
                    info.language = lang
                    info.config_files.append(file_pattern)
                    break
            elif file_pattern in files:
                info.language = lang
                info.config_files.append(file_pattern)
                break
        if info.language:
            break

    for entry_point in [
        "__main__.py",
        "main.py",
        "app.py",
        "cli.py",
        "index.js",
        "main.js",
        "main.go",
        "Program.cs",
    ]:
        if entry_point in files:
            info.entry_points.append(entry_point)

    if "tests" in dirs or "test" in dirs or "__tests__" in dirs:
        info.has_tests = True

    if (
        "Dockerfile" in files
        or "docker-compose.yml" in files
        or "docker-compose.yaml" in files
    ):
        info.has_docker = True

    if ".github" in dirs or ".github/workflows" in dirs:
        info.has_github_actions = True

    if "README.md" in files or "README.rst" in files or "README" in files:
        info.has_readme = True

    if "LICENSE" in files or "LICENSE.md" in files:
        info.has_license = True

    if "CONTRIBUTING.md" in files or "CONTRIBUTING.rst" in files:
        info.has_contributing = True

    if "CHANGELOG.md" in files or "CHANGELOG.rst" in files or "CHANGES.md" in files:
        info.has_changelog = True

    return info


def detect_language(project_path: str) -> str:
    """Detect the primary programming language of the project."""
    info = analyze_project_structure(project_path)
    return info.language


def extract_package_info(project_path: str) -> ProjectInfo:
    """Extract package information from various configuration files."""
    info = analyze_project_structure(project_path)

    path = Path(project_path)
    if path.is_file():
        path = path.parent

    package_json = path / "package.json"
    if package_json.exists():
        try:
            with open(package_json, "r", encoding="utf-8") as f:
                data = json.load(f)
                info.name = data.get("name", info.name)
                info.description = data.get("description", "")
                info.version = data.get("version", "")
                info.author = data.get("author", "")
                info.homepage = data.get("homepage", "")
                info.repository = data.get("repository", {}).get("url", "")

                deps = data.get("dependencies", {})
                info.dependencies = list(deps.keys())

                dev_deps = data.get("devDependencies", {})
                info.dev_dependencies = list(dev_deps.keys())

                if "react" in deps:
                    info.frameworks.append("React")
                elif "vue" in deps:
                    info.frameworks.append("Vue")
                elif "angular" in deps:
                    info.frameworks.append("Angular")
                elif "express" in deps:
                    info.frameworks.append("Express")
                elif "next" in deps:
                    info.frameworks.append("Next.js")
        except (json.JSONDecodeError, IOError):
            pass

    pyproject_toml = path / "pyproject.toml"
    if pyproject_toml.exists():
        try:
            content = pyproject_toml.read_text(encoding="utf-8")

            name_match = re.search(r'name\s*=\s*["\']([^"\']+)["\']', content)
            if name_match:
                info.name = name_match.group(1)

            desc_match = re.search(r'description\s*=\s*["\']([^"\']*)["\']', content)
            if desc_match:
                info.description = desc_match.group(1)

            version_match = re.search(r'version\s*=\s*["\']([^"\']+)["\']', content)
            if version_match:
                info.version = version_match.group(1)

            deps_match = re.findall(
                r'"([^"]+)"',
                content.split("[project.dependencies]")[1].split("[")[0]
                if "[project.dependencies]" in content
                else "",
            )
            info.dependencies = deps_match

            if "pytest" in content:
                info.has_tests = True
            if "pytest" in content or "black" in content or "ruff" in content:
                info.dev_dependencies = re.findall(
                    r'"([^"]+)"',
                    content.split("[tool.pytest")[0]
                    .split("[project.optional-dependencies]")[1]
                    .split("[")[0]
                    if "[project.optional-dependencies]" in content
                    else "",
                )
        except (IOError, IndexError):
            pass

    setup_py = path / "setup.py"
    if setup_py.exists():
        try:
            content = setup_py.read_text(encoding="utf-8")

            name_match = re.search(r'name\s*=\s*["\']([^"\']+)["\']', content)
            if name_match:
                info.name = name_match.group(1)

            version_match = re.search(r'version\s*=\s*["\']([^"\']+)["\']', content)
            if version_match:
                info.version = version_match.group(1)

            author_match = re.search(r'author\s*=\s*["\']([^"\']+)["\']', content)
            if author_match:
                info.author = author_match.group(1)
        except IOError:
            pass

    go_mod = path / "go.mod"
    if go_mod.exists():
        try:
            content = go_mod.read_text(encoding="utf-8")
            lines = content.split("\n")

            for line in lines:
                if line.startswith("module "):
                    info.name = line.replace("module ", "").strip()
                elif line.startswith("go "):
                    info.version = line.replace("go ", "").strip()
        except IOError:
            pass

    cargo_toml = path / "Cargo.toml"
    if cargo_toml.exists():
        try:
            content = cargo_toml.read_text(encoding="utf-8")

            name_match = re.search(r'name\s*=\s*"([^"]+)"', content)
            if name_match:
                info.name = name_match.group(1)

            version_match = re.search(r'version\s*=\s*"([^"]+)"', content)
            if version_match:
                info.version = version_match.group(1)
        except IOError:
            pass

    return info


def generate_badges(info: ProjectInfo) -> List[Dict[str, str]]:
    """Generate badges for the project."""
    badges = []

    if info.language and info.language in SUPPORTED_LANGUAGES:
        lang_info = SUPPORTED_LANGUAGES[info.language]
        badges.append(
            {
                "name": info.language.title(),
                "url": lang_info["badge"],
                "color": lang_info["color"],
            }
        )

    if info.version:
        badges.append(
            {
                "name": f"Version {info.version}",
                "url": f"https://img.shields.io/badge/Version-{info.version}-green",
                "color": "green",
            }
        )

    if info.license:
        badges.append(
            {
                "name": info.license,
                "url": f"https://img.shields.io/badge/License-{info.license}-green",
                "color": "green",
            }
        )

    if info.has_tests:
        badges.append(
            {
                "name": "Tests",
                "url": "https://img.shields.io/badge/Tests-passing-green",
                "color": "green",
            }
        )

    if info.has_docker:
        badges.append(
            {
                "name": "Docker",
                "url": "https://img.shields.io/badge/Docker-Yes-2496ED",
                "color": "2496ED",
            }
        )

    if info.has_github_actions:
        badges.append(
            {
                "name": "CI/CD",
                "url": "https://img.shields.io/badge/CI%2FCD-GitHub_Actions-2088FF",
                "color": "2088FF",
            }
        )

    return badges


def format_badges(badges: List[Dict[str, str]]) -> str:
    """Format badges as Markdown."""
    if not badges:
        return ""

    badge_markdown = " ".join(
        [f"[![{b['name']}]({b['url']})](https://example.com)" for b in badges]
    )
    return badge_markdown + "\n"


def generate_installation_section(info: ProjectInfo) -> str:
    """Generate the installation section."""
    sections = ["## Installation\n"]

    if info.language == "python":
        sections.append("```bash\npip install " + info.name + "\n```\n")

        if info.package_managers:
            sections.append("Or using poetry:\n")
            sections.append("```bash\npoetry install\n```\n")

    elif info.language in ["javascript", "typescript"]:
        sections.append("```bash\nnpm install " + info.name + "\n```\n")

        sections.append("Or using yarn:\n")
        sections.append("```bash\nyarn add " + info.name + "\n```\n")

    elif info.language == "go":
        sections.append(
            "```bash\ngo install github.com/" + info.name + "@latest\n```\n"
        )

    elif info.language == "rust":
        sections.append("```bash\ncargo install " + info.name + "\n```\n")

    elif info.language == "java":
        sections.append("Add to your Maven pom.xml:\n")
        sections.append(
            "```xml\n<dependency>\n  <groupId>"
            + info.name
            + "</groupId>\n  <artifactId>"
            + info.name
            + "</artifactId>\n  <version>"
            + info.version
            + "</version>\n</dependency>\n```\n"
        )

    elif info.language == "ruby":
        sections.append("```bash\ngem install " + info.name + "\n```\n")

    elif info.language == "php":
        sections.append("```bash\ncomposer require " + info.name + "\n```\n")

    else:
        sections.append("Clone the repository and follow the setup instructions.\n")

    if info.has_docker:
        sections.append("\n### Docker\n")
        sections.append("```bash\ndocker build -t " + info.name + " .\n```\n")

    return "".join(sections)


def generate_usage_section(info: ProjectInfo) -> str:
    """Generate the usage section."""
    sections = ["## Usage\n"]

    if info.language == "python":
        if "cli" in info.entry_points or "cli.py" in info.entry_points:
            sections.append("```bash\n" + info.name + " --help\n```\n")
        sections.append(
            "```python\nimport " + info.name + "\n\n" + info.name + ".run()\n```\n"
        )

    elif info.language in ["javascript", "typescript"]:
        if "index.js" in info.entry_points or "index.ts" in info.entry_points:
            sections.append(
                "```javascript\nconst "
                + info.name
                + " = require('"
                + info.name
                + "');\n\n"
                + info.name
                + ".init();\n```\n"
            )
        elif "server.js" in info.entry_points or "server.ts" in info.entry_points:
            sections.append("```bash\nnpm start\n```\n")

    elif info.language == "go":
        sections.append("```bash\n" + info.name + "\n```\n")

    elif info.language == "rust":
        sections.append("```bash\ncargo run --release\n```\n")

    else:
        sections.append("Refer to the documentation for usage examples.\n")

    return "".join(sections)


def generate_configuration_section(info: ProjectInfo) -> str:
    """Generate the configuration section."""
    if not info.config_files:
        return ""

    sections = ["## Configuration\n"]

    for config_file in info.config_files:
        sections.append(f"- `{config_file}`\n")

    sections.append("\n")

    if info.language in ["javascript", "typescript"]:
        sections.append(
            '```json\n{\n  "' + info.name + '": {\n    "option": "value"\n  }\n}\n```\n'
        )
    elif info.language == "python":
        sections.append(
            "```python\n# config.py\n"
            + info.name.upper().replace("-", "_")
            + '_OPTION = "value"\n```\n'
        )

    return "".join(sections)


def generate_testing_section(info: ProjectInfo) -> str:
    """Generate the testing section."""
    if not info.has_tests:
        return ""

    sections = ["## Testing\n"]

    if info.language == "python":
        sections.append("```bash\npytest\n```\n")
        sections.append("Or with coverage:\n")
        sections.append("```bash\npytest --cov=" + info.name + "\n```\n")

    elif info.language in ["javascript", "typescript"]:
        sections.append("```bash\nnpm test\n```\n")
        sections.append("Or with coverage:\n")
        sections.append("```bash\nnpm run test:coverage\n```\n")

    elif info.language == "go":
        sections.append("```bash\ngo test ./...\n```\n")

    elif info.language == "rust":
        sections.append("```bash\ncargo test\n```\n")

    return "".join(sections)


def generate_development_section(info: ProjectInfo) -> str:
    """Generate the development section."""
    sections = ["## Development\n"]

    if info.language == "python":
        sections.append(
            "```bash\ngit clone https://github.com/"
            + info.repository.split("/")[-2]
            + "/"
            + info.name
            + ".git\ncd "
            + info.name
            + "\npip install -e .\npip install -r requirements-dev.txt\n```\n"
        )
        sections.append("Run tests:\n")
        sections.append("```bash\npytest\n```\n")

    elif info.language in ["javascript", "typescript"]:
        sections.append(
            "```bash\ngit clone https://github.com/"
            + info.repository.split("/")[-2]
            + "/"
            + info.name
            + ".git\ncd "
            + info.name
            + "\nnpm install\nnpm run dev\n```\n"
        )

    elif info.language == "go":
        sections.append(
            "```bash\ngit clone https://github.com/"
            + info.repository.split("/")[-2]
            + "/"
            + info.name
            + ".git\ncd "
            + info.name
            + "\ngo mod download\ngo run main.go\n```\n"
        )

    elif info.language == "rust":
        sections.append(
            "```bash\ngit clone https://github.com/"
            + info.repository.split("/")[-2]
            + "/"
            + info.name
            + ".git\ncd "
            + info.name
            + "\ncargo build\ncargo test\n```\n"
        )

    return "".join(sections)


def generate_dependencies_section(info: ProjectInfo) -> str:
    """Generate the dependencies section."""
    if not info.dependencies and not info.dev_dependencies:
        return ""

    sections = ["## Dependencies\n"]

    if info.dependencies:
        sections.append("### Runtime Dependencies\n")
        for dep in info.dependencies[:10]:
            sections.append(f"- `{dep}`\n")
        if len(info.dependencies) > 10:
            sections.append(f"- ... and {len(info.dependencies) - 10} more\n")

    if info.dev_dependencies:
        sections.append("\n### Development Dependencies\n")
        for dep in info.dev_dependencies[:10]:
            sections.append(f"- `{dep}`\n")
        if len(info.dev_dependencies) > 10:
            sections.append(f"- ... and {len(info.dev_dependencies) - 10} more\n")

    return "".join(sections)


def generate_contributing_section(info: ProjectInfo) -> str:
    """Generate the contributing section."""
    sections = ["## Contributing\n"]

    sections.append("Contributions are welcome! Please follow these steps:\n\n")
    sections.append("1. Fork the repository\n")
    sections.append(
        "2. Create your feature branch (`git checkout -b feature/amazing-feature`)\n"
    )
    sections.append(
        "3. Commit your changes (`git commit -m 'Add some amazing feature'`)\n"
    )
    sections.append(
        "4. Push to the branch (`git push origin feature/amazing-feature`)\n"
    )
    sections.append("5. Open a Pull Request\n")

    if info.has_contributing:
        sections.append(
            "\nPlease read the [CONTRIBUTING](CONTRIBUTING.md) file for details.\n"
        )

    return "".join(sections)


def generate_license_section(info: ProjectInfo) -> str:
    """Generate the license section."""
    if not info.license:
        return ""

    sections = ["## License\n"]
    sections.append(f"This project is licensed under the {info.license} license.\n")

    return "".join(sections)


def generate_contact_section(info: ProjectInfo) -> str:
    """Generate the contact section."""
    sections = ["## Contact\n"]

    if info.author:
        sections.append(f"Author: {info.author}\n")

    if info.homepage:
        sections.append(f"Project Homepage: {info.homepage}\n")

    if info.repository:
        sections.append(f"Repository: {info.repository}\n")

    return "".join(sections)


def readme_generator(project_path: str, options: dict = None) -> dict:
    """
    Main function to generate README for a project.

    Args:
        project_path: Path to the project directory or file
        options: Optional configuration dictionary with:
            - template: str - Template to use (minimal, standard, comprehensive)
            - include_sections: List[str] - Sections to include
            - exclude_sections: List[str] - Sections to exclude
            - add_custom_sections: Dict[str, str] - Custom sections to add

    Returns:
        Dictionary with status, sections, readme content, and badges
    """
    if options is None:
        options = {}

    template = options.get("template", "standard")
    include_sections = options.get("include_sections", [])
    exclude_sections = options.get("exclude_sections", [])
    custom_sections = options.get("custom_sections", {})

    project_info = extract_package_info(project_path)

    if not project_info.name:
        project_info.name = (
            Path(project_path).name if Path(project_path).exists() else "project"
        )

    all_sections = {
        "badges": format_badges(generate_badges(project_info)),
        "title": f"# {project_info.name}\n",
        "description": f"{project_info.description}\n"
        if project_info.description
        else "",
        "table_of_contents": "",
        "installation": "",
        "usage": "",
        "configuration": "",
        "testing": "",
        "development": "",
        "dependencies": "",
        "contributing": "",
        "license": "",
        "contact": "",
    }

    if template == "minimal":
        sections_to_generate = ["title", "description", "installation", "usage"]
    elif template == "comprehensive":
        sections_to_generate = list(all_sections.keys())
    else:
        sections_to_generate = [
            "title",
            "description",
            "badges",
            "installation",
            "usage",
            "development",
            "contributing",
            "license",
        ]

    if include_sections:
        sections_to_generate = include_sections

    if exclude_sections:
        sections_to_generate = [
            s for s in sections_to_generate if s not in exclude_sections
        ]

    generated_sections = {}

    if "title" in sections_to_generate:
        generated_sections["title"] = all_sections["title"]

    if "badges" in sections_to_generate:
        generated_sections["badges"] = all_sections["badges"]

    if "description" in sections_to_generate:
        generated_sections["description"] = all_sections["description"]

    if "installation" in sections_to_generate:
        generated_sections["installation"] = generate_installation_section(project_info)

    if "usage" in sections_to_generate:
        generated_sections["usage"] = generate_usage_section(project_info)

    if "configuration" in sections_to_generate:
        generated_sections["configuration"] = generate_configuration_section(
            project_info
        )

    if "testing" in sections_to_generate:
        generated_sections["testing"] = generate_testing_section(project_info)

    if "development" in sections_to_generate:
        generated_sections["development"] = generate_development_section(project_info)

    if "dependencies" in sections_to_generate:
        generated_sections["dependencies"] = generate_dependencies_section(project_info)

    if "contributing" in sections_to_generate:
        generated_sections["contributing"] = generate_contributing_section(project_info)

    if "license" in sections_to_generate:
        generated_sections["license"] = generate_license_section(project_info)

    if "contact" in sections_to_generate:
        generated_sections["contact"] = generate_contact_section(project_info)

    for section_name, section_content in custom_sections.items():
        generated_sections[section_name] = section_content

    readme_content = "".join(generated_sections.values())

    return {
        "status": "success",
        "project_info": {
            "name": project_info.name,
            "language": project_info.language,
            "version": project_info.version,
            "description": project_info.description,
            "author": project_info.author,
            "license": project_info.license,
        },
        "sections": list(generated_sections.keys()),
        "readme": readme_content,
        "badges": generate_badges(project_info),
    }


def invoke(payload: dict) -> dict:
    """
    MCP skill invocation function.

    Args:
        payload: Dictionary with action and parameters

    Returns:
        Result dictionary with skill output
    """
    action = payload.get("action", "generate")
    project_path = payload.get("project_path", payload.get("path", ""))
    options = payload.get("options", {})

    if not project_path:
        return {
            "status": "error",
            "error": "No project_path provided",
        }

    if action == "generate":
        result = readme_generator(project_path, options)
    elif action == "analyze":
        info = analyze_project_structure(project_path)
        result = {
            "status": "success",
            "project_info": {
                "name": info.name,
                "language": info.language,
                "has_tests": info.has_tests,
                "has_docker": info.has_docker,
                "has_github_actions": info.has_github_actions,
                "has_readme": info.has_readme,
                "has_license": info.has_license,
            },
        }
    elif action == "badges":
        info = extract_package_info(project_path)
        result = {
            "status": "success",
            "badges": generate_badges(info),
        }
    else:
        result = {
            "status": "error",
            "error": f"Unknown action: {action}",
        }

    return {"result": result}


def register_skill() -> dict:
    """
    Return skill metadata for registration.

    Returns:
        Dictionary with skill name, description, version, and domain
    """
    return {
        "name": "readme-generator",
        "description": "Generate comprehensive README files for various project types (Python, JavaScript, Go, Rust, etc.) with badges, installation, usage, and other sections",
        "version": "1.0.0",
        "domain": "DOCUMENTATION",
        "capabilities": [
            "Analyze project structure",
            "Detect programming language",
            "Extract dependencies and configuration",
            "Generate README sections",
            "Create Markdown badges",
            "Support multiple templates (minimal, standard, comprehensive)",
        ],
        "supported_languages": list(SUPPORTED_LANGUAGES.keys()),
    }
