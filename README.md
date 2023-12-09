# Data Generation Toolkit

This repository contains a set of Python scripts for generating synthetic data related to e-commerce transactions. The data includes information about merchants, orders, payment links, and transactions. The generated data can be useful for testing and development purposes.

## Files

### 1. `product_data_generator.py`

This script defines a `ProductLoader` class, which is responsible for loading product data and selecting random products and categories.

### 2. `sequential_datagen.py`

The `sequential_datagen.py` script generates sequential data for merchants, payment links, transactions, and orders. It utilizes fake data and the `ProductLoader` from `product_data_generator.py` to create a realistic dataset. The output data is stored in JSON Lines (JSONL) format, where each line is a perfect JSON, facilitating easy creation and loading without consuming excessive memory.

### 3. `secret_string_generator.py`

This script defines a `SecretGenerator` class for generating random secret strings, which are used as payment reference numbers.

### 4. `main.py`

The `main.py` script serves as the entry point for the data generation process. It provides a command-line interface for specifying the type of data to generate, start and end dates, and other parameters.

### 5. `config.py`

The `config.py` file contains configuration settings, including file paths, city populations, and weights. It imports the `ProductLoader` and `SecretGenerator` for data generation.

### 6. `gen_fake_timestamps.py`

This script generates fake timestamps based on predefined weights for hours and weekdays. It is used in the data generation process to create realistic timestamped data.

### 7. `push_to_database.py`

The `push_to_database.py` script is an optional utility for pushing the generated JSONL data into a database. It supports PostgreSQL and MySQL databases, allowing users to easily transfer the generated data for further analysis or application testing.

## Usage

To generate data, run the `main.py` script with appropriate command-line arguments. For example:

```bash
python main.py transactions --start-date 2022-01-01 --end-date 2023-12-31 -m 1000
```

This command generates transaction data for the specified date range with a maximum of 1000 entries per day.

To push the generated data to a database, use the `push_to_database.py` script. Update the script with your database connection details and run:

```bash
python push_to_database.py
```

Ensure that the required dependencies are installed before running the scripts.

Feel free to explore and modify the scripts based on your specific requirements.
