from langchain_community.chat_models import ChatOpenAI

from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
import os
def get_tutor_response(vectorstore, question):
    llm = ChatOpenAI(
        temperature=0,
        openai_api_key=os.getenv("OPENAI_API_KEY")
    )
    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True
    )
    qa = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory
    )
    result = qa.run(question)
    return result
