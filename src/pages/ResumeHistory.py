

import os 

import streamlit as st 
import pandas as pd 

from model .resume_analyzer import get_user_resume_scans 
from utils .helper import page_header ,format_list_or_text 
from utils .report_pdf import build_resume_report_pdf 


def render ():


    page_header ("📄 Resume Scan History","Review your past resume scans and export any report as a PDF")

    user_id =st .session_state .get ("user_id")
    scans =get_user_resume_scans (user_id )

    if not scans :
        st .info ("You haven't scanned any resumes yet.")
        return 


    table_rows =[]
    for scan in scans :
        table_rows .append ({
        "Date":scan .get ("created_at","")[:10 ],
        "File Name":scan .get ("file_name",""),
        "Job Role":scan .get ("job_role","-")or "-",
        "ATS Score":scan .get ("ats_score","-"),
        })

    st .dataframe (pd .DataFrame (table_rows ),use_container_width =True ,hide_index =True )

    st .markdown ("---")
    st .markdown ("#### 🔍 View a Previous Scan")


    options ={
    f"{s .get ('created_at','')[:10 ]} - {s .get ('file_name','')} ({s .get ('job_role','-')or '-'})":s ["id"]
    for s in scans 
    }
    selected_label =st .selectbox ("Choose a past scan",list (options .keys ()))

    if st .button ("View Scan Details",use_container_width =True ):
        show_scan_detail (options [selected_label ],scans )


def show_scan_detail (scan_id ,scans ):


    scan =next ((s for s in scans if s ["id"]==scan_id ),None )
    if not scan :
        st .error ("Scan not found.")
        return 

    st .markdown ("### 📊 ATS Score Breakdown")

    score =scan .get ("ats_score",0 )
    with st .container (border =True ):
        st .markdown (
        f"<div class='ia-ring' style='--pct:{score };'>"
        f"<div class='ia-ring-inner'>{score }</div></div>",
        unsafe_allow_html =True ,
        )
        st .caption ("Overall ATS Compatibility Score (out of 100)")

    col1 ,col2 ,col3 =st .columns (3 )
    col1 .metric ("Keyword Match",f"{scan .get ('keyword_match_score',0 )} / 100")
    col2 .metric ("Formatting",f"{scan .get ('formatting_score',0 )} / 100")
    col3 .metric ("Structure",f"{scan .get ('structure_score',0 )} / 100")

    matched =[k .strip ()for k in (scan .get ("matched_keywords")or "").split (",")if k .strip ()]
    missing =[k .strip ()for k in (scan .get ("missing_keywords")or "").split (",")if k .strip ()]

    col_match ,col_missing =st .columns (2 )
    with col_match :
        with st .container (border =True ):
            st .markdown ("###### ✅ Matched Keywords")
            st .write (", ".join (matched )if matched else "Not available")
    with col_missing :
        with st .container (border =True ):
            st .markdown ("###### ⚠️ Missing Keywords")
            st .write (", ".join (missing )if missing else "Not available")

    with st .container (border =True ):
        st .markdown ("###### 💪 Strengths")
        st .markdown (format_list_or_text (scan .get ("strengths")))

    with st .container (border =True ):
        st .markdown ("###### 📉 Weaknesses")
        st .markdown (format_list_or_text (scan .get ("weaknesses")))

    with st .container (border =True ):
        st .markdown ("###### 📈 Suggestions to Improve")
        st .markdown (format_list_or_text (scan .get ("suggestions")))

    pdf_bytes =build_resume_report_pdf ({
    "file_name":scan .get ("file_name",""),
    "job_role":scan .get ("job_role",""),
    "ats_score":scan .get ("ats_score",0 ),
    "keyword_match_score":scan .get ("keyword_match_score",0 ),
    "formatting_score":scan .get ("formatting_score",0 ),
    "structure_score":scan .get ("structure_score",0 ),
    "matched_keywords":matched ,
    "missing_keywords":missing ,
    "strengths":scan .get ("strengths",""),
    "weaknesses":scan .get ("weaknesses",""),
    "suggestions":scan .get ("suggestions",""),
    })
    base_name =os .path .splitext (scan .get ("file_name")or "resume")[0 ]
    st .download_button (
    "⬇️ Export This Report as PDF",
    data =pdf_bytes ,
    file_name =f"IntervueAI_Resume_Report_{base_name }.pdf",
    mime ="application/pdf",
    use_container_width =True ,
    )
