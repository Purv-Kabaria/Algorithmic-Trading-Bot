import yfinance as yf
from datetime import datetime, timedelta
import time

def get_next_minute():
    now = datetime.now()
    next_minute = (now + timedelta(minutes=1)).replace(second=0, microsecond=0)
    return (next_minute - now).total_seconds()

def get_data():
    try:
        nifty = yf.Ticker("^NSEI")
        data = nifty.history(period="1d", interval="1m")
        
        if not data.empty:
            latest = data.iloc[-1]
            current_time = datetime.now().replace(second=0, microsecond=0)
            
            print(current_time.strftime("%Y-%m-%d %H:%M:00"))
            print(f"O: ₹{latest['Open']:.2f}")
            print(f"H: ₹{latest['High']:.2f}")
            print(f"L: ₹{latest['Low']:.2f}")
            print(f"C: ₹{latest['Close']:.2f}")
            print()
        return data
    
    except Exception as e:
        print(f"Error: {e}")
        return None

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