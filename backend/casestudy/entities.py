from pydantic import BaseModel

class SecurityInfo(BaseModel):
    id: int
    name: str
    ticker: str

class SecurityPrice(BaseModel):
    id: int
    security: SecurityInfo
    latest_price: float
    last_updated: datetime

class User(BaseModel):
    id: int
    username: str

class Watchlist(BaseModel):
    id: int
    user: User
    securities: List[SecurityPrice]

