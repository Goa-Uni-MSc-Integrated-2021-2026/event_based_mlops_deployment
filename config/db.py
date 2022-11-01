from sqlalchemy import create_engine

engine = create_engine("mysql+pymysql://root@db:3306/users")