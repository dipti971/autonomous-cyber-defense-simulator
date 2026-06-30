import networkx as nx

def create_enterprise_network():
    """
    Initializes a software-defined Directed Graph (DiGraph) replicating
    a realistic corporate infrastructure with contextual vulnerability matrices.
    """
    G = nx.DiGraph()
    
    # 1. Define Network Devices with custom cybersecurity state profiles
    nodes_config = {
        "Employee_Laptop_A": {"type": "endpoint", "os": "Windows 11", "patched": True,  "compromised_status": 0, "vulnerability_score": 0.3},
        "Employee_Laptop_B": {"type": "endpoint", "os": "Windows 10", "patched": False, "compromised_status": 0, "vulnerability_score": 0.7},
        "Corporate_Router":  {"type": "gateway",  "os": "Cisco IOS",  "patched": True,  "compromised_status": 0, "vulnerability_score": 0.1},
        "Main_Firewall":     {"type": "firewall", "os": "Linux-PF",   "patched": True,  "compromised_status": 0, "vulnerability_score": 0.1},
        "App_Server":        {"type": "server",   "os": "Ubuntu 22.04","patched": False, "compromised_status": 0, "vulnerability_score": 0.6},
        "Crown_Jewel_DB":    {"type": "database", "os": "RHEL 9",     "patched": True,  "compromised_status": 0, "vulnerability_score": 0.9}
    }
    
    for node, attributes in nodes_config.items():
        G.add_node(node, **attributes)
        
    # 2. Establish Strict Network Paths (Bridges the Attacker must follow)
    network_edges = [
        ("Employee_Laptop_A", "Corporate_Router"),
        ("Employee_Laptop_B", "Corporate_Router"),
        ("Corporate_Router", "Main_Firewall"),
        ("Main_Firewall", "App_Server"),
        ("App_Server", "Crown_Jewel_DB")
    ]
    G.add_edges_from(network_edges)
    
    print(f"🚀 Success: Virtual Enterprise Network Compiled!")
    print(f"Total Network Nodes: {G.number_of_nodes()} | Connected Traffic Edges: {G.number_of_edges()}\n")
    
    # Print out properties of our constructed assets
    for node in G.nodes(data=True):
        print(f"Asset: {node[0]} -> Type: {node[1]['type']} | Vuln Score: {node[1]['vulnerability_score']}")
        
    return G

if __name__ == "__main__":
    # Test local execution
    simulated_company = create_enterprise_network()
