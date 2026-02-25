# Smart Retail Assistant - Open Hack Solution

This project implements a **RAG-Based Chatbot Agent** that helps users find products in a Walmart catalog using natural language. It leverages the latest AI features in **Azure SQL Database** to perform high-performance vector similarity search.

## 🚀 Features
- **Semantic Product Discovery**: Users can ask natural questions like "I need something for a 10-year-old who likes space" instead of using keywords.
- **RAG (Retrieval-Augmented Generation)**: The AI assistant's answers are strictly grounded in the retrieved SQL data to prevent hallucinations.
- **Modern UI**: A clean, responsive chat interface built with Tailwind CSS.
- **Azure SQL Native Vectors**: Uses the new `VECTOR` data type and `VECTOR_SEARCH` function for efficient retrieval.

## 🛠️ Tech Stack
- **Frontend**: HTML5, JavaScript, Tailwind CSS.
- **Backend**: Python 3.11, FastAPI, Uvicorn.
- **Database**: Azure SQL Database (Free Tier / 2025 Preview).
- **AI**: Azure OpenAI (`gpt-4o-mini`, `text-embedding-3-small`).

## 📋 Prerequisites
1. **Azure SQL Database**: Create a free instance [here](https://aka.ms/sqlfreeoffer).
2. **OpenAI / Azure OpenAI API Key**: For generating embeddings and chat responses.
3. **Python 3.10+**: Installed on your local machine.

## ⚙️ Setup Instructions

### 1. Database Configuration
1. Connect to your Azure SQL Database using SSMS or Azure Portal.
2. Run the [setup.sql](data/setup.sql) script to create the table and vector index.

### 2. Environment Variables
1. Copy [.env.template](.env.template) to `.env`.
2. Fill in your `SQL_CONNECTION_STRING` and `OPENAI_API_KEY`.

### 3. Data Ingestion
1. Download the [Walmart Product Dataset](https://www.kaggle.com/datasets/mauridb/product-data-from-walmart-usa-with-embeddings) from Kaggle.
2. Place the CSV file in the `data/` folder.
3. Install dependencies:
   ```bash
   pip install -r backend/requirements.txt
   ```
4. Run the ingestion script:
   ```bash
   python data/ingest.py
   ```

### 4. Start the Application
1. Start the FastAPI backend:
   ```bash
   cd backend
   python main.py
   ```
2. Open `frontend/index.html` in your web browser.

## 📺 Demo
*Include your demo video link here for the submission!*

