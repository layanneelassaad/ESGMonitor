from typing import Iterable
from transformers import AutoTokenizer


# Token-aware chunking with overlap


def chunk_text(text: str, model_name: str = "facebook/bart-large-cnn", max_tokens: int = 800, overlap: int = 80) -> Iterable[str]:
    tok = AutoTokenizer.from_pretrained(model_name)
    ids = tok.encode(text, add_special_tokens=False)
    if not ids:
        return []
    out = []
    start = 0
    while start < len(ids):
        end = min(start + max_tokens, len(ids))
        chunk_ids = ids[start:end]
        out.append(tok.decode(chunk_ids))
        if end == len(ids):
            break
        start = end - overlap
        if start < 0:
            start = 0
    return out