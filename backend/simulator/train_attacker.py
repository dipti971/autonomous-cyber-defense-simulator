import os
from stable_baselines3 import PPO
from backend.simulator.cyber_env import CyberDefenseEnv

def train_attacker_agent():
    print("\n" + "="*50)
    print("🤖 INITIALIZING ATTACKER REINFORCEMENT LEARNING TRAINING")
    print("="*50 + "\n")
    
    # 1. Instantiate our software-defined cyber range environment
    env = CyberDefenseEnv()
    
    # 2. Configure the PPO Agent (The Brain)
    # MLPPolicy creates a standard Multi-Layer Perceptron Deep Neural Network
    model = PPO(
        "MlpPolicy", 
        env, 
        verbose=1, 
        learning_rate=0.0003,
        tensorboard_log="./tensorboard_logs/"
    )
    
    # 3. Train the AI over 10,000 simulated attack cycles
    print("🏋️‍♂️ Training agent... Please wait while the AI explores paths...")
    model.learn(total_timesteps=10000)
    
    # 4. Save the trained brain so we can load it later into our dashboard server
    model_path = os.path.join("backend", "simulator", "trained_attacker_ppo")
    model.save(model_path)
    
    print("\n" + "="*50)
    print(f"🏆 TRAINING COMPLETE! AI Agent Saved to: {model_path}.zip")
    print("="*50 + "\n")

if __name__ == "__main__":
    train_attacker_agent()
