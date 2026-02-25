-- 1. Create the Product Table with Vector support
DROP TABLE IF EXISTS [dbo].[products];

CREATE TABLE [dbo].[products]
(
    [id] [int] IDENTITY(1,1) PRIMARY KEY,
    [product_name] [nvarchar](200) NOT NULL,
    [description] [nvarchar](max) NULL,
    [category] [nvarchar](1000) NULL,
    [list_price] [decimal](18, 2) NULL,
    [brand] [nvarchar](500) NULL,
    [embedding] [vector](1536) NULL
);
GO

-- 2. Enable AI Preview Features
ALTER DATABASE SCOPED CONFIGURATION SET PREVIEW_FEATURES = ON;
GO

-- 3. Create Vector Index
CREATE VECTOR INDEX idx_product_embeddings
ON dbo.products(embedding)
WITH (METRIC = 'COSINE', TYPE = 'DISKANN');
GO

-- 4. Stored Procedure for Similarity Search
CREATE OR ALTER PROCEDURE [dbo].[search_products]
    @queryVector VECTOR(1536),
    @top INT = 5
AS
BEGIN
    SELECT TOP (@top) 
        id,
        product_name,
        description,
        category,
        list_price,
        brand,
        1 - distance AS similarity
    FROM VECTOR_SEARCH(
        TABLE = dbo.products,
        COLUMN = embedding,
        SIMILAR_TO = @queryVector,
        METRIC = 'cosine',
        TOP_N = @top
    )
    ORDER BY distance;
END
GO
