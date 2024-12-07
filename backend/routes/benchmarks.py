from fastapi import APIRouter
from typing import List
router = APIRouter()

@router.get("/industry-benchmark")
def get_industry_benchmark(company_scores: List[float]):
    """
    Compares a company's ESG scores to industry averages.
    """
    industry_average = sum(company_scores) / len(company_scores) if company_scores else 0
    return {"industry_average": round(industry_average, 2)}
