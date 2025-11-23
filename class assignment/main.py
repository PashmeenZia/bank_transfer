from fastapi import FastAPI

app = FastAPI()

from fastapi import FastAPI, HTTPException

app = FastAPI()

# In-memory database for users
users = {
    "umaima": {"pin_number": "1234", "bank_balance": 5000},
    "izhaan": {"pin_number": "1000", "bank_balance": 10000},
    "zia": {"pin_number": "1005", "bank_balance": 50000},
}

@app.get("/")
async def root():
    return {"message": "Welcome to the Bank API"}

@app.get("/authenticate")
async def authenticate(name: str, pin_number: str):
    user = users.get(name)
    if not user or user["pin_number"] != pin_number:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"name": name, "bank_balance": user["bank_balance"]}

@app.post("/deposit")
async def deposit(name: str, pin_number: str, amount: float):
    user = users.get(name)
    if not user or user["pin_number"] != pin_number:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    if amount <= 0:
        raise HTTPException(status_code=400, detail="Deposit amount must be positive")
    
    user["bank_balance"] += amount
    return {"message": "Deposit successful", "new_balance": user["bank_balance"]}

@app.post("/bank-transfer")
async def bank_transfer(sender_name: str, sender_pin: str, recipient_name: str, amount: float):
    # Authenticate sender
    sender = users.get(sender_name)
    if not sender or sender["pin_number"] != sender_pin:
        raise HTTPException(status_code=401, detail="Invalid sender credentials")

    # Check if recipient exists
    recipient = users.get(recipient_name)
    if not recipient:
        raise HTTPException(status_code=404, detail="Recipient not found")

    # Check for sufficient balance
    if sender["bank_balance"] < amount:
        raise HTTPException(status_code=400, detail="Insufficient balance")

    # Perform transfer
    sender["bank_balance"] -= amount
    recipient["bank_balance"] += amount

    return {
        "message": "Transfer successful",
        "sender_new_balance": sender["bank_balance"],
        "recipient_authenticated_balance": {"name": recipient_name, "bank_balance": recipient["bank_balance"]}
    }