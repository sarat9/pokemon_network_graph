import pyvis
import networkx as nx
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from pyvis.network import Network
import requests


print("All libraries imported successfully!")

# Function to fetch Pokemon details
def fetch_api_call(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    if response.status_code != 200:
        print("Failed to fetch Pokemon list!")
        exit()
    return None

# Create a network graph
LIMIT = 50
# Fetch the list of all Pokemon
pokemon_list_url = "https://pokeapi.co/api/v2/pokemon?limit=" + str(LIMIT)  # Adjust the limit as needed
response = fetch_api_call(pokemon_list_url);
pokemon_list = response['results']
print(pokemon_list)

# Add Pokemon list to Pandas DataFrame
df = pd.DataFrame(pokemon_list)
# Add an additional column for the ID (derived from the URL)
df['id'] = df['url'].apply(lambda x: x.rstrip('/').split('/')[-1])
# Display the DataFrame
print(df)

# Create a Pyvis network graph
net = Network(height="1000px", width="100%", notebook=True, directed=True)

# Fetch data for each Pokemon and enhance the graph
for pokemon in pokemon_list:
    pokemon_name = pokemon['name']
    pokemon_url = pokemon['url']
    # Fetch details for each Pokemon
    pokemon_data = fetch_api_call(pokemon_url)

    if not pokemon_data:
        continue

    # Add the Pokemon as a node
    pokemon_types = [ptype['type']['name'] for ptype in pokemon_data['types']]
    tooltip = f"Name: {pokemon_name}\nTypes: {', '.join(pokemon_types)}"
    net.add_node(pokemon_name, label=pokemon_name, title=tooltip, color="green", shape="circle")
    print(f"Added Pokemon: {pokemon_name} (Types: {', '.join(pokemon_types)})")

    # Add Pokemon types as nodes and connect them
    for ptype in pokemon_types:
        net.add_node(ptype, label=ptype, color="orange", shape="box")
        net.add_edge(pokemon_name, ptype)
    
    # Add abilities as nodes and connect them to the Pokemon
    for ability in pokemon_data['abilities']:
        ability_name = ability['ability']['name']
        net.add_node(ability_name, label=ability_name, color="yellow", shape="ellipse")
        net.add_edge(pokemon_name, ability_name)
        print(f"  Connected Ability: {ability_name}")

    # Add base stats as nodes and connect them to the Pokemon
    for stat in pokemon_data['stats']:
        stat_name = stat['stat']['name']
        stat_value = stat['base_stat']
        stat_label = f"{stat_name}: {stat_value}"
        net.add_node(stat_label, label=stat_label, color="pink", shape="dot")
        net.add_edge(pokemon_name, stat_label)
        print(f"  Added Stat: {stat_name} ({stat_value})")

# Show the interactive graph
net.show("pokemon_network.html")
print("Enhanced graph created: pokemon_network.html")

