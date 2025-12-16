import requests
import json
import time

nodes = [
    "http://127.0.0.1:5001",
    "http://127.0.0.1:5002",
    "http://127.0.0.1:5003"
]

def check_health():
    print("Checking node health...")
    for node in nodes:
        try:
            r = requests.get(f"{node}/get_chain")
            if r.status_code == 200:
                print(f"Node {node} is UP. Chain length: {r.json()['length']}")
            else:
                print(f"Node {node} returned {r.status_code}")
        except Exception as e:
            print(f"Node {node} is DOWN: {e}")

def connect_nodes():
    print("\nConnecting nodes...")
    # Connect 5002 and 5003 to 5001
    payload = {"nodes": ["http://127.0.0.1:5002", "http://127.0.0.1:5003"]}
    try:
        r = requests.post(f"{nodes[0]}/connect_node", json=payload)
        print(f"Connect to 5001: {r.json()}")
    except Exception as e:
        print(f"Failed to connect to 5001: {e}")

    # Connect others similarly if needed, but usually connecting to one known node is enough if gossip is implemented, 
    # but here we might need full mesh manually if gossip isn't automatic. 
    # Let's just connect everyone to everyone for safety.
    for i, node in enumerate(nodes):
        others = [n for n in nodes if n != node]
        payload = {"nodes": others}
        try:
            r = requests.post(f"{node}/connect_node", json=payload)
            print(f"Connected peers to {node}: {r.status_code}")
        except Exception as e:
            print(f"Failed to connect peers to {node}: {e}")

def mine_block(node_index):
    node = nodes[node_index]
    print(f"\nMining block on {node}...")
    try:
        r = requests.get(f"{node}/mine_block")
        print(f"Mined: {r.json().get('message', r.text)}")
    except Exception as e:
        print(f"Mining failed on {node}: {e}")

def sync_chains():
    print("\nSyncing chains (consensus)...")
    for node in nodes:
        try:
            r = requests.get(f"{node}/replace_chain")
            print(f"Sync {node}: {r.json().get('message', r.text)}")
        except Exception as e:
            print(f"Sync failed on {node}: {e}")

def verify_consensus():
    print("\nVerifying consensus...")
    chains = []
    for node in nodes:
        try:
            r = requests.get(f"{node}/get_chain")
            chain = r.json()['chain']
            chains.append(chain)
            print(f"Node {node} chain length: {len(chain)}")
        except Exception as e:
            print(f"Failed to get chain from {node}: {e}")
            return

    # Check if all chains are identical
    if all(c == chains[0] for c in chains):
        print("SUCCESS: All chains are identical.")
    else:
        print("FAILURE: Chains diverge!")
        for i, c in enumerate(chains):
            print(f"Node {i} last block: {c[-1]['index']}")

if __name__ == "__main__":
    time.sleep(2) # Wait for nodes to be fully ready
    check_health()
    connect_nodes()
    
    mine_block(0) # Mine on 5001
    sync_chains() # 5002 and 5003 should pick up 5001's chain
    verify_consensus()
    
    mine_block(1) # Mine on 5002
    sync_chains() # 5001 (len 2) < 5002 (len 3), so 5001 should update. 5003 should update.
    verify_consensus()
