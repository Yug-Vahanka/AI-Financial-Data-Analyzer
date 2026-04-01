# IMPORT LIBRARIES 
from sqlalchemy import Column, Integer, Float, String
# Integer, Float, String → data types for columns
from app.core.database import Base
# Base class for all database models (tables)
#  DATABASE MODEL 
class FinancialData(Base):
    """
    This class represents the 'financial_data' table in SQLite database.
    Each attribute = column in the table.
    """
    # Name of the table in database
    __tablename__ = "financial_data"
    # PRIMARY KEY 

    id = Column(Integer, primary_key=True, index=True)
    #  ASSET DETAILS 
    asset_type = Column(String)

    # Total value of asset 
    asset_value = Column(Integer)

    # User's savings amount
    user_savings = Column(Integer)
    loan_interest_rate = Column(Float)
    loan_tenure_years = Column(Integer)
    down_payment_percentage = Column(Integer)
    monthly_emi_capability = Column(Integer)
    investment_preference = Column(String)