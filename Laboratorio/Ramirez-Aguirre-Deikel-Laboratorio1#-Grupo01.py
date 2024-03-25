import random
from colorama import Fore, Style
import os
import json
from datetime import datetime

# Global variables
cancha = [['' for _ in range(10)] for _ in range(10)]
MAX_OCCUPIED = 15

# Seat prices
PRICES = {
    'row_1_4': 5000,
    'row_5_7': 10000,
    'row_8_10': 15000
}

# Generate occupied seats
def GenerateOccupiedSeats():
    occupied_seats = 0
    while occupied_seats < MAX_OCCUPIED:
        row = random.randint(0, 9)
        column = random.randint(0, 9)
        if not cancha[row][column].endswith(Style.RESET_ALL):
            cancha[row][column] = Fore.RED + 'X' + Style.RESET_ALL
            occupied_seats += 1

# Generate seat matrix
def CreateField():
    for i in range(10):
        for j in range(10):
            row = i + 1
            seat = f"{str(row)}{chr(65 + j)}"  # chr converts ASCII code to letters
            cancha[i][j] = seat
    GenerateOccupiedSeats()

# Print seat matrix
def ShowField():
    print("  " + " ".join([chr(65 + j) for j in range(10)]))
    for i in range(10):
        print(str(i + 1) + " " + " ".join(cancha[i]))

# Show seat prices
def ShowSeatPrices():
    print("\nSeat Prices:")
    print("Seats in rows 1 - 4: 5000 colones")
    print("Seats in rows 5 - 7: 10000 colones")
    print("Seats in rows 8 - 10: 15000 colones")

# Spectator registration
def SpectatorRegistration():
    print("\nSpectator Registration")
    while True:
        id_number = input("Enter your ID number (9 digits): ")
        if id_number.isdigit() and len(id_number) == 9:
            break
        else:
            print("The ID number must contain exactly 9 digits.")

    # Check if the user is already registered
    for buyer in buyers:
        if buyer["id_number"] == id_number:
            print("The user is already registered.")
            return

    while True:
        name = input("Enter your name: ")
        if all(char.isalpha() or char.isspace() for char in name):
            break
        else:
            print("The name can only contain letters and spaces.")

    while True:
        gender = input("Enter your gender (M/F): ").upper()
        if gender == 'M' or gender == 'F':
            break
        else:
            print("Invalid gender. Enter 'M' for male or 'F' for female.")

    buyers.append({
        "id_number": id_number,
        "name": name,
        "gender": gender,
        "seats_purchased": [],
        "male_tickets": 0,
        "female_tickets": 0
    })

    print("Registration successful.")

def load_buyers():
    try:
        with open("sales_report.json", "r") as f:
            buyers = json.load(f)
    except FileNotFoundError:
        buyers = []
    return buyers

buyers = load_buyers()


