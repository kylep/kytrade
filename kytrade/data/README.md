# Data Usage Example

## Using Pandas

NOTE: Pandas SQL does not support sqlalchemy 2.0 so future=False is set in the engine.

```python
import pandas as pd
from sqlalchemy import select, insert, update, delete, desc
from kytrade.data.models import DailyStockPrice
from kytrade.data.db import engine, save_dataframe

# Read entire table to DF
query = select(DailyStockPrice).where(DailyStockPrice.date == "2020-01-01")
df = pd.read_sql(query, engine)


# Read with a more complicated query
dt = datetime.date.fromisoformat("2020-01-01")
query = (
  select([DailyStockPrice])
  .order_by(desc(DailyStockPrice.date))
  .where(DailyStockPrice.date <= dt)
  .where(DailyStockPrice.ticker == "SPY")
  .limit(10)
)
pd.read_sql(query, engine)


# Write entire DF to table
save_dataframe(DailyStockPrice, df)

```


## Using the ORM

The ORM is easier to test with pytest and more feature-rich.
I prefer to use Pandas when possible for consistency.

```python
from sqlalchemy import select, insert, update, delete
from kytrade.data import db
from kytrade.data.models import DailyStockPrice

session = db.session()

# Read Query
statement = select(DailyStockPrice).where(DailyStockPrice.ticker == "FOO")
result = session.execute(statement)
for row in result:
 	  open = row[0].open
	  ticker = row[0].ticker
    # so on


# Insert ORM object
foo1 = DailyStockPrice(ticker='FOO', date='2020-01-01', open=10.23, close=12.23, low=10.11, high=13.44, volume=1234)
session = session()
session.add(foo1)
session.commit()


# Update Query
statement = (
		update(DailyStockPrice)
		.where(DailyStockPrice.ticker == "FOO")
		.where(DailyStockPrice.date == "2020-01-02")
		.values(high=222.12)
)
session.execute(statement)
session.commit()

# Or just add it using the session it was created with the commit


# Delete Query
statement = delete(DailyStockPrice).where(DailyStockPrice.ticker == "FOO")
session.execute(statement)
session.commit()
```
