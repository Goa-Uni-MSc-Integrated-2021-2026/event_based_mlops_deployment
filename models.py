from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

class User:
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)

class Project:
    __tablename__ = "projects"
    project_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = ForeignKey()

class Tasks:
    __tablename__ = "tasks"
    task_id = Column(Integer, primary_key=True, autoincrement=True)
    project_id = ForeignKey()