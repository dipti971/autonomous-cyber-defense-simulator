import asyncio
import json
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from backend.simulator.cyber_env import CyberDefenseEnv

app = FastAPI(title="Autonomous Cyber Defense Simulator API")

# Allow your future React frontend dashboard to talk to this backend server smoothly
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"status": "online", "message": "Cyber Defense Engine Live Server Ready"}

@app.websocket("/ws/simulation")
async def websocket_endpoint(websocket: WebSocket):
    """
    WebSocket endpoint that boots a live simulation session and streams 
    step-by-step state changes instantly to the frontend browser.
    """
    await websocket.accept()
    print("🔌 Dashboard Client connected to live simulation stream!")
    
    # Initialize a fresh cyber simulation playground instance
    env = CyberDefenseEnv()
    state, _ = env.reset()
    
    try:
        # Send the initial baseline network state layout immediately on connection
        initial_payload = {
            "event": "system_init",
            "nodes": env.nodes_list,
            "current_state": state.tolist(),
            "attacker_position": env.attacker_position
        }
        await websocket.send_text(json.dumps(initial_payload))
        await asyncio.sleep(1.5)
        
        # Run an active simulation battle loop automatically for the visual stream
        for step_idx in range(20):
            # The simulator picks a random network action step to demonstrate live tracking
            action = env.action_space.sample() 
            target_node = env.nodes_list[action]
            
            # Execute step inside our environment matrix
            next_state, reward, terminated, truncated, _ = env.step(action)
            
            # Construct a data snapshot frame payload
            frame_payload = {
                "event": "simulation_step",
                "step": step_idx + 1,
                "target_node": target_node,
                "current_state": next_state.tolist(),
                "attacker_position": env.attacker_position,
                "reward_earned": int(reward),
                "is_game_over": bool(terminated)
            }
            
            # Broadcast the live snapshot instantly over WebSockets to the web dashboard
            await websocket.send_text(json.dumps(frame_payload))
            print(f"📡 Broadcasted Frame {step_idx + 1}: Attacker targeted {target_node}")
            
            if terminated:
                break
                
            # Wait 2 seconds between cycles so humans can watch the dashboard change color live
            await asyncio.sleep(2.0)
            
        await websocket.send_text(json.dumps({"event": "simulation_complete", "message": "Simulation Run Concluded."}))
        
    except WebSocketDisconnect:
        print("🔌 Dashboard Client disconnected from simulation stream.")
    finally:
        await websocket.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main.app", host="0.0.0.0", port=8000, reload=True)
