from typing import Dict, Any, Callable, List
from typing import Optional

class Tool:
    def __init__(self, name: str, func: Callable, description: str, parameters: Dict[str, Any]):
        self.name = name
        self.func = func
        self.description = description
        self.parameters = parameters

class ToolRegistry:
    _instance = None
    _tools: Dict[str, Tool] = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ToolRegistry, cls).__new__(cls)
            cls._register_all_tools()  # Register all tools when the singleton is first created
        return cls._instance

    @classmethod
    def register(cls, tool: Tool):
        print(f"Registering tool: {tool.name}")  # Debug statement
        cls._tools[tool.name] = tool

    @classmethod
    def get_tool(cls, name: str) -> Tool:
        return cls._tools.get(name)

    @classmethod
    def get_all_tools(cls) -> Dict[str, Tool]:
        return cls._tools

    @classmethod
    def get_tool_description(cls, name: str) -> Optional[Dict[str, Any]]:
        tool = cls.get_tool(name)
        if tool is None:
            return None  # or return {} if you prefer an empty dictionary

        # Create a copy of the tool parameters and remove 'required' from properties
        properties = {
            param: {k: v for k, v in details.items() if k != "required"}
            for param, details in tool.parameters.items()
        }

        # Ensure the 'required' field is always a list
        required_params = [param for param, details in tool.parameters.items() if details.get("required", False)]

        return {
            "type": "function",
            "function": {
                "name": tool.name,
                "description": tool.description,
                "parameters": {
                    "type": "object",
                    "properties": properties,
                    "required": required_params if required_params else []  # Ensure it's always an array
                }
            }
        }

    @classmethod
    def _register_all_tools(cls):
        # Import the tool registration functions here
        try:
            from litemultiagent.tools.io_tool import register_io_tools
            print("Registering IO tools...")  # Debug statement
            register_io_tools()
            print("Finished registering IO tools.")  # Debug statement
            from litemultiagent.tools.db_retrieval_tool import register_db_retrieval_tools
            print("Registering DB retrieval tools...")  # Debug statement
            register_db_retrieval_tools()
            print("Finished registering DB retrieval tools.")  # Debug statement
            from litemultiagent.tools.file_retrieval_tool import register_file_retrieval_tools
            print("Registering File retrieval tools...")  # Debug statement
            register_file_retrieval_tools()
            print("Finished registering file retrieval tools.")  # Debug statement
            from litemultiagent.tools.web_retrieval_tool import register_web_retrieval_tools
            print("Registering Web retrieval tools...")  # Debug statement
            register_web_retrieval_tools()
            print("Finished registering web retrieval tools.")  # Debug statement
            from litemultiagent.tools.exec_tool import register_exec_tools
            print("Registering Exec tools...")  # Debug statement
            register_exec_tools()
            print("Finished registering exec tools.")  # Debug statement
            from litemultiagent.tools.file_system_tool import register_file_system_tools
            print("Registering File System tools...")  # Debug statement
            register_file_system_tools()
            print("Finished registering file system tools.")  # Debug statement
            from litemultiagent.tools.web_agent_tool import register_webagent_tools
            print("Registering Web Agent tools...")  # Debug statement
            register_webagent_tools()
            print("Finished registering web agent tools.")  # Debug statement
        except Exception as e:
            print(f"Error while registering tools: {e}")  # Debug statement to catch any import or registration issues



