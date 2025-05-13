import time
import requests
import schedule
from datetime import datetime
from threading import Thread

# === CONFIGURATION ===
symbol = "eurusd"
high_price = 1.1250
low_price = 1.1070

USE_DISCORD = True
DISCORD_WEBHOOK_URL = "https://discordapp.com/api/webhooks/1371951555204481064/P1b-VuB-OhrERfKQmQDf0BGjQURl9dlosuGiMEOcWp8RxuXCytLvkZuJXdeCqGA0sJQ-"

DELAYED_SEND = True  # ⬅️ Set to True for 24hr delayed notification

alerted = False

def fetch_price():
    try:
        url = f"https://api.exchangerate.host/latest?base=EUR&symbols=USD"
        response = requests.get(url).json()
        return response["rates"]["USD"]
    except Exception as e:
        print("❌ Error fetching price:", e)
        return None

def send_notification(triggered_price):
    message = f"EURUSD hit {triggered_price}. {'Reminder set for 24h.' if DELAYED_SEND else 'Notification sent now.'}"

    def notify():
        if DELAYED_SEND:
            time.sleep(86400)  # 24 hours
        if USE_DISCORD:
            requests.post(DISCORD_WEBHOOK_URL, json={"content": message})
        print("✅ Notification sent.")

    Thread(target=notify).start()

def check_price():
    global alerted
    if alerted:
        return
    price = fetch_price()
    if price:
        print(f"[{datetime.now()}] EURUSD price: {price}")
        if price >= high_price or price <= low_price:
            print("🚨 Price level hit.")
            alerted = True
            send_notification(price)

# Schedule checks every minute
schedule.every(1).minutes.do(check_price)

print("🟢 EURUSD Bot Running...")
while True:
    schedule.run_pending()
    time.sleep(1)
