import logging
import os
from datetime import datetime


class Logger:
    """Custom logger for API test automation"""

    def __init__(self, log_level=logging.INFO):
        # Create logs directory if it doesn't exist
        log_dir = os.path.join(os.getcwd(), 'logs')
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        # Create a log file with timestamp in the name
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        log_file = os.path.join(log_dir, f'api_test_{timestamp}.log')

        # Configure logging
        self.logger = logging.getLogger('api_tests')
        self.logger.setLevel(log_level)

        # Create handlers
        file_handler = logging.FileHandler(log_file)
        console_handler = logging.StreamHandler()

        # Create formatters
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        # Add handlers to logger
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

        self.log_file = log_file
        self.logger.info(f"Logging initialized to {log_file}")

    def info(self, message):
        """Log info level message"""
        self.logger.info(message)

    def error(self, message):
        """Log error level message"""
        self.logger.error(message)

    def warning(self, message):
        """Log warning level message"""
        self.logger.warning(message)

    def debug(self, message):
        """Log debug level message"""
        self.logger.debug(message)

    def critical(self, message):
        """Log critical level message"""
        self.logger.critical(message)

    def log_request(self, method, url, headers=None, params=None, json=None, data=None):
        """Log details of an API request"""
        self.logger.info(f"REQUEST: {method} {url}")
        if params:
            self.logger.info(f"Request params: {params}")
        if json:
            self.logger.info(f"Request JSON: {json}")
        if data:
            self.logger.info(f"Request data: {data}")
        if headers:
            self.logger.debug(f"Request headers: {headers}")

    def log_response(self, response):
        """Log details of an API response"""
        self.logger.info(f"RESPONSE: Status {response.status_code}")
        try:
            self.logger.info(f"Response body: {response.json()}")
        except:
            self.logger.info(f"Response text: {response.text}")

    def get_log_file_path(self):
        """Return the current log file path"""
        return self.log_file
