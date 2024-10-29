# tool_creation_agent.py

import logging
import json
import ast
import importlib.util
import shutil
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
from litellm import completion

logger = logging.getLogger(__name__)


class Colors:
    """ANSI color codes for terminal output."""
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class ToolValidator(ast.NodeVisitor):
    """Validates Python AST for potentially unsafe operations."""

    def __init__(self):
        self.errors: List[str] = []

    def visit_Import(self, node: ast.Import) -> None:
        """Check for unsafe imports."""
        for name in node.names:
            if name.name.startswith('_'):
                self.errors.append(f"Attempted to import private module: {name.name}")
        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        """Check for unsafe import from statements."""
        if node.module and node.module.startswith('_'):
            self.errors.append(f"Attempted to import from private module: {node.module}")
        for name in node.names:
            if name.name.startswith('_'):
                self.errors.append(f"Attempted to import private name: {name.name}")
        self.generic_visit(node)

    def visit_Call(self, node: ast.Call) -> None:
        """Check for unsafe function calls."""
        if isinstance(node.func, ast.Name):
            if node.func.id in ['eval', 'exec', 'compile']:
                self.errors.append(f"Attempted to use {node.func.id}")
        elif isinstance(node.func, ast.Attribute):
            if node.func.attr.startswith('_'):
                self.errors.append(f"Attempted to call private method: {node.func.attr}")
        self.generic_visit(node)

    def visit_Attribute(self, node: ast.Attribute) -> None:
        """Check for unsafe attribute access."""
        if node.attr.startswith('__'):
            self.errors.append(f"Attempted to access private attribute: {node.attr}")
        self.generic_visit(node)

def get_default_system_prompt() -> str:
    """Get the default system prompt for the agent."""
    return """You are an AI assistant designed to iteratively build and execute Python functions using tools provided to you.

When creating tools, you MUST ALWAYS include all four required arguments:
1. "name": The name of the tool (string)
2. "code": The Python code for the tool (string)
3. "description": A description of what the tool does (string)
4. "parameters": A dictionary defining the input parameters the function accepts, following this exact format:
    {
        "parameter_name": {
            "type": "type_of_parameter",
            "description": "description_of_parameter"
        }
    }

Example of a correct tool creation:
{
    "name": "calculate_sum",
    "code": "def calculate_sum(a, b):\\n    return a + b",
    "description": "Adds two numbers together",
    "parameters": {
        "a": {"type": "number", "description": "First number to add"},
        "b": {"type": "number", "description": "Second number to add"}
    }
}

Never omit the parameters field, even if the function has no parameters (use an empty object in that case).

Your workflow should include:
- Creating tools with ALL required arguments (name, code, description, AND parameters)
- Handling errors by adjusting your tools or arguments as necessary
- Being token-efficient: avoid returning excessively long outputs
- When creating or updating tools, provide the complete code as it will be used without any edits
- Testing your tools after creation

Remember: Every tool creation MUST include the parameters field that matches the function's parameters."""

