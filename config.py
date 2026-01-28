"""
Configuration constants for SpaceX CLI.
"""
# API Configuration
API_URL = "https://api.spacexdata.com/v4/launches"
API_TIMEOUT = 15
API_ALLOWED_RETRY_COUNT = 1
API_RETRY_ALLOWED_ON_TIMEOUT = True
API_RETRY_ALLOWED_ON_HTTP_CODES = [503]
