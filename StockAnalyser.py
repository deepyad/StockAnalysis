# https://www.perplexity.ai/search/just-add-eps-earning-per-share-ParpkhPlRNOhMCdn00iAqQ

import pandas as pd
import yfinance as yf
import os
import datetime
import numpy as np
import time
import matplotlib.pyplot as plt

# ================== RSI, MACD, PE Calculation Functions ==================

import requests
from bs4 import BeautifulSoup


import requests
from bs4 import BeautifulSoup

import requests

def get_latest_news_link_newsdata(ticker_symbol, positive=True, apikey="pub_0ddc8208bc3746b2b1470feaf234c927"):
    """
    Fetches the latest positive or negative news for the given ticker using NewsData.io API.
    Returns headline and url.
    """
    query = f"{ticker_symbol}"
    url = f"https://newsdata.io/api/1/news"
    params = {
        "apikey": apikey,
        "q": query,
        "language": "en",
        "country": "in",
        "category": "business"
    }
    try:
        resp = requests.get(url, params=params, timeout=10)
        data = resp.json()
        keywords_pos = ['surge', 'profit', 'beats', 'rise', 'growth', 'record', 'gain', 'buy', 'up', 'upgrade', 'outperform']
        keywords_neg = ['loss', 'decline', 'drops', 'down', 'plunge', 'sell', 'downgrade', 'bearish', 'fall', 'lower', 'misses']
        search_keywords = keywords_pos if positive else keywords_neg
        for news in data.get('results', []):
            title = news.get('title', '').lower()
            link = news.get('link', None)
            if any(k in title for k in search_keywords) and link:
                return news.get('title'), link
        # fallback: return latest headline (if exists)
        if data.get('results'):
            return data['results'][0].get('title', None), data['results'].get('link', None)
    except Exception as e:
        print("Error fetching news:", e)
    return None, None


def calculate_RSI(prices, period=14):
    delta = prices.diff()
    gain = np.where(delta > 0, delta, 0)
    loss = np.where(delta < 0, -delta, 0)
    avg_gain = pd.Series(gain).rolling(window=period).mean()
    avg_loss = pd.Series(loss).rolling(window=period).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def classify_RSI_per_day(rsi_series):
    status = rsi_series.apply(lambda x: "Overbought" if x > 70 else ("Oversold" if x < 30 else "Neutral"))
    return status

def calculate_MACD(prices, short_window=12, long_window=26, signal_window=9):
    ema_short = prices.ewm(span=short_window, adjust=False).mean()
    ema_long = prices.ewm(span=long_window, adjust=False).mean()
    macd_line = ema_short - ema_long
    signal_line = macd_line.ewm(span=signal_window, adjust=False).mean()
    return macd_line, signal_line

def classify_MACD_per_day(macd_series, signal_series):
    """
    Classifies MACD status with extreme/medium/neutral levels.
    Extreme Overbought: diff > 1.5
    Medium Overbought: diff > 0.7
    Neutral: -0.7 <= diff <= 0.7
    Medium Oversold: diff < -0.7
    Extreme Oversold: diff < -1.5
    """
    diff = macd_series - signal_series

    def classify_val(x):
        if x > 1.5:
            return "Extreme Overbought"
        elif x > 0.7:
            return "Medium Overbought"
        elif x < -1.5:
            return "Extreme Oversold"
        elif x < -0.7:
            return "Medium Oversold"
        else:
            return "Neutral"

    status = diff.apply(classify_val)
    return status

def get_PE_history(ticker, period="5y", interval="1mo"):
    # Get monthly close prices for 5 years
    stock = yf.Ticker(ticker)
    hist = stock.history(period=period, interval=interval)
    try:
        info = stock.info
        trailing_eps = info.get('trailingEps', None)
        # If EPS is not available, return empty series
        if trailing_eps in [None, 0, 'nan']:
            return pd.Series([np.nan]*len(hist), index=hist.index)
        pe_series = hist['Close'] / trailing_eps
        return pe_series
    except Exception as e:
        print(f"Error fetching PE history for {ticker}: {e}")
        return pd.Series([np.nan]*len(hist), index=hist.index)