class ToolCreationAgent:
    """
    An agent that interacts with LLMs, validates, generates, and executes tools.
    """

    DEFAULT_TOOL_CONFIG = [{
        "type": "function",
        "function": {
            "name": "create_or_update_tool",
            "description": "Creates or updates a tool with the specified name, code, description, and parameters using a secure file-based approach.",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "The tool name."},
                    "code": {"type": "string", "description": "The Python code for the tool."},
                    "description": {"type": "string", "description": "A description of the tool."},
                    "parameters": {
                        "type": "object",
                        "description": "A dictionary defining the parameters for the tool.",
                        "additionalProperties": {
                            "type": "object",
                            "properties": {
                                "type": {"type": "string", "description": "Data type of the parameter."},
                                "description": {"type": "string", "description": "Description of the parameter."}
                            },
                            "required": ["type", "description"]
                        }
                    }
                },
                "required": ["name", "code", "description", "parameters"]
            }
        }
    }]

    def __init__(
            self,
            model_name: str = "anthropic/claude-3-5-sonnet-20240620",
            tools: List[Dict[str, Any]] = None,
            max_retries: int = 3,
            cache_dir: str = "cache"
    ):
        self.system_prompt = get_default_system_prompt()
        self.model_name = model_name
        self.tools = tools or self.DEFAULT_TOOL_CONFIG
        self.max_retries = max_retries
        self.messages: List[Dict[str, str]] = [
            {"role": "system", "content": self.system_prompt}
        ]
        self.available_functions: Dict[str, callable] = {}
        self.cache_dir = Path(cache_dir)
        self.initialize_cache()

        # Automatically register the create_or_update_tool function
        self.register_tool("create_or_update_tool", self.create_or_update_tool)

    def initialize_cache(self) -> None:
        try:
            if self.cache_dir.exists():
                shutil.rmtree(self.cache_dir)
            self.cache_dir.mkdir(exist_ok=True)
            (self.cache_dir / "__init__.py").touch()
            logger.info("Cache directory initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing cache directory: {e}")
            raise

    def cleanup_cache(self) -> None:
        try:
            if self.cache_dir.exists():
                shutil.rmtree(self.cache_dir)
                logger.info("Cache directory cleaned up successfully")
        except Exception as e:
            logger.error(f"Error cleaning up cache directory: {e}")

    def validate_tool_code(self, code: str) -> List[str]:
        validator = ToolValidator()
        try:
            tree = ast.parse(code)
            validator.visit(tree)
            return validator.errors
        except SyntaxError as e:
            return [f"Syntax error in code: {str(e)}"]

    def create_tool_module(self, name: str, code: str) -> Path:
        try:
            module_path = self.cache_dir / f"{name}.py"
            with open(module_path, 'w') as f:
                f.write(code)
            return module_path
        except Exception as e:
            logger.error(f"Error creating tool module: {e}")
            raise

    def load_tool_module(self, name: str, module_path: Path) -> Any:
        try:
            spec = importlib.util.spec_from_file_location(name, module_path)
            if spec is None:
                raise ImportError(f"Could not load spec for module {name}")

            module = importlib.util.module_from_spec(spec)
            if spec.loader is None:
                raise ImportError(f"Could not load module {name}")

            spec.loader.exec_module(module)
            return getattr(module, name)
        except Exception as e:
            logger.error(f"Error loading tool module: {e}")
            raise

    def create_or_update_tool(self, name: str, code: str, description: str,
                              parameters: Dict[str, Any]) -> Tuple[str, callable, str, Dict[str, Any]]:
        try:
            validation_errors = self.validate_tool_code(code)
            if validation_errors:
                error_msg = f"Tool validation failed: {'; '.join(validation_errors)}"
                logger.error(error_msg)
                raise ValueError(error_msg)

            module_path = self.create_tool_module(name, code)
            func = self.load_tool_module(name, module_path)

            return name, func, description, parameters
        except Exception as e:
            logger.error(f"Error creating/updating tool '{name}': {e}")
            raise

    def register_tool(self, name: str, func: callable) -> None:
        self.available_functions[name] = func
        logger.info(f"Registered tool: {name}")
        print(f"{Colors.OKGREEN}{Colors.BOLD}Registered tool:{Colors.ENDC} {name}")

    def send_prompt(self, user_input: str) -> Optional[Tuple[str, callable, str, Dict[str, Any]]]:
        try:
            self.messages.append({"role": "user", "content": user_input})
            return self._send_completion_request()
        except Exception as e:
            logger.error(f"Error in send_prompt: {e}")
            self.messages.append({"role": "error", "content": f"Error: {str(e)}"})
            return None

    def _send_completion_request(
            self,
            retry_count: int = 0
    ) -> Optional[Tuple[str, callable, str, Dict[str, Any]]]:
        try:
            if retry_count >= self.max_retries:
                logger.error("Max retries reached")
                self.messages.append({
                    "role": "error",
                    "content": "Max retries reached without successful completion"
                })
                return None

            response = completion(
                model=self.model_name,
                messages=self.messages,
                tools=self.tools,
                tool_choice="required"
            )

            response_message = response.choices[0].message

            if response_message.content:
                logger.info(f"LLM Response: {response_message.content}")
                print(f"{Colors.OKCYAN}{Colors.BOLD}LLM Response:{Colors.ENDC}\n{response_message.content}\n")

            self.messages.append(response_message)

            if response_message.tool_calls:
                for tool_call in response_message.tool_calls:
                    function_name = tool_call.function.name
                    args = json.loads(tool_call.function.arguments)

                    logger.info(f"Calling tool: {function_name} with args: {args}")
                    tool_result = self._call_tool(function_name, args)

                    self.messages.append({
                        "role": "tool",
                        "name": function_name,
                        "tool_call_id": tool_call.id,
                        "content": self._serialize_tool_result(tool_result)
                    })

                    if isinstance(tool_result, tuple) and len(tool_result) == 4:
                        return tool_result

                return self._send_completion_request(retry_count + 1)

            return self._send_completion_request(retry_count + 1)

        except Exception as e:
            logger.error(f"Error in completion request: {e}")
            self.messages.append({"role": "error", "content": f"Error: {str(e)}"})
            return self._send_completion_request(retry_count + 1)

    def _call_tool(self, function_name: str, args: Dict[str, Any]) -> Any:
        try:
            func = self.available_functions.get(function_name)
            if not func:
                error_msg = f"Tool '{function_name}' not found."
                logger.error(error_msg)
                print(f"{Colors.FAIL}{Colors.BOLD}Error:{Colors.ENDC} {error_msg}")
                return error_msg

            print(f"{Colors.OKBLUE}{Colors.BOLD}Calling tool:{Colors.ENDC} {function_name} with args: {args}")
            result = func(**args)
            print(f"{Colors.OKCYAN}{Colors.BOLD}Result of {function_name}:{Colors.ENDC} {result}")
            return result

        except Exception as e:
            error_msg = f"Error executing '{function_name}': {e}"
            logger.error(error_msg)
            return error_msg

    def _serialize_tool_result(self, tool_result: Any, max_length: int = 5000) -> str:
        try:
            serialized_result = json.dumps(tool_result)
            if len(serialized_result) > max_length:
                truncated = serialized_result[:max_length]
                return truncated + f"\n\n{Colors.WARNING}(Note: Result was truncated to {max_length} characters out of {len(serialized_result)} total characters.){Colors.ENDC}"
            return serialized_result
        except TypeError:
            return str(tool_result)

    def get_message_history(self) -> List[Dict[str, str]]:
        """Get the complete message history."""
        return self.messages

    def clear_message_history(self) -> None:
        """Clear the message history except for the system prompt."""
        self.messages = [{"role": "system", "content": self.system_prompt}]