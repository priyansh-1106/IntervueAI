import os 

import streamlit as st 

from model .resume_analyzer import read_resume_file ,scan_resume 
from utils .helper import page_header ,format_list_or_text 
from utils .report_pdf import build_resume_report_pdf 


def render ():
    page_header ("🧾 Resume ATS Score Analyzer","Check how well your resume matches a job and passes ATS screening")

    resume_file =st .file_uploader ("Upload your Resume",type =["pdf","docx"])

    col1 ,col2 =st .columns (2 )
    with col1 :
        job_role =st .text_input ("Target Job Role",placeholder ="e.g. Python Developer")
    with col2 :
        job_description =st .text_area ("Target Job Description (optional)",height =100 )

    if st .button ("Analyze Resume",use_container_width =True ):
        run_analysis (resume_file ,job_role ,job_description )

    if st .session_state .get ("last_ats_result"):
        render_result (st .session_state ["last_ats_result"])

    st .caption ("Want to revisit an older scan? Head to the **Resume History** page from the sidebar.")


def run_analysis (resume_file ,job_role ,job_description ):
    if resume_file is None :
        st .error ("Please upload a resume (PDF or DOCX) first.")
        return 

    with st .spinner ("Reading your resume..."):
        resume_text =read_resume_file (resume_file )

    if not resume_text .strip ():
        st .error ("Could not read any text from that file. Please try a different file.")
        return 

    with st .spinner ("Scoring your resume..."):
        user_id =st .session_state .get ("user_id")
        result =scan_resume (user_id ,resume_file .name ,resume_text ,job_role ,job_description )



    result ["file_name"]=resume_file .name 
    result ["job_role"]=job_role 

    st .session_state ["last_ats_result"]=result 


def render_result (result ):
    st .markdown ("### 📊 ATS Score Breakdown")

    score =result .get ("ats_score",0 )
    with st .container (border =True ):
        st .markdown (
        f"<div class='ia-ring' style='--pct:{score };'>"
        f"<div class='ia-ring-inner'>{score }</div></div>",
        unsafe_allow_html =True ,
        )
        st .caption ("Overall ATS Compatibility Score (out of 100)")

    col1 ,col2 ,col3 =st .columns (3 )
    col1 .metric ("Keyword Match",f"{result .get ('keyword_match_score',0 )} / 100")
    col2 .metric ("Formatting",f"{result .get ('formatting_score',0 )} / 100")
    col3 .metric ("Structure",f"{result .get ('structure_score',0 )} / 100")

    col_match ,col_missing =st .columns (2 )
    with col_match :
        with st .container (border =True ):
            st .markdown ("###### ✅ Matched Keywords")
            matched =result .get ("matched_keywords",[])
            st .write (", ".join (matched )if matched else "Not available")
    with col_missing :
        with st .container (border =True ):
            st .markdown ("###### ⚠️ Missing Keywords")
            missing =result .get ("missing_keywords",[])
            st .write (", ".join (missing )if missing else "Not available")

    with st .container (border =True ):
        st .markdown ("###### 💪 Strengths")
        st .markdown (format_list_or_text (result .get ("strengths")))

    with st .container (border =True ):
        st .markdown ("###### 📉 Weaknesses")
        st .markdown (format_list_or_text (result .get ("weaknesses")))

    with st .container (border =True ):
        st .markdown ("###### 📈 Suggestions to Improve")
        st .markdown (format_list_or_text (result .get ("suggestions")))

    pdf_bytes =build_resume_report_pdf (result )
    base_name =os .path .splitext (result .get ("file_name")or "resume")[0 ]
    st .download_button (
    "⬇️ Export This Report as PDF",
    data =pdf_bytes ,
    file_name =f"IntervueAI_Resume_Report_{base_name }.pdf",
    mime ="application/pdf",
    use_container_width =True ,
    )
