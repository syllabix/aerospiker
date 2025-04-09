# Aerospiker

A benchmarking and testing suite for Aerospike, featuring multiple client implementations in Rust, Go, and Python.

## Overview

Aerospiker is a barebones toolkit for testing and benchmarking Aerospike database performance. It includes:

- Multiple client implementations (Rust, Go)
- Benchmarking tools
- Data loading utilities
- Development environment setup

## Prerequisites

- Docker and Docker Compose
- Rust
- Go
- Python (with uv package manager)
- oha (for benchmarking)

## Quick Start

1. Install dependencies:
```bash
make deps
```

2. Start the development environment:
```bash
make devenv.start
```

3. Load test data:
```bash
make testdata
```

4. Run benchmarks:
```bash
make benchmark
```

## Project Structure

- `aerospike-conf/` - Aerospike configuration files
- `aerospike-data/` - Persistent data storage
- `benchmark/` - Benchmarking tools and configurations
- `gopsike/` - Go implementation
- `loader/` - Data loading utilities
- `pyspike/` - Python implementation (pending)
- `rspike/` - Rust implementation

## Available Commands

- `make deps` - Install all required dependencies
- `make devenv.start` - Start the development environment
- `make devenv.stop` - Stop the development environment
- `make testdata` - Load test data and generate URLs
- `make urls` - Generate URLs for benchmarking
- `make gopsike.run` - Run the Go implementation
- `make rspike.run` - Run the Rust implementation
- `make benchmark` - Run the benchmark suite

## Development

The project uses Docker Compose for the Aerospike server setup. The default configuration includes:
- Client port: 3000
- Fabric port: 3001
- Mesh port: 3002
- Info port: 3003

## License

This project is released into the public domain under the Unlicense. See the [LICENSE](LICENSE) file for details. 