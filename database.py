from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base,sessionmaker


engine=create_engine('postgresql://postgres:Rekha123@localhost/InventoryManagement',
    echo=True
)

Base=declarative_base()

Session=sessionmaker()