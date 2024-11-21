import dspy
from typing import List, Dict, Any, Optional
from pydantic import BaseModel
import logging
import os
import json

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("io_agent.log", mode="w"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Configure LM
lm = dspy.LM('openai/gpt-4o-mini')
dspy.configure(lm=lm)

class FileToolOutput(BaseModel):
    """Output format for file operations"""
    status: str
    content: Optional[str] = None
    error: Optional[str] = None

class FileReactSignature(dspy.Signature):
    """Process file operations using available tools and return results"""
    instruction = dspy.InputField(desc="User instruction for file operation")
    tools_description = dspy.InputField(desc="Description of available tools")
    answer = dspy.OutputField(desc="Result of the file operation")

class ReadFileTool:
    """Tool for reading file contents"""
    name = "read_file"
    description = """Read content from a file. 
    Input must be a JSON string with 'file_path' and optional 'encoding'.
    Example: '{"file_path": "test_files/example.txt", "encoding": "utf-8"}'"""
    args = {"file_path": str, "encoding": str}
    
    def __call__(self, tool_input: str, *args, **kwargs) -> str:
        try:
            # Ensure the tool_input is a proper dictionary string
            if not tool_input.strip().startswith('{'):
                tool_input = f'{{"file_path": "{tool_input.strip()}", "encoding": "utf-8"}}'
            
            # Parse input
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

class WriteFileTool:
    """Tool for writing content to files"""
    name = "write_file"
    description = """Write content to a file. 
    Input must be a JSON string with 'file_path', 'text', and optional 'encoding'.
    Example: '{"file_path": "test_files/output.txt", "text": "Hello World", "encoding": "utf-8"}'"""
    args = {"file_path": str, "text": str, "encoding": str}
    
    def __call__(self, tool_input: str, *args, **kwargs) -> str:
        try:
            logger.info(f"Write tool received input: {tool_input}")
            
            # Handle string input formatting
            if not tool_input.strip().startswith('{'):
                # Try to parse from instruction-like format
                parts = tool_input.split(' to file ')
                if len(parts) == 2:
                    content = parts[0].strip('"\'')
                    file_path = parts[1].strip('"\'')
                    tool_input = json.dumps({
                        "file_path": file_path,
                        "text": content,
                        "encoding": "utf-8"
                    })
            
            # Parse input
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

class IOAgent(dspy.Module):
    """Agent for handling file operations using ReAct framework"""
    
    def __init__(self):
        super().__init__()
        
        # Create test directory
        os.makedirs("test_files", exist_ok=True)
        
        # Create some initial test files
        self._create_initial_files()
        
        # Initialize tools
        self.read_tool = ReadFileTool()
        self.write_tool = WriteFileTool()
        
        # Tool descriptions with explicit examples
        self.tools_description = """
        Available tools:

        1. read_file: Read content from a file
           IMPORTANT: Input must be a properly formatted JSON string.
           Example: '{"file_path": "test_files/example.txt", "encoding": "utf-8"}'
           
        2. write_file: Write content to a file
           IMPORTANT: Input must be a properly formatted JSON string.
           Example: '{"file_path": "test_files/output.txt", "text": "Hello World", "encoding": "utf-8"}'
           
        For writing files, you must ALWAYS use proper JSON format with the exact field names shown above.
        For reading files, you must ALWAYS use proper JSON format with the exact field names shown above.
        The test_files directory already exists and can be used directly.
        """
        
        # Initialize ReAct agent
        self.agent = dspy.ReAct(
            signature=FileReactSignature,
            tools=[self.read_tool, self.write_tool]
        )
    
    def _create_initial_files(self):
        """Create initial test files"""
        with open("test_files/sample.txt", "w") as f:
            f.write("This is a sample file content.\nIt has multiple lines.\n")
        
        with open("test_files/config.json", "w") as f:
            json.dump({"name": "test", "version": "1.0"}, f)
    
    def forward(self, instruction: str) -> str:
        """Process the instruction and return results"""
        try:
            logger.info(f"Processing instruction: {instruction}")
            result = self.agent(
                instruction=instruction,
                tools_description=self.tools_description
            )
            logger.info(f"Result: {result.answer}")
            return result.answer
        except Exception as e:
            logger.error(f"Error in IOAgent.forward: {str(e)}")
            return f"Error processing instruction: {str(e)}"

def main():
    """Example usage of the IOAgent"""
    # Initialize agent
    agent = IOAgent()
    
    # Test instructions
    test_instructions = [
        'Write "Hello, this is a test file!" to file "test_files/input.txt"',
        'Read the content of file "test_files/input.txt"',
        'Write the following JSON content to "test_files/config.json": {"name": "test", "version": "1.0"}',
        'Read "test_files/config.json" and write its content to "test_files/config_backup.json"',
        'Read a non-existent file "test_files/missing.txt"'
    ]
    
    print("\nProcessing test instructions:\n")
    for idx, instruction in enumerate(test_instructions, 1):
        print(f"\nInstruction {idx}: {instruction}")
        result = agent(instruction)
        print(f"Result: {result}")
        print("-" * 70)

if __name__ == "__main__":
    main()