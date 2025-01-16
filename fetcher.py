import yfinance as yf
from datetime import datetime, timedelta
import streaming_indicators as si
import time

period = 5
SMA = si.SMA(period)

def get_next_minute():
    now = datetime.now()
    next_minute = (now + timedelta(minutes=1)).replace(second=0, microsecond=0)
    return (next_minute - now).total_seconds()

def get_data():
    try:
        nifty = yf.Ticker("^NSEI")
        data = nifty.history(period="1d", interval="1m")
        
        if not data.empty:
            latest_candle = data.iloc[-1]
            close_price = latest_candle['Close']
            sma = SMA.update(close_price)
            current_time = datetime.now().replace(second=0, microsecond=0)
            
            print(f"\n{current_time.strftime('%Y-%m-%d %H:%M:00')}")
            print(f"Latest Close Price: ₹{close_price:.2f}")
            print(sma)
    
    except Exception as e:
        print(f"Error: {e}")

def monitor():
    print("Starting price monitor...")
    
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