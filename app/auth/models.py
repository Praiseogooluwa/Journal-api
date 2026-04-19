from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy import func
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id= Column(Integer, primary_key= True, index= True)
    username= Column(String, nullable= False, index= True, unique= True)
    email= Column(String, index= True, nullable= False, unique= True)
    password= Column(String, nullable= False)
    created_at= Column(DateTime(timezone= True), server_default= func.now())