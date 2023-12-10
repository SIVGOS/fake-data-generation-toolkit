from sequential_datagen import check_existing_files, generate_order_data
from gen_fake_timestamps import generate_fake_dates
import argparse
from datetime import datetime, date, timedelta

def parse_arguments():
    yesterday = date.today() - timedelta(days=1)

    parser = argparse.ArgumentParser(description='Command line parser for trans and dates commands.')

    parser.add_argument('cmd', choices=['transactions', 'dates'], default='transactions', nargs='?',
                        help='Specify the command to execute. Default is trans.')

    parser.add_argument('--start-date', default='2021-01-01', type=lambda s: datetime.strptime(s, '%Y-%m-%d').date(),
                        help='Specify the start date in the format YYYY-MM-DD. Default is 2022-01-01.')

    parser.add_argument('--end-date', default=str(yesterday), type=lambda s: datetime.strptime(s, '%Y-%m-%d').date(),
                        help='Specify the end date in the format YYYY-MM-DD. Default is the yesterday.')
    parser.add_argument('-mc', '--daily-max-entries-per-merchant', default=10, type=int, 
                        help='Specify the maximum number of entries per day per merchant.')
    parser.add_argument('-mm', '--max-merchant-count', default=10, type=int,
                        help='Specify the maximum number of merchants to be created.')
    parser.add_argument('-em', '--existing-merchants-count', default=3, type=int,
                        help='Specify the number of existing stores.')

    args = parser.parse_args()
    return args

if __name__ == '__main__':
    args = parse_arguments()

    if args.cmd is None:
        print("No command provided. Use --help or -h for more information.")
        exit(0)

    if args.cmd == 'transactions':
        if check_existing_files():
            generate_order_data(args.start_date, args.end_date, args.max_merchant_count, 
                                args.daily_max_entries_per_merchant, args.existing_merchants_count)
    
    if args.cmd == 'dates':
        generate_fake_dates(args.start_date, args.end_date, args.daily_max_entries_per_merchant)
