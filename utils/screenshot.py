import json
import os
import time
from datetime import datetime

import allure
from allure_commons.types import AttachmentType
import requests

from api.endpoints import HOST


class ApiScreenshot:
    """
    Utility class for taking "screenshots" of API state
    This captures API responses as JSON files for debugging purposes
    """

    def __init__(self):
        """Initialize the screenshot directory"""
        self.screenshots_dir = os.path.join(os.getcwd(), 'screenshots')
        if not os.path.exists(self.screenshots_dir):
            os.makedirs(self.screenshots_dir)

    def take_api_snapshot(self, name="api_snapshot"):
        """
        Take a snapshot of various API endpoints to capture the current state
        Attach the snapshots to the Allure report and save them as files
        """
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{name}_{timestamp}.json"
        filepath = os.path.join(self.screenshots_dir, filename)

        # Try to get a snapshot of all entities
        try:
            response = requests.get(f"{HOST}/api/getAll")
            if response.status_code == 200:
                data = response.json()

                # Save to file
                with open(filepath, 'w') as f:
                    json.dump(data, f, indent=4)

                # Attach to Allure report
                allure.attach(
                    json.dumps(data, indent=4),
                    name=f"API Snapshot: {name}",
                    attachment_type=AttachmentType.JSON
                )

                return filepath
            else:
                error_message = f"Failed to take API snapshot. Status code: {response.status_code}"
                allure.attach(
                    error_message,
                    name="API Snapshot Error",
                    attachment_type=AttachmentType.TEXT
                )
                return None
        except Exception as e:
            error_message = f"Exception while taking API snapshot: {str(e)}"
            allure.attach(
                error_message,
                name="API Snapshot Error",
                attachment_type=AttachmentType.TEXT
            )
            return None

    def take_service_health_snapshot(self):
        """
        Take a snapshot of the service health by checking various endpoints
        Returns a dictionary with health status information
        """
        health_data = {
            "timestamp": datetime.now().isoformat(),
            "endpoints": {}
        }

        # List of key endpoints to check
        endpoints = [
            "/api/getAll",
            # Add other endpoints you want to check
        ]

        for endpoint in endpoints:
            try:
                start_time = time.time()
                response = requests.get(f"{HOST}{endpoint}")
                response_time = time.time() - start_time

                health_data["endpoints"][endpoint] = {
                    "status_code": response.status_code,
                    "response_time": round(response_time, 3),
                    "available": response.status_code < 400
                }
            except Exception as e:
                health_data["endpoints"][endpoint] = {
                    "status_code": None,
                    "response_time": None,
                    "available": False,
                    "error": str(e)
                }

        # Save and attach the health snapshot
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"health_snapshot_{timestamp}.json"
        filepath = os.path.join(self.screenshots_dir, filename)

        with open(filepath, 'w') as f:
            json.dump(health_data, f, indent=4)

        allure.attach(
            json.dumps(health_data, indent=4),
            name="Service Health Snapshot",
            attachment_type=AttachmentType.JSON
        )

        return health_data
