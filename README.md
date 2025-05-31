# LiteMultiAgent
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.15500241.svg)](https://doi.org/10.5281/zenodo.15500241)

Please note that the LiteMultiAgent repository is in development mode. We have open-sourced the repository to foster collaboration between contributors.

repo owner: Danni (Danqing) Zhang (danqing.zhang.personal@gmail.com)

In our exploration of building multi-agent systems, we have investigated AutoGen, CrewAI, LangGraph, and MetaGPT, but failed to find a multi-agent system that intuitively makes multi-agent systems more efficient. We have found that most examples provided by these frameworks could be accomplished with just one agent. We reimplemented the multi-agent examples using only one agent with a set of self-defined tools. However, we then realized that this system is not scalable when we have more and more tools. But if we can categorize the agents with different sets of tools into categories, then we are building a hierarchy of agents, where we could accomplish more types of tasks. At the same time, because of this design, the execution of sub-agents is naturally parallelized by parallel function calling, since agents use sub-agents as tools.


## 📰 News
* [2024-10-29] Generate and register tools for function calling at runtime: [example](https://github.com/PathOnAI/LiteMultiAgent/blob/main/examples/new_tool/add_llm_generated_function_example.py) 
* [2024-10-02] Major framework refactoring introduces new agent classes: Function Calling, React, and High-Level Planning. It also defines Atomic agents using functions as tools and Composite agents employing both functions and sub-agents as tools, enhancing overall system flexibility.
* [2024-10-01] Integrate [LiteWebAgent](https://github.com/PathOnAI/LiteWebAgent) into LiteMultiAgent repo to enable hierarchical multi-agent framework with web browsing capacities.
* [2024-09-28] LiteMultiAgent was refactored into a flexible hierarchical multi-agent framework, adding ToolRegistry, AgentFactory, and AgentManager, allowing users to register their own base tools and create custom agent hierarchies.
* [2024-08-06] the initial version of LiteMultiAgent was released, showcasing a hierarchical multi-agent system capable of accomplishing a wide range of tasks.

## ✈️ 1. Getting Started

### (1) Installation
From PyPI: https://pypi.org/project/litemultiagent/
```
pip install litemultiagent 
```

Set up locally
First set up virtual environment, and allow your code to be able to see 'litemultiagent'
```bash
python3 -m venv venv
. venv/bin/activate
pip install -e .
```
Then please create a .env file, and update your API keys:

```bash
cp .env.example .env
```

#### (Optional) Supabase Database Set Up
If you want to save log to Supabase. Set up a Supabase project and retrieve the database URL from: https://supabase.com/dashboard/project/[PROJECT_NAME]/settings/database.

The DATABASE_URL follows: postgresql://<username>:<password>@<host>:<port>/<database>. You can get this from Project Settings -> Database -> Connection string.

Save this URL in the .env file as SUPABASE_DATABASE_URL. Then, run:

```bash
python supabase_db_setup.py
```
This will create the multiagent table in your database



### (2) Quickstart
After setting up your API keys, you can explore the examples in the examples folder:
* The atomic agent uses functions as its tools.
* The composite agent can utilize sub-agents as tools while also leveraging functions.

```bash
python examples/atomic/IOAgent.py   
```
```bash
python examples/composite/MasterAgent.py
```

### (3) Generate and register tools at runtime
```bash
python examples/new_tool/add_llm_generated_function_example.py
```

## 🚀 2. Contributions
For how to contribute, see [CONTRIBUTE](https://github.com/PathOnAI/LiteMultiAgent/blob/main/CONTRIBUTE.md). If you would like to contribute to the codebase, [issues](https://github.com/PathOnAI/LiteMultiAgent/issues) or [pull requests](https://github.com/PathOnAI/LiteMultiAgent/pulls) are always welcome!

[![LiteMultiAgent contributors](https://contrib.rocks/image?repo=PathOnAI/LiteMultiAgent)](https://github.com/PathOnAI/LiteMultiAgent/graphs/contributors)


## 📄 3. Citing LiteMultiAgent
```
@misc{zhang2024litemultiagent,
  title={LiteMultiAgent: The Library for LLM-based multi-agent applications},
  author={Zhang, Danqing and Rama, Balaji and He, Shiying and Ni, Jingyi},
  year         = 2024,
  publisher    = {Zenodo},
  doi          = {10.5281/zenodo.15500241},
  url          = {https://doi.org/10.5281/zenodo.15500241}
}
```

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=PathOnAIOrg/LiteMultiAgent&type=Date)](https://star-history.com/#PathOnAIOrg/LiteMultiAgent&Date)
