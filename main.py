import os
import time
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.prompts import PromptTemplate
from langchain.prompts import ChatPromptTemplate
from langchain_community.vectorstores.chroma import Chroma
from langchain_community.document_loaders import Docx2txtLoader
from langchain_core.output_parsers import StrOutputParser
from langchain.chains.conversational_retrieval.base import ConversationalRetrievalChain
from langchain_core.vectorstores import VectorStoreRetriever
from langchain.prompts import ChatMessagePromptTemplate
from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate
)
from langchain.memory import ConversationBufferMemory
from ingestion import __name__
from ingestion import create_chroma_db
#create_chroma_db()
#from ingestion import create_chroma_db.vector_db
#chroma_attr = create_chroma_db()
#retriever_context = chroma_attr.create_chroma_db()
apikey = 'AIzaSyCZfnOGVL81JkV6-Z3TUG6_0aiwDIekx-4'
template = """You are a Customer Relationship Management Chat Bot. Your task is to read the given context first. Then understand the context.  answer the question after thoroughly understanding the question. Dont just answer the question matching the key words.  follow the below conditions
Conditions to follow:
1.First read the given context. Try to understand the context first. 
2.Now read the question properly and try to understand the question. Based on that you can give the response. try to understand the question rather than matching the key words.
2.Don't use your prior knowledge and only use the context provided to answer the question
3.If the given context is not related to question respond with "Context not related"
4.Focus on the question and avoid unnecessary characters,symbols, gramamtical errors attached to question
Context : delimeted between <ctx> </ctx>
<ctx>
{context}
</ctx>
 
Questions : delimited between <qs> </qs>
<qs>
{question}
</qs>
 
I need response in the below format. 
provide your answer here
"""

#context = __name__.vector_db.as_retriever(search_kwargs={'k': 3})
st.title('CRM CHAT BOT')
#st.chat_message("assistant").markdown('Hi!..How can I help you today ?')
with st.sidebar:
    st.markdown("CRM Chat Bot")
    #st.pa
#print('Hello')
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hi there!  How can I help you today?"}]
for messages in st.session_state.messages:
    with st.chat_input(messages["role"]):
        st.markdown(messages["content"])


question = st.chat_input("Ask something")
if question:
    try:       
        llm = ChatGoogleGenerativeAI(model='gemini-pro', google_api_key=apikey, convert_system_message_to_human=True)
        embeddings = GoogleGenerativeAIEmbeddings(model='models/embedding-001', google_api_key=apikey)
        #vector_db = Chroma(persist_directory='./chroma_db/',embedding_function=embeddings)
        #vector_chunks = create_chroma_db.vector_db
        vector_db = create_chroma_db() 
        #vector_db = Chroma(persist_directory='./chroma_db/',embedding_function=embeddings)
        context = vector_db.as_retriever(search_kwargs={'k': 3})
        parser = StrOutputParser()
        chat_history= []
        memory = ConversationBufferMemory(memory_key='chat_history',return_messages = True)
        messages = [
 
            SystemMessagePromptTemplate.from_template(template),
 
            HumanMessagePromptTemplate.from_template("{question}")
         ]
        qa_prompt = ChatPromptTemplate.from_messages(messages)
 
        #print("qa_prompt", qa_prompt)
        #context = __name__.context
        s_chain=ConversationalRetrievalChain.from_llm(
        llm=llm,
        chain_type="stuff",         
        retriever = context,
        memory = memory,
        verbose=True,
        combine_docs_chain_kwargs={"prompt": qa_prompt},
        return_source_documents=False
        )   
        
        llm_response=s_chain.invoke(question)
        parsed_response = parser.parse(llm_response)#output from llm

        with st.chat_message('Human'):
            st.write(f"{question}")
            #st.chat_message("Assistant")
            st.write(f"{parsed_response['answer']}")
        st.session_state.messages.append({"role":"Human","content":question})

        with st.chat_message("assistant"):
            st.markdown(st.write(f"{parsed_response['answer']}"))
        st.session_state.messages.append({"role": "assistant", "content": parsed_response['answer']})

    except Exception as e:
        st.error(f"Error: {e}")
