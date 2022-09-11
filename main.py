import requests
import telegram_send

# API for checking iPhone 14 Pro - Sliver - 256GB
# MODEL = "MQ103ZP/A"
MODEL = "MQ2V3ZP/A"
URL = "https://www.apple.com/th/shop/fulfillment-messages?pl=true&mts.0=regular&parts.0=%s&location=11130" %(MODEL)

def load():
    # Load the data from the API
    response = requests.get(URL)
    return response.json()

def check_availability(data):
    # Check if the iPhone is available or not
    availability_stores = []
    for store in data["body"]["content"]["pickupMessage"]["stores"]:
        if store["partsAvailability"][MODEL]["messageTypes"]["regular"]["storeSelectionEnabled"] == True:
            availability_stores.append(store["storeName"])

    return availability_stores

def send_notification(availability_stores):
    # Send notification to Telegram
    stores_text = ["-  `%s`" %(i) for i in availability_stores]
    if len(availability_stores) > 0:
        telegram_send.send(
            messages=["__*iPhone 14 Pro - Sliver - 256GB*__ is available at\n\n%s" %("\n".join(stores_text))], 
            parse_mode="Markdown",
            conf="/Users/phongsathorn/Projects/AppleStore/apple.conf"
        )

def main():
    data = load()
    availability_stores = check_availability(data)

    if availability_stores:
        print("Found available stores: %s" %(availability_stores))
        send_notification(availability_stores)
    else:
        print("No available stores")


if __name__ == "__main__":
    main()
