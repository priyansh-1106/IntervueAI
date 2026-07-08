from pypdf import PdfReader 
from docx import Document 

from database .config import supabase 
from utils .helper import new_id ,current_timestamp ,format_list_or_text 
from model .llm import analyze_resume_ats 


def read_resume_file (uploaded_file ):


    file_name =uploaded_file .name .lower ()

    if file_name .endswith (".docx"):
        document =Document (uploaded_file )
        return "\n".join (paragraph .text for paragraph in document .paragraphs if paragraph .text )

    reader =PdfReader (uploaded_file )
    text =""
    for page in reader .pages :
        page_text =page .extract_text ()
        if page_text :
            text +=page_text +"\n"
    return text 


def scan_resume (user_id ,file_name ,resume_text ,job_role ,job_description ):


    result =analyze_resume_ats (resume_text ,job_description )

    supabase .table ("resume_scans").insert ({
    "id":new_id (),
    "user_id":user_id ,
    "file_name":file_name ,
    "job_role":job_role ,
    "ats_score":result .get ("ats_score",0 ),
    "keyword_match_score":result .get ("keyword_match_score",0 ),
    "formatting_score":result .get ("formatting_score",0 ),
    "structure_score":result .get ("structure_score",0 ),
    "matched_keywords":", ".join (result .get ("matched_keywords",[])or []),
    "missing_keywords":", ".join (result .get ("missing_keywords",[])or []),
    "strengths":format_list_or_text (result .get ("strengths"),empty_message =""),
    "weaknesses":format_list_or_text (result .get ("weaknesses"),empty_message =""),
    "suggestions":format_list_or_text (result .get ("suggestions"),empty_message =""),
    "created_at":current_timestamp (),
    }).execute ()

    return result 


def get_user_resume_scans (user_id ):

    result =(
    supabase .table ("resume_scans")
    .select ("*")
    .eq ("user_id",user_id )
    .order ("created_at",desc =True )
    .execute ()
    )
    return result .data 
