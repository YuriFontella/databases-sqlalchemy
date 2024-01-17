from sqlalchemy import *

metadata = MetaData()

customers = Table(
    'customers',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('customer_id', String(length=255), nullable=False),
    Column('status', Boolean, server_default=text('FALSE')),
    Column('date', DateTime, server_default=text('NOW()')),

    Index('customers_index_customer_id', 'customer_id'),
    UniqueConstraint('customer_id')
)

files = Table(
    'files',
    metadata,
    Column('id', Integer, primary_key=true),
    Column('customer_id', Integer, ForeignKey('customers.id', ondelete='CASCADE'), nullable=False),
    Column('date', DateTime, server_default=text('NOW()')),

    Index('files_index_customer_id', 'customer_id')
)