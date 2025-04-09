import csv
import random
import string
import uuid

def generate_random_string(length=10):
    """Generate a random string of specified length."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def generate_random_value():
    """Generate a random value that could be a string, number, or boolean."""
    value_type = random.choice(['string', 'number', 'boolean'])
    if value_type == 'string':
        return generate_random_string()
    elif value_type == 'number':
        return str(random.randint(1, 1000000))
    else:
        return str(random.choice([True, False]))

# Create the CSV file
with open('loader/base_data.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    # Write header
    writer.writerow(['set', 'key', 'name', 'value'])
    
    # Generate 100,000 rows
    for i in range(100000):
        # Alternate between 10 sets
        set_name = f'spike_{(i % 10) + 1}'
        # Generate random key (UUID)
        key = str(uuid.uuid4())
        # Generate random name
        name = generate_random_string(8)
        # Generate random value
        value = generate_random_value()
        
        writer.writerow([set_name, key, name, value])

print("CSV file has been generated successfully!") 