# Save purchase to JSON
def SavePurchase(purchased_tickets, buyer_name, buyer_gender):
    total_purchase = 0  # Variable to store the total purchase
    for ticket in purchased_tickets:
        row = int(ticket[0]) - 1
        column = ord(ticket[1].upper()) - ord('A')

        for buyer in buyers:
            if buyer["name"] == buyer_name:
                # Calculate seat price
                if row < 4:
                    seat_price = PRICES['row_1_4']
                elif row < 7:
                    seat_price = PRICES['row_5_7']
                else:
                    seat_price = PRICES['row_8_10']
                total_purchase += seat_price  # Add to total purchase

                buyer["seats_purchased"].append({
                    "seat": ticket,
                    "price": seat_price,  # Register seat price
                    "purchase_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })

                # Update gender-specific ticket count
                if buyer_gender == 'M':
                    buyer["male_tickets"] = buyer.get("male_tickets", 0) + 1
                elif buyer_gender == 'F':
                    buyer["female_tickets"] = buyer.get("female_tickets", 0) + 1

    # Save information to a JSON file
    with open("sales_report.json", "w") as f:
        json.dump(buyers, f, indent=4)

    return total_purchase  # Return the total purchase value

def PurchaseTickets():
    print("\nPurchase Tickets")

    # Check if there are registered spectators
    if not buyers:
        print("There are no registered spectators. Please register first.")
        input("Press enter to continue...")
        return

    # Enter ID number
    id_number = input("Enter your ID number (9 digits): ")

    # Check if the spectator is already registered
    buyer_name = ""
    buyer_gender = ""
    for buyer in buyers:
        if buyer["id_number"] == id_number:
            buyer_name = buyer["name"]
            buyer_gender = buyer["gender"]
            break

    if buyer_name == "":
        print("No registered buyer found with that ID number.")
        input("Press enter to continue...")
        return

    print(f"Welcome back, {buyer_name}.")

    # Enter number of tickets to buy
    num_tickets = int(input("Enter the number of tickets you want to buy (1-3): "))
    if num_tickets < 1 or num_tickets > 3:
        print("Invalid number of tickets.")
        input("Press enter to continue...")
        return

    # List to store purchased tickets
    purchased_tickets = []

    for i in range(num_tickets):
        while True:
            try:
                row = int(input(f"Enter the row of ticket {i + 1} (1-10): "))
                column = input(f"Enter the column of ticket {i + 1} (A-J): ")

                # Validate row and column
                if row < 1 or row > 10 or column.upper() < 'A' or column.upper() > 'J':
                    print("Invalid seat.")
                    continue

                # Check if the seat is occupied
                if not cancha[row - 1][ord(column.upper()) - ord('A')].endswith(Style.RESET_ALL):
                    purchased_tickets.append((row, column))
                    cancha[row - 1][ord(column.upper()) - ord('A')] = Fore.BLUE + 'X' + Style.RESET_ALL
                    print("Seat selected successfully.")
                    break
                else:
                    print("The selected seat is occupied. Please select another one.")
                    continue
            except ValueError:
                print("Invalid input. Please enter a valid number for the row.")

    if len(purchased_tickets) == num_tickets:
        total_purchase = SavePurchase(purchased_tickets, buyer_name, buyer_gender)  # Purchase registration and total obtained
        if total_purchase is not None:
            print(f"Purchase successful. Total tickets: {num_tickets}. Total purchase: {total_purchase} colones.")
        else:
            print("Error processing the purchase. Please try again later.")
        input("Press enter to continue...")
    else:
        print("The purchase was canceled due to occupied seats.")
        input("Press enter to continue...")

# Function to calculate total income
def CalculateTotalIncome():
    total_income = sum([len(buyer['seats_purchased']) for buyer in buyers])
    return total_income

# Function to load seat status from JSON file
def LoadSeatStatus():
    try:
        with open("sales_report.json", "r") as f:
            try:
                purchases = json.load(f)
                if purchases:  # Check if there is data in the file
                    for buyer in purchases:
                        for purchased_seat in buyer["seats_purchased"]:
                            row = int(purchased_seat["seat"][0]) - 1
                            column = ord(purchased_seat["seat"][1].upper()) - ord('A')
                            cancha[row][column] = Fore.BLUE + 'X' + Style.RESET_ALL
                else:
                    print("The sales_report.json file is empty.")
            except json.decoder.JSONDecodeError:
                print("The sales_report.json file is empty or does not contain valid JSON format.")
    except FileNotFoundError:
        pass

def PrintSalesReport():
    print("\nSales Report")

    # Initialize counters
    male_tickets_sold = 0
    female_tickets_sold = 0
    total_income = 0

    # Print details of each purchase
    for buyer in buyers:
        print(f"Buyer: {buyer['name']} - ID Number: {buyer['id_number']} - Gender: {buyer['gender']}")
        print("Purchase details:")
        for seat in buyer["seats_purchased"]:
            seat_number = ''.join(map(str, seat['seat']))  # Convert seat to string format
            print(f"Seat: {seat_number} - Price: {seat['price']} colones")
            total_income += seat['price']  # Accumulate total income
        if buyer['gender'] == 'M':
            male_tickets_sold += len(buyer['seats_purchased'])
        elif buyer['gender'] == 'F':
            female_tickets_sold += len(buyer['seats_purchased'])

    # Print summary
    total_tickets_sold = male_tickets_sold + female_tickets_sold
    print(f"Total tickets sold: {total_tickets_sold}")
    print(f"Total tickets sold to males: {male_tickets_sold}")
    print(f"Total tickets sold to females: {female_tickets_sold}")
    print(f"Total income: {total_income} colones")

    # Save the report to a JSON file
    with open("sales_report.json", "w") as f:
        json.dump(buyers, f, indent=4)


# Main app
CreateField()
LoadSeatStatus()

while True:
    os.system('cls')  # Clear the console
    print("--------------------------------------------------")
    print("Welcome to the seating management system for football matches".center(50))
    print("--------------------------------------------------")
    print("1. View stadium and seat prices \n"
          + "2. Spectator registration \n"
          + "3. Purchase tickets \n"
          + "4. Sales Report \n"
          + "5. Exit")
    print("-------------------------------------------------")

    choice = input("Select an option: ")

    if choice == '1':
        os.system('cls')
        print("-----------------------------------------")
        print("Welcome to the purchasing module".center(40))
        print("-----------------------------------------")
        print("AVAILABLE SEATS".center(40))
        print("Tip: Sits with an Red X are occupied".center(40))
        print("-----------------------------------------")
        ShowField()
        ShowSeatPrices()  # Show seat prices
        print("Tip: Sits with a red X are occupied".center(40))
        print("-----------------------------------------")
        input("Press enter to continue...")

    elif choice == '2':
        os.system('cls')
        SpectatorRegistration()

    elif choice == '3':
        os.system('cls')
        PurchaseTickets()

    elif choice == '4':
        os.system('cls')
        PrintSalesReport()
        input("Press enter to continue...")

    elif choice == '5':
        os.system('cls')
        print("System closed...")
        break

    else:
        os.system('cls')
        print("Invalid option")
        