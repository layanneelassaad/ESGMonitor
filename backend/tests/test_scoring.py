from backend.nlp.scoring import compute_scores


def test_scoring_shape():
    topics = {"pillars": {"E": [{"label": "GHG emissions", "score": 0.7}], "S": [], "G": []}}
    e, s, g, total, contrib = compute_scores(topics, 0.6)
    assert isinstance(total, float) and isinstance(contrib, dict)