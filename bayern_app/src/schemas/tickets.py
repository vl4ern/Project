from pydantic import BaseModel

class TicketPurchase(BaseModel):
    seat_id: int # Фанат присылает только ID места, которое хочет купить