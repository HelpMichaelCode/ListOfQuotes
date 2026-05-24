import json
import urllib.request
import os
import csv

discord_Webhook_URL = os.getenv("API_KEY")

def get_quotes():
    webURL = "https://dummyjson.com/quotes"

    response = urllib.request.Request(url=webURL,headers={'User-Agent': 'Mozilla/5.0'})
    data = json.load(urllib.request.urlopen(response))
    quotes = data['quotes']

    return quotes

def send_quotes_to_discord(quotes):
    number_of_quotes = 0

    userChoice = input("Please select either options:\n[1] Send a number of quotes to Discord Channel\n[2] Send all quotes to Discord Channel\nEnter your choice (1 or 2): ")

    while userChoice not in ["1", "2"]:
            print("Invalid choice. Please try again.")
            userChoice = input("Please select either options:\n[1] Send a number of quotes to Discord Channel\n[2] Send all quotes to Discord Channel\nEnter your choice (1 or 2): ")
    
    if userChoice == "1":
        print("You have selected to send a number of quotes to Discord Channel.")
        number_of_quotes = input("How many quotes do you want to send to Discord? The number must be between 1 and 30: ")

        while not (number_of_quotes.isdigit() and 1 <= int(number_of_quotes) <= 30):
            print("Invalid choice. Please try again.")
            number_of_quotes = input("How many quotes do you want to send to Discord? The number must be between 1 and 30: ")

        number_of_quotes = quotes[:int(number_of_quotes)]

    elif userChoice == "2":
        print("You have selected to send all quotes to Discord Channel.")
        number_of_quotes = quotes

    for quote in number_of_quotes:
        quote_text = quote['quote']
        quote_author = quote['author']
        message = f'**{quote_author}**: *{quote_text}*'

        payload = {
            "content": message
        }

        try:
            response = urllib.request.Request(
                url=discord_Webhook_URL,
                data=json.dumps(payload).encode('utf-8'),
                headers={'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
                method='POST'
            )
            urllib.request.urlopen(response)
            print(f'Sent to Discord: {message}')
        except Exception as e:
            print(f'Failed to send to Discord: {e}')

def save_quotes_to_csv(quotes):
    # Implement the function to save quotes to CSV file
        with open('quotes.csv', mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Author', 'Quote'])  # Write the header
    
            for quote in quotes:
                writer.writerow([quote['author'], quote['quote']])  # Write each quote as a new row
        print("Quotes have been saved to quotes.csv")

listOfQuotes = get_quotes()

print("Welcome to the Quote Generator!")
print("Please select the following options:")
print("[1] Send qoutes to Discord Channel")
print("[2] Save qoutes to CSV file")

choice = input("Enter your choice (1 or 2): ")

while True:
    if choice == "1":
        print("You have selected to send quotes to Discord Channel.")
        send_quotes_to_discord(listOfQuotes)
        break
    elif choice == "2":
        print("You have selected to save quotes to CSV file.")
        save_quotes_to_csv(listOfQuotes)
        break
    else:
        print("Invalid choice. Please enter 1 or 2.")
        print("[1] Send qoutes to Discord Channel")
        print("[2] Save qoutes to CSV file")
        choice = input("Enter your choice (1 or 2): ")