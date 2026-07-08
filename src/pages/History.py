

import streamlit as st 
import pandas as pd 

from model .interview import get_user_interviews ,get_interview_answers 
from utils .helper import page_header ,format_list_or_text 
from utils .report_pdf import build_report_pdf 


def render ():


    page_header ("📜 Interview History","Review your past interviews and feedback")

    user_id =st .session_state .get ("user_id")
    interviews =get_user_interviews (user_id )

    if not interviews :
        st .info ("You haven't taken any interviews yet.")
        return 


    table_rows =[]
    for interview in interviews :
        table_rows .append ({
        "Date":interview .get ("created_at","")[:10 ],
        "Job Role":interview .get ("job_role",""),
        "Interview Type":interview .get ("interview_type",""),
        "Difficulty":interview .get ("difficulty","-"),
        "Score":interview .get ("overall_score","-"),
        "Proctoring Flags":interview .get ("proctoring_flags",0 ),
        })

    st .dataframe (pd .DataFrame (table_rows ),use_container_width =True ,hide_index =True )

    st .markdown ("---")
    st .markdown ("#### 🔍 View a Previous Report")


    options ={
    f"{i .get ('created_at','')[:10 ]} - {i .get ('job_role','')} ({i .get ('interview_type','')})":i ["id"]
    for i in interviews 
    }
    selected_label =st .selectbox ("Choose an interview",list (options .keys ()))

    if st .button ("View Feedback",use_container_width =True ):
        show_interview_detail (options [selected_label ],interviews )


def show_interview_detail (interview_id ,interviews ):


    interview =next ((i for i in interviews if i ["id"]==interview_id ),None )
    if not interview :
        st .error ("Interview not found.")
        return 

    st .markdown ("### 📋 Summary")
    col1 ,col2 ,col3 =st .columns (3 )
    col1 .metric ("Overall Score",f"{interview .get ('overall_score','-')} / 10")
    col2 .metric ("Technical Score",f"{interview .get ('technical_score','-')} / 10")
    col3 .metric ("Communication Score",f"{interview .get ('communication_score','-')} / 10")

    flags =interview .get ("proctoring_flags",0 )
    if flags and flags >0 :
        st .warning (f"⚠️ {flags } proctoring flag(s) were raised during this interview.")
    else :
        st .success ("✅ No proctoring flags were raised during this interview.")

    st .markdown (f"**Skill Analysis:** {format_list_or_text (interview .get ('skill_analysis'),'-')}")
    st .markdown (f"**Strengths:** {format_list_or_text (interview .get ('strengths'),'-')}")
    st .markdown (f"**Weaknesses:** {format_list_or_text (interview .get ('weaknesses'),'-')}")
    st .markdown (f"**Improvements:** {format_list_or_text (interview .get ('improvements'),'-')}")
    st .write (f"**Recommendation:** {interview .get ('recommendation','-')}")

    st .markdown ("### 💬 Question by Question Feedback")
    answers =get_interview_answers (interview_id )

    for i ,answer in enumerate (answers ,start =1 ):
        with st .container (border =True ):
            st .markdown (f"**Q{i }: {answer .get ('question','')}**")
            st .write (f"Your Answer: {answer .get ('answer','')}")
            st .write (
            f"Score: {answer .get ('score','-')} / 10 "
            f"(Technical: {answer .get ('technical_accuracy','-')}, "
            f"Communication: {answer .get ('communication','-')}, "
            f"Relevance: {answer .get ('relevance','-')})"
            )
            st .markdown (f"Strengths: {format_list_or_text (answer .get ('strengths'),'-')}")
            st .markdown (f"Weaknesses: {format_list_or_text (answer .get ('weaknesses'),'-')}")
            st .markdown (f"Tip: {format_list_or_text (answer .get ('tips'),'-')}")
            if answer .get ("model_answer"):
                st .write (f"Model Answer: {answer .get ('model_answer')}")


    pdf_bytes =build_report_pdf (interview ,answers )
    st .download_button (
    "⬇️ Export This Report as PDF",
    data =pdf_bytes ,
    file_name ="IntervueAI_Report.pdf",
    mime ="application/pdf",
    use_container_width =True ,
    )
