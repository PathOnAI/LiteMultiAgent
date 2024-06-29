from dotenv import load_dotenv
import os
from langchain_core.messages import (
    BaseMessage,
    HumanMessage,
    ToolMessage,
)
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langgraph.graph import END, StateGraph
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.tools import tool
from langchain_experimental.utilities import PythonREPL
import operator
from typing import Annotated, Sequence, TypedDict
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import ToolNode
from typing import Literal
import sys
import io

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")


def create_agent(llm, tools, system_message: str):
    """Create an agent."""
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are a helpful AI assistant, collaborating with other assistants."
                " Use the provided tools to progress towards answering the question."
                " If you are unable to fully answer, that's OK, another assistant with different tools "
                " will help where you left off. Execute what you can to make progress."
                " If you or any of the other assistants have the final answer or deliverable,"
                " prefix your response with FINAL ANSWER so the team knows to stop."
                " You have access to the following tools: {tool_names}.\n{system_message}",
            ),
            MessagesPlaceholder(variable_name="messages"),
        ]
    )
    prompt = prompt.partial(system_message=system_message)
    prompt = prompt.partial(tool_names=", ".join([tool.name for tool in tools]))
    return prompt | llm.bind_tools(tools)




tavily_tool = TavilySearchResults(max_results=5)

# Warning: This executes code locally, which can be unsafe when not sandboxed

repl = PythonREPL()


import sys
import subprocess
import tempfile
import os
@tool()
def python_repl(code: Annotated[str, "The python code to execute to generate your chart."],):
    """Execute Python code in a subprocess, save any generated plots, and return the output."""
    # Create a temporary file to store the code
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as temp_file:
        # Modify the code to save the plot instead of showing it
        # modified_code = code.replace("plt.show()", "plt.savefig('plot.png')")

        # Add import statements at the beginning of the code
        full_code = "import matplotlib\nmatplotlib.use('Agg')\n" + code

        # Write the modified code to the temporary file
        temp_file.write(full_code)
        temp_file_path = temp_file.name

    try:
        # Run the Python script as a subprocess
        result = subprocess.run(
            [sys.executable, temp_file_path],
            capture_output=True,
            text=True,
            check=True
        )
        output = result.stdout

    except subprocess.CalledProcessError as e:
        output = f"Error: {e.stderr}"
    finally:
        # Clean up the temporary file
        os.unlink(temp_file_path)

    result_str = f"Executed:\n```python\n{code}\n```\nOutput:\n{output}"
    return result_str + "\n\nIf you have completed all tasks, respond with FINAL ANSWER."


# This defines the object that is passed between each node
# in the graph. We will create different nodes for each agent and tool
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]
    sender: str

import functools

from langchain_core.messages import AIMessage


# Helper function to create a node for a given agent
def agent_node(state, agent, name):
    result = agent.invoke(state)
    # We convert the agent output into a format that is suitable to append to the global state
    if isinstance(result, ToolMessage):
        pass
    else:
        result = AIMessage(**result.dict(exclude={"type", "name"}), name=name)
    return {
        "messages": [result],
        # Since we have a strict workflow, we can
        # track the sender so we know who to pass to next.
        "sender": name,
    }


llm = ChatOpenAI(model="gpt-4-1106-preview")

# Research agent and node
research_agent = create_agent(
    llm,
    [tavily_tool],
    system_message="You should provide accurate data for the chart_generator to use.",
)
research_node = functools.partial(agent_node, agent=research_agent, name="Researcher")

# chart_generator
chart_agent = create_agent(
    llm,
    [python_repl],
    system_message="Create charts and save to the chart locally.",
)
chart_node = functools.partial(agent_node, agent=chart_agent, name="chart_generator")


tools = [tavily_tool, python_repl]
tool_node = ToolNode(tools)




def router(state) -> Literal["call_tool", "__end__", "continue"]:
    # This is the router
    messages = state["messages"]
    last_message = messages[-1]
    if last_message.tool_calls:
        # The previous agent is invoking a tool
        return "call_tool"
    if "FINAL ANSWER" in last_message.content:
        # Any agent decided the work is done
        return "__end__"
    return "continue"

workflow = StateGraph(AgentState)

workflow.add_node("Researcher", research_node)
workflow.add_node("chart_generator", chart_node)
workflow.add_node("call_tool", tool_node)

workflow.add_conditional_edges(
    "Researcher",
    router,
    {"continue": "chart_generator", "call_tool": "call_tool", "__end__": END},
)
workflow.add_conditional_edges(
    "chart_generator",
    router,
    {"continue": "Researcher", "call_tool": "call_tool", "__end__": END},
)

workflow.add_conditional_edges(
    "call_tool",
    # Each agent node updates the 'sender' field
    # the tool calling node does not, meaning
    # this edge will route back to the original agent
    # who invoked the tool
    lambda x: x["sender"],
    {
        "Researcher": "Researcher",
        "chart_generator": "chart_generator",
    },
)
workflow.set_entry_point("Researcher")
graph = workflow.compile()


try:
    img_data = graph.get_graph(xray=True).draw_mermaid_png()
    with open("output_image.png", "wb") as file:
        file.write(img_data)
except Exception:
    # This requires some extra dependencies and is optional
    pass






events = graph.stream(
    {
        "messages": [
            HumanMessage(
                content="Fetch the UK's GDP over the past 5 years,"
                " then draw a line graph of it."
                " Once you code it up, finish."
            )
        ],
    },
    # Maximum number of steps to take in the graph
    {"recursion_limit": 150},
)
for s in events:
    print(s)
    print("----")


# just use one agent, to get the response, how?
# can I have self defined agent with langgraph?