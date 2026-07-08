

import streamlit as st 
from utils .helper import page_header 


def render ():


    page_header ("💡 Interview Preparation Tips","Quick guidance before you practice")

    with st .container (border =True ):
        st .markdown ("#### 📄 Resume Tips")
        st .markdown (
        "- Keep your resume to one page if possible.\n"
        "- Use bullet points and action verbs (built, led, improved).\n"
        "- Highlight measurable results, e.g. 'reduced load time by 30%'.\n"
        "- Tailor your skills section to match the job description."
        )

    with st .container (border =True ):
        st .markdown ("#### 🤝 HR Interview Tips")
        st .markdown (
        "- Prepare a short, clear introduction about yourself.\n"
        "- Research the company before the interview.\n"
        "- Be honest about your strengths and weaknesses.\n"
        "- Have questions ready to ask the interviewer."
        )

    with st .container (border =True ):
        st .markdown ("#### 💻 Technical Interview Tips")
        st .markdown (
        "- Revise the core concepts of your main programming language.\n"
        "- Practice explaining your projects in simple terms.\n"
        "- Think out loud while solving problems.\n"
        "- It's okay to ask clarifying questions before answering."
        )

    with st .container (border =True ):
        st .markdown ("#### 🗣️ Communication Tips")
        st .markdown (
        "- Speak clearly and at a steady pace.\n"
        "- Structure answers using a simple format: situation, action, result.\n"
        "- Avoid filler words like 'um' and 'like' as much as possible.\n"
        "- Maintain good eye contact and confident body language."
        )
