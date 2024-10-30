import pandas as pd
from matplotlib import pyplot as plt
from anytree import Node, RenderTree
from anytree.exporter import DotExporter
import json

# Load the data
file_path_latest = 'log/multiagent_data_20241030.csv'
task_id = 1
meta_task_id = 'master_agent_task'
data_latest = pd.read_csv(file_path_latest)

# Filter data for task_id = 1 and a specific meta_task_id
task_1_data = data_latest[(data_latest['task_id'] == task_id) &
                          (data_latest['meta_task_id'] == meta_task_id)]


# Clear previous nodes and dictionary
nodes_dict = {}

# Create the root node (Main Agent at the top level)
root_node = Node(f"Main Agent")
nodes_dict['main_agent'] = root_node

## change agent name

# Iterate through task_1_data to build the hierarchy based on agent interactions
last_agent_node = root_node

import pandas as pd
import json
import networkx as nx
import matplotlib.pyplot as plt
import json

# Create a directed graph
G = nx.MultiDiGraph()
# Assuming 'task_1_data' is your DataFrame
formatted_data = []
# root_node = Node("main_agent")
mapping = {}
G.add_node('user_request')
G.add_node('main_agent')
count = 0
# Add initial edge between 'user_request' and 'main_agent'
G.add_edge('user_request', 'main_agent', key=count, label=f'step {count}: user prompting main_agent')
mapping['main_agent'] = 'user_request'
count += 1

for _, row in task_1_data.iterrows():
    print(count)
    agent = row['agent']
    depth = row['depth']
    response = json.loads(row['response'])
    tool_calls = response['tool_calls']

    if agent not in G:
        print("error")

    if tool_calls:
        for tool_call in tool_calls:
            tool = tool_call['function']['name']
            if 'agent' in tool:
                formatted_data.append({
                    'agent': agent,
                    'depth': depth,
                    'action': f'calling sub agent: {tool}'
                })
                G.add_edge(agent, tool, key=count, label=f'step {count}: agent {agent} calling sub agent {tool}')
                mapping[tool] = agent
                count += 1
            else:
                formatted_data.append({
                    'agent': agent,
                    'depth': depth,
                    'action': f'calling tool: {tool}'
                })
                G.add_edge(agent, tool, key=count, label=f'step {count}: agent {agent} calling tool {tool}')
                count += 1
    else:
        formatted_data.append({
            'agent': agent,
            'depth': depth,
            'action': 'go back to parent node'
        })
        G.add_edge(agent, mapping[agent], key=count, label=f'step {count}: sub agent {agent} going back to parent agent {mapping[agent]}')
        count += 1

# import pygraphviz as pgv
# from networkx.drawing.nx_agraph import to_agraph

print(G.edges)
import networkx as nx
import matplotlib.pyplot as plt

layout_configs = {
    1: {
        0: [('user_request', 0.5)],
        1: [('main_agent', 0.5)],
        2: [('io_agent', 0.5)],
        3: [('generate_and_download_image', 0.5)],
    },
    2: {
        0: [('user_request', 0.5)],
        1: [('main_agent', 0.5)],
        2: [('exec_agent', 0.5)],
        3: [('run_python_script', 0.3), ('execute_shell_command', 0.7)],
    },
    3: {
        0: [('user_request', 0.5)],
        1: [('main_agent', 0.5)],
        2: [('retrieval_agent', 0.4), ('io_agent', 0.6)],
        3: [('web_retrieval_agent', 0.4), ('write_to_file', 0.6)],
        4: [('bing_search', 0.3), ('scrape', 0.5)]
    },
}


def plot_hierarchical_multi_edge_graph(G, output_file=f'log/agent_interaction_graph{task_id}.png'):
    plt.figure(figsize=(12, 8))

    # Define levels with adjusted positions for a more compact layout
    # Define levels with adjusted positions for a more compact layout
    # levels = {
    #     0: [('user_request', 0.5)],
    #     1: [('main_agent', 0.5)],
    #     2: [('use_io_agent', 0.2), ('use_exec_agent', 0.4), ('use_retrieval_agent', 0.6), ('use_structure_agent', 0.8)],
    #     3: [('write_to_file', 0.1), ('read_file', 0.3), ('run_python_script_exec', 0.4),
    #         ('run_shell_script_exec', 0.5),
    #         ('use_web_retrieval_agent', 0.6), ('use_db_retrieval_agent', 0.7), ('use_file_structure_agent', 0.8),
    #         ('use_code_structure_agent', 0.9)],
    #     4: [('bing_search', 0.55), ('scrape', 0.65)]
    # }
    # Define levels with adjusted positions for a more compact layout
    # levels = {
    #     0: [('user_request', 0.5)],
    #     1: [('main_agent', 0.5)],
    #     2: [('exec_agent', 0.5)],
    #     3: [('run_python_script', 0.3), ('execute_shell_command', 0.7)],
    # }

    # Define levels with adjusted positions for a more compact layout
    # levels = {
    #     0: [('user_request', 0.5)],
    #     1: [('main_agent', 0.5)],
    #     2: [('io_agent', 0.5)],
    #     3: [('generate_and_download_image', 0.5)],
    # }

    levels = layout_configs[task_id]

    # Calculate positions
    pos = {}
    for level, nodes in levels.items():
        y = 1 - (level / 4)  # Adjust vertical spacing
        for node, x in nodes:
            pos[node] = (x, y)

    # Draw nodes
    for level, nodes in levels.items():
        nx.draw_networkx_nodes(G, pos, nodelist=[n for n, _ in nodes], node_size=2000,
                               node_color=['lightgreen' if n == 'user_request'
                                           else 'lightyellow' if n == 'main_agent'
                               else 'lightblue' for n, _ in nodes])
        nx.draw_networkx_labels(G, pos, {n: n for n, _ in nodes}, font_size=8, font_weight='bold')

    # Draw directed edges with reduced curvature and all labels
    edge_labels = {}
    for (u, v, key, data) in G.edges(keys=True, data=True):
        if u in pos and v in pos:
            rad = 0.15 + (0.05 * key)
            if key % 2 == 0:
                rad *= -1

            # Draw directed edge
            nx.draw_networkx_edges(G, pos, edgelist=[(u, v)], connectionstyle=f'arc3,rad={rad}',
                                   edge_color='gray', arrows=True, arrowsize=15,
                                   arrowstyle='->', width=1)

            label = data.get('label', '')
            edge_labels[(u, v, key)] = label

    # Draw edge labels with adjusted positions
    for (u, v, key), label in edge_labels.items():
        x = (pos[u][0] * 0.6 + pos[v][0] * 0.4)  # Adjust label position towards the source
        y = (pos[u][1] * 0.6 + pos[v][1] * 0.4)

        num_edges = len([k for (a, b, k) in edge_labels.keys() if a == u and b == v])
        if num_edges > 1:
            offset = (key - (num_edges - 1) / 2) * 0.05
            x += offset * (pos[v][0] - pos[u][0])
            y += offset * (pos[v][1] - pos[u][1])

        plt.text(x, y, label, fontsize=6, ha='center', va='center',
                 bbox=dict(facecolor='white', edgecolor='none', alpha=0.7))

    plt.axis('off')
    plt.tight_layout()
    plt.savefig(output_file, format='PNG', dpi=300, bbox_inches='tight')
    plt.close()

    print(f"Graph saved to {output_file}")

# Usage:
plot_hierarchical_multi_edge_graph(G)

## TODO: pass hierarchies
## TODO: arrow text