def get_latest_PE(ticker_symbol):
    try:
        stock = yf.Ticker(ticker_symbol)
        info = stock.info
        trailing_eps = info.get('trailingEps', None)
        latest_price = info.get('regularMarketPrice', None)
        if trailing_eps in [None, 0, 'nan'] or latest_price in [None, 'nan']:
            return np.nan
        return latest_price / trailing_eps
    except Exception as e:
        print(f"Error fetching PE for {ticker_symbol}: {e}")
        return np.nan

# ================== Utility Functions ==================

def format_percent_change(change):
    if pd.isna(change):
        return None
    return f"{'+' if change > 0 else ''}{change:.2f}%"

def get_analyst_recommendation(stock, ticker_symbol):
    try:
        recommendations = stock.recommendations
        if recommendations is not None and not recommendations.empty:
            latest_rec = recommendations.iloc[-1]
            if 'To Grade' in latest_rec:
                return latest_rec['To Grade'].upper()
        info = stock.info
        if 'recommendationKey' in info:
            rec_key = info['recommendationKey'].upper()
            rec_map = {
                'STRONG_BUY': 'STRONG BUY',
                'BUY': 'BUY',
                'HOLD': 'HOLD',
                'UNDERPERFORM': 'SELL',
                'SELL': 'STRONG SELL'
            }
            return rec_map.get(rec_key, rec_key)
        return "N/A"
    except:
        return "N/A"

def get_price_target_pct(stock, current_price, ticker_symbol):
    try:
        info = stock.info
        if 'targetMeanPrice' in info and info['targetMeanPrice'] is not None:
            target_price = info['targetMeanPrice']
            return ((target_price - current_price) / current_price) * 100
        return np.nan
    except:
        return np.nan

def generate_recommendation(week_change, month_change, three_month_change, analyst_rec, target_pct):
    if analyst_rec not in ["N/A"]:
        return analyst_rec
    week_change = 0 if pd.isna(week_change) else week_change
    month_change = 0 if pd.isna(month_change) else month_change
    three_month_change = 0 if pd.isna(three_month_change) else three_month_change
    target_pct = 0 if pd.isna(target_pct) else target_pct
    if target_pct != 0:
        score = (0.15 * week_change) + (0.2 * month_change) + (0.25 * three_month_change) + (0.4 * target_pct)
    else:
        score = (0.2 * week_change) + (0.3 * month_change) + (0.5 * three_month_change)
    if score > 15:
        return "BUY"
    elif score < -10:
        return "SELL"
    else:
        return "HOLD"

# ================== Chart Creation Function ==================
def create_indicator_chart(ticker, hist, rsi_series, macd_line, signal_line, pe_series, save_dir="charts"):
    os.makedirs(save_dir, exist_ok=True)
    fig, axes = plt.subplots(3, 1, figsize=(4, 5), sharex=False,
                             gridspec_kw={'height_ratios': [2, 1, 1]})
    # MACD graph (no close price)
    axes[0].plot(hist.index, macd_line, label='MACD', color='blue', linewidth=1)
    axes[0].plot(hist.index, signal_line, label='Signal', color='red', linewidth=1, linestyle='--')
    axes[0].legend(fontsize=6)
    axes[0].set_title(f"{ticker} - MACD", fontsize=8)
    # RSI graph
    axes[1].plot(hist.index, rsi_series, label='RSI', color='purple', linewidth=1)
    axes[1].axhline(70, color='red', linestyle='--', linewidth=0.7)
    axes[1].axhline(30, color='green', linestyle='--', linewidth=0.7)
    axes[1].set_ylim(0, 100)
    axes[1].legend(fontsize=6)
    axes[1].set_title("RSI", fontsize=8)
    # PE Ratio graph (5-year monthly)
    if pe_series is not None and not pe_series.empty:
        axes[2].plot(pe_series.index, pe_series, label='PE Ratio', color='orange', linewidth=1)
        axes[2].legend(fontsize=6)
        axes[2].set_title("PE Ratio (5yr)", fontsize=8)
    else:
        axes[2].set_title("PE Ratio unavailable", fontsize=8)
    plt.tight_layout()
    filepath = os.path.join(save_dir, f"{ticker}_chart.png")
    plt.savefig(filepath, dpi=80)
    plt.close(fig)
    return filepath

