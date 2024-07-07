import streamlit as st  # webUI
from dotenv import load_dotenv # Private doc
from PyPDF2 import PdfReader # python library to read PDF file
from langchain.text_splitter import CharacterTextSplitter  # split into chunks
from langchain.embeddings import OpenAIEmbeddings, HuggingFaceInstructEmbeddings # doing vector embedding
from langchain.vectorstores import FAISS # vector datastore
from langchain.chat_models import ChatOpenAI # gpt-3.4-turbo
from langchain.memory import ConversationBufferMemory # Store previous data
from langchain.chains import ConversationalRetrievalChain # extract the data from the knowledge base
from htmlTemplates import css, bot_template, user_template # Web UI template
#from langchain.llms import HuggingFaceHub  # For hugging face LLM
from langchain.llms import OpenAI
import os
import time

def get_pdf_text(pdf_docs):
    """Extract text from uploaded PDF documents."""
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

def get_text_chunks(text):
    """Split text into smaller chunks for processing."""
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks

def get_vectorstore(text_chunks):
    """Create a vector store from text chunks."""
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    return vectorstore

def get_conversation_chain(vectorstore):
    """Initialize the conversation chain for the chatbot."""
    llm = ChatOpenAI()
    memory = ConversationBufferMemory(
        memory_key='chat_history', return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory
    )
    return conversation_chain

def handle_userinput(user_question):
    """Handle user input and update the chat history."""
    response = st.session_state.conversation({'question': user_question})
    st.session_state.chat_history = response['chat_history']

    # Display previous messages
    for i, message in enumerate(st.session_state.chat_history[:-1]):
        if i % 2 == 0:
            st.write(user_template.replace(
                "{{MSG}}", message.content), unsafe_allow_html=True)
        else:
            st.write(bot_template.replace(
                "{{MSG}}", message.content), unsafe_allow_html=True)

    # Typing effect for the latest message
    latest_message = st.session_state.chat_history[-1]
    if len(st.session_state.chat_history) % 2 == 0:
        message_placeholder = st.empty()
        for j in range(len(latest_message.content) + 1):
            message_placeholder.markdown(bot_template.replace(
                "{{MSG}}", latest_message.content[:j]), unsafe_allow_html=True)
            time.sleep(0.05)  # Adjust the delay for typing speed
    else:
        st.write(user_template.replace(
            "{{MSG}}", latest_message.content), unsafe_allow_html=True)

def main():
    """Main function to run the Streamlit app."""
    load_dotenv()
    st.set_page_config(page_title="Marklytics Investment Insight Bot",
                       page_icon=":leaves:")
    st.write(css, unsafe_allow_html=True)

    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None

    st.header("Marklytics GreenScribe :leaves:")
    user_question = st.text_input("Ask a question about your documents:")
    if user_question:
        handle_userinput(user_question)

    with st.sidebar:
        st.subheader("Your documents")
        pdf_docs = st.file_uploader(
            "Upload your PDFs here and click on 'Process'", accept_multiple_files=True)
        if st.button("Process"):
            if pdf_docs:
                with st.spinner("Processing"):
                    try:
                        # get pdf text
                        raw_text = get_pdf_text(pdf_docs)

                        # get the text chunks
                        text_chunks = get_text_chunks(raw_text)

                        # create vector store
                        vectorstore = get_vectorstore(text_chunks)

                        # create conversation chain
                        st.session_state.conversation = get_conversation_chain(
                            vectorstore)
                        st.success("Documents processed successfully!")
                    except Exception as e:
                        st.error(f"An error occurred: {e}")
            else:
                st.error("Please upload at least one PDF document.")

if __name__ == '__main__':
    main()
