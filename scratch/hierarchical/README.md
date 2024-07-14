# README
## 07/13
* create a separate web search agent and wrap it in a function
  * just create a tool and pass to the llm [done]
    * master agent use downstream agent as tool, and just function calling to decide when to call downstream agent
  * create a workflow agent [done]

```
Traceback (most recent call last):
  File "/Users/danqingzhang/Desktop/MultiAgent/scratch/hierarchical/research_agent.py", line 125, in <module>
    prompt = hub.pull("rlm/rag-prompt")
             ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/danqingzhang/Desktop/AI_MLE/code/rag-starter-code/venv/lib/python3.11/site-packages/langchain/hub.py", line 82, in pull
    client = _get_client(api_url=api_url, api_key=api_key)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/danqingzhang/Desktop/AI_MLE/code/rag-starter-code/venv/lib/python3.11/site-packages/langchain/hub.py", line 20, in _get_client
    raise ImportError(
ImportError: Could not import langchainhub, please install with `pip install langchainhub`.
```
* TODO
  * refactor the agent creation code
* what's needed as sub-agent to the main agent?
  * retrieval
  * output file
    * write file
    * write to image
    * xxx
* other agent on the same level as main agent
  * planner agent
  * evaluation agent