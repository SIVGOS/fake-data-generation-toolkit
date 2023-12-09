import os, json
import sqlalchemy as sa
import pandas as pd
from dotenv import load_dotenv
from config import merchants_file, order_file, payment_links_file, transactions_file

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

def push_file_to_dataframe(jsonl_file_path, table_name, connection_string):
    if not os.path.exists(jsonl_file_path):
        raise FileNotFoundError(jsonl_file_path)
    
    engine = sa.create_engine(connection_string)
    batches = read_jsonl_in_batches(jsonl_file_path)
    push_batches_to_database(batches, table_name, engine)


if __name__=='__main__':
    postgres_url = sa.engine.URL.create(
        drivername='postgresql',
        username=os.getenv('PG_DB_USER'),
        password=os.getenv('PG_DB_PASS'),
        host=os.getenv('PG_DB_HOST'),
        port=os.getenv('PG_DB_PORT'),
        database=os.getenv('PG_DB_NAME')
    )

    mysql_url = sa.engine.URL.create(
        drivername='mysql',
        username=os.getenv('MS_DB_USER'),
        password=os.getenv('MS_DB_PASS'),
        host=os.getenv('MS_DB_HOST'),
        port=os.getenv('MS_DB_PORT'),
        database=os.getenv('MS_DB_NAME')
    )

    push_file_to_dataframe(merchants_file, 'merchants', postgres_url)
    push_file_to_dataframe(order_file, 'orders', postgres_url)
    push_file_to_dataframe(payment_links_file, 'payment_links', mysql_url)
    push_file_to_dataframe(transactions_file, 'payment_transactions', mysql_url)

