# Vivek_Singh_Backend

```
Approach

The solution is a simple RESTful API implemented using FastAPI that
provides CRUD (Create, Read, Update, Delete) functionality for trades.
It uses a dummy data list trades_db to store the trades instead of a
database for simplicity.

The API has four endpoints:

1. GET /trades: Returns a list of trades filtered by search term,
asset class, trade date range, price range, and trade type.

2. GET /trades/{trade_id}: Returns a single trade identified by its
ID.

3. POST /trades: Creates a new trade.

4. PUT /trades/{trade_id}: Updates an existing trade identified by
its ID.

5. DELETE /trades/{trade_id}: Deletes an existing trade identified
by its ID.

The API uses Pydantic to define the data model for the Trade object.
Pydantic is a data validation library that allows us to specify
constraints and data types for our data. The Trade object contains
several fields, including assetClass, counterparty, instrumentId,
instrumentName, tradeDateTime, tradeDetails, tradeId, and trader.

The API implementation is straightforward and easy to follow.

1. list_trades() function filters the list of trades based on the
provided parameters, such as asset class, date range, price
range, and trade type.

2. get_trade_by_id() function returns a single trade identified by
its ID.

3. create_trade() function creates a new trade and appends it to the
in-memory list.

4. update_trade() function updates an existing trade identified by
its ID. Finally,

5. delete_trade() function deletes an existing trade identified by
its ID.


Overall, the provided code is a simple and effective implementation of
a trading data API using FastAPI and Pydantic.

Advanced filtering

The users would now like the ability to filter trades. Your endpoint
for fetching a list of trades will need to support filtering using the
following optional query parameters:






```
