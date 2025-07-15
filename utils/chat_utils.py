from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.prompts import PromptTemplate

def create_qa_chain(llm, retriever):
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    prompt = PromptTemplate(
        input_variables=["context", "question"],
        template="""
        Use the following context to answer the question. If you don't know the answer, say so.

        Context:
        {context}

        Question:
        {question}

        Answer:
        """
    )
    return ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        combine_docs_chain_kwargs={"prompt": prompt},
        memory=ConversationBufferMemory(
            memory_key="chat_history", return_messages=True
        )
    )
    # return ConversationalRetrievalChain.from_llm(llm, retriever=retriever, memory=memory, chain_type_kwargs={"prompt": prompt})


def create_qa_chain_conversational(llm, retriever):
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    prompt = PromptTemplate(
        input_variables=["context", "question"],
        template="""
        Use the following context to answer the question. If you don't know the answer, say so.

        Context:
        {context}

        Question:
        {question}

        Answer:
        """
    )
    return ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        combine_docs_chain_kwargs={"prompt": prompt},
        memory=ConversationBufferMemory(
            memory_key="chat_history", return_messages=True
        )
    )