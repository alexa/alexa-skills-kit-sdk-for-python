"""Test Django settings file, to run adapter view unit tests."""

# Mandatory settings attribute
SECRET_KEY = 'dummy'

# Settings attribute to not provide log messages during tests
DEBUG = False

# Default Charset required for test responses
DEFAULT_CHARSET = "utf-8"

# Default Content Type required for test responses
DEFAULT_CONTENT_TYPE = "text/html"
