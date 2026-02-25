import os
import pandas as pd
import pyodbc
import json
from openai import AzureOpenAI, OpenAI
from dotenv import load_dotenv
import tqdm

load_dotenv()

# Configuration
CSV_PATH = "../data/walmart-product-with-embeddings-dataset-usa-text-3-small.csv"
TABLE_NAME = "dbo.products"

# Initialize OpenAI Client (for embedding generation if needed)
if os.getenv("OPENAI_ENDPOINT"):
    client = AzureOpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
        api_version=os.getenv("OPENAI_API_VERSION"),
        azure_endpoint=os.getenv("OPENAI_ENDPOINT")
    )
else:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_db_connection():
    conn_str = os.getenv("SQL_CONNECTION_STRING")
    return pyodbc.connect(conn_str)

def ingest_data():
    if not os.path.exists(CSV_PATH):
        print(f"Error: CSV file not found at {CSV_PATH}")
        print("Please download it from Kaggle and place it in the 'data' folder.")
        return

    print("Reading CSV...")
    df = pd.read_csv(CSV_PATH)
    
    # We only need a subset for the demo to keep it fast
    df = df.head(1000) 
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    print(f"Ingesting {len(df)} products into Azure SQL...")
    
    insert_query = f"""
    INSERT INTO {TABLE_NAME} (product_name, description, category, list_price, brand, embedding)
    VALUES (?, ?, ?, ?, ?, ?)
    """
    
    for _, row in tqdm.tqdm(df.iterrows(), total=len(df)):
        try:
            # The CSV from Kaggle already has an 'embedding' column as a string representation of a list
            # We need to ensure it's in a format SQL's VECTOR type accepts (JSON array string)
            embedding_raw = row['embedding']
            if isinstance(embedding_raw, str):
                # Ensure it's valid JSON
                embedding_json = embedding_raw 
            else:
                embedding_json = json.dumps(embedding_raw.tolist())

            cursor.execute(insert_query, (
                row['product_name'][:200],
                row['description'],
                row['category'][:1000],
                row['list_price'],
                row['brand'][:500],
                embedding_json
            ))
        except Exception as e:
            print(f"Error inserting row: {e}")
            continue
            
    conn.commit()
    conn.close()
    print("Ingestion complete!")

if __name__ == "__main__":
    ingest_data()
