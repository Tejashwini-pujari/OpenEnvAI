from models import Observation, Action, Reward

class SupportEnv:
    def __init__(self):
        self.tickets = [
            {
                "text": "Payment deducted but order not placed",
                "category": "billing",
                "urgency": "high",
                "action": "escalate"
            },
            {
                "text": "App crashes when I open settings",
                "category": "technical",
                "urgency": "high",
                "action": "resolve"
            },
            {
                "text": "I was charged twice for my subscription",
                "category": "billing",
                "urgency": "high",
                "action": "escalate"
            },
            {
                "text": "Unable to login after password reset",
                "category": "technical",
                "urgency": "medium",
                "action": "resolve"
            },
            {
                "text": "How to change profile name?",
                "category": "general",
                "urgency": "low",
                "action": "ask_info"
            }
        ]
        self.index = 0

    def reset(self):
        self.index = 0
        return Observation(ticket=self.tickets[self.index]["text"])

    def step(self, action: Action):
        correct = self.tickets[self.index]
        score = 0.0

        if action.category == correct["category"]:
            score += 0.4
        if action.urgency == correct["urgency"]:
            score += 0.3
        if action.action == correct["action"]:
            score += 0.3

        if action.action == "ask_info" and correct["urgency"] == "high":
            score -= 0.2

        if len(action.response) < 10:
            score -= 0.1

        if action.action == "resolve" and correct["urgency"] == "high":
            score -= 0.2

        score = max(0.0, min(score, 1.0))

        self.index += 1
        done = self.index >= len(self.tickets)

        next_obs = None
        if not done:
            next_obs = Observation(ticket=self.tickets[self.index]["text"])

        return next_obs, Reward(score=round(score, 2)), done, {}

    def state(self):
        return {"current_index": self.index}