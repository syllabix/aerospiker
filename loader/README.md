# Aerospike Data Loader

This project provides tools for loading data into Aerospike.

## Setup

1. Install uv package manager if you haven't already:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

2. Install dependencies using uv:
```bash
uv pip install -r requirements.txt
```

## Usage

1. Generate sample data (if needed):
```bash
python generate_data.py
```

2. Load data into Aerospike:
```bash
python load_data.py
```

## Configuration

The loader is configured to connect to Aerospike at `localhost:3000` by default. The data will be loaded into the `test` namespace.

## Data Structure

The loader expects a CSV file with the following columns:
- set: The Aerospike set name (spike_1 through spike_10)
- key: Unique identifier for the record
- name: Name field for the record
- value: Value field for the record 