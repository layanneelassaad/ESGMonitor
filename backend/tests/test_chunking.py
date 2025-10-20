from backend.nlp.chunking import chunk_text


def test_chunking_basic():
    txt = "word " * 2000
    chunks = chunk_text(txt, max_tokens=100, overlap=20)
    assert len(chunks) > 1