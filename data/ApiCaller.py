"""
API Caller module with retry logic and timeout handling.
"""
import time
import logging
import socket
from typing import Optional, Dict, Any, Callable
from urllib.request import urlopen, Request
from urllib.error import HTTPError, URLError
import json


class ApiCaller:
    """Handles API calls with configurable retry logic and timeout."""
    
    def __init__(
        self,
        timeout: int = 15,
        allowed_retry_count: int = 1,
        retry_allowed_on_timeout: bool = True,
        retry_allowed_on_http_codes: list[int] = None,
        retry_delay: float = 1.0,
        exponential_backoff: bool = False
    ):
        """
        Initialize API caller.
        
        Args:
            timeout: HTTP timeout in seconds
            allowed_retry_count: Maximum number of retries
            retry_allowed_on_timeout: Whether to retry on timeout
            retry_allowed_on_http_codes: List of HTTP status codes that allow retry (e.g., [404, 503])
            retry_delay: Initial delay between retries in seconds
            exponential_backoff: Use exponential backoff for retries
        """
        self.timeout = timeout
        self.allowed_retry_count = allowed_retry_count
        self.retry_allowed_on_timeout = retry_allowed_on_timeout
        self.retry_allowed_on_http_codes = retry_allowed_on_http_codes or []
        self.retry_delay = retry_delay
        self.exponential_backoff = exponential_backoff
        self.logger = logging.getLogger(__name__)
    
    def fetch(self, url: str) -> tuple[Optional[list[Dict[str, Any]]], Optional[int], Optional[str]]:
        """
        Fetch data from URL with retry logic.
        
        Returns:
            Tuple of (data, error_code, error_message)
            - data: Parsed JSON data if successful, None otherwise
            - error_code: 1 for timeout, 2 for non-200 response, 3 for unexpected error
            - error_message: Error description
        """
        attempt = 0
        delay = self.retry_delay
        
        while attempt <= self.allowed_retry_count:
            try:
                if attempt > 0:
                    self.logger.debug(f"Retry attempt {attempt} for URL: {url}")
                
                request = Request(url)
                with urlopen(request, timeout=self.timeout) as response:
                    status_code = response.getcode()
                    
                    if status_code != 200:
                        self.logger.debug(f"HTTP status code: {status_code}")
                        
                        if status_code in self.retry_allowed_on_http_codes and attempt < self.allowed_retry_count:
                            self.logger.debug(f"Status code {status_code} is retryable, retrying...")
                            attempt += 1
                            if self.exponential_backoff:
                                delay *= 2
                            time.sleep(delay)
                            continue
                        
                        return None, 2, f"Non-200 HTTP response: {status_code}"
                    
                    data = json.loads(response.read().decode('utf-8'))
                    return data, None, None
                    
            except (TimeoutError, socket.timeout) as e:
                self.logger.debug(f"HTTP timeout after {self.timeout} seconds")
                
                if self.retry_allowed_on_timeout and attempt < self.allowed_retry_count:
                    attempt += 1
                    if self.exponential_backoff:
                        delay *= 2
                    time.sleep(delay)
                    continue
                
                return None, 1, f"Request timeout: {str(e)}"
                
            except HTTPError as e:
                status_code = e.code
                self.logger.debug(f"HTTP error code: {status_code}")
                
                if status_code in self.retry_allowed_on_http_codes and attempt < self.allowed_retry_count:
                    self.logger.debug(f"Status code {status_code} is retryable, retrying...")
                    attempt += 1
                    if self.exponential_backoff:
                        delay *= 2
                    time.sleep(delay)
                    continue
                
                return None, 2, f"HTTP error {status_code}: {str(e)}"
                
            except URLError as e:
                self.logger.debug(f"URL error: {str(e)}")
                
                if self.retry_allowed_on_timeout and attempt < self.allowed_retry_count:
                    attempt += 1
                    if self.exponential_backoff:
                        delay *= 2
                    time.sleep(delay)
                    continue
                
                return None, 1, f"URL error: {str(e)}"
                
            except Exception as e:
                self.logger.debug(f"Unexpected error: {str(e)}")
                return None, 3, f"Unexpected error: {str(e)}"
        
        return None, 1, "Max retries exceeded"
    
    def fetch_stream(self, url: str) -> tuple[Optional[Any], Optional[int], Optional[str]]:
        """
        Fetch data as a stream (generator) for large datasets.
        
        Returns:
            Generator yielding JSON objects, or tuple with error info
        """
        # For now, we'll fetch all data and yield items
        # In future, could implement true streaming JSON parsing
        data, error_code, error_message = self.fetch(url)
        if error_code:
            return None, error_code, error_message
        
        def stream_generator():
            for item in data:
                yield item
        
        return stream_generator(), None, None
