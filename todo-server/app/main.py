from fastapi import FastAPI
from sqlmodel import SQLModel, Field, create_engine, Session
from contextlib import asynccontextmanager
from app import settings

# step:1 Database Table schema

class Todo(SQLModel, table=True):
    id:int | None = Field(default=None, primary_key=True)
    title:str

# Connection to the database
    
connection_string : str = str (settings.DATABASE_URL).replace("postgresql", "postgresql+psycopg")

engine = create_engine(connection_string)

def create_db_table():
    print("create_db_tables")
    SQLModel.metadata.create_all(engine)
    print("done")

@asynccontextmanager
async def lifespan(todo_server: FastAPI):
    print("Server Startup")
    create_db_table()
    yield 

# Table Data save, get, update, delete

todo_server: FastAPI = FastAPI(lifespan=lifespan)

@todo_server.get("/")
def hello():
    return {"Hello": "World"}

@todo_server.get("/db")
def db_var():
    return  {"DB": settings.DATABASE_URL, "Connection": connection_string}

@todo_server.post("/todo")
def create_todo(todo_data: Todo):
    with Session(engine) as session:
        session.add(todo_data)
        session.commit()
        session.refresh(todo_data)
        return todo_data