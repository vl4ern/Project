from pydantic import BaseModel, Field

class WalletDeposit(BaseModel):
    # Field(gt=0) означает "Greater Than 0" (Строго больше нуля). 
    # Если пришлют минус или ноль - Pydantic сам выдаст ошибку 422!
    amount: float = Field(..., gt=0, description="Сумма для пополнения")