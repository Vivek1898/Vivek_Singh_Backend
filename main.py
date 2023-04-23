
from fastapi import FastAPI, HTTPException
from typing import List, Optional
import datetime as dt
from pydantic import BaseModel, Field
import uuid

app = FastAPI()

# Dummy data to be used in place of a database
trades_db = [
    {
        "id": 1,
        "assetClass": "Equity",
        "counterparty": "Goldman Sachs",
        "instrumentId": "AAPL",
        "instrumentName": "Apple Inc.",
        "tradeDateTime": "2022-04-14T10:00:00",
        "tradeDetails": {
            "buySellIndicator": "BUY",
            "price": 155.0,
            "quantity": 100
        },
        "trader": "John Doe"
    },
    {
        "id": 2,
        "assetClass": "Bond",
        "counterparty": "JP Morgan",
        "instrumentId": "GOOGL",
        "instrumentName": "Alphabet Inc.",
        "tradeDateTime": "2022-04-14T11:00:00",
        "tradeDetails": {
            "buySellIndicator": "SELL",
            "price": 600.0,
            "quantity": 50
        },
        "trader": "Jane Doe"
    }
]


# Pydantic model representing a single Trade
class TradeDetails(BaseModel):
    buySellIndicator: str = Field(description="A value of BUY for buys, SELL for sells.")
    price: float = Field(description="The price of the Trade.")
    quantity: int = Field(description="The amount of units traded.")


class Trade(BaseModel):
    assetClass: Optional[str] = Field(alias="assetClass", default=None, description="The asset class of the instrument traded. E.g. Bond, Equity, FX...etc")
    counterparty: Optional[str] = Field(default=None, description="The counterparty the trade was executed with. May not always be available")
    instrumentId: str = Field(alias="instrumentId", description="The ISIN/ID of the instrument traded. E.g. TSLA, AAPL, AMZN...etc")
    instrumentName: str = Field(alias="instrumentName", description="The name of the instrument traded.")
    tradeDateTime: dt.datetime = Field(alias="tradeDateTime", description="The date-time the Trade was executed")
    tradeDetails: TradeDetails = Field(alias="tradeDetails", description="The details of the trade, i.e. price, quantity")
    tradeId: Optional[str] = Field(alias="tradeId", default=None, description="The unique ID of the trade")
    trader: str = Field(description="The name of the Trader")






# Endpoint to fetch a list of trades
@app.get("/trades", response_model=List[Trade])
async def list_trades(
    search: Optional[str] = None,
    assetClass: Optional[str] = None,
    start: Optional[dt.datetime] = None,
    end: Optional[dt.datetime] = None,
    minPrice: Optional[float] = None,
    maxPrice: Optional[float] = None,
    tradeType: Optional[str] = None
) -> List[Trade]:
    result = trades_db
    
    # Search for trades by the provided search term
    if search:
        result = [trade for trade in result if search.lower() in str(trade).lower()]
    
    # Filter trades by the provided parameters
    if assetClass:
        result = [trade for trade in result if trade["assetClass"] == assetClass]

    if start:
        result = [trade for trade in result if dt.datetime.fromisoformat(trade["tradeDateTime"]) >= start]
    if end:
        result = [trade for trade in result if dt.datetime.fromisoformat(trade["tradeDateTime"]) <= end]

    if minPrice:
        result = [trade for trade in result if trade["tradeDetails"]["price"] >= minPrice]
    if maxPrice:
        result = [trade for trade in result if trade["tradeDetails"]["price"] <= maxPrice]
    if tradeType:
        result = [trade for trade in result if trade["tradeDetails"]["buySellIndicator"] == tradeType]
        
    return result

@app.get("/trades/{trade_id}", response_model=Trade)
async def get_trade_by_id(trade_id: str) -> Trade:
    for trade in trades_db:
        if trade["id"] == int(trade_id):
            return trade
    raise HTTPException(status_code=404, detail="Trade not found")

@app.post("/trades", response_model=Trade)
async def create_trade(trade: Trade) -> Trade:
    trade_dict = trade.dict()
    trade_dict["tradeId"] = str(uuid.uuid4())
    trades_db.append(trade_dict)
    return trade_dict

@app.put("/trades/{trade_id}", response_model=Trade)
async def update_trade(trade_id: str, trade: Trade) -> Trade:
    for t in trades_db:
        if t["id"] == int(trade_id):
            trades_db.remove(t)
            trades_db.append(trade.dict())
            return trade
    raise HTTPException(status_code=404, detail="Trade not found")

@app.delete("/trades/{trade_id}")
async def delete_trade(trade_id: str):
    for t in trades_db:
        if t["id"] == int(trade_id):
            trades_db.remove(t)
            return {"message": "Trade deleted successfully"}
    raise HTTPException(status_code=404, detail="Trade not found")
