import os
from dotenv import load_dotenv
import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL

load_dotenv()

"""
READ CSV
"""
df = pd.read_csv("clean/results.csv", parse_dates=["race_date"])
print(f"Read {len(df)} rows from clean/results.csv")

"""
CONNECT TO MYSQL SERVER
"""
url = URL.create(
    "mysql+pymysql",
    username = os.getenv("USER"),
    password = os.getenv("PASSWORD"), 
    host = os.getenv("HOST"),
    port = os.getenv("PORT"),
    database = os.getenv("DATABASE"),
)

engine = create_engine(url)

"""
LOADING RESULTS TO DB
"""
df.to_sql("results", engine, if_exists= "replace", index= False)
print(f"Loaded {len(df)} rows into MySQL table")

# verifying connection
with engine.connect() as conn:
    count = conn.execute(text("SELECT COUNT(*) FROM results")).scalar()
print(f"MySQL says the table has {count} rows")
