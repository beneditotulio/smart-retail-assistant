import os
import json
from typing import List, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pyodbc
from openai import AzureOpenAI, OpenAI
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Smart Retail Assistant API")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize OpenAI Client
if os.getenv("OPENAI_ENDPOINT"):
    client = AzureOpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
        api_version=os.getenv("OPENAI_API_VERSION"),
        azure_endpoint=os.getenv("OPENAI_ENDPOINT")
    )
else:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Database connection helper
def get_db_connection():
    conn_str = os.getenv("SQL_CONNECTION_STRING")
    return pyodbc.connect(conn_str)

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[ChatMessage]

class Product(BaseModel):
    id: int
    product_name: str
    description: Optional[str]
    category: Optional[str]
    list_price: Optional[float]
    brand: Optional[str]
    similarity: float

def generate_embedding(text: str) -> List[float]:
    model = os.getenv("EMBEDDING_MODEL_NAME", "text-embedding-3-small")
    response = client.embeddings.create(input=[text], model=model)
    return response.data[0].embedding

def search_sql_products(embedding: List[float], top: int = 5) -> List[Product]:
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Convert embedding list to a JSON string or format suitable for the VECTOR type
    # In SQL 2025/Azure SQL, we can pass it as a JSON array string
    embedding_json = json.dumps(embedding)
    
    query = """
    EXEC [dbo].[search_products] @queryVector = ?, @top = ?
    """
    
    cursor.execute(query, (embedding_json, top))
    rows = cursor.fetchall()
    
    products = []
    for row in rows:
        products.append(Product(
            id=row.id,
            product_name=row.product_name,
            description=row.description,
            category=row.category,
            list_price=float(row.list_price) if row.list_price else None,
            brand=row.brand,
            similarity=row.similarity
        ))
    
    conn.close()
    return products

@app.post("/chat")
async def chat(request: ChatRequest):
    try:
        user_query = request.messages[-1].content
        
        # 1. Generate embedding for user query
        query_embedding = generate_embedding(user_query)
        
        # 2. Search for relevant products in SQL
        relevant_products = search_sql_products(query_embedding)
        
        # 3. Construct context from products
        context = "Here are some relevant products found in our catalog:\n"
        for p in relevant_products:
            context += f"- {p.product_name} ({p.category}): {p.description[:200]}... Price: ${p.list_price}\n"
        
        # 4. Generate AI response
        system_prompt = (
            "You are a helpful Smart Retail Assistant for a Walmart-like store. "
            "Use the provided product context to answer user questions. "
            "If the context doesn't contain the answer, politely say you couldn't find exactly what they were looking for, "
            "but suggest the closest matches from the context. "
            "Always be friendly and professional."
        )
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "system", "content": f"Context:\n{context}"}
        ]
        
        # Add user conversation history (last 5 messages)
        for msg in request.messages[-5:]:
            messages.append({"role": msg.role, "content": msg.content})
            
        response = client.chat.completions.create(
            model=os.getenv("OPENAI_MODEL_NAME", "gpt-4o-mini"),
            messages=messages,
            temperature=0.7
        )
        
        ai_message = response.choices[0].message.content
        
        return {
            "answer": ai_message,
            "sources": relevant_products
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
