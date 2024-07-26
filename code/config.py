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
            "model_name" : "gpt-4o-mini",
            "tool_choice" : "auto",
         },
    "db_retrieval_agent":{
            "model_name" : "claude-3-5-sonnet-20240620",
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