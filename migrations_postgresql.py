import os
import sqlalchemy as sa
from sqlalchemy.orm import declarative_base, relationship
from dotenv import load_dotenv

if os.path.exists('.env'):
    load_dotenv()

merchants_table = 'merchant'
order_table = 'order'

Base = declarative_base()

class Merchant(Base):
    __tablename__ = merchants_table
    merchant_id = sa.Column(sa.Integer, primary_key=True)
    username = sa.Column(sa.String(32), nullable=False)
    business_name = sa.Column(sa.String(64), nullable=False)
    email = sa.Column(sa.String(64), nullable=False)
    city = sa.Column(sa.String(32), nullable=False)
    phone_number = sa.Column(sa.String(32), nullable=False)
    created_on = sa.Column(sa.DateTime, nullable=False)

class Order(Base):
    __tablename__ = order_table

    order_id = sa.Column(sa.Integer, primary_key=True)
    merchant_id = sa.Column(sa.Integer, sa.ForeignKey(Merchant.merchant_id), nullable=False)
    product_category = sa.Column(sa.String(64), nullable=False)
    product_name = sa.Column(sa.String(1024), nullable=False)
    product_price = sa.Column(sa.Float, nullable=False)
    payment_method = sa.Column(sa.String(32), nullable=False)
    payment_ref_number = sa.Column(sa.String(32), nullable=True)
    payment_status = sa.Column(sa.String(32), nullable=False)
    created_on = sa.Column(sa.DateTime, nullable=False)

    # Define a relationship with the Merchant table
    merchant = relationship(Merchant, back_populates='orders')

# Add a relationship property to the Merchant class
Merchant.orders = relationship('Order', back_populates='merchant')
# Create the tables in the database
postgres_url = sa.engine.URL.create(
    drivername='postgresql',
    username=os.getenv('PG_DB_USER'),
    password=os.getenv('PG_DB_PASS'),
    host=os.getenv('PG_DB_HOST'),
    port=os.getenv('PG_DB_PORT'),
    database=os.getenv('PG_DB_NAME')
)

postgres_engine = sa.create_engine(postgres_url)

Base.metadata.drop_all(postgres_engine)
Base.metadata.create_all(bind=postgres_engine)

