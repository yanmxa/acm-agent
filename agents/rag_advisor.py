import os.path
import os
from llama_index.core import (
    VectorStoreIndex,
    SummaryIndex,
    SimpleDirectoryReader,
    StorageContext,
    ServiceContext,
    load_index_from_storage,
)

from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.groq import Groq
from llama_index.core import Settings

from dotenv import load_dotenv

load_dotenv()

current_working_directory = os.path.dirname(os.path.realpath(__file__))

llm = Groq(model="llama3-8b-8192")
llm_70b = Groq(model="llama3-70b-8192")
os.environ["TOKENIZERS_PARALLELISM"] = "false"
embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")
# define global settings so you don't have to pass the LLM / embedding model objects everywhere.
Settings.llm = llm
Settings.embed_model = embed_model

# refer: https://github.com/run-llama/llama_index/blob/main/docs/docs/examples/cookbooks/llama3_cookbook_groq.ipynb

storage_dir = os.path.join(current_working_directory, "__storage__")
if not os.path.exists(storage_dir):
    # load the documents and create the index
    documents = SimpleDirectoryReader(
        input_dir=os.path.join(current_working_directory, "..", "runbooks"),
    ).load_data()
    index = VectorStoreIndex.from_documents(documents)
    index.storage_context.persist(persist_dir=storage_dir)
else:
    # load the existing index
    storage_context = StorageContext.from_defaults(persist_dir=storage_dir)
    index = load_index_from_storage(storage_context)

query_engine = index.as_query_engine(similarity_top_k=3)

response = query_engine.query(
    "What's the reason for the managed cluster status is unknown?"
)
print("What's the reason for the managed cluster status is unknown?")
print(str(response))

response = query_engine.query(
    "Please give me the '## Diagnosis' steps, include the code block, for the unknown status of the managed cluster?"
)
print(
    "Please give me the diagnosis steps for the unknown status of the managed cluster!"
)
print(str(response))

# # Basic RAG (Summarization)
# summary_index = SummaryIndex.from_documents(documents)
# summary_engine = summary_index.as_query_engine()
# response = summary_engine.query(
#     "what's the reason for the managed cluster status is unknown?"
# )
# print(str(response))

# # Advanced RAG (Routing)
# # Build a Router that can choose whether to do vector search or summarization
# from llama_index.core.tools import QueryEngineTool, ToolMetadata
# vector_tool = QueryEngineTool(
#     index.as_query_engine(),
#     metadata=ToolMetadata(
#         name="vector_search",
#         description="Useful for searching for specific facts.",
#     ),
# )
# summary_tool = QueryEngineTool(
#     index.as_query_engine(response_mode="tree_summarize"),
#     metadata=ToolMetadata(
#         name="summary",
#         description="Useful for summarizing an entire document.",
#     ),
# )
# from llama_index.core.query_engine import RouterQueryEngine
# query_engine = RouterQueryEngine.from_defaults(
#     [vector_tool, summary_tool], select_multi=False, verbose=True, llm=llm_70b
# )
# response = query_engine.query(
#     "what's the reason for the managed cluster status is unknown?"
# )
# print(str(response))


# # Index as Retriever
# retriever = index.as_retriever(similarity_top_k=3)

# retrieved_nodes = retriever.retrieve(
#     "what's the reason for the managed cluster status is unknown?"
# )


# from llama_index.core.response.notebook_utils import display_source_node

# for text_node in retrieved_nodes:
#     display_source_node(text_node, source_length=500)

# embed_model = GeminiEmbedding(model_name="models/embedding-001")

# # llm = Groq(model="llama3-70b-8192", api_key=GROQ_API_KEY)
# # node_parser = SemanticSplitterNodeParser(
# #     llm=Groq(model="mixtral-8x7b-32768", api_key=GROQ_API_KEY),
# #     num_workers=8,
# # )
# splitter = SemanticSplitterNodeParser(
#               buffer_size=1,
#               breakpoint_percentile_threshold=95,
#               embed_model=embed_model
#            )

# nodes = splitter.get_nodes_from_documents(documents, show_progress=True)
