import os
import sqlalchemy as sa
from sqlalchemy.orm import declarative_base, relationship
from dotenv import load_dotenv

if os.path.exists('.env'):
    load_dotenv()

payment_links_table = 'payment_links'
transactions_table = 'payment_transactions'

Base = declarative_base()

class PaymentLink(Base):
    __tablename__ = payment_links_table

    link_id = sa.Column(sa.Integer, primary_key=True)
    merchant_id = sa.Column(sa.Integer)
    amount = sa.Column(sa.Float)
    expiry_date = sa.Column(sa.DateTime)
    payment_reference_number = sa.Column(sa.String(32))
    status = sa.Column(sa.String(16))
    callback_url = sa.Column(sa.String(128))
    created_on = sa.Column(sa.DateTime)

class Transaction(Base):
    __tablename__ = transactions_table

    transaction_id = sa.Column(sa.Integer, primary_key=True)
    link_id = sa.Column(sa.Integer, sa.ForeignKey(PaymentLink.link_id))
    payment_method = sa.Column(sa.String(32))
    status = sa.Column(sa.String(16))
    transaction_time = sa.Column(sa.DateTime)

    payment_link = relationship(PaymentLink, back_populates="transactions")

# Create the tables in the database

mysql_url = sa.engine.URL.create(
    drivername='mysql',
    username=os.getenv('MS_DB_USER'),
    password=os.getenv('MS_DB_PASS'),
    host=os.getenv('MS_DB_HOST'),
    port=os.getenv('MS_DB_PORT'),
    database=os.getenv('MS_DB_NAME')
)
mysql_engine = sa.create_engine(mysql_url)
Base.metadata.drop_all(mysql_engine)
Base.metadata.create_all(mysql_engine)

