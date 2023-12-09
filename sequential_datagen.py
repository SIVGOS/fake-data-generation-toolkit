import os, json, uuid
import random as rd
import datetime as dt
from gen_fake_timestamps import get_weighted_timestamps
from config import (order_file, merchants_file, payment_links_file, transactions_file, cities, city_weights,
                    fake, product_loader, gen_reference_number)

order_counter = 0
merchant_counter = 0
payment_link_counter = 0
transaction_counter = 0


def add_new_merchant(time):
    global merchant_counter
    merchant_counter += 1
    merchant = {
        'merchant_id': merchant_counter,
        'username': fake.unique.user_name(),
        'business_name': fake.company(),
        'email': fake.email(),
        'city': rd.choices(cities, weights=city_weights)[0],
        'phone_number': fake.phone_number(),
        'created_on': time.strftime('%Y-%m-%d %H:%S:%M')
    }
    with open(merchants_file, 'a') as fout:
        fout.write(json.dumps(merchant) + '\n')
    return merchant_counter

def generate_payment_link(time, status, amount, payment_ref_number, merchant_id=None):
    global payment_link_counter
    payment_link_counter += 1
    payment_link = {
        "link_id": payment_link_counter,
        "merchant_id": merchant_id if (merchant_id is not None and isinstance(merchant_id, int)) else rd.randint(1, merchant_counter-1),
        "amount": amount,
        "expiry_date": (time + dt.timedelta(seconds=600)).strftime('%Y-%m-%d %H:%S:%M'),
        "payment_reference_number": payment_ref_number,
        "status": status,
        "callback_url": 'https://pay4u.com/payment/?key=%s' %(str(uuid.uuid4())),
        'created_on': time.strftime('%Y-%m-%d %H:%S:%M')
    }
    with open(payment_links_file, 'a') as fout:
        fout.write(json.dumps(payment_link) + '\n')
    return payment_link_counter

def generate_payment_info(time, payment_link_id, status):
    global transaction_counter
    transaction_counter += 1
    transaction_time = time + dt.timedelta(seconds=rd.randint(60, 599))
    transaction = {
        'transaction_id': transaction_counter,
        'link_id': payment_link_id,
        'payment_method': rd.choice(['Net Banking', 'Credit Card', 'Debit Card', 'UPI']),
        'status': status,
        'transaction_time': transaction_time.strftime('%Y-%m-%d %H:%S:%M')
    }
    with open(transactions_file, 'a') as fout:
        fout.write(json.dumps(transaction)+'\n')

def generate_order(time, merchant_id):
    global order_counter
    order_counter += 1

    payment_method = rd.choice(['CASH', 'ONLINE'])

    if payment_method == 'CASH':
        payment_status = 'SUCCESS'
        payment_ref_number = None
    else:
        payment_status = rd.choices(['SUCCESS', 'EXPIRED', 'FAILED', 'RETRIED'], weights=[0.9, 0.02, 0.05, 0.03])[0]
        payment_ref_number = gen_reference_number(16)

    product_category = product_loader.pick_a_category()
    product_name, product_price = product_loader.pick_a_product(product_category)

    order = {
        'order_id': order_counter,
        'merchant_id': merchant_id,
        'product_category': product_category,
        'product_name': product_name,
        'product_price': product_price,
        'payment_method': payment_method,
        'payment_ref_number': payment_ref_number,
        'payment_status': 'SUCCESS' if payment_status in ('SUCCESS', 'RETRIED') else 'FAILED',
        'created_on': time.strftime('%Y-%m-%d %H:%S:%M')
    }
    with open(order_file, 'a') as fout:
        fout.write(json.dumps(order) + '\n')
    
    return payment_status, product_price, payment_ref_number


def data_generator(ts):
    if merchant_counter < 3 or rd.random() < 0.01:
        add_new_merchant(ts)
        return
    merchant_id=rd.randint(1, merchant_counter)

    payment_status, product_price, payment_ref_number = generate_order(ts, merchant_id)

    if payment_ref_number is None:
        return

    if payment_status in ('SUCCESS', 'FAILED'):
        link_id = generate_payment_link(time=ts, status=payment_status, amount=product_price, payment_ref_number=payment_ref_number, merchant_id=merchant_id)
        generate_payment_info(time=ts+dt.timedelta(seconds=rd.randint(40, 300)),
                              payment_link_id=link_id,
                              status=payment_status)
        return
    if payment_status == 'EXPIRED':
        link_id = generate_payment_link(time=ts, status=payment_status, amount=product_price, payment_ref_number=payment_ref_number, merchant_id=merchant_id)
        return
    
    link_id = generate_payment_link(time=ts, status='SUCCESS', amount=product_price, payment_ref_number=payment_ref_number, merchant_id=merchant_id)

    generate_payment_info(time=ts+dt.timedelta(seconds=rd.randint(40, 200)),
                          payment_link_id=link_id,
                          status='FAILED')
    
    generate_payment_info(time=ts+dt.timedelta(seconds=rd.randint(201, 300)),
                          payment_link_id=link_id,
                          status='SUCCESS')

def generate_order_data(start_date, end_date, max_entries_per_day):
    n_days = (end_date-start_date).days + 1
    for i in range(n_days):
        cur_date = start_date + dt.timedelta(days=i)
        timestamps = get_weighted_timestamps(cur_date, max_entries_per_day)
        n_timestamps = len(timestamps)
        for j, timestamp in enumerate(timestamps):
            data_generator(timestamp)
            print(f'Generating data: day {i} of {n_days}\ttimestamps: {j} of {n_timestamps}')

def check_existing_files():
    output_files = [order_file, merchants_file, transactions_file, payment_links_file]
    existing_files = [f for f in output_files if os.path.exists(f)]
    if existing_files:
        opt = input('Are you sure that you want to delete existing files and create new ones? Y/N')
        if opt.lower()!='y':
            return False
    for f in existing_files:
        os.remove(f)

    return True    

if __name__=='__main__':
    start_date = dt.date(2021,1,1)
    end_date = dt.date.today() - dt.timedelta(days=1)
    if check_existing_files():
        generate_order_data(start_date, end_date, 20)

