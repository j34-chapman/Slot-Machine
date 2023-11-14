
# Global constant never changes declared at the top with capitals
MAX_LINES = 3
MAX_BET = 100
MIN_BET = 1

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
                print (f"Amount must be between £{MIN_BET} - £{MAX_BET}.")
        else:
            print("Enter a number")

    return amount


def main():
    balance = deposit()
    lines = get_number_of_lines()
    bet = get_bet()
    print(balance,lines)

main()