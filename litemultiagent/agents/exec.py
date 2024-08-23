from litemultiagent.agents.base import Agent

import subprocess
from typing import Optional

from litemultiagent.utils.tools import Tools

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



available_tools = {
    "run_python_script": run_python_script,
    "execute_shell_command": execute_shell_command,
}

class Exec_Agent(Agent):
    def __init__(self, meta_task_id: Optional[str] = None, task_id: Optional[int] = None):
        super().__init__("exec_agent", Tools._exec, available_tools, meta_task_id, task_id)




