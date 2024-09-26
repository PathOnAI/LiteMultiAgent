import subprocess

from litemultiagent.agents.core.DefaultAgent import DefaultAgent

from typing import Optional

def execute_shell_command(command, wait=True):
    try:
        if wait:
            result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)
            return result.stdout.strip() if result.stdout else result.stderr.strip()
        else:
            subprocess.Popen(command, shell=True)
            return "Command executed in non-blocking mode."
    except subprocess.CalledProcessError as e:
        return f"Error executing command '{command}': {e.stderr.strip()}"

def run_python_script(script_name):
    try:
        result = subprocess.run(["python", script_name], capture_output=True, text=True, check=True)
        res = f"stdout:{result.stdout}"
        if result.stderr:
            res += f"stderr:{result.stderr}"
        return res
    except subprocess.CalledProcessError as e:
        return f"Error:{e}"

tools = [
    {
        "type": "function",
        "function": {
            "name": "run_python_script",
            "description": "Execute a Python script in a subprocess.",
            "parameters": {
                "type": "object",
                "properties": {
                    "script_name": {
                        "type": "string",
                        "description": "The name with path of the script to be executed."
                    }
                },
                "required": [
                    "script_name"
                ]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "execute_shell_command",
            "description": "Execute a shell command in a subprocess.",
            "parameters": {
                "type": "object",
                "properties": {
                    "command": {
                        "type": "string",
                        "description": "The shell command to be executed."
                    },
                    "wait": {
                        "type": "boolean",
                        "description": "Wait for the command to complete. Set to true for blocking execution and false for non-blocking."
                    }
                },
                "required": [
                    "command"
                ]
            }
        }
    }
]

available_tools = {
    "run_python_script": run_python_script,
    "execute_shell_command": execute_shell_command,
}

class ExecAgent(DefaultAgent):
    def __init__(self, meta_task_id: Optional[str] = None, task_id: Optional[int] = None):
        super().__init__("use_exec_agent", tools, available_tools, meta_task_id, task_id)

if __name__ == "__main__":
    def use_exec_agent(query: str, meta_task_id: Optional[str] = None, task_id: Optional[int] = None) -> str:
        agent = ExecAgent(meta_task_id, task_id)
        agent.messages = [{"role": "system", "content":"You will exec some scripts. Either by shell or run python script"}]
        return agent.send_prompt(query)


    def main():
        response = use_exec_agent(
            "read file 3 lines of file agent.py in the current folder")
        print(response)
        response = use_exec_agent(
            "pip list to show installed python environment")
        print(response)
        response = use_exec_agent(
            "show me the python path of this virtual environment")
        print(response)
    
    main()