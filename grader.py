def grade(action, correct):
    score = 0.0

    if action.category == correct["category"]:
        score += 0.4
    if action.urgency == correct["urgency"]:
        score += 0.3
    if action.action == correct["action"]:
        score += 0.3

    return round(score, 2)