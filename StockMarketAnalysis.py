# Databricks notebook source
import yfinance as yf

data = yf.download("AAPL", start="2023-01-01", end="2024-01-01")

data.head()

# COMMAND ----------

spark_df = spark.createDataFrame(data.reset_index())

spark_df.show()

# COMMAND ----------

from pyspark.sql.functions import avg

# COMMAND ----------

spark_df = spark.createDataFrame(data.reset_index())

spark_df = spark_df.toDF(
    "Date",
    "Close",
    "High",
    "Low",
    "Open",
    "Volume"
)

spark_df.show()

# COMMAND ----------

from pyspark.sql.functions import avg

spark_df.select(avg("Close")).show()

# COMMAND ----------

from pyspark.sql.functions import col

spark_df = spark_df.withColumn("Daily_Return", col("Close") - col("Open"))

spark_df.select("Date","Open","Close","Daily_Return").show()

# COMMAND ----------

from pyspark.sql.functions import max

spark_df.select(max("High")).show()

# COMMAND ----------

pandas_df = spark_df.select("Date", "Close", "Open", "High", "Low", "Volume").toPandas()

pandas_df.head()

# COMMAND ----------

pandas_df["MA_7"] = pandas_df["Close"].rolling(7).mean()

plt.figure(figsize=(14,7))

plt.plot(pandas_df["Date"], pandas_df["Close"], 
         color="blue", linewidth=2, label="Close Price")

plt.plot(pandas_df["Date"], pandas_df["MA_7"], 
         color="red", linewidth=2, label="7-Day Moving Avg")

plt.title("Apple Stock Price Trend with Moving Average", fontsize=18)
plt.xlabel("Date")
plt.ylabel("Price (USD)")

plt.grid(True, linestyle="--", alpha=0.6)
plt.legend()

plt.xticks(rotation=45)

plt.tight_layout()
plt.show()

# COMMAND ----------

plt.savefig("apple_stock_trend.png")

# COMMAND ----------

import yfinance as yf

stocks = ["AAPL", "MSFT", "TSLA", "NVDA"]

data = yf.download(stocks, start="2023-01-01", end="2024-01-01")

data.head()

# COMMAND ----------

close_prices = data["Close"]

close_prices.head()

# COMMAND ----------

from pyspark.sql.functions import col

spark_df = spark_df.withColumn("Daily_Return", col("Close") - col("Open"))
spark_df.select("Date", "Open", "Close", "Daily_Return").show()

# COMMAND ----------

import yfinance as yf
import matplotlib.pyplot as plt

stocks = ["AAPL", "MSFT", "TSLA", "NVDA"]
data = yf.download(stocks, start="2023-01-01", end="2024-01-01")
close_prices = data["Close"]

plt.figure(figsize=(14,7))
for stock in close_prices.columns:
    plt.plot(close_prices.index, close_prices[stock], label=stock)

plt.title("Stock Price Comparison (2023–2024)", fontsize=18)
plt.xlabel("Date")
plt.ylabel("Price (USD)")
plt.legend()
plt.grid(True, linestyle="--", alpha=0.6)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# COMMAND ----------

plt.figure(figsize=(14,7))

colors = {
    "AAPL": "#1f77b4",
    "MSFT": "#ff7f0e",
    "NVDA": "#2ca02c",
    "TSLA": "#d62728"
}

for stock in close_prices.columns:
    plt.plot(close_prices.index, close_prices[stock],
             label=stock,
             linewidth=2.5,
             color=colors[stock])

plt.title("Stock Price Comparison (2023–2024)", fontsize=18)
plt.xlabel("Date", fontsize=12)
plt.ylabel("Price (USD)", fontsize=12)

plt.legend(title="Company")
plt.grid(True, linestyle="--", alpha=0.6)

plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# COMMAND ----------

plt.savefig("stock_comparison_chart.png")

# COMMAND ----------

normalized = close_prices / close_prices.iloc[0] * 100

plt.figure(figsize=(14,7))

for stock in normalized.columns:
    plt.plot(normalized.index, normalized[stock], label=stock, linewidth=2)

plt.title("Stock Growth Comparison (Indexed to 100)", fontsize=18)
plt.xlabel("Date")
plt.ylabel("Growth Index")

plt.legend()
plt.grid(True, linestyle="--", alpha=0.6)

plt.xticks(rotation=45)
plt.tight_layout()
plt.show()