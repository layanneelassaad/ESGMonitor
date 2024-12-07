from fastapi import APIRouter
from models.clause_extraction import extract_clauses

router = APIRouter()

@router.post("/analyze-document")
def analyze_document(text: str):
    """
    Extracts key ESG clauses and entities from the document.
    """
    entities = extract_clauses(text)
    key_topics = [entity["word"] for entity in entities if entity["entity_group"] == "ORG"]
    return {"entities": entities, "key_topics": key_topics}
