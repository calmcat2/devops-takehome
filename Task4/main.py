from typing import Optional
from fastapi import FastAPI, Depends, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select
import os

app = FastAPI()

#Create a model
class Store(SQLModel,table=True):
    id: Optional[int]=Field(default=None,primary_key=True)
    name: str

#Create an Engine with the postgres database
def get_engine():
    user=os.environ.get('PGUSER')
    password=os.environ.get('PGPASSWORD')
    db=os.environ.get('POSTGRES_DB')
    sql_url = "postgresql://"+user+":"+password+"@database:5432/"+db
    return create_engine(sql_url)

engine = get_engine()

# Method to create tables
def create_db_and_tables(engine):
    SQLModel.metadata.create_all(engine)

# Method to create a session dependency
def get_session():
    print("Creating a session")
    with Session(engine) as session:
        yield session

# Method for app start up.
@app.on_event("startup")
def on_startup():
    # Initialize the database
    create_db_and_tables(engine)
    try:
        if os.environ['LOG_LEVEL']=='debug':
            print("mode is: ",os.environ['MODE'])   
    except Exception as e: 
        print(f"Error getting env variables {e}")

# Method for GET at path "/"
@app.get("/")
def read_root():
    return {"Hello": "World"}
# Method for POST at path "/stores"
@app.post("/stores")
def create_store(store: Store, session: Session=Depends(get_session)):
    if session.get(Store,store.id)!=None:
        print("Store ID already exists")
        raise HTTPException(status_code=400, detail="Store ID already exists")
    else:
        session.add(store)
        session.commit()
        session.refresh(store)
        return store

# Method for GET at path "/stores"
@app.get("/get-stores")
def get_store(session: Session=Depends(get_session),offset: int=0,limit: int=Query(100,le=100)):
    try:
        stores=session.exec(select(Store).offset(offset).limit(limit)).all()
        return stores
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    