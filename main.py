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

# Втори API: Изчисляване на общата възвръщаемост на инвестицията
@app.get("/roi")
def calculate_roi(
    initialInvestment: float,
    annualReturnRate: float,
    years: int
) -> Dict[str, str]:
    if initialInvestment <= 0 or annualReturnRate <= 0 or years <= 0:
        return {"error": "Грешка: Невалидни параметри."}

    finalAmount = initialInvestment * ((1 + (annualReturnRate / 100)) ** years)
    profit = finalAmount - initialInvestment

    return {
        "initialInvestment": str(initialInvestment),
        "finalAmount": str(round(finalAmount, 2)),
        "profit": str(round(profit, 2)),
        "message": f"След {years} години инвестицията ще бъде {round(finalAmount, 2)} (печалба: {round(profit, 2)})"
    }

@app.get("/compound_interest")
def calculate_compound_interest(
    principal: float, rate: float, time: int, times_compounded: int
) -> Dict[str, str]:
    if principal <= 0 or rate <= 0 or time <= 0 or times_compounded <= 0:
        return {"error": "Грешка: Невалидни параметри."}

    amount = principal * (1 + (rate / (100 * times_compounded))) ** (times_compounded * time)
    interest = amount - principal

    return {
        "finalAmount": str(round(amount, 2)),
        "interestEarned": str(round(interest, 2)),
        "message": f"След {time} години ще имаш {round(amount, 2)} (лихва: {round(interest, 2)})"
    }
