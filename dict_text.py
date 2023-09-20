# Sample dictionary
my_dict = {'a': "ADAM", 'b': 20, 'c': 30, 'd': 40}

# Define a predicate function
def my_predicate(key, value):
    return key == 'a'  # For example, we want to update the value associated with key 'b'

# Update values based on the predicate using a dictionary comprehension
new_value = "foo"
my_dict = {key: (value.lower() if my_predicate(key, value) else value) for key, value in my_dict.items()}


# Print the updated dictionary
print(my_dict)
