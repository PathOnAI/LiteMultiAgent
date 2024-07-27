# groq/llama3-8b-8192
# gpt-4o-mini
# claude-3-5-sonnet-20240620
# gemini/gemini-pro
agent_to_model = {
    "main_agent":
        {
            "model_name" : "gpt-4o-mini",
            "tool_choice" : "auto",
         },
    "io_agent": {
            "model_name" : "claude-3-5-sonnet-20240620",
            "tool_choice" : "auto",
         },
    "retrieval_agent": {
            "model_name" : "gpt-4o-mini",
            "tool_choice" : "auto",
         },
    "web_search_agent":{
            "model_name" : "gemini/gemini-pro",
            "tool_choice" : "auto",
         },
    "db_retrieval_agent":{
            "model_name" : "gpt-4o-mini",
            "tool_choice" : "auto",
         },
    "exec_agent":{
            "model_name" : "claude-3-5-sonnet-20240620",
            "tool_choice" : "auto",
         },
    "file_retrieve_agent":{
            "model_name" : "gpt-4o-mini",
            "tool_choice" : "auto",
         },
}


class Config:
    def __init__(self):
        self.use_parallel = True
        self.max_workers = None

# Create a global configuration object
function_calling_config = Config()