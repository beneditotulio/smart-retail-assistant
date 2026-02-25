using System.Data;
using System.Text;
using System.Text.Json;
using Dapper;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Data.SqlClient;
using OpenAI.Chat;
using OpenAI.Embeddings;
using OpenAI;
using SmartRetailAssistant.Api.Models;
using Azure.AI.OpenAI;
using System.ClientModel;

namespace SmartRetailAssistant.Api.Controllers
{
    [ApiController]
    [Route("[controller]")]
    public class ChatController : ControllerBase
    {
        private readonly string _connectionString;
        private readonly string _openaiApiKey;
        private readonly string? _openaiEndpoint;
        private readonly string _chatModel;
        private readonly string _embeddingModel;

        public ChatController(IConfiguration configuration)
        {
            _connectionString = Environment.GetEnvironmentVariable("SQL_CONNECTION_STRING") ?? "";
            _openaiApiKey = Environment.GetEnvironmentVariable("OPENAI_API_KEY") ?? "";
            _openaiEndpoint = Environment.GetEnvironmentVariable("OPENAI_ENDPOINT");
            _chatModel = Environment.GetEnvironmentVariable("OPENAI_MODEL_NAME") ?? "gpt-4o-mini";
            _embeddingModel = Environment.GetEnvironmentVariable("EMBEDDING_MODEL_NAME") ?? "text-embedding-3-small";
        }

        private (ChatClient, EmbeddingClient) GetOpenAIClient()
        {
            if (!string.IsNullOrEmpty(_openaiEndpoint))
            {
                var azureClient = new AzureOpenAIClient(new Uri(_openaiEndpoint), new ApiKeyCredential(_openaiApiKey));
                return (azureClient.GetChatClient(_chatModel), azureClient.GetEmbeddingClient(_embeddingModel));
            }
            else
            {
                var client = new OpenAIClient(_openaiApiKey);
                return (client.GetChatClient(_chatModel), client.GetEmbeddingClient(_embeddingModel));
            }
        }

        [HttpPost]
        public async Task<ActionResult<ChatResponse>> Post([FromBody] ChatRequest request)
        {
            try
            {
                if (request.Messages == null || request.Messages.Count == 0)
                {
                    return BadRequest("No messages provided.");
                }

                var userQuery = request.Messages.Last().Content;
                var (chatClient, embeddingClient) = GetOpenAIClient();

                // 1. Generate embedding for user query
                OpenAIEmbedding embedding = await embeddingClient.GenerateEmbeddingAsync(userQuery);
                var queryVector = embedding.ToFloats().ToArray();
                var embeddingJson = JsonSerializer.Serialize(queryVector);

                // 2. Search for relevant products in SQL
                var relevantProducts = await SearchProducts(embeddingJson);

                // 3. Construct context from products
                var context = new StringBuilder("Here are some relevant products found in our catalog:\n");
                foreach (var p in relevantProducts)
                {
                    context.AppendLine($"- {p.Product_Name} ({p.Category}): {(p.Description?.Length > 200 ? p.Description[..200] : p.Description)}... Price: ${p.List_Price}");
                }

                // 4. Generate AI response
                var systemPrompt = "You are a specialized Smart Retail Assistant for a Walmart-like store. " +
                                   "Your primary goal is to help users find products based ONLY on the provided context from our SQL database. " +
                                   "STRICT GROUNDING RULES: " +
                                   "1. Only discuss products that are explicitly listed in the 'Context' section below. " +
                                   "2. If the user asks for something not in the context, say: 'I'm sorry, I couldn't find any products matching that description in our current catalog.' " +
                                   "3. Do not use outside knowledge about products, prices, or availability. " +
                                   "4. Always mention the price and category when recommending a product. " +
                                   "5. Be professional, helpful, and concise.";

                var messages = new List<OpenAI.Chat.ChatMessage>
                {
                    new SystemChatMessage(systemPrompt),
                    new SystemChatMessage($"Context:\n{context}")
                };

                // Add last 5 messages for history
                var historyCount = Math.Min(request.Messages.Count, 5);
                var history = request.Messages.Skip(request.Messages.Count - historyCount);

                foreach (var msg in history)
                {
                    if (msg.Role.ToLower() == "user")
                        messages.Add(new UserChatMessage(msg.Content));
                    else if (msg.Role.ToLower() == "assistant")
                        messages.Add(new AssistantChatMessage(msg.Content));
                }

                ChatCompletion response = await chatClient.CompleteChatAsync(messages);
                var aiMessage = response.Content[0].Text;

                return Ok(new ChatResponse
                {
                    Answer = aiMessage,
                    Sources = relevantProducts
                });
            }
            catch (Exception ex)
            {
                return StatusCode(500, ex.Message);
            }
        }

        private async Task<List<Product>> SearchProducts(string embeddingJson, int top = 5)
        {
            using IDbConnection db = new SqlConnection(_connectionString);
            var result = await db.QueryAsync<Product>(
                "[dbo].[search_products]",
                new { queryVector = embeddingJson, top = top },
                commandType: CommandType.StoredProcedure
            );
            return result.ToList();
        }
    }
}
