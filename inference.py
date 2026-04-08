import requests
import os

BASE_URL = "http://localhost:7860"   # change for HF deployment

print("[START] task=customer-support env=support-env model=rule-based")

# RESET
res = requests.get(f"{BASE_URL}/reset")
ticket = res.json()["observation"]

rewards = []
done = False
step_num = 0

while not done:
    step_num += 1

    # Rule-based agent
    if "Payment" in ticket["ticket"]:
        action_data = {
            "category": "billing",
            "urgency": "high",
            "action": "escalate",
            "response": "Escalating billing issue"
        }

    elif "Password" in ticket["ticket"]:
        action_data = {
            "category": "technical",
            "urgency": "medium",
            "action": "resolve",
            "response": "Reset instructions sent"
        }

    else:
        action_data = {
            "category": "general",
            "urgency": "low",
            "action": "ask_info",
            "response": "Providing details"
        }

    res = requests.post(f"{BASE_URL}/step", json=action_data)
    data = res.json()

    reward = data["reward"]
    done = data["done"]

    rewards.append(reward)

    print(f"[STEP] step={step_num} action={action_data['category']},{action_data['urgency']},{action_data['action']} reward={reward:.2f} done={str(done).lower()} error=null")

score = sum(rewards) / len(rewards)

print(f"[END] success=true steps={step_num} score={score:.2f} rewards={','.join([str(r) for r in rewards])}")