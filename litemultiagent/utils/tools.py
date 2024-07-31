

class Tools:
    _exec: list[dict]
    _io: list[dict]
    _db: list[dict]
    _file: list[dict]
    _retrieve: list[dict]
    _web: list[dict]

    _demo: list[dict]

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

Tools._retrieve = [
    {
        "type": "function",
        "function": {
            "name": "use_web_retrieval_agent",
            "description": "Perform a search using API and return the searched results.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The task description describing what to read or write."
                    }
                },
                "required": [
                    "query"
                ]
            }
        }
    },
    {
      "type": "function",
      "function": {
        "name": "use_db_retrieval_agent",
        "description": "Use a database retrieval agent to fetch information based on a given query.",
        "parameters": {
          "type": "object",
          "properties": {
            "query": {
              "type": "string",
              "description": "The query to be processed by the database retrieval agent."
            }
          },
          "required": [
            "query"
          ]
        }
      }
    },
    {
      "type": "function",
      "function": {
        "name": "use_file_retrieve_agent",
        "description": "Retrieve information from local documents to answer questions or perform tasks.",
        "parameters": {
          "type": "object",
          "properties": {
            "query": {
              "type": "string",
              "description": "The task description specifying the local file and the question to be answered. specify this in natural language"
            }
          },
          "required": [
            "query"
          ]
        }
      }
    }
]

Tools._web = [    
    {
        "type": "function",
        "function": {
            "name": "bing_search",
            "description": "Bing search for relevant information given a query.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Bing search query."
                    }
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "scrape",
            "description": "Scraping website content based on url from Bing search.",
            "parameters": {
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "Website url to scrape."
                    }
                },
                "required": ["url"]
            }
        }
    },
]

Tools._demo = tools = [
    {
        "type": "function",
        "function": {
            "name": "use_io_agent",
            "description": "Read or write content from/to a file, or generate and save an image using text input",
            "parameters": {
                "type": "object",
                "properties": {
                    "description": {
                        "type": "string",
                        "description": "The task description detailing what to read, write, or generate. This can include file operations or image generation requests."
                    }
                },
                "required": [
                    "description"
                ]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "use_exec_agent",
            "description": "Execute some script in a subprocess, either run a bash script, or run a python script ",
            "parameters": {
                "type": "object",
                "properties": {
                    "description": {
                        "type": "string",
                        "description": "The task description describing what to execute in the subprocess.",
                    }
                },
                "required": [
                    "query"
                ]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "scan_folder",
            "description": "Scan a directory recursively for files with path with depth 2. You can also use this function to understand the folder structure in a given folder path.",
            "parameters": {
                "type": "object",
                "properties": {
                    "folder_path": {
                        "type": "string",
                        "description": "The folder path to scan."
                    }
                },
                "required": [
                    "folder_path"
                ]
            },
            "return_type": "list: A list of file paths str with the given extension, or all files if no extension is specified."
        }
    },
    {
        "type": "function",
        "function": {
            "name": "use_retrieval_agent",
            "description": "Use a smart research assistant to look up information using multiple sources including web search, database retrieval, and local file retrieval.",
            "parameters": {
                "type": "object",
                "properties": {
                    "description": {
                        "type": "string",
                        "description": "The task description specifying the information source (web search, database, local file) and the question to be answered. specify this in natural language"
                    }
                },
                "required": [
                    "query"
                ]
            }
        }
    },
]
