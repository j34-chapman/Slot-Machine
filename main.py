import random
# Global constant never changes declared at the top with capitals
MAX_LINES = 3
MAX_BET = 100
MIN_BET = 1

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

def check_winnings(columns, lines, bet, values):
    winnings = 0
    winning_lines = []
    for line in range(lines):
        symbol = columns[0][line]
        for column in columns:
            symbol_to_check = column[line]
            if symbol != symbol_to_check:
                break
        else:
            winnings += values[symbol] * bet
            winning_lines.append(line +1 )
            
    return winnings , winning_lines



# Function to simulate a slot machine spin
def get_slot_machine_spin(rows, cols, symbols):
    all_symbols = []

    #  Iterate over each symbol and its count in the symbols dictionary 
    #    Key         Value    in   dictionary.symbols
    for symbol, symbol_quantity in symbols.items():
        for _ in range(symbol_quantity):
            all_symbols.append(symbol)

    # Initialize a list to store columns in the slot machine
    columns = []
    for _ in range(cols):
        column = []
        current_symbols = all_symbols[:] # This makes a copy
        for _ in range(rows):
            # Choose a random symbol from the current_symbols list
            value = random.choice(current_symbols)
            
            # Remove the chosen symbol from the current_symbols list to avoid repetition
            current_symbols.remove(value)
            column.append(value)
        columns.append(column)
    return columns

def print_slot_machine (columns):
    for row in range(len(columns[0])):
        for i, column in enumerate(columns):
            if i !=len(columns) - 1:
                print(column[row] , end=" | ")
            else:
                print(column[row], end = "")
                
        print()


def deposit():
    while True :
         # this is like using a scanner
        amount = input ("What would you like to deposit? £")

        # if its valid digit , is it greater than 0 , must be greater than 0 
        if amount.isdigit():
            # conver string to digit (amount)
            amount = int (amount) 
            if amount > 0:
                break
            else:
                print ("Amount must be be greater than 0")
                break
        else:
            print("Enter a number")

    return amount


def get_number_of_lines():
    while True :
         # Ive casacaded the variable value to be included in the scanner question - quite powerful
        lines = input ("Enter number of lines to bet on (1-" + str(MAX_LINES) + ")? ")

        if lines.isdigit():
            lines= int (lines) 
            # if lines is greater than and equal to 1 and less than or equal to MAX_LINES , break
            if 1 <= lines <= MAX_LINES:
                break
            else:
                print ("Enter a valid number of lines")
        else:
            print("Enter a number")

    return lines


def get_bet():
    while True :
        amount = input ("What would you like to bet on each line? £")

        if amount.isdigit():
            amount = int (amount) 
            if MIN_BET <= amount <= MAX_BET:
                break
            else:
                print (f"Amount must be between £{MIN_BET} - £{MAX_BET}.") # Another way but cleaner than ln 29
        else:
            print("Enter a number")

    return amount


    
def spin(balance):
    lines = get_number_of_lines()
    while True:
        bet = get_bet()
        total_bet = bet * lines

        if total_bet > balance:
            print(
                f"You do not have enough to bet that amount, your current balance is: £{balance}")
        else:
            break

    print(
        f"You are betting £{bet} on {lines} lines. Total bet is equal to: £{total_bet}")

    slots = get_slot_machine_spin(ROWS, COLS, symbol_count)
    print_slot_machine(slots)
    winnings, winning_lines = check_winnings(slots, lines, bet, symbol_value)
    print(f"You won ${winnings}.")
    print(f"You won on lines:", *winning_lines)
    return winnings - total_bet



def main():
    balance = deposit()
    while True:
        print(f"Current balance is £{balance}")
        answer = input("Press enter to play (q to quit).")
        if answer == "q":
            break
        balance += spin(balance)

    print(f"You left with £{balance}")


main()

