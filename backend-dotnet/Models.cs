using System.Collections.Generic;

namespace SmartRetailAssistant.Api.Models
{
    public class ChatMessage
    {
        public string Role { get; set; } = string.Empty;
        public string Content { get; set; } = string.Empty;
    }

    public class ChatRequest
    {
        public List<ChatMessage> Messages { get; set; } = new();
    }

    public class Product
    {
        public int Id { get; set; }
        public string Product_Name { get; set; } = string.Empty;
        public string? Description { get; set; }
        public string? Category { get; set; }
        public decimal? List_Price { get; set; }
        public string? Brand { get; set; }
        public double Similarity { get; set; }
    }

    public class ChatResponse
    {
        public string Answer { get; set; } = string.Empty;
        public List<Product> Sources { get; set; } = new();
    }
}