# ================== Main Data Function ==================
def get_stock_data(ticker_symbol):
    try:
        stock = yf.Ticker(ticker_symbol)
        hist = stock.history(period="100d")
        if len(hist) < 2:
            empty_series = pd.Series(dtype=np.float64)
            empty_status = pd.Series(dtype=object)
            return np.nan, np.nan, np.nan, "N/A", np.nan, empty_series, empty_status, empty_series, empty_series, empty_status, np.nan, empty_series, ""
        latest_close = hist['Close'].iloc[-1]
        latest_date = hist.index[-1].date()
        hist_dates = [d.date() for d in hist.index]
        def find_closest_trading_day(target_date):
            valid_dates = [d for d in hist_dates if d <= target_date]
            if not valid_dates:
                return 0
            closest_date = max(valid_dates)
            return hist_dates.index(closest_date)
        week_idx = find_closest_trading_day(latest_date - datetime.timedelta(days=7))
        month_idx = find_closest_trading_day(latest_date - datetime.timedelta(days=30))
        three_month_idx = find_closest_trading_day(latest_date - datetime.timedelta(days=90))
        week_chg = ((latest_close - hist['Close'].iloc[week_idx]) / hist['Close'].iloc[week_idx]) * 100
        month_chg = ((latest_close - hist['Close'].iloc[month_idx]) / hist['Close'].iloc[month_idx]) * 100
        three_m_chg = ((latest_close - hist['Close'].iloc[three_month_idx]) / hist['Close'].iloc[three_month_idx]) * 100
        recommendation = get_analyst_recommendation(stock, ticker_symbol)
        target_pct = get_price_target_pct(stock, latest_close, ticker_symbol)
        rsi_series = calculate_RSI(hist['Close'])
        rsi_status = classify_RSI_per_day(rsi_series)
        macd_line, signal_line = calculate_MACD(hist['Close'])
        macd_status = classify_MACD_per_day(macd_line, signal_line)
        # PE ratio values
        pe_series = get_PE_history(ticker_symbol, period="5y", interval="1mo")
        latest_pe = get_latest_PE(ticker_symbol)
        chart_path = create_indicator_chart(ticker_symbol, hist, rsi_series, macd_line, signal_line, pe_series)
        latest_news=get_latest_news_link_newsdata(ticker_symbol)
        return (week_chg, month_chg, three_m_chg, recommendation, target_pct,
                rsi_series, rsi_status, macd_line, signal_line, macd_status, latest_pe, pe_series, chart_path,latest_news)
    except Exception as e:
        print(f"Error fetching data for {ticker_symbol}: {e}")
        empty_series = pd.Series(dtype=np.float64)
        empty_status = pd.Series(dtype=object)
        return np.nan, np.nan, np.nan, "N/A", np.nan, empty_series, empty_status, empty_series, empty_series, empty_status, np.nan, empty_series, ""

