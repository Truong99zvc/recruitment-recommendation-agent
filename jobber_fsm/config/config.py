import os

from loguru import logger

# Base Paths
PROJECT_SOURCE_ROOT: str = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT: str = os.path.dirname(PROJECT_SOURCE_ROOT)

# Derived Paths
SOURCE_LOG_FOLDER_PATH: str = os.path.join(PROJECT_SOURCE_ROOT, "log_files")
USER_PREFERENCES_PATH: str = os.path.join(PROJECT_SOURCE_ROOT, "user_preferences")
PROJECT_TEMP_PATH: str = os.path.join(PROJECT_ROOT, "temp")
PROJECT_TEST_ROOT: str = os.path.join(PROJECT_ROOT, "test")


def _ensure_dir_exists(path: str, dir_name: str) -> None:
    """Ensure a directory exists, creating it and logging if necessary."""
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)
        logger.debug(f"Created {dir_name} folder at: {path}")


# Initialize necessary directories
_ensure_dir_exists(SOURCE_LOG_FOLDER_PATH, "log")
_ensure_dir_exists(USER_PREFERENCES_PATH, "user preferences")
_ensure_dir_exists(PROJECT_TEMP_PATH, "temp")
