import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.llms import HuggingFacePipeline
from langchain.document_loaders import DirectoryLoader
from langchain.document_loaders import UnstructuredWordDocumentLoader
from torch import cuda, bfloat16
import transformers
from transformers import StoppingCriteria, StoppingCriteriaList
import torch
from langchain.chains import ConversationalRetrievalChain
from config import CONFIG


def load_chain():
    bnb_config = transformers.BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_use_double_quant=True,
        bnb_4bit_compute_dtype=bfloat16,
    )
    model_config = transformers.AutoConfig.from_pretrained(
        CONFIG.model_id,
        # use_auth_token=hf_auth
    )

    model = transformers.AutoModelForCausalLM.from_pretrained(
        CONFIG.model_id,
        trust_remote_code=True,
        config=model_config,
        quantization_config=bnb_config,
        device_map="auto",
        # use_auth_token=hf_auth
    )
    # enable evaluation mode to allow model inference
    model.eval()
    print(f"Model llama loaded on {CONFIG.device}")
    tokenizer = transformers.AutoTokenizer.from_pretrained(
        CONFIG.model_id,
        # use_auth_token=hf_auth
    )

    ####################stop list ###############
    stop_list = ["\nHuman:", "\n```\n"]

    stop_token_ids = [tokenizer(x)["input_ids"] for x in stop_list]
    stop_token_ids
    stop_token_ids = [torch.LongTensor(x).to(CONFIG.device) for x in stop_token_ids]

    class StopOnTokens(StoppingCriteria):
        def __call__(
            self, input_ids: torch.LongTensor, scores: torch.FloatTensor, **kwargs
        ) -> bool:
            for stop_ids in stop_token_ids:
                if torch.eq(input_ids[0][-len(stop_ids) :], stop_ids).all():
                    return True
            return False

    stopping_criteria = StoppingCriteriaList([StopOnTokens()])

    ###################################################
    generate_text = transformers.pipeline(
        model=model,
        tokenizer=tokenizer,
        return_full_text=True,  # langchain expects the full text
        task="text-generation",
        # we pass model parameters here too
        stopping_criteria=stopping_criteria,  # without this model rambles during chat
        temperature=0.1,  # 'randomness' of outputs, 0.0 is the min and 1.0 the max
        max_new_tokens=512,  # max number of tokens to generate in the output
        repetition_penalty=1.1,  # without this output begins repeating
    )

    llm = HuggingFacePipeline(pipeline=generate_text)
    # # read text
    txt_loader = DirectoryLoader(
        "sotaysinhvien", glob="./*.docx", loader_cls=UnstructuredWordDocumentLoader
    )
    documents = txt_loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=20)
    all_splits = text_splitter.split_documents(documents)
    model_kwargs = {"device": "cuda"}
    embeddings = HuggingFaceEmbeddings(
        model_name=CONFIG.model_name, model_kwargs=model_kwargs
    )
    # storing embeddings in the vector store
    vectorstore = FAISS.from_documents(all_splits, embeddings)
    chain = ConversationalRetrievalChain.from_llm(
        llm, vectorstore.as_retriever(), return_source_documents=True
    )

    return chain


if __name__ == "__main__":
    chat_history = []

    query = "Khi nào thì một sinh viên bị đuổi học?"
    LANGCHAIN_PIPELINE = load_chain()
    result = LANGCHAIN_PIPELINE({"question": query, "chat_history": chat_history})
    print("*" * 50)
    print(f"Question: {query}")
    print("\n Answers:\n")
    print(result["answer"])

    print("\n reference:\n")
    print(result["source_documents"])
