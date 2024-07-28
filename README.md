# LiteMultiAgent
repo owner: Danni (Danqing) Zhang (danqing.zhang.personal@gmail.com)
main contributors: Balaji Rama (balajirw10@gmail.com) and Shiying He (sy.he0303@gmail.com)

<a href='https://discord.gg/YX5tJ2zH'><img src='https://img.shields.io/badge/Community-Discord-8A2BE2'></a>
<a href='https://danqingz.github.io/blog/2024/07/27/LiteMultiAgent.html'><img src='https://img.shields.io/badge/Blog-181717?style=for-the-badge&logo=github&logoColor=white'></a>


## ✈️ 1. Getting Started

### (1) Installation
First set up virtual environment
```bash
$ python3 -m venv venv
$ . venv/bin/activate
$ pip install -r requirements.txt
```
Then set up a Supabase project to retrieve the API keys, and create a table if you want to save the results to a Supabase table. Please add the below columns to your Supabase table, and disable RLS.

| Column Name     | Data Type     |
|-----------------|---------------|
| agent           | text          |
| depth           | int8          |
| response        | text          |
| role            | text          |
| prompt_tokens   | int8          |
| completion_tokens | int8        |
| input_cost      | float8        |
| output_cost     | float8        |
| total_cost      | float8        |
| model_name      | text          |
| meta_task_id    | text          |
| task_id         | int8          |

Then please create a .env file, and update your API keys:

```bash
cp env.example .env
```

### (2) Quickstart
After configuring your API keys, you can run main.py, where the sub-agents are already parallelized through parallel function calling.
```bash
python main.py
```
Then we can get the total execution time for all tasks: 67.07 seconds.

You can parallelize the execution of the tasks of main agents:

```bash
python main.py --main-workers-parallel
```
Then it's further sped up. Total execution time for all tasks: 29.34 seconds.

## 🏠 2. Architecture Design

![design.png](images/design.png)

## 🚀 3. Contributions
For how to contribute, see [CONTRIBUTE](https://github.com/PathOnAI/LiteMultiAgent/blob/main/CONTRIBUTE.md). If you would like to contribute to the codebase, [issues](https://github.com/PathOnAI/LiteMultiAgent/issues) or [pull requests](https://github.com/PathOnAI/LiteMultiAgent/pulls) are always welcome!

