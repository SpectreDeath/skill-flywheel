"""
Constants for the Skill Flywheel Server.
"""

if __name__ == "__main__":
    # Discovery constants
    DEFAULT_LIMIT = 100
    DEFAULT_OFFSET = 0
    CACHE_THRESHOLD = 10

    # Security constants
    MIN_JWT_SECRET_LENGTH = 32
    INSECURE_SECRET_PATTERNS = [
        "your-openai-api-key-here",
        "your-gemini-api-key-here",
        "test-key-for-local-development",
        "sk-test-key",
        "placeholder",
    ]

    # Server constants
    SERVER_NAME = "SkillFlywheel"
    TRANSPORT = "stdio"
    PORT = 8000