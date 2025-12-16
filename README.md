# BCoin

BCoin is a lightweight, Python-based cryptocurrency implementation designed to demonstrate the fundamental mechanics of blockchain technology. It mimics the core architecture of Bitcoin, including Proof-of-Work mining, decentralized nodes, and consensus algorithms.

## Core Concepts

*   **Blockchain**: A distributed, immutable ledger where transactions are recorded in blocks. Each block is cryptographically linked to the previous one via a SHA-256 hash.
*   **Proof of Work (Mining)**: To add a block, nodes must solve a computational puzzle. This prevents spam and secures the network. The miner who solves it first is rewarded with coin.
*   **Decentralization**: The network consists of multiple nodes (computers) that talk to each other. No single node remains in charge.
*   **Consensus (Longest Chain Rule)**: If nodes disagree on the history (e.g., two blocks mined at once), the network automatically adopts the longest valid chain as the truth, ensuring everyone stays in sync.

## Installation

1.  **Clone the repository**:
    ```bash
    git clone <repository-url>
    cd BCoin
    ```

2.  **Install dependencies**:
    BCoin requires Flask (for the API) and Requests (for node communication).
    ```bash
    pip install Flask requests
    ```

## How to Run the Network

To simulate a decentralized network, we will run **3 separate nodes** on your local machine using different ports (5001, 5002, 5003).

1.  **Start the Nodes**:
    Open 3 separate terminal windows/tabs and run the following in each:

    *   **Terminal 1 (Node 1)**:
        ```bash
        cd module_2_cryptocurrency
        python bcoin_node_5001.py
        ```

    *   **Terminal 2 (Node 2)**:
        ```bash
        cd module_2_cryptocurrency
        python bcoin_node_5002.py
        ```

    *   **Terminal 3 (Node 3)**:
        ```bash
        cd module_2_cryptocurrency
        python bcoin_node_5003.py
        ```

## Interacting with the Blockchain

You can communicate with the nodes using `curl` or an API client like Postman.

### 1. Connect the Nodes
Tell Node 1 about the other nodes so they can gossip and sync data.
```bash
curl -X POST -H "Content-Type: application/json" -d '{"nodes": ["http://127.0.0.1:5002", "http://127.0.0.1:5003"]}' http://127.0.0.1:5001/connect_node
```

### 2. Mine a Block
Trigger the mining process on Node 1. This creates a new block and rewards the miner.
```bash
curl http://127.0.0.1:5001/mine_block
```

### 3. View the Chain
See the current state of the blockchain on any node.
```bash
curl http://127.0.0.1:5001/get_chain
```

### 4. Sync the Network (Consensus)
If you mine on one node, the others need to catch up. Run this on Node 2 or 3 to pull the latest chain from Node 1.
```bash
curl http://127.0.0.1:5002/replace_chain
```
