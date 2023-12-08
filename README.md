# Fake Commerce Data Generator

## Overview
This is a Python script for generating fake transaction data for testing and development purposes. The script simulates the generation of orders, merchants, payment links, and transactions, populating corresponding JSON files with realistic-looking data.

## Prerequisites
Make sure you have Python installed on your machine. Additionally, the script relies on the following external libraries:
- `shutil`
- `os`
- `json`
- `uuid`
- `random`
- `datetime`

You can install these dependencies using the following command:
```bash
pip install faker
```

## Usage
1. Clone this repository to your local machine.
2. Open a terminal and navigate to the project directory.
3. Run the script by executing the following command:
   ```bash
   python fake_data_generator.py
   ```
4. Follow the prompts to confirm if you want to delete existing data files and create new ones.

## Data Files
The script generates the following data files in the 'data' directory:

1. `orders.json`: Contains information about generated orders.
2. `merchants.json`: Contains information about generated merchants.
3. `payment_links.json`: Contains information about generated payment links.
4. `transactions.json`: Contains information about generated transactions.

## Customization
You can customize the script by modifying the `config.py` file, where you can adjust various parameters such as city weights, product categories, and payment methods.

## Important Note
This script is intended for testing and development purposes only. The generated data is entirely fictional and should not be used for any real-world transactions or analyses. 

## Disclaimer
The script uses the [Faker](https://faker.readthedocs.io/en/master/) library to generate realistic-looking fake data. Faker is a Python library that helps you generate fake data such as names, addresses, countries, and more.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