# ================ Holdings Processing ================
def process_holdings_file(
    input_file="./content/drive/MyDrive/holdings_with_changes_14_Aug.csv",
    output_file="OUTPUT_21_Aug.xlsx"):

    import re

    if not os.path.exists(input_file):
        print(f"Error: File '{input_file}' not found in {os.getcwd()}")
        return
    holdings_df = pd.read_csv(input_file)
    ticker_col = "Instrument"
    holdings_df['Last_Week_Change_%'] = None
    holdings_df['1_Month_Change_%'] = None
    holdings_df['3_Month_Change_%'] = None
    holdings_df['Broker_Recommendation'] = None
    holdings_df['12_Month_Target_%'] = None
    holdings_df['RSI_Score'] = None
    holdings_df['RSI_Status'] = None
    holdings_df['MACD_Value'] = None
    holdings_df['Signal_Value'] = None
    holdings_df['MACD_Status'] = None
    holdings_df['PE_Ratio'] = None
    holdings_df['Indicator_Chart'] = None
    holdings_df['Indicator_Chart'] = None
    holdings_df['latest_news'] = None
    for i, row in holdings_df.iterrows():
        ticker = str(row[ticker_col]).strip()
        if pd.isna(ticker) or ticker == "":
            continue
        if "." in ticker:
            ticker = ticker.split(".")[0]
        nse_ticker = f"{ticker}.NS"
        print(f"Processing {nse_ticker} ({i+1}/{len(holdings_df)}) ...")
        (week_chg, month_chg, three_m_chg, analyst_rec, target_pct,
         rsi_series, rsi_status, macd_line, sig_line, macd_status,
         latest_pe, pe_series, chart_path,latest_news) = get_stock_data(nse_ticker)
        holdings_df.at[i, 'Last_Week_Change_%'] = format_percent_change(week_chg)
        holdings_df.at[i, '1_Month_Change_%'] = format_percent_change(month_chg)
        holdings_df.at[i, '3_Month_Change_%'] = format_percent_change(three_m_chg)
        holdings_df.at[i, '12_Month_Target_%'] = format_percent_change(target_pct)
        holdings_df.at[i, 'Broker_Recommendation'] = generate_recommendation(week_chg, month_chg, three_m_chg, analyst_rec, target_pct)
        holdings_df.at[i, 'RSI_Score'] = round(rsi_series.iloc[-1], 2) if not rsi_series.empty and pd.notna(rsi_series.iloc[-1]) else None
        holdings_df.at[i, 'RSI_Status'] = rsi_status.iloc[-1] if not rsi_status.empty else None
        holdings_df.at[i, 'MACD_Value'] = round(macd_line.iloc[-1], 4) if not macd_line.empty and pd.notna(macd_line.iloc[-1]) else None
        holdings_df.at[i, 'Signal_Value'] = round(sig_line.iloc[-1], 4) if not sig_line.empty and pd.notna(sig_line.iloc[-1]) else None
        holdings_df.at[i, 'MACD_Status'] = macd_status.iloc[-1] if not macd_status.empty else None
        holdings_df.at[i, 'PE_Ratio'] = round(latest_pe, 2) if pd.notna(latest_pe) else None
        holdings_df.at[i, 'Indicator_Chart'] = chart_path
        holdings_df.at[i, 'latest_news'] =latest_news

        time.sleep(0.5)

    # 1. Extract numeric 12_Month_Target for sorting
    def parse_pct(val):
        if pd.isna(val):
            return -float('inf')
        try:
            return float(str(val).replace('%','').replace('+',''))
        except Exception:
            return -float('inf')
    holdings_df['_sort_12mo'] = holdings_df['12_Month_Target_%'].apply(parse_pct)

    # 2. Custom sort order for Broker_Recommendation
    rec_sort = {
        "STRONG BUY": 1,
        "BUY": 2,
        "HOLD": 3, "NONE": 3, "N/A": 3,
        "SELL": 4, "STRONG SELL": 4
    }
    def get_rec_rank(val):
        if isinstance(val, str):
            return rec_sort.get(val.strip().upper(), 5)
        return 5
    holdings_df['_rec_rank'] = holdings_df['Broker_Recommendation'].apply(get_rec_rank)

    # 3. Sort by rec_rank, then by _sort_12mo descending
    holdings_df = holdings_df.sort_values(by=['_rec_rank', '_sort_12mo'], ascending=[True, False])
    holdings_df = holdings_df.drop(columns=['_sort_12mo', '_rec_rank'])

    import datetime
    today_str = datetime.datetime.now().strftime('%d_%b')
    # Write to Excel
    # holdings_df.to_excel(output_file, index=False)
    output_file = f"OUTPUT_{today_str}.xlsx"
    holdings_df.to_excel(output_file, index=False)
    print(f"\nOutput saved to {output_file}")
    print(f"Charts saved in 'charts/' folder.")


if __name__ == "__main__":
    process_holdings_file()
    print("\nDone!")
