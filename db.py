import configparser
import os
import sqlalchemy

from sqlalchemy.dialects import postgresql

from databases import Database
from contextlib import asynccontextmanager

from tables import metadata

dialect = postgresql.dialect()

config = configparser.ConfigParser()
config.read('config.ini')

env = os.environ.get('PYTHON_ENV', 'development')
    
database = Database(url=config.get(env, 'URL'), min_size=2, max_size=4)

@asynccontextmanager
async def pool(app):
    await database.connect()

    for table in metadata.tables.values():
        schema = sqlalchemy.schema.CreateTable(table, if_not_exists=True)
        query = str(schema.compile(dialect=dialect))
        
        await database.execute(query=query)

    yield
    await database.disconnect()
