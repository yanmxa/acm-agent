# from llama_index.core import (
#     VectorStoreIndex,
#     SimpleDirectoryReader,
#     StorageContext,
#     ServiceContext,
#     load_index_from_storage
# )
# from llama_index.core.node_parser import SemanticSplitterNodeParser
# from llama_index.embeddings.gemini import GeminiEmbedding
# from llama_index.llms.groq import Groq

from agents.search_engine import embedding_files

# embedding_files(None)


# use the google gemini embedding, an alternative is the local HuggingFaceEmbedding
# from llama_index.embeddings.gemini import GeminiEmbedding
# from llama_index.llms.groq import Groq

# import os
# from dotenv import load_dotenv

# load_dotenv()

# GOOGLE_API_KEY = os.getenv("GEMINI_API_KEY")
# GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# reader = SimpleDirectoryReader(input_dir="runbooks")
# documents = reader.load_data()

# # https://makersuite.google.com/app/apikey
# embed_model = GeminiEmbedding(model_name="models/embedding-001")

# llm = Groq(model="llama3-70b-8192", api_key=GROQ_API_KEY)

# transformations = [SentenceSplitter(chunk_size=1024)]

# index = VectorStoreIndex.from_documents(
#     documents, embed_model=embed_model, transformations=transformations
# )

# query_engine = index.as_query_engine(llm=llm)

# response = query_engine.query("What the reason caused cluster status unknown")
# print(response)
