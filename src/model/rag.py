

import os 
from langchain_community .document_loaders import PyPDFLoader 
from langchain_community .vectorstores import Chroma 
from langchain_community .embeddings import SentenceTransformerEmbeddings 



try :
    from langchain_text_splitters import RecursiveCharacterTextSplitter 
except ModuleNotFoundError :
    from langchain .text_splitter import RecursiveCharacterTextSplitter 


DATA_FOLDER ="src/model/data"
HR_PDF =os .path .join (DATA_FOLDER ,"hr_questions.pdf")
TECHNICAL_PDF =os .path .join (DATA_FOLDER ,"technical_questions.pdf")
CHROMA_FOLDER ="src/vectorstore/chroma_db"


embedding_function =SentenceTransformerEmbeddings (model_name ="all-MiniLM-L6-v2")


def build_vectorstore ():


    splitter =RecursiveCharacterTextSplitter (chunk_size =300 ,chunk_overlap =30 )
    all_chunks =[]


    hr_docs =PyPDFLoader (HR_PDF ).load ()
    hr_chunks =splitter .split_documents (hr_docs )
    for chunk in hr_chunks :
        chunk .metadata ["category"]="hr"
    all_chunks .extend (hr_chunks )


    tech_docs =PyPDFLoader (TECHNICAL_PDF ).load ()
    tech_chunks =splitter .split_documents (tech_docs )
    for chunk in tech_chunks :
        chunk .metadata ["category"]="technical"
    all_chunks .extend (tech_chunks )


    vectorstore =Chroma .from_documents (
    documents =all_chunks ,
    embedding =embedding_function ,
    persist_directory =CHROMA_FOLDER ,
    )
    vectorstore .persist ()

    return len (all_chunks )


def get_vectorstore ():

    return Chroma (
    persist_directory =CHROMA_FOLDER ,
    embedding_function =embedding_function ,
    )


def retrieve_questions (interview_type ,search_text ,num_questions ):


    category ="hr"if interview_type =="HR"else "technical"

    vectorstore =get_vectorstore ()


    results =vectorstore .similarity_search (
    query =search_text ,
    k =num_questions +5 ,
    filter ={"category":category },
    )

    questions =[]
    for doc in results :
        text =doc .page_content .strip ()
        if text and text not in questions :
            questions .append (text )
        if len (questions )>=num_questions :
            break 

    return questions 
