from fastapi import FastAPI
from pydantic import BaseModel, Field
from uuid import uuid4

app = FastAPI(
    title="SecurePay Cloud",
    description="A simulated payment processing API",
    version="0.1.0",
)


class PaymentRequest(BaseModel):
    amount: float = Field(gt=0, le=10000)
    currency: str = Field(min_length=3, max_length=3)


@app.get("/")
def home():
    return {"message": "Welcome to SecurePay Cloud"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.post("/payments")
def create_payment(payment: PaymentRequest):
    return {
        "payment_id": str(uuid4()),
        "amount": payment.amount,
        "currency": payment.currency.upper(),
        "status": "simulated",
    }
