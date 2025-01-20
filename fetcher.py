import yfinance as yf
from datetime import datetime, timedelta
import streaming_indicators as si
import time

period = 100
SMA = si.SMA(period)

def get_next_minute():
    now = datetime.now()
    next_minute = (now + timedelta(minutes=1)).replace(second=0, microsecond=0)
    return (next_minute - now).total_seconds()

def get_data():
    try:
        nifty = yf.Ticker("^NSEI")
        data = nifty.history(period="5d", interval="1m")
        
        if not data.empty:
            current_candle = data.iloc[-1]
            close_price = current_candle['Close']
            open_price = current_candle['Open']
            high_price = current_candle['High']
            low_price = current_candle['Low']
            
            historical_prices = data['Close'].tail(period).tolist()
            for price in historical_prices[:-1]:
                SMA.update(price)
            
            sma_value = SMA.update(close_price)
            current_time = datetime.now().replace(second=0, microsecond=0)
            
            print(f"\n{current_time.strftime('%Y-%m-%d %H:%M:00')}")
            print(f"Open Price: ₹{open_price:.2f}")
            print(f"High Price: ₹{high_price:.2f}")
            print(f"Low Price: ₹{low_price:.2f}")
            print(f"Current Price: ₹{close_price:.2f}")
            print(f"SMA({period}): ₹{sma_value:.2f}")
            
            signal = "Call" if close_price > sma_value else "Put"
            print(f"Signal: {signal}")
    
    except Exception as e:
        print(f"Error: {e}")

def monitor():
    print("Starting price monitor...")
    print(f"Calculating {period}-minute Simple Moving Average...")
    
    while True:
        try:
            wait_time = get_next_minute()
            time.sleep(wait_time)
            get_data()
            
        except KeyboardInterrupt:
            print("\nStopping monitor...")
            break

        except Exception as e:
            print(f"Error: {e}")
            time.sleep(get_next_minute())

monitor()