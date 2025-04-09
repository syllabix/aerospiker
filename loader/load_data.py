import csv
import aerospike
from tqdm import tqdm
import sys
from typing import Dict, Any

def connect_to_aerospike() -> aerospike.Client:
    """Establish connection to Aerospike."""
    config = {
        'hosts': [('localhost', 3000)]
    }
    try:
        client = aerospike.client(config)
        client.connect()
        return client
    except Exception as e:
        print(f"Failed to connect to Aerospike: {e}")
        sys.exit(1)

def create_set(client: aerospike.Client, namespace: str, set_name: str) -> None:
    """Create a set if it doesn't exist."""
    try:
        client.index_string_create(namespace, set_name, 'name', 'name_idx')
    except aerospike.exception.IndexAlreadyExists:
        pass
    except Exception as e:
        print(f"Failed to create index for set {set_name}: {e}")
        sys.exit(1)

def load_data(client: aerospike.Client, csv_path: str, namespace: str = 'test') -> None:
    """Load data from CSV into Aerospike."""
    try:
        with open(csv_path, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            total_rows = sum(1 for _ in open(csv_path)) - 1  # Subtract header row
            
            with tqdm(total=total_rows, desc="Loading data") as pbar:
                for row in reader:
                    set_name = row['set']
                    key = row['key']
                    name = row['name']
                    value = row['value']
                    
                    # Create key tuple
                    key_tuple = (namespace, set_name, key)
                    
                    # Prepare record
                    record = {
                        'name': name,
                        'value': value
                    }
                    
                    try:
                        # Write record
                        client.put(key_tuple, record)
                        pbar.update(1)
                    except Exception as e:
                        print(f"\nError writing record {key}: {e}")
                        continue

    except FileNotFoundError:
        print(f"CSV file not found: {csv_path}")
        sys.exit(1)
    except Exception as e:
        print(f"Error loading data: {e}")
        sys.exit(1)

def main():
    """Main function to load data into Aerospike."""
    csv_path = 'base_data.csv'
    namespace = 'test'
    
    print("Connecting to Aerospike...")
    client = connect_to_aerospike()
    
    print("Loading data...")
    load_data(client, csv_path, namespace)
    
    print("Data loading completed successfully!")

if __name__ == "__main__":
    main() 