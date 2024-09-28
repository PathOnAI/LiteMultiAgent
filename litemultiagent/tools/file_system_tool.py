import os
from litemultiagent.tools.registry import ToolRegistry, Tool

def scan_folder(folder_path, depth=2):
    ignore_patterns = [".*", "__pycache__"]
    file_paths = []
    for subdir, dirs, files in os.walk(folder_path):
        dirs[:] = [
            d for d in dirs
            if not any(
                d.startswith(pattern) or d == pattern for pattern in ignore_patterns
            )
        ]
        if subdir.count(os.sep) - folder_path.count(os.sep) >= depth:
            del dirs[:]
            continue
        for file in files:
            file_paths.append(os.path.join(subdir, file))
    return file_paths


def register_file_system_tools():
    ToolRegistry.register(Tool(
        "scan_folder",
        scan_folder,
        "Scan a directory recursively for files with path with depth 2. You can also use this function to understand the folder structure in a given folder path.",
        {
            "folder_path": {
                "type": "string",
                "description": "The folder path to scan.",
                "required": True
            }
        }
    ))