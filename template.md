The Smart Retail Assistant is a high-performance RAG (Retrieval-Augmented Generation) chatbot designed to help users navigate a Walmart-like product catalog using natural language. 

**What problem is it solving?**
Traditional retail search often fails when users have complex, intent-based queries (e.g., "I need a gift for a 10-year-old who likes space"). Our assistant solves this by leveraging semantic vector search to find relevant products that keyword-based search might miss.

**What is it doing?**
- **Semantic Retrieval**: It uses the native `VECTOR` data type and `VECTOR_SEARCH` in Azure SQL to find the most relevant products based on the user's intent.
- **Grounded Responses**: It uses .NET 9 and OpenAI to generate helpful responses grounded strictly in the retrieved SQL data, preventing AI hallucinations.
- **Modern UX**: Provides a clean, responsive chat interface with product recommendations, match percentages, and source attribution.

**Architecture**:
- **Backend**: ASP.NET Core 9 Web API
- **Database**: Azure SQL Database (with 2025 Vector Preview features)
- **AI**: OpenAI `gpt-4o-mini` and `text-embedding-3-small`
- **Frontend**: HTML5, Tailwind CSS, JavaScript