import os
import sys
import logging
import multiprocessing as mp
from typing import List, Tuple

from dgo.core.agent import Agent
from dgo.core.swarm import Swarm
from dgo.core.governance import GovernanceProtocol
from dgo.utils.config import load_config
from dgo.utils.network import discover_agents, connect_agents

def main():
    """Main entry point for the Decentralized Governance Orchestrator (DGO)."""
    # Load configuration
    config = load_config("config.yaml")

    # Initialize logging
    logging.basicConfig(level=config["logging_level"])

    # Discover and connect agents
    agents = discover_agents(config["agent_discovery_endpoints"])
    connect_agents(agents)

    # Create governance protocol
    protocol = GovernanceProtocol(
        agents=agents,
        consensus_mechanism=config["consensus_mechanism"],
        decision_making_process=config["decision_making_process"]
    )

    # Execute governance processes
    protocol.run()

if __name__ == "__main__":
    main()
