import os
from product_data_generator import ProductLoader
from faker import Faker
from secret_string_generator import SecretGenerator

data_dir = 'data'

if not os.path.exists(data_dir):
    os.makedirs(data_dir)

order_file = os.path.join(data_dir, 'orders.jsonl')
merchants_file = os.path.join(data_dir, 'merchants.jsonl')
transactions_file = os.path.join(data_dir, 'transactions.jsonl')
payment_links_file = os.path.join(data_dir, 'payment_links.jsonl')
fake_dates_file = os.path.join(data_dir, 'fake-dates.txt')

city_populations = {
    "New Delhi": 16314838,
    "Mumbai": 18414288,
    "Kolkata": 4496694,
    "Chennai": 8696010,
    "Bengaluru": 8499399,
    "Ahmedabad": 6352254,
    "Hyderabad": 8499399
}

cities = list(city_populations.keys())
max_population = max(city_populations.values())
city_weights = [round(city_populations[c]/max_population, 2) for c in cities]


fake = Faker()
product_loader = ProductLoader()

sg = SecretGenerator()

def gen_reference_number(n):
    return sg.generate_secret(n)

