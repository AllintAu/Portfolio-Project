import random 

MAX_LINES = 3
MAX_BET = 1000
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

def check_winnings(columns, lines, bet, values): #columns is a list of lists represent symbol, values is a dictionary where symbol is a key  
    winnings = 0 #initialize total won amount to 0 and an empty list to keep tracking of winning value
    winning_lines = [] 
    for line in range(lines):
        symbol = columns[0][line]
        for column in columns:
            symbol_to_check = column[line]
            if symbol != symbol_to_check:
                break
        else:
            winnings += values[symbol] * bet
            winning_lines.append(line + 1)

    return winnings, winning_lines

def get_slot_machine_spin(rows, cols, symbols): # rows is the number of rows in slot machine, cols is a column for slot machine
    all_symbol = [] #create a list containing symbol based on it count specified in symbols dictionary
    for symbol, symbol_count in symbols.items(): 
        for _ in range(symbol_count):
            all_symbol.append(symbol) # append use for adding value or object in to a list 

    columns = []
    for _ in range(cols): #generate numbers of column, for each column randomly sekect symbol from all_symbol
        column = []
        current_symbol = all_symbol[:] #[:] use to copy object in this function is copy of a list
        for _ in range(rows):
            value = random.choice(current_symbol)
            current_symbol.remove(value) 
            column.append(value) # append use for adding value or object in to a list 
        columns.append(column) 

    return columns

def print_slot_machine(columns): # columns is a list that representing the symbol in slot machine 
    for row in range(len(columns[0])):
        for i, column in enumerate(columns):
            if i != len(columns) - 1:
                print(column[row],end=" | ") # print | as a separator but not at the last column
            else:
                print(column[row], end="")
        
        print()


def deposit():
    while True:
        amount = input("How much would you like to deposit? $")
        if amount.isdigit(): # isdigit use to check that input value is a number (not a digit)
            amount = int(amount)
            if amount > 0:
                break
            else:
                print("Amount must be greater than 0.")
        else:
            print("Please enter a number.")

    return amount

def get_number_of_line():
    while True:
        lines = input(
            "Enter the number of lines to bet on (1-" + str(MAX_LINES) + ")? ")
        if lines.isdigit(): # isdigit use to check that input value is a number (not a digit)
            lines = int(lines)
            if 1 <= lines <= MAX_LINES:
                break
            else:
                print("Enter a valid number of lines.")
        else:
            print("Please enter a number.")

    return lines

def get_bet():
    while True:
        amount = input("How much would you like to bet on each line? $")
        if amount.isdigit(): 
            amount = int(amount)
            if MIN_BET <= amount <= MAX_BET:
                break
            else:
                print(f"amount must be between ${MIN_BET} - ${MAX_BET}")
        else:
            print("Please enter a number.")

    return amount    

def deposit(balance):
    deposit_amount = int(input("Enter the amount that you wish to deposit. $"))
    new_balance = balance + deposit_amount
    print(f"Deposit of ${deposit_amount} successful. Your new balance is ${new_balance}.")
    return new_balance

def main():
    balance = 0 # Initiallize balance to 0 
    balance = deposit(balance) # Pass the initialize balance to deposit function
    while True:
        lines = get_number_of_line()
        bet = get_bet()
        total_bet = bet * lines
    
        print(f"You are betting ${bet} on {lines}. Total bet is equal to: ${total_bet}")
        slots = get_slot_machine_spin(ROWS, COLS, symbol_count)
        print_slot_machine(slots)
        winnings, winning_lines = check_winnings(slots, lines, bet, symbol_value)

        #display winnings and update balance 
        if winnings > 0:
            print(f"You won ${winnings}.")
            print(f"You won on line number", *winning_lines) #asterisk act as unpack operator, it's gonna pass the value from row 126 winning_lines in it
            balance += winnings
        else:
            print("There's no winning lines. keep going dude!")
            balance -= total_bet
        
        print(f"Your current balance is {balance}")

            #continue playing
        continue_play = input("Press enter to spin next round (q to quit) (d to make deposit).")
        if continue_play.lower() == "d":
            balance = deposit(balance) #Update the balance when returned value from deposit()
        elif continue_play.lower() == "q":
            print("Thank you for your money, see you next time!!")
            break
main()
