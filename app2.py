import gradio as gr
from langchain_community.document_loaders import WebBaseLoader
from langchain.vectorstores.chroma import Chroma
from langchain_community import embeddings
from langchain_community.chat_models import ChatOllama
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_text_splitters import CharacterTextSplitter

def process_input(urls, question):
    model_local = ChatOllama(model="mistral-openorca")

    # Convert string of URLS to list
    urls_list = urls.split("\n")
    docs = [WebBaseLoader(url).load() for url in urls_list]
    docs_list = [item for sublist in docs for item in sublist]

    text_splitter = CharacterTextSplitter.from_tiktoken_encoder(chunk_size=7500, chunk_overlap=100)
    docs_splits = text_splitter.split_documents(docs_list)

    vectorstore = Chroma.from_documents(
        documents=docs_splits,
        collection_name="rag-chroma",
        embedding=embeddings.ollama.OllamaEmbeddings(model='nomic-embed-text'),
    )
    retriever = vectorstore.as_retriever()

    after_rag_template = """Answer the question based only on the following context: 
    {context}
    Question: {question}
    """

    after_rag_prompt = ChatPromptTemplate.from_template(after_rag_template)
    after_rag_chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | after_rag_prompt
        | model_local
        | StrOutputParser()
    )
    return after_rag_chain.invoke(question)

# Define Gradio interface
iface = gr.Interface(fn=process_input,
                     inputs=[gr.Textbox(label="Enter URLS by new lines"), gr.Textbox(label="Question")],
                     outputs="text",
                     title="Document Query with Ollama",
                     description="Enter URLS and shit")
iface.launch()
