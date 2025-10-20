from typing import Dict, List
import nltk
from .pipelines import ner, summarizer, sentiment, zero_shot
from .chunking import chunk_text
from .labels import ALL_LABELS, ESG_LABELS


nltk.download("punkt", quiet=True)




def extract_locations(sent: str) -> List[str]:
    ents = ner(sent)
    return [e["word"] for e in ents if e.get("entity_group") == "LOC"]




def summarize_long(text: str) -> str:
    chunks = chunk_text(text, max_tokens=700, overlap=80)
    out = []
    for ch in chunks:
        try:
            res = summarizer(ch, max_length=180, min_length=60, do_sample=False)
            out.append(res[0]["summary_text"])
        except Exception:
            continue
    return " ".join(out) if out else text[:800]




def classify_esg_topics(text: str, k: int = 3) -> Dict[str, List[Dict]]:
    """Return top-k labels overall and per pillar."""
    overall = zero_shot(text, candidate_labels=ALL_LABELS, multi_label=True)
    scores = dict(zip(overall["labels"], overall["scores"]))
    per = {}
    for pillar, labels in ESG_LABELS.items():
        ranked = sorted([(l, scores.get(l, 0.0)) for l in labels], key=lambda x: x[1], reverse=True)[:k]
        per[pillar] = [{"label": l, "score": s} for l, s in ranked]
    top_overall = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:k]
    return {
        "overall": [{"label": l, "score": s} for l, s in top_overall],
        "pillars": per,
    }




def analyze_sentiment(text: str) -> Dict[str, float]:
    res = sentiment(text[:1000])  # cap for speed
    r = res[0]
    score = r["score"] if r["label"].upper().startswith("POS") else (1 - r["score"])
    return {"label": r["label"], "confidence": r["score"], "pos_score": score}




def branch_summaries(text: str) -> Dict[str, str]:
    sents = nltk.sent_tokenize(text)
    buckets: Dict[str, List[str]] = {}
    for s in sents:
        locs = extract_locations(s)
        for loc in locs or ["Global"]:
            buckets.setdefault(locs[0] if locs else "Global", []).append(s)
    out = {}
    for loc, lst in buckets.items():
        try:
            joined = " ".join(lst)
            sm = summarizer(joined, max_length=140, min_length=40, do_sample=False)
            out[loc] = sm[0]["summary_text"]
        except Exception:
            out[loc] = " ".join(lst)[:240]
    return out