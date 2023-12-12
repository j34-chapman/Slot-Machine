from decimal import MIN_ETINY
import random

# Global constant never changes declared at the top with capitals
MAX_LINES = 3
TWOPOUND_BET = 2
ONEPOUND_BET = 1
FIFTYP_BET = 0.5
TWENTYP_BET = 0.25
MAX_DEPOSIT = 50

ROWS = 3
COLS = 3

symbol_count = {
    "A": 2,
    "B": 4,
    "C": 6,
    "D": 8
}

symbol_value = {
    "A": 5,
    "B": 4,
    "C": 3,
    "D": 2
}

def check_winnings(columns, bet, values):
    winnings = 0
    winning_lines = []

    # Get the symbols in the middle row of each column
    middle_row_symbols = [column[len(column)//2] for column in columns]

    # Check if all symbols in the middle row are the same
    if len(set(middle_row_symbols)) == 1:
        symbol = middle_row_symbols[0]
        winnings += values[symbol] * bet
        winning_lines.append(len(columns)//2 + 1)

    return winnings, winning_lines

# Function to simulate a slot machine spin
def get_slot_machine_spin(rows, cols, symbols):
    all_symbols = []

    # Iterate over each symbol and its count in the symbols dictionary
    for symbol, symbol_quantity in symbols.items():
        for _ in range(symbol_quantity):
            all_symbols.append(symbol)

    # Initialize a list to store columns in the slot machine
    columns = []
    for _ in range(cols):
        column = []
        current_symbols = all_symbols[:]
        for _ in range(rows):
            value = random.choice(current_symbols)
            current_symbols.remove(value)
            column.append(value)
        columns.append(column)
    return columns

def print_slot_machine(columns):
    for row in range(len(columns[0])):
        for i, column in enumerate(columns):
            if i != len(columns) - 1:
                print(column[row], end=" | ")
            else:
                print(column[row], end="")
        print()

def deposit():
    while True:
        amount = input(f"What would you like to deposit? (Max Deposit : £{MAX_DEPOSIT})  : £ ")

        if amount.isdigit():
            amount = int(amount)
            if 0 < amount <= MAX_DEPOSIT:
                break
            else:
                print(f"Amount must be greater than 0 and no larger than £{MAX_DEPOSIT}")
                break
        else:
            print("Enter a number")

    return amount

def get_bet():
    while True:
        choice = input("Choose your bet amount: 1 - £0.25, 2 - £0.50, 3 - £1, 4 - £2: ")

        if choice.isdigit():
            choice = int(choice)
            if 1 <= choice <= 4:
                amount = [TWENTYP_BET, FIFTYP_BET, ONEPOUND_BET, TWOPOUND_BET][choice - 1]
                break
            else:
                print("Enter a valid choice (1, 2, 3, or 4).")
        else:
            print("Enter a valid choice (1, 2, 3, or 4).")

    return amount

def nudge_columns(columns, balance, bet):
    nudge_count = 0
    winnings = 0

    while nudge_count < 2:
        nudge_choice = input(
            f"Choose a column to nudge (1, 2, or 3) or press Enter to spin again, or 'e' to exit: ")

        if nudge_choice.isdigit():
            nudge_choice = int(nudge_choice)

            if 1 <= nudge_choice <= 3:
                columns[nudge_choice - 1] = get_slot_machine_spin(ROWS, 1, symbol_count)[0]
                nudge_count += 1
                print_slot_machine(columns)

                winnings, winning_lines = check_winnings(columns, bet, symbol_value)
                if winnings > 0:
                    print(f"You won £{winnings}.")
                    print("You won on lines:", *winning_lines)
                    balance += winnings
                else:
                    print("Sorry, you didn't win this time.")
            else:
                print("Enter a valid choice (1, 2, or 3).")

        elif nudge_choice == "":
            # Allow for a new spin if Enter is pressed
            columns = get_slot_machine_spin(ROWS, COLS, symbol_count)
            print_slot_machine(columns)

            winnings, winning_lines = check_winnings(columns, bet, symbol_value)
            if winnings > 0:
                print(f"You won £{winnings}.")
                balance += winnings
            else:
                print("Sorry, you didn't win this time.")
            break

        elif nudge_choice.lower() == "e":
            return None

        else:
            print("Enter a valid choice (1, 2, or 3) or press Enter to spin again, or 'e' to exit.")

    print("You have nudged twice. Press Enter to spin again, or 'e' to exit.")
    while True:
        choice = input()
        if choice == "":
            columns = get_slot_machine_spin(ROWS, COLS, symbol_count)
            print_slot_machine(columns)

            winnings, winning_lines = check_winnings(columns, bet, symbol_value)
            if winnings > 0:
                print(f"You won £{winnings}.")
                balance += winnings
            else:
                print("Sorry, you didn't win this time.")
            break
        elif choice.lower() == "e":
            return None
        else:
            print("Invalid choice. Press Enter to spin again or 'e' to exit.")

    return columns



def spin(balance):
    bet = get_bet()
    total_bet = bet * 1

    if total_bet > balance:
        print(f"You do not have enough to bet that amount, your current balance is: £{balance}")
        return 0, total_bet  # Return 0 as winnings and the total bet amount
    else:
        print(f"You are betting £{bet} on 1 line. Total bet is equal to: £{total_bet}")

    slots = get_slot_machine_spin(ROWS, COLS, symbol_count)
    print_slot_machine(slots)

    winnings, winning_lines = check_winnings(slots, bet, symbol_value)
    if winnings > 0:
        print(f"You won £{winnings}.")
        balance += winnings  # Add the winnings to the balance
    else:
        print("Sorry, you didn't win this time.")

    # Deduct the total bet amount from the balance
    balance -= total_bet

    while True:
        choice = input("Choose a column to nudge (1, 2, or 3) or press Enter to spin again, or 'e' to exit: ")
        if choice == "":
            return winnings, total_bet
        elif choice.lower() == "e":
            return winnings, total_bet
        elif choice.isdigit():
            column = int(choice)
            if 1 <= column <= 3:
                slots[column - 1] = get_slot_machine_spin(ROWS, 1, symbol_count)[0]
                print_slot_machine(slots)

                winnings, winning_lines = check_winnings(slots, bet, symbol_value)
                if winnings > 0:
                    print(f"You won £{winnings}.")
                    balance += winnings
                else:
                    print("Sorry, you didn't win this time.")
            else:
                print("Enter a valid choice (1, 2, or 3).")
        else:
            print("Enter a valid choice (1, 2, or 3) or press Enter to spin again, or 'e' to exit.")

def main():
    balance = deposit()
    while True:
        print(f"Current balance is £{balance}")
        answer = input("Press Spin to Play or Exit to Collect Winnings (s to spin again, e to exit): ")
        if answer.lower() == "e":
            break
        elif answer.lower() == "s" or answer == "":
            winnings, total_bet = spin(balance)
            balance += winnings - total_bet  # Deduct the total bet amount only if the user exits without winning
        else:
            print("Invalid choice. Press Enter to play, 's' to spin again, or 'e' to exit.")

    print(f"You left with £{balance}")

main()


