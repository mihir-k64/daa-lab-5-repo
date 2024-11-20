# Example of fractional_knapsack function
def fractional_knapsack(capacity, items):
    if capacity <= 0:
        raise ValueError("Capacity of the knapsack must be greater than zero.")
    if len(items) == 0:
        raise ValueError("Item list cannot be empty.")
    
    total_value = 0  # Total value accumulated
    current_weight = 0  # Current weight of the knapsack
    
    for item in items:
        if current_weight + item.weight <= capacity:
            # Take the whole item
            current_weight += item.weight
            total_value += item.value
        else:
            # Take fraction of the item
            remaining_capacity = capacity - current_weight
            fraction = remaining_capacity / item.weight
            total_value += item.value * fraction
            break  # Knapsack is full
    
    return total_value


# Code for Item class and test cases
class Item:
    def __init__(self, weight, value, shelf_life):
        self.weight = weight
        self.value = value
        self.shelf_life = shelf_life

    # Check for validity
    def validate(self):
        errors = []
        if not isinstance(self.weight, (int, float)) or isinstance(self.weight, bool):
            errors.append(f"Invalid weight: {self.weight}. Weight must be a numeric value.")
        elif self.weight <= 0:
            errors.append(f"Invalid weight: {self.weight}. Weight must be greater than zero.")
        if self.value < 0:
            errors.append(f"Invalid value: {self.value}. Value cannot be negative.")
        if self.shelf_life <= 0:
            errors.append(f"Invalid shelf life: {self.shelf_life}. Shelf life must be greater than zero.")
        return errors


# Function to validate and display errors for each item
def validate_items(items):
    for idx, item in enumerate(items):
        errors = item.validate()
        if errors:
            print(f"Item {idx + 1}:")
            for error in errors:
                print(f"  - {error}")
        else:
            print(f"Item {idx + 1}: Valid")


# Negative Test Cases
print("Negative Test Cases\n")

# Test Case 1: Negative values
items_with_errors_1 = [
    Item(5, -10, 3),       
    Item(10, -20, 4),      
    Item(15, -30, 5),      
    Item(20, -40, 6),      
]

# Test Case 2: Negative weight
items_with_errors_2 = [
    Item(-5, 10, 3),       
    Item(-10, 20, 4),      
    Item(-15, 30, 5),      
    Item(-20, 40, 6),      
]

# Test Case 3: Empty knapsack capacity
try:
    print("\nTest Case 3: Empty knapsack capacity")
    fractional_knapsack(0, items_with_errors_1)  
except ValueError as e:
    print(f"Error: {e}")

# Test Case 4: String in weight
items_with_errors_3 = [
    Item("five", 10, 3),    
    Item("ten", 20, 4),     
    Item("fifteen", 30, 5), 
    Item("twenty", 40, 6),  
]

# Test Case 5: All items with 0 weight
items_with_errors_4 = [
    Item(0, 10, 3),    
    Item(0, 20, 4),     
    Item(0, 30, 5), 
    Item(0, 40, 6),  
]

# Run validation for all cases
print("\nTest Case 1: Negative values")
validate_items(items_with_errors_1)

print("\nTest Case 2: Negative weight")
validate_items(items_with_errors_2)

print("\nTest Case 4: String in weight")
validate_items(items_with_errors_3)

print("\nTest Case 5: All items with 0 weight")
validate_items(items_with_errors_4)
