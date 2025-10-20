from typing import Dict


# Transparent scoring: weighted combination of pillar evidences + sentiment
DEFAULT_WEIGHTS = {
"E": 0.4,
"S": 0.3,
"G": 0.3,
"sentiment": 0.1, # sentiment nudges total score
}




def _pillar_score(pillar_top: list[dict]) -> float:
# Map mean of top-3 scores to [0, 100]
    if not pillar_top:
        return 50.0
    mean = sum(x["score"] for x in pillar_top) / len(pillar_top)
    return round(mean * 100, 2)




def compute_scores(topic_view: Dict, sentiment_pos: float, weights: Dict | None = None):
    w = {**DEFAULT_WEIGHTS, **(weights or {})}
    e = _pillar_score(topic_view["pillars"].get("E", []))
    s = _pillar_score(topic_view["pillars"].get("S", []))
    g = _pillar_score(topic_view["pillars"].get("G", []))
    sentiment_component = round(sentiment_pos * 100, 2)


    total = round((w["E"] * e + w["S"] * s + w["G"] * g + w["sentiment"] * sentiment_component)
/ (w["E"] + w["S"] + w["G"] + w["sentiment"]), 2
)



    contributions = {"E": e * w["E"],
"S": s * w["S"],
"G": g * w["G"],
"sentiment": sentiment_component * w["sentiment"],
}

    return e, s, g, total, contributions    #