from litewebagent.agents.webagent import setup_function_calling_web_agent

from litemultiagent.tools.registry import Tool


def call_webagent(starting_url, goal):
    agent_type = "FunctionCallingAgent"
    plan = ''
    log_folder = "log"
    model = "gpt-4o-mini"
    features = "axtree"
    branching_factor = None
    storage_state = None

    agent = setup_function_calling_web_agent(starting_url, goal, model_name=model, agent_type=agent_type, features=features,
                                             tool_names=["navigation", "select_option", "upload_file"], branching_factor=branching_factor, log_folder=log_folder, storage_state=storage_state)
    response = agent.send_prompt(plan)
    print(response)
    print(agent.messages)
    playwright_manager = agent.playwright_manager
    playwright_manager.close()
    return response


call_webagent_tool = Tool(
    "call_webagent",
    call_webagent,
    "Call a web agent to perform a task starting from a given URL.",
    {
        "starting_url": {
            "type": "string",
            "description": "The URL where the web agent should start its task.",
            "required": True
        },
        "goal": {
            "type": "string",
            "description": "The goal or task that the web agent should accomplish.",
            "required": True
        }
    }
)
