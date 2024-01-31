from decimal import MIN_ETINY
import random

# Global constant never changes declared at the top with capitals
ONEPOUND_BET = 1

ROWS = 3
COLS = 3

ROWSLARGE = 5
COLSLARGE = 5

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

symbol_count_large = {
    "A": 16,
    "B": 5,
    "C": 4,
    
}

symbol_value_large = {
    "A": 10,
    "B": 8,
    "C": 6,
    
}

def get_balance(balance):
    return balance

def add_balance(balance, amount):
    return balance + amount

def minus_balance(balance, amount):
    return balance - amount


def generate_random_number():
    return random.randint(1, 100)

# Define a function called "print_slot_machine" that takes in a matrix
def print_slot_machine(columns):
    for row in range(len(columns[0])):
        for i, column in enumerate(columns):
            if i != len(columns) - 1:
                print(column[row], end=" | ")
            else:
                print(column[row], end="")
        print()

def create_symbol_list(symbols):
    all_symbols = [symbol for symbol, symbol_quantity in symbols.items() for _ in range(symbol_quantity)]
    return all_symbols

def create_symbol_grid(rows, cols, symbols):
    all_symbols = create_symbol_list(symbols)
    columns = [[random.choice(all_symbols) for _ in range(rows)] for _ in range(cols)]
    return columns

def get_slot_machine_spin(rows, cols, symbols):
    columns = create_symbol_grid(rows, cols, symbols)
    return columns


# Define a function called "check_winnings" that takes in a matrix, a bet, a symbol count map, and a player
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

# Define a function called "spin" that takes in a balance and returns the winnings, total bet amount, and updated balance
def spin(balance):
    bet = ONEPOUND_BET
    total_bet = bet * 1

    if bet > balance:
        print(f"You do not have enough to bet that amount, your current balance is: £{balance}")
        return 0, bet  # Return 0 as winnings and the total bet amount
    else:
        slots = get_slot_machine_spin(ROWS, COLS, symbol_count)
        print_slot_machine(slots)

        winnings, winning_lines = check_winnings(slots, bet, symbol_value)
        if winnings > 0:
            print(f"You won £{winnings}.")
            balance = add_balance(balance, winnings)  # Add the winnings to the balance
        else:
            print("Sorry, you didn't win this time.")

    return winnings, total_bet, balance

# Define a function called "spinLarge" that takes in a balance and returns the winnings, total bet amount, and updated balance
def spinLarge(balance):
    bet = ONEPOUND_BET
    total_bet = bet * 1

    if bet > balance:
        print(f"You do not have enough to bet that amount, your current balance is: £{balance}")
        return 0, bet  # Return 0 as winnings and the total bet amount
    else:
        slots = get_slot_machine_spin(ROWSLARGE, COLSLARGE, symbol_count_large)
        print_slot_machine(slots)

        winnings, winning_lines = check_winnings(slots, bet, symbol_value_large)
        if winnings > 0:
            print(f"You won £{winnings}.")
            balance = add_balance(balance, winnings)  # Add the winnings to the balance
        else:
            print("Sorry, you didn't win this time.")

    return winnings, total_bet, balance


# Define a function called "get_balance" that takes in a balance
def main():
    balance = 10
    
    while True:
        random_number = generate_random_number()
        
        print(f"Current balance is £{get_balance(balance)}")
        answer = input("Press Spin to Play or Exit to Collect Winnings (s to spin, e to exit): ")
        if answer.lower() == "e":
            break
        elif answer.lower() == "s":
            if random_number < 50:
                winnings, total_bet, balance = spin(balance)
            else:
                winnings, total_bet, balance = spinLarge(balance)

            if winnings == 0:
                balance = minus_balance(balance, total_bet)  # Deduct the total bet amount only if the user exits without winning
        else:
            print("Invalid choice. Press Enter to play, 's' to spin again, or 'e' to exit.")

    print(f"You left with £{get_balance(balance)}")

main()
