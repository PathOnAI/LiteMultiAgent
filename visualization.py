import pandas as pd
from matplotlib import pyplot as plt
import json
import networkx as nx

# Load data
file_path_latest = 'log/multiagent_data_20241030.csv'
task_id = 3
meta_task_id = 'master_agent_task'
data_latest = pd.read_csv(file_path_latest)

# Filter data
task_data = data_latest[(data_latest['task_id'] == task_id) & 
                          (data_latest['meta_task_id'] == meta_task_id)]

# Initialize graph and add root nodes
G = nx.MultiDiGraph()
G.add_node('user_request')
G.add_node('main_agent')
G.add_edge('user_request', 'main_agent', key=0, label='step 0: user prompting main_agent')

# Helper to map agent to its parent node
parent_mapping = {'main_agent': 'user_request'}

# Build graph based on agent interactions
step = 1
for _, row in task_data.iterrows():
    agent = row['agent']
    depth = row['depth']
    response = json.loads(row['response'])
    tool_calls = response.get('tool_calls', None)
    if tool_calls:
        for tool_call in tool_calls:
            tool = tool_call['function']['name']
            is_agent = 'agent' in tool
            action = f'calling {"sub agent" if is_agent else "tool"}: {tool}'
            
            # Add formatted data
            if is_agent:
                parent_mapping[tool] = agent
            G.add_edge(agent, tool, key=step, label=f'step {step}: {action}')
            step += 1
    else:
        G.add_edge(agent, parent_mapping[agent], key=step, label=f'step {step}: sub agent {agent} going back to parent agent {parent_mapping[agent]}')
        step += 1

print(G.edges)

def plot_hierarchical_multi_edge_graph(G, output_file=f'log/agent_interaction_graph{task_id}.png'):
    plt.figure(figsize=(12, 8))
    pos = nx.nx_agraph.graphviz_layout(G, prog='dot')
    print(pos)
    # Draw nodes
    colors = ['lightgreen' if n == 'user_request'
                else 'lightyellow' if n == 'main_agent'
                else 'lightblue' for n in G.nodes()]
    nx.draw_networkx_nodes(G, pos, node_color=colors, node_size=3000)
    nx.draw_networkx_labels(G, pos, font_size=8, font_weight='bold')

    # Draw directed edges with labels
    edge_labels = {(u, v, k): d['label'] for u, v, k, d in G.edges(keys=True, data=True)}
    for (u, v, key), label in edge_labels.items():
        print(u, v, key)
        rad = 0.15 + 0.05 * key * (-1 if key % 2 == 0 else 1)
        nx.draw_networkx_edges(G, pos, edgelist=[(u, v)], connectionstyle=f'arc3,rad={rad}', 
                               edge_color='gray', arrows=True, arrowsize=15, arrowstyle='->', width=1)
        x, y = pos[u][0] * 0.6 + pos[v][0] * 0.4, pos[u][1] * 0.6 + pos[v][1] * 0.4
        num_edges = len([k for (a, b, k) in edge_labels.keys() if a == u and b == v])
        if num_edges > 1:
            offset = (key - (num_edges - 1) / 2) * 0.05
            x += offset * (pos[v][0] - pos[u][0])
            y += offset * (pos[v][1] - pos[u][1])

        plt.text(x, y, label, fontsize=6, ha='center', va='center', bbox=dict(facecolor='white', alpha=0.7))

    plt.axis('off')
    plt.tight_layout()
    plt.savefig(output_file, format='PNG', dpi=300, bbox_inches='tight')
    plt.close()

    print(f"Graph saved to {output_file}")

# Usage:
plot_hierarchical_multi_edge_graph(G)

## TODO: pass hierarchies
## TODO: arrow text

