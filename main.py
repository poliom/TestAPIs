from fastapi import FastAPI
from typing import Dict

app = FastAPI()

@app.get("/calculate")
def calculate_investment_time(
    targetMonthlyIncome: float,
    dividendFrequency: int,
    stockPrice: float,
    dividendPerShare: float,
    monthlyInvestment: float
) -> Dict[str, str]:
    if stockPrice <= 0 or dividendPerShare <= 0:
        return {"error": "Грешка: Липсваща цена на акция или дивидент."}

    months = 0
    totalShares = 0
    paymentsPerYear = dividendFrequency

    while (totalShares * dividendPerShare * paymentsPerYear / 12) < targetMonthlyIncome:
        months += 1
        newShares = monthlyInvestment / stockPrice
        totalShares += newShares

        if months % (12 / paymentsPerYear) == 0:
            dividendsReceived = totalShares * dividendPerShare
            reinvestedShares = dividendsReceived / stockPrice
            totalShares += reinvestedShares

    years = months // 12
    remainingMonths = months % 12

    return {
        "years": str(years),
        "months": str(remainingMonths),
        "message": f"{years} години и {remainingMonths} месеца"
    }
