from typing import Any, Union
import requests

from core.tools.entities.tool_entities import ToolInvokeMessage
from core.tools.tool.builtin_tool import BuiltinTool


class OdooGetTimeOffTool(BuiltinTool):
    
    def _invoke(
        self, user_id: str, tool_parameters: dict[str, Any]
    ) -> Union[ToolInvokeMessage, list[ToolInvokeMessage]]:
        """
        invoke tools
        """
        odoo_email = tool_parameters.get("odooEmail")
        odoo_password = tool_parameters.get("odooPassword")
        
        auth_session = self.login_odoo(odoo_email, odoo_password)
        
        if auth_session:
            time_off_response = self.get_time_off(auth_session)
            print(time_off_response, 'time off response')
            if time_off_response:
                return self.create_text_message(time_off_response)
            else:
                return self.create_text_message("Unknown Timeoff")
        else:
            return self.create_text_message("Authentication failed.")
        
    
    def login_odoo(self,email: str, password: str) -> Union[requests.Session, None]:
        url = "https://odoo-internal.delightfulbeach-a9c21e19.southeastasia.azurecontainerapps.io/web/session/authenticate"
        headers = {
            'Content-Type': 'application/json',
        }
        data = {
            "jsonrpc": "2.0",
            "method": "call",
            "params": {
                "db": "odoo-internal",
                "login": email,
                "password": password
            }
        }
        
        session = requests.Session()
        
        response = session.post(url, headers=headers, json=data)

        if response.status_code == 200:
            return session
        else:
            return None
        
    def get_time_off(self, session:  requests.Session):
        url = 'https://odoo-internal.delightfulbeach-a9c21e19.southeastasia.azurecontainerapps.io/api/time_off'
    
    
        user_data = {
        "username": "Do Thanh Tung",
        "sick_leaves": 15,
        "personal_leaves": 2,
        "annual_leaves": 16,
        "happy_leaves": 4
        }

        formatted_data = (
            f"username: \"{user_data['username']}\",\n"
            f"sick_leaves: {user_data['sick_leaves']}\n"
            f"personal_leaves: {user_data['personal_leaves']}\n"
            f"annual_leaves: {user_data['annual_leaves']}\n"
            f"happy_leaves: {user_data['happy_leaves']}"
        )
    
        response = session.get(url) 
        if response.status_code == 200:
            return formatted_data
            # return response.json().get('result')
        else:
            return None
        
