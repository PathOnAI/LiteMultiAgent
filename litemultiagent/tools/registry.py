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
    CORE_TOOLS = None

    
    @classmethod
    def load_core_tools(cls):
        from litemultiagent.tools.db_retrieval import retrieve_db_tool
        from litemultiagent.tools.exec import run_python_script_tool, execute_shell_command_tool
        from litemultiagent.tools.file_retrieval import retrieve_file_tool
        from litemultiagent.tools.file_system import scan_folder_tool
        from litemultiagent.tools.io import read_file_tool, write_to_file_tool, generate_and_download_image_tool
        from litemultiagent.tools.web_agent import call_webagent_tool
        from litemultiagent.tools.web_retrieval import scrape_tool, bing_search_tool

        
        cls.CORE_TOOLS  = [
            retrieve_db_tool,
            run_python_script_tool,
            execute_shell_command_tool,
            retrieve_file_tool,
            scan_folder_tool,
            read_file_tool,
            write_to_file_tool,
            generate_and_download_image_tool,
            call_webagent_tool,
            scrape_tool,
            bing_search_tool
        ]

    @classmethod
    def register(cls, *tools: tuple[Tool]):
        for tool in tools:
            print(f"Registering tool: {tool.name}")  # Debug statement
            cls._tools[tool.name] = tool

    @classmethod
    def get_tool(cls, name: str) -> Tool:
        if cls.CORE_TOOLS == None:
            cls.load_core_tools()
        #check if tool is part of core
        get_corresponding_core_tool = [core_tool for core_tool in cls.CORE_TOOLS if core_tool.name == name]

        is_core_tool = len(get_corresponding_core_tool) > 0
        #if not registered, register here
        if is_core_tool and cls._tools.get(name) == None:
            cls._tools[name] = get_corresponding_core_tool[0]

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

   


