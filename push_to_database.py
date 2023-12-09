import os, json
import pandas as pd
from dotenv import load_dotenv
from config import merchants_file, order_file, payment_links_file, transactions_file
from migrations_mysql import mysql_engine, payment_links_table, transactions_table
from migrations_postgresql import postgres_engine, merchants_table, order_table

if os.path.exists('.env'):
    load_dotenv()

sql_load_batch_size = int(os.getenv('SQL_LOAD_BATCH_SIZE', '5000'))

def read_jsonl_in_batches(file_path, batch_size=sql_load_batch_size):
    with open(file_path, 'r') as file:
        batch = []
        for line in file:
            data = json.loads(line)
            batch.append(data)

            if len(batch) == batch_size:
                yield batch
                batch = []

        # Yield the last batch (if any)
        if batch:
            yield batch

def push_batches_to_database(batches, table_name, engine):
    for i, batch in enumerate(batches, start=1):
        df = pd.DataFrame(batch)
        df.to_sql(table_name, con=engine, if_exists='append', index=False)

        print(f"Batch {i} pushed to the table {table_name}.")

def push_file_to_dataframe(jsonl_file_path, table_name, engine):
    if not os.path.exists(jsonl_file_path):
        raise FileNotFoundError(jsonl_file_path)

    batches = read_jsonl_in_batches(jsonl_file_path)
    push_batches_to_database(batches, table_name, engine)


if __name__=='__main__':
    push_file_to_dataframe(merchants_file, merchants_table, postgres_engine)
    push_file_to_dataframe(order_file, order_table, postgres_engine)
    push_file_to_dataframe(payment_links_file, payment_links_table, mysql_engine)
    push_file_to_dataframe(transactions_file, transactions_table, mysql_engine)

