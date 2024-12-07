import re

def extract_goals_and_achievements(text):
    """
    Extract goals and achievements from the ESG report text.
    """
    print("Starting goal and achievement extraction...")
    goals = []
    achievements = []

    # Improved pattern matching for goals
    goal_matches = re.findall(
        r"(goal[s]?|target[s]?|aim[s]?|commitment[s]?|objective[s]?):\s*(.+?)(\.|\n|$)", text, re.IGNORECASE
    )
    print(f"Found {len(goal_matches)} goal(s).")
    for match in goal_matches:
        print(f"Goal extracted: {match[1]}")
        goals.append(match[1].strip())

    # Improved pattern matching for achievements
    achievement_matches = re.findall(
        r"(achieved|completed|recognized|awarded|milestone[s]?):\s*(.+?)(\.|\n|$)", text, re.IGNORECASE
    )
    print(f"Found {len(achievement_matches)} achievement(s).")
    for match in achievement_matches:
        print(f"Achievement extracted: {match[1]}")
        achievements.append(match[1].strip())

    print("Goal and achievement extraction complete.")
    return {"goals": goals, "achievements": achievements}
