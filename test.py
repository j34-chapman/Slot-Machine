def fruit():
    # Define a dictionary with fruit names and quantities.
    # Each key is a fruit name, and each value is the quantity.
    my_dict = {"apple": 3, "banana": 5, "orange": 2}

    # Using items() to get an iterable of key-value pairs.
    # Iterate over each key-value pair in the dictionary.
    for fruit, quantity in my_dict.items():
        # Print a message about the quantity of each fruit.
        print(f"I have {quantity} {fruit}s.")

        # Add each fruit to a list based on its quantity.
        fruits_list = []
        for _ in range(quantity):
            fruits_list.append(fruit)

        # Print the list to see the result.
        print(fruits_list)

def main():
    # Call the fruit function
    fruit()

# Run the main function
main()


""" for _ in range(symbol_value):
    all_symbols.append(symbol_key)

This loop is iterating over the range of symbol_value, 
and during each iteration, it appends symbol_key to the all_symbols list.
So, if symbol_value is, for example, 2, it will append symbol_key 
(the fruit name) to all_symbols two times.In your example, if we have two 
apples (symbol_key is "apple" and symbol_value is 2), the loop will run
twice, and after the loop, all_symbols will contain two occurrences of
"apple". So, your understanding is correct. It's a way of adding the symbols
to all_symbols based on their counts specified in the dictionary. 
Each symbol is added to all_symbols as many times as its count (symbol_value).
 """

