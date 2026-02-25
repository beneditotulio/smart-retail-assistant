# Smart Retail Assistant - SQL + AI Open Hack Solution

This repository contains the submission for the **SQL + AI Datathon Open Hack Challenge**. 

The **Smart Retail Assistant** is a RAG-based Chatbot (Option 1) that allows users to discover products from a Walmart catalog using natural language. It is built using **.NET 9**, **Azure SQL Database (Vector Search)**, and **Azure OpenAI**.

## 🏗️ Architecture & Approach

Our solution implements the **Retrieval-Augmented Generation (RAG)** pattern using a modern technical stack:

1.  **Vector Storage**: Product data is stored in **Azure SQL Database** using the new native `VECTOR` data type.
2.  **Semantic Retrieval**: When a user asks a question, the .NET backend generates an embedding using `text-embedding-3-small`. It then executes a **Vector Similarity Search** using the native `VECTOR_SEARCH` function in Azure SQL to find the top 5 most relevant products.
3.  **Prompt Augmentation**: The retrieved product details (Name, Description, Price, Category) are injected into a system prompt as context.
4.  **Grounded Generation**: The LLM (`gpt-4o-mini`) generates a response based **strictly** on the retrieved context, ensuring the assistant provides accurate, non-hallucinated product information.
5.  **Modern UX**: A responsive web interface built with Tailwind CSS provides a seamless chat experience, complete with product cards and similarity match indicators.

## 🚀 Key Features (Open Hack Alignment)

-   **Native SQL Vector Search**: Leverages the 2025 preview features of Azure SQL for high-performance vector retrieval.
-   **Strict RAG Grounding**: The system prompt is engineered to prevent hallucinations by restricting the AI to the provided SQL context.
-   **Source Attribution**: The UI explicitly displays the "Recommended Products" retrieved from SQL, providing evidence of the RAG flow.
-   **Full-Stack .NET**: A clean, professional implementation using ASP.NET Core 9.

## 📋 Prerequisites

1.  **Azure SQL Database**: Create a free instance [here](https://aka.ms/sqlfreeoffer).
2.  **OpenAI / Azure OpenAI API Key**: For generating embeddings and chat responses.
3.  **.NET 9 SDK**: Installed on your local machine.

## ⚙️ Setup Instructions

### 1. Database Configuration
1. Connect to your Azure SQL Database.
2. Run the [setup.sql](data/setup.sql) script to:
    - Create the `dbo.products` table with the `VECTOR` column.
    - Enable AI preview features.
    - Create a `DISKANN` vector index for fast retrieval.
    - Create the `search_products` stored procedure.

### 2. Data Ingestion
1. Download the [Walmart Product Dataset](https://www.kaggle.com/datasets/mauridb/product-data-from-walmart-usa-with-embeddings) from Kaggle.
2. Place the CSV file in the `data/` folder.
3. Run the ingestion script (Requires Python 3.10+):
   ```bash
   pip install pandas pyodbc openai python-dotenv tqdm
   python data/ingest.py
   ```

### 3. Environment Variables
1. Create a `.env` file in the root directory (use [.env.template](.env.template) as a guide).
2. Provide your `SQL_CONNECTION_STRING` and `OPENAI_API_KEY`.

### 4. Start the Application
1. Start the .NET backend:
   ```bash
   cd backend-dotnet
   dotnet run
   ```
2. Open [frontend/index.html](frontend/index.html) in your browser.

## 📺 Demo
*Video link will be provided here.*
