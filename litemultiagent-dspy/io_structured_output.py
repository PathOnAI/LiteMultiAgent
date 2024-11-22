import os
import json
import logging
from typing import Any, Dict
from datetime import datetime
from ast import literal_eval

import dspy
from dsp import LM
from openai import OpenAI
from dotenv import load_dotenv
from pydantic import BaseModel, Field

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("dspy_io.log", mode="w"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

class OpenAILLM(LM):
    """Custom LLM client using OpenAI's API"""
    def __init__(
            self,
            model: str,
            api_key: str,
            **kwargs
    ):
        super().__init__(model=model)
        self.api_key = api_key
        self.model = model
        self.kwargs.update(kwargs)

    def basic_request(self, prompt, **kwargs):
        config = dict()
        config.update(self.kwargs)
        config['model'] = self.model
        config.update(kwargs)

        messages = [
            {
                "role": "system",
                "content": "You are a helpful assistant."
            },
            {
                'role': 'user',
                'content': prompt
            }
        ]

        client = OpenAI(
            api_key=self.api_key
        )

        response = client.chat.completions.create(
            messages=messages,
            **config,
        )

        self.history.append({
            'prompt': prompt,
            'response': response,
            'kwargs': config,
        })

        return response

    def get_choice_text(self, choice: Dict[str, Any]) -> str:
        message = choice.message
        content = message.content
        if message.tool_calls is not None:
            return str([
                {
                    'name': tool.function.name,
                    'arguments': tool.function.arguments
                } for tool in message.tool_calls])
        return content

    def __call__(self, prompt, only_completed=True, return_sorted=False, **kwargs):
        response = self.request(prompt, **kwargs)
        completions = [self.get_choice_text(choice)
                      for choice in response.choices]
        return completions

class FileTool:
    """Base class for file operation tools"""
    def __init__(self, name: str, description: str, args: Dict[str, type]):
        self.name = name
        self.description = description
        self.args = args

    def __call__(self, tool_input: str) -> str:
        """Process the tool input and return result"""
        raise NotImplementedError()

class ReadFileTool(FileTool):
    """Tool for reading file contents"""
    def __init__(self):
        super().__init__(
            name="read_file",
            description="""Read content from a file. 
            Input must be a JSON string with 'file_path' and optional 'encoding'.
            Example: '{"file_path": "test_files/example.txt", "encoding": "utf-8"}'""",
            args={"file_path": str, "encoding": str}
        )

    def __call__(self, tool_input: str) -> str:
        try:
            # Parse input
            if not tool_input.strip().startswith('{'):
                tool_input = f'{{"file_path": "{tool_input.strip()}", "encoding": "utf-8"}}'
            
            params = json.loads(tool_input.replace("'", '"'))
            file_path = params.get("file_path", "").strip('"\'')
            encoding = params.get("encoding", "utf-8")
            
            logger.info(f"Reading file: {file_path} with encoding: {encoding}")
            
            if not file_path:
                raise ValueError("File path cannot be empty")
            
            if not os.path.exists(file_path):
                return json.dumps({
                    "status": "error",
                    "error": f"File not found: {file_path}"
                })
            
            with open(file_path, 'r', encoding=encoding) as f:
                content = f.read()
            
            return json.dumps({
                "status": "success",
                "content": content
            })
            
        except Exception as e:
            logger.error(f"Error in ReadFileTool: {str(e)}")
            return json.dumps({
                "status": "error",
                "error": str(e)
            })

class WriteFileTool(FileTool):
    """Tool for writing content to files"""
    def __init__(self):
        super().__init__(
            name="write_file",
            description="""Write content to a file. 
            Input must be a JSON string with 'file_path', 'text', and optional 'encoding'.
            Example: '{"file_path": "test_files/output.txt", "text": "Hello World", "encoding": "utf-8"}'""",
            args={"file_path": str, "text": str, "encoding": str}
        )

    def __call__(self, tool_input: str) -> str:
        try:
            logger.info(f"Write tool received input: {tool_input}")
            
            # Handle string input formatting
            if not tool_input.strip().startswith('{'):
                parts = tool_input.split(' to file ')
                if len(parts) == 2:
                    content = parts[0].strip('"\'')
                    file_path = parts[1].strip('"\'')
                    tool_input = json.dumps({
                        "file_path": file_path,
                        "text": content,
                        "encoding": "utf-8"
                    })
            
            params = json.loads(tool_input.replace("'", '"'))
            file_path = params.get("file_path", "").strip('"\'')
            text = params.get("text", "").strip('"\'')
            encoding = params.get("encoding", "utf-8")
            
            logger.info(f"Writing to file: {file_path}")
            logger.info(f"Content: {text}")
            
            if not file_path:
                raise ValueError("File path cannot be empty")
            
            # Create directory if it doesn't exist
            dir_path = os.path.dirname(os.path.abspath(file_path))
            if dir_path:
                os.makedirs(dir_path, exist_ok=True)
            
            with open(file_path, 'w', encoding=encoding) as f:
                f.write(text)
            
            return json.dumps({
                "status": "success",
                "content": f"Successfully wrote to {file_path}"
            })
            
        except Exception as e:
            logger.error(f"Error in WriteFileTool: {str(e)}")
            return json.dumps({
                "status": "error",
                "error": str(e)
            })

class IOToolHandler:
    """Handler for file I/O operations"""
    def __init__(self):
        self.read_tool = ReadFileTool()
        self.write_tool = WriteFileTool()
        
        # Create test directory
        os.makedirs("test_files", exist_ok=True)
        
        # Create some initial test files
        self._create_initial_files()

    def _create_initial_files(self):
        """Create initial test files"""
        with open("test_files/sample.txt", "w") as f:
            f.write("This is a sample file content.\nIt has multiple lines.\n")
        
        with open("test_files/config.json", "w") as f:
            json.dump({"name": "test", "version": "1.0"}, f)
        
    def convert_to_schema(self, tool: FileTool) -> Dict[str, Any]:
        """Convert a tool to OpenAI function calling schema"""
        return {
            'type': 'function',
            'function': {
                'name': tool.name,
                'description': tool.description,
                'parameters': {
                    'type': 'object',
                    'properties': {
                        param: {'type': 'string'} for param in tool.args.keys()
                    },
                    'required': list(tool.args.keys())
                }
            }
        }

    def process_tool_response(self, response: str, tool_name: str) -> str:
        """Process the LLM's tool calling response"""
        try:
            json_calling = literal_eval(response)[0]
            tool_args = literal_eval(json_calling['arguments'])
            
            if tool_name == 'read_file':
                return self.read_tool(json.dumps(tool_args))
            elif tool_name == 'write_file':
                return self.write_tool(json.dumps(tool_args))
            else:
                return f"Tool {tool_name} not found"
        except Exception as e:
            return f"Error processing tool response: {str(e)}\nResponse: {response}"

def main():
    # Initialize the LLM client
    lm = OpenAILLM(
        model=os.getenv('MODEL_NAME', 'gpt-4o-mini'),
        api_key=os.getenv('OPENAI_API_KEY'),
        max_tokens=2048,
        temperature=0.1
    )

    # Configure DSPy to use our LLM
    dspy.settings.configure(lm=lm)

    # Initialize IO tool handler
    io_handler = IOToolHandler()

    # Define available tools with their schemas
    tools = [
        io_handler.convert_to_schema(io_handler.read_tool),
        io_handler.convert_to_schema(io_handler.write_tool)
    ]

    # Create predictor
    predictor = dspy.Predict('question -> answer', tools=tools)
    
    # Test file operations
    test_cases = [
        'Write "Hello, this is a test file!" to file "test_files/output.txt"',
        'Read the content of file "test_files/output.txt"',
        'Write a JSON configuration to "test_files/config.json" with content {"name": "test", "version": "2.0"}',
        'Read the content of file "test_files/config.json"',
        'Read a non-existent file "test_files/missing.txt"'
    ]

    for question in test_cases:
        print(f"\nProcessing: {question}")
        gen = predictor(question=question)
        
        # Determine which tool to use based on the question
        tool_name = 'write_file' if 'Write' in question else 'read_file'
        result = io_handler.process_tool_response(gen.answer, tool_name)
        print(f"Result: {result}")

if __name__ == "__main__":
    main()