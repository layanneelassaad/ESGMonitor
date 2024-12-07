from collections import defaultdict

def summarize_by_branches(text):
    """
    Summarize ESG content by geographic branches.
    """
    entities = defaultdict(list)
    sentences = text.split(".")  # Simplified for demo purposes

    for sentence in sentences:
        if "location" in sentence:  # Placeholder for NER-based logic
            entities["Global"].append(sentence)

    return {branch: " ".join(content) for branch, content in entities.items()}

def generate_esg_recommendations(branch_summaries, ghg_summary=None):
    """
    Generate ESG recommendations based on branch summaries and GHG efforts.
    """
    recommendations = []

    if ghg_summary:
        recommendations.append(f"Focus on reducing emissions: {ghg_summary[:150]}...")

    for branch, summary in branch_summaries.items():
        recommendations.append(f"In {branch}: Enhance ESG practices related to {summary[:100]}.")

    return recommendations or ["No specific recommendations available."]
