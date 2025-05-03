from pymongo import MongoClient
import pprint
from pymongo.errors import CollectionInvalid
from datetime import datetime
import os
from dotenv import load_dotenv
from colorama import Fore, Back, Style, init

# Initialize colorama
init(autoreset=True)

# Load environment variables from .env file
load_dotenv()

# Get MongoDB URI from environment variable
mongodb_uri = os.environ.get("MONGODB_URI", "mongodb://localhost:27017/")

# Connect to MongoDB using environment variable
client = MongoClient(mongodb_uri)  
db = client["finance_db"]  

# --- TRANSACTIONS COLLECTION ---
# Drop and recreate the transactions collection each time
if "transactions" in db.list_collection_names():
    db.transactions.drop()
    print(f"{Fore.YELLOW}Dropped existing 'transactions' collection")

# Create transactions collection
db.create_collection("transactions")
print(f"{Fore.GREEN}Collection 'transactions' created")

# --- ACCOUNTS: SCHEMA VALIDATED COLLECTION ---
# Drop and recreate the accounts collection
if "accounts" in db.list_collection_names():
    db.accounts.drop()
    print(f"{Fore.YELLOW}Dropped existing 'accounts' collection")

# Define schema for accounts
account_schema = {
    "bsonType": "object",
    "required": ["account_id", "name", "balance", "account_type"],
    "properties": {
        "account_id": {"bsonType": "string"},
        "name": {"bsonType": "string"},
        "balance": {"bsonType": "double", "minimum": 0},
        "account_type": {"enum": ["checking", "savings", "investment", "credit"]},
        "creation_date": {"bsonType": "date"},
        "status": {"enum": ["active", "closed", "suspended"]}
    }
}

# Create accounts collection with validation
db.create_collection(
    "accounts",
    validator={"$jsonSchema": account_schema}
)
print(f"{Fore.GREEN}Collection 'accounts' created with schema validation")

# Insert two example accounts
checking_account = {
    "account_id": "12345",
    "name": "Primary Checking",
    "balance": 1500.00,
    "account_type": "checking",
    "creation_date": datetime.now(),
    "status": "active"
}

savings_account = {
    "account_id": "67890",
    "name": "Emergency Savings",
    "balance": 3000.00,
    "account_type": "savings",
    "creation_date": datetime.now(),
    "status": "active"
}

db.accounts.insert_many([checking_account, savings_account])
print(f"{Fore.BLUE}Two accounts added successfully")

# Display initial account balances
print(f"\n{Style.BRIGHT}{Fore.CYAN}=== INITIAL ACCOUNT BALANCES ===")
for account in db.accounts.find():
    print(f"{Fore.MAGENTA}{account['name']}: {Style.BRIGHT}${account['balance']:.2f}")

# Prepare transfer transaction
transfer_amount = 500.00
transaction = {  
    "transaction_id": "TX" + datetime.now().strftime("%Y%m%d%H%M%S"),
    "from_account": "12345",  
    "to_account": "67890",
    "amount": transfer_amount,
    "transaction_date": datetime.now(),
    "description": "Transfer to savings",
    "category": "transfer",
    "tags": {"purpose": "emergency fund", "method": "online banking"}  
}  

# Atomic Transactions - Transfer funds between accounts
print(f"\n{Style.BRIGHT}{Fore.CYAN}=== PROCESSING TRANSFER ===")
print(f"{Fore.YELLOW}Transferring ${transfer_amount:.2f} from Checking to Savings...")

with client.start_session() as session:  
    with session.start_transaction():  
        # Debit from checking account
        db.accounts.update_one(
            {"account_id": "12345"}, 
            {"$inc": {"balance": -transfer_amount}}, 
            session=session
        )
        
        # Credit to savings account
        db.accounts.update_one(
            {"account_id": "67890"}, 
            {"$inc": {"balance": transfer_amount}}, 
            session=session
        )
        
        # Record transaction in history
        db.transactions.insert_one(transaction, session=session)
        
print(f"{Fore.GREEN}{Style.BRIGHT}Transfer completed successfully!")

# Display updated balances
print(f"\n{Style.BRIGHT}{Fore.CYAN}=== UPDATED ACCOUNT BALANCES ===")
for account in db.accounts.find():
    print(f"{Fore.MAGENTA}{account['name']}: {Style.BRIGHT}${account['balance']:.2f}")

# Display transaction history
print(f"\n{Style.BRIGHT}{Fore.CYAN}=== TRANSACTION HISTORY ===")
for tx in db.transactions.find():
    print(f"{Fore.YELLOW}Transaction ID: {Style.BRIGHT}{tx['transaction_id']}")
    print(f"{Fore.YELLOW}From Account: {tx['from_account']} → To Account: {tx['to_account']}")
    print(f"{Fore.YELLOW}Amount: ${tx['amount']:.2f}")
    print(f"{Fore.YELLOW}Date: {tx['transaction_date']}")
    print(f"{Fore.YELLOW}Category: {tx['category']}")
    print(f"{Fore.YELLOW}Description: {tx['description']}")

