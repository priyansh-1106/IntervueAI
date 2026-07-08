

import os 
import sys 

sys .path .insert (0 ,os .path .join (os .path .dirname (os .path .abspath (__file__ )),"src"))

from model .rag import build_vectorstore 

if __name__ =="__main__":
    print ("Building the ChromaDB vector store from the question PDFs...")
    total_chunks =build_vectorstore ()
    print (f"Done! Stored {total_chunks } question chunks in src/vectorstore/chroma_db")
