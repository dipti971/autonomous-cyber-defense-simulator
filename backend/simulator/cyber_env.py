import gymnasium as gym
from gymnasium import spaces
import numpy as np
from .network_env import create_enterprise_network

class CyberDefenseEnv(gym.Env):
    """
    A custom Gymnasium environment that turns our NetworkX graph into an 
    interactive cyber range for Reinforcement Learning agents.
    """
    def __init__(self):
        super(CyberDefenseEnv, self).__init__()
        
        # 1. Initialize our network graph
        self.network = create_enterprise_network()
        self.nodes_list = list(self.network.nodes)
        
        # 2. Define Action Space: Attacker can target any node
        # (In Phase 2, this will represent specific exploits like scanning or breaching)
        self.action_space = spaces.Discrete(len(self.nodes_list))
        
        # 3. Define Observation Space: The current compromise status of all nodes
        # 0 = Secure, 1 = Breached
        self.observation_space = spaces.MultiBinary(len(self.nodes_list))
        
        # Start the attacker at the initial entry point
        self.attacker_position = "Employee_Laptop_B" 
        self.network.nodes[self.attacker_position]["compromised_status"] = 1

    def reset(self, seed=None, options=None):
        """Resets the network to its baseline security state for a new game."""
        super().reset(seed=seed)
        
        # Clear all compromises
        for node in self.network.nodes:
            self.network.nodes[node]["compromised_status"] = 0
            
        # Reposition attacker at the entry point laptop
        self.attacker_position = "Employee_Laptop_B"
        self.network.nodes[self.attacker_position]["compromised_status"] = 1
        
        # Return initial observation array [0, 1, 0, 0, 0, 0]
        obs = np.array([self.network.nodes[n]["compromised_status"] for n in self.nodes_list], dtype=np.int8)
        return obs, {}

    def step(self, action):
        """Executes one step of the cyber attack simulation."""
        target_node = self.nodes_list[action]
        reward = 0
        terminated = False
        
        print(f"💥 Attacker attempts to exploit: {target_node}")
        
        # Rule Validation: Can the attacker actually reach the target from where they are?
        if self.network.has_edge(self.attacker_position, target_node):
            # Roll a probability check against the node's vulnerability score
            vuln_score = self.network.nodes[target_node]["vulnerability_score"]
            success = np.random.rand() < vuln_score
            
            if success:
                self.network.nodes[target_node]["compromised_status"] = 1
                self.attacker_position = target_node
                print(f"🎯 SUCCESS: {target_node} has been BREACHED!")
                
                # Assign rewards based on asset criticality
                if self.network.nodes[target_node]["type"] == "database":
                    reward = 100  # Stole the crown jewels!
                    terminated = True
                else:
                    reward = 20   # Advancing through the network
            else:
                print(f"🛡️ FAIL: Attack on {target_node} was blocked by security controls.")
                reward = -5
        else:
            print(f"❌ INVALID MOVE: No direct network path from {self.attacker_position} to {target_node}.")
            reward = -10  # Penalize for breaking network rules
            
        # Generate the updated state observation
        obs = np.array([self.network.nodes[n]["compromised_status"] for n in self.nodes_list], dtype=np.int8)
        return obs, reward, terminated, False, {}

if __name__ == "__main__":
    # Quick simulation test run
    env = CyberDefenseEnv()
    state, _ = env.reset()
    print(f"Initial State Matrix: {state}")
    
    # Simulate a sample attack step targeting the Corporate Router (Node index 2)
    new_state, reward, done, _, _ = env.step(2)
    print(f"Updated State Matrix: {new_state} | Reward Earned: {reward}")
