# Project Submission: Smart Retail Assistant

## Project Name
Smart Retail Assistant

## Description
The Smart Retail Assistant is a high-performance RAG (Retrieval-Augmented Generation) chatbot designed to help users navigate a Walmart-like product catalog using natural language. 

**What problem is it solving?**
Traditional retail search often fails when users have complex, intent-based queries (e.g., "I need a gift for a 10-year-old who likes space"). Our assistant solves this by leveraging semantic vector search to find relevant products that keyword-based search might miss, providing a more human-like shopping experience.

**What is it doing?**
- **Semantic Retrieval**: It uses the native `VECTOR` data type and `VECTOR_SEARCH` in Azure SQL (2025 Preview) to find the most relevant products based on the user's intent, going beyond simple keyword matching.
- **Grounded Responses**: It utilizes a .NET 9 backend to orchestrate the RAG flow, using OpenAI's `gpt-4o-mini` to generate helpful responses grounded strictly in the retrieved SQL data to ensure accuracy and prevent hallucinations.
- **Modern UX**: It provides a clean, responsive chat interface with real-time feedback, typing indicators, and clear product recommendation cards with similarity match percentages.

**Architecture**:
- **Backend**: [SmartRetailAssistant.Api](file:///c:/Users/tulio.benedito/Documents/GitHub/smart-retail-assistant/backend-dotnet) - Built with ASP.NET Core 9, Dapper, and the OpenAI SDK.
- **Database**: [setup.sql](file:///c:/Users/tulio.benedito/Documents/GitHub/smart-retail-assistant/data/setup.sql) - Azure SQL Database leveraging native Vector support and DiskANN indexing.
- **AI**: OpenAI `gpt-4o-mini` (Chat) and `text-embedding-3-small` (Embeddings).
- **Frontend**: [index.html](file:///c:/Users/tulio.benedito/Documents/GitHub/smart-retail-assistant/frontend/index.html) - Modern responsive UI using Tailwind CSS and vanilla JavaScript.

## Type
RAG-Based Chatbot

## Project Repository URL
[https://github.com/beneditotulio/smart-retail-assistant](https://github.com/beneditotulio/smart-retail-assistant)

## Project Video
[https://youtu.be/58NQYUGr30s](https://youtu.be/58NQYUGr30s)
