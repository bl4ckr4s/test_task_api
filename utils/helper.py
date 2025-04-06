import json

import allure
from allure_commons.types import AttachmentType


class Helper:

    def attach_response(self, response: dict[str, object] | list[dict[str, object]]) -> None:
        """Attach API response to Allure report

        Args:
            response: Response data to attach
        """
        response_str = json.dumps(response, indent=4)
        allure.attach(body=response_str, name="Ответ API", attachment_type=AttachmentType.JSON)
