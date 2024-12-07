from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class ESGScoreInput(BaseModel):
    sentiment_score: float
    benchmark_score: float
    violations: int
    public_perception: float

@router.post("/calculate-score")
def calculate_esg_score(input_data: ESGScoreInput):
    base_score = 100
    final_score = (
        base_score
        - 0.4 * (100 - input_data.sentiment_score)
        - 0.3 * input_data.benchmark_score
        - 0.2 * input_data.violations
        - 0.1 * (100 - input_data.public_perception)
    )
    return {"esg_score": max(0, round(final_score, 2))}
