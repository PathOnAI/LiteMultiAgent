from typing import Dict, Any, List, Callable, Union
from abc import ABC, abstractmethod

class Tool:
    def __init__(self, name: str, func: Callable, description: str):
        self.name = name
        self.func = func
        self.description = description

class ToolRegistry:
    _tools: Dict[str, Tool] = {}

    @classmethod
    def register(cls, tool: Tool):
        cls._tools[tool.name] = tool

    @classmethod
    def get_tool(cls, name: str) -> Tool:
        return cls._tools[name]

    @classmethod
    def get_all_tools(cls) -> List[Dict[str, Any]]:
        return [
            {
                "type": "function",
                "function": {
                    "name": tool.name,
                    "description": tool.description,
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "args": {
                                "type": "object",
                                "description": "Arguments for the function"
                            }
                        },
                        "required": ["args"]
                    }
                }
            }
            for tool in cls._tools.values()
        ]