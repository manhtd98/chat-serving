from langchain.vectorstores import FAISS

from langchain.embeddings import HuggingFaceEmbeddings
from langchain.retrievers import TFIDFRetriever, EnsembleRetriever
from langchain.embeddings import HuggingFaceEmbeddings

from underthesea import text_normalize
import pandas as pd
from langchain.schema import Document
import logging

logging.basicConfig(
    format=f"\n\x00%(asctime)s.%(msecs)03d [%(levelname)s]: %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.StreamHandler(),
    ],
)

df = pd.read_csv("c3.csv")
output_chunk = []
for doc in df.iterrows():
    output_chunk.append(Document(page_content=text_normalize(doc[1].text)))
all_splits = output_chunk

logging.info("TFIDF - RETRIEVER")

tfidf_retriever = TFIDFRetriever.from_documents(
    all_splits,
    search_type="similarity",
    search_kwargs={"k": 2, "include_metadata": False},
)

logging.info("vinai/phobert-base-v2 - RETRIEVER")

embeddings = HuggingFaceEmbeddings(model_name="vinai/phobert-base-v2")
vectorstore = FAISS.from_documents(all_splits, embeddings)

emb_retriever = vectorstore.as_retriever(
    search_type="mmr", search_kwargs={"k": 2, "include_metadata": False}
)

logging.info("vinai/bartpho-syllable - RETRIEVER")
qa_embeddings = HuggingFaceEmbeddings(model_name="vinai/bartpho-syllable")
_qa_vector_store = FAISS.from_documents(all_splits, qa_embeddings)
qa_retriever = _qa_vector_store.as_retriever(
    search_type="mmr", search_kwargs={"k": 2, "include_metadata": False}
)
ensemble_retriever = EnsembleRetriever(
    retrievers=[tfidf_retriever, emb_retriever, qa_retriever],
    weights=[0.4, 0.3, 0.2],
    search_kwargs={"k": 3, "include_metadata": False},
)


documents = ensemble_retriever.get_relevant_documents("Giờ giảng dạy là gì?")

for doc in documents:
    print(doc.page_content)
