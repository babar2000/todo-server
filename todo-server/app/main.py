from fastapi import FastAPI, Depends
from typing import Annotated
from sqlmodel import SQLModel, Field, create_engine, Session, select
from contextlib import asynccontextmanager
from app import settings

# step:1 Database Table schema

class Todo(SQLModel, table=True):
    id:int | None = Field(default=None, primary_key=True)
    title:str
    description: str
    
# Connection to the database
    
connection_string : str = str (settings.DATABASE_URL).replace(
     "postgresql", "postgresql+psycopg")

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


# @todo_server.get("/")
# def hello():
#     return {"Hello": "World"}

@todo_server.get("/db")
def db_var():
    return  {"DB": settings.DATABASE_URL, "Connection": connection_string}

def get_session():
    with Session(engine) as session:
        yield session

@todo_server.get("/")
def hello_world():
	return {"Greet": "Hello World"} 


@todo_server.post("/todo")
def create_todo(try_content: Todo, session:Annotated[Session, Depends(get_session)]):
        session.add(try_content)
        session.commit()
        session.refresh(try_content)
        #session.close
        return try_content
    
# Get all todos data
@todo_server.get("/todo")
def get_all_todos(new_concept: Annotated[Session, Depends(get_session)]):
    #with Session(engine) as session: # will close session automatically
        # Todos Select
        query = select(Todo)
        all_todos = new_concept.exec(query).all()
        return all_todos
