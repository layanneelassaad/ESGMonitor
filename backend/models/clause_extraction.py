import nltk
from transformers import pipeline

ner_pipeline = pipeline("ner", model="dslim/bert-base-NER", device=0)

def extract_clauses(document):
    """
    Extract clauses from a document and annotate entities using NER.
    """
    nltk.download("punkt", quiet=True)
    sentences = nltk.sent_tokenize(document)
    clauses = []

    for sentence in sentences:
        ner_results = ner_pipeline(sentence)
        entities = []
        for entity in ner_results:
            # Dynamically check for 'entity_group' or 'entity'
            entity_type = entity.get("entity_group") or entity.get("entity")  # Fallback to 'entity'
            if entity_type:  # Only add if entity type exists
                entities.append({
                    "word": entity.get("word"),
                    "entity_type": entity_type,
                    "score": entity.get("score"),
                })
        clauses.append({"text": sentence, "entities": entities})

    print(f"Extracted {len(clauses)} clauses", flush=True)
    return clauses
