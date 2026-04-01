from pydantic import BaseModel, Field, model_validator
import uuid

# INPUT MODEL

class UserInput(BaseModel):
    """
    Model for user input request.
    """

    # Auto-generate request_id
    request_id: str = Field(default_factory=lambda: str(uuid.uuid4()))

    # User input text (must be between 5 and 500 characters)
    user_input: str = Field(
        ...,
        min_length=5,
        max_length=500
    )


# OUTPUT MODEL 

class ExtractedData(BaseModel):
    """
    Model for structured financial data extracted from AI.
    Includes validation rules and defaults.
    """

    asset_type: str = Field(default="property")
    asset_value: int = Field(..., gt=0)
    user_savings: int = Field(..., ge=0)

    # LOAN DETAILS 
    loan_interest_rate: float = Field(..., gt=0, lt=100)
    loan_tenure_years: int = Field(..., gt=0, lt=50)
    down_payment_percentage: int = Field(..., ge=0, le=100)

    monthly_emi_capability: int = Field(..., gt=0)
    investment_preference: str = Field(default="moderate")

    # BUSINESS RULE VALIDATION 
    @model_validator(mode="after")
    def check_business_rules(self):
        if self.user_savings > self.asset_value:
            self.user_savings = self.asset_value
        return self