# README
## (1) environment set up
For each framework, go to the corresponding folder of each environment, and install the Python environment by running the following commands:
```bash
$ python3 -m venv venv
$ . venv/bin/activate
$ pip install -r requirements.txt
```
Create a .env file, and update your API keys:

```bash
cp env.example .env
```

## (2) testing
run 
```bash
python test_supabase_table.py
```
to test whether connected to supabase

run
```bash
python web_search_agent.py
```
to test subagent implementation