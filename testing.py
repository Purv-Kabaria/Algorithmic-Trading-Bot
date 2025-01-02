import yfinance as yf
import time

def get_data():
    try:
        nifty = yf.Ticker("^NSEI")
        data = nifty.history(period="1d", interval="1m")
        
        if not data.empty:
            latest = data.iloc[-1]
            
            print(f"O:   ₹{latest['Open']:.2f}")
            print(f"H:   ₹{latest['High']:.2f}")
            print(f"L:    ₹{latest['Low']:.2f}")
            print(f"C:  ₹{latest['Close']:.2f}")
            print()
            
        return data
    except Exception as e:
        print(f"{e}")
        return None

def monitor(interval_seconds=60):
    print("Starting Nifty 50 price monitor...")
    
    while True:
        try:
            get_data()
            time.sleep(interval_seconds)
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"{e}")
            time.sleep(interval_seconds)

monitor(10)