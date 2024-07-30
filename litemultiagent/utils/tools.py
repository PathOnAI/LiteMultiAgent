

class Tools:
    _exec: list[dict]
    _io: list[dict]
    _db: list[dict]
    _file: list[dict]

Tools._exec = [
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

Tools._io = [
    {
        "type": "function",
        "function": {
            "name": "write_to_file",
            "description": "Write string content to a file.",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "Full file name with path where the content will be written."
                    },
                    "text": {
                        "type": "string",
                        "description": "Text content to be written into the file."
                    },
                    "encoding": {
                        "type": "string",
                        "default": "utf-8",
                        "description": "Encoding to use for writing the file. Defaults to 'utf-8'."
                    }
                },
                "required": [
                    "file_path",
                    "text"
                ]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Read a file and return its contents as a string.",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "The full file name with path to read."
                    },
                    "encoding": {
                        "type": "string",
                        "default": "utf-8",
                        "description": "The encoding used to decode the file. Defaults to 'utf-8'."
                    }
                },
                "required": [
                    "file_path"
                ]
            }
        }
    },
    {
      "type": "function",
      "function": {
        "name": "generate_and_download_image",
        "description": "Generate an image using DALL-E 2 based on a prompt and download it.",
        "parameters": {
          "type": "object",
          "properties": {
            "prompt": {
              "type": "string",
              "description": "The text prompt to generate the image from."
            },
            "filename": {
              "type": "string",
              "description": "The filename (including path) to save the downloaded image."
            }
          },
          "required": [
            "prompt",
            "filename"
          ]
        }
      }
    }
]

Tools._db = [{
  "type": "function",
  "function": {
    "name": "retrieve_db",
    "description": "Retrieve data from a specified database (currently supports Supabase) based on input parameters.",
    "parameters": {
      "type": "object",
      "properties": {
        "client": {
          "type": "string",
          "description": "The database client to use. Currently supports 'SUPABASE'."
        },
        "db": {
          "type": "string",
          "description": "The name of the database table to query."
        },
        "input_column": {
          "type": "string",
          "description": "The column name to search in."
        },
        "output_column": {
          "type": "string",
          "description": "The column name to retrieve data from."
        },
        "input_value": {
          "type": "string",
          "description": "The value to search for in the input column."
        }
      },
      "required": [
        "client",
        "db",
        "input_column",
        "output_column",
        "input_value"
      ]
    }
  }
}]

Tools._file = [
    {
        "type": "function",
        "function": {
            "name": "retrieve_file",
            "description": "Processes a list of PDFs based on a query and saves the results in the specified directory.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The query string to use for processing."
                    },
                    "pdf_list": {
                        "type": "array",
                        "items": {
                            "type": "string"
                        },
                        "description": "List of paths to PDF files."
                    },
                },
                "required": [
                    "query",
                    "pdf_list"
                ]
            }
        }
    }
]