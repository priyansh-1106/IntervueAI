

import io 
from xml .sax .saxutils import escape 

from reportlab .lib .pagesizes import letter 
from reportlab .platypus import SimpleDocTemplate ,Paragraph ,Spacer 
from reportlab .lib .styles import getSampleStyleSheet 

from utils .helper import format_list_or_text 

styles =getSampleStyleSheet ()


def _safe_paragraph (text ):

    return escape (str (text )).replace ("\n","<br/>")


def build_report_pdf (interview_info ,answers ):


    buffer =io .BytesIO ()
    doc =SimpleDocTemplate (buffer ,pagesize =letter )
    story =[]


    story .append (Paragraph ("IntervueAI - Interview Report",styles ["Title"]))
    story .append (Spacer (1 ,10 ))
    story .append (Paragraph (
    f"Job Role: {interview_info .get ('job_role','-')} &nbsp;&nbsp; "
    f"Interview Type: {interview_info .get ('interview_type','-')}",
    styles ["Normal"],
    ))
    story .append (Spacer (1 ,16 ))


    story .append (Paragraph ("Summary",styles ["Heading2"]))
    story .append (Paragraph (f"Overall Score: {interview_info .get ('overall_score','-')} / 10",styles ["Normal"]))
    story .append (Paragraph (f"Technical Score: {interview_info .get ('technical_score','-')} / 10",styles ["Normal"]))
    story .append (Paragraph (f"Communication Score: {interview_info .get ('communication_score','-')} / 10",styles ["Normal"]))
    story .append (Paragraph (f"Recommendation: {interview_info .get ('recommendation','-')}",styles ["Normal"]))
    story .append (Paragraph (f"Proctoring Flags Raised: {interview_info .get ('proctoring_flags',0 )}",styles ["Normal"]))
    story .append (Spacer (1 ,12 ))

    for heading ,key in [
    ("Skill Analysis","skill_analysis"),
    ("Strengths","strengths"),
    ("Weaknesses","weaknesses"),
    ("Suggested Improvements","improvements"),
    ]:
        story .append (Paragraph (heading ,styles ["Heading3"]))
        story .append (Paragraph (interview_info .get (key ,"Not available"),styles ["Normal"]))
        story .append (Spacer (1 ,10 ))


    story .append (Paragraph ("Question by Question Feedback",styles ["Heading2"]))
    story .append (Spacer (1 ,8 ))

    for i ,item in enumerate (answers ,start =1 ):
        story .append (Paragraph (f"Q{i }. {item .get ('question','')}",styles ["Heading4"]))
        story .append (Paragraph (f"Answer: {item .get ('answer','')}",styles ["Normal"]))
        story .append (Paragraph (
        f"Score: {item .get ('score','-')} / 10 &nbsp; "
        f"(Technical: {item .get ('technical_accuracy','-')}, "
        f"Communication: {item .get ('communication','-')}, "
        f"Relevance: {item .get ('relevance','-')})",
        styles ["Normal"],
        ))
        story .append (Paragraph (f"Strengths: {item .get ('strengths','-')}",styles ["Normal"]))
        story .append (Paragraph (f"Weaknesses: {item .get ('weaknesses','-')}",styles ["Normal"]))
        story .append (Paragraph (f"Tip: {item .get ('tips','-')}",styles ["Normal"]))
        if item .get ("model_answer"):
            story .append (Paragraph (f"Model Answer: {item .get ('model_answer')}",styles ["Normal"]))
        story .append (Spacer (1 ,14 ))

    doc .build (story )
    buffer .seek (0 )
    return buffer .getvalue ()


def build_resume_report_pdf (scan_info ):


    buffer =io .BytesIO ()
    doc =SimpleDocTemplate (buffer ,pagesize =letter )
    story =[]

    def as_list (value ):
        if isinstance (value ,(list ,tuple )):
            return [str (v ).strip ()for v in value if str (v ).strip ()]
        return [v .strip ()for v in str (value or "").split (",")if v .strip ()]

    matched =as_list (scan_info .get ("matched_keywords"))
    missing =as_list (scan_info .get ("missing_keywords"))


    story .append (Paragraph ("IntervueAI - Resume ATS Report",styles ["Title"]))
    story .append (Spacer (1 ,10 ))
    story .append (Paragraph (
    f"File: {_safe_paragraph (scan_info .get ('file_name','-'))} &nbsp;&nbsp; "
    f"Target Role: {_safe_paragraph (scan_info .get ('job_role','-')or '-')}",
    styles ["Normal"],
    ))
    story .append (Spacer (1 ,16 ))


    story .append (Paragraph ("Score Breakdown",styles ["Heading2"]))
    story .append (Paragraph (f"Overall ATS Score: {scan_info .get ('ats_score','-')} / 100",styles ["Normal"]))
    story .append (Paragraph (f"Keyword Match: {scan_info .get ('keyword_match_score','-')} / 100",styles ["Normal"]))
    story .append (Paragraph (f"Formatting: {scan_info .get ('formatting_score','-')} / 100",styles ["Normal"]))
    story .append (Paragraph (f"Structure: {scan_info .get ('structure_score','-')} / 100",styles ["Normal"]))
    story .append (Spacer (1 ,12 ))

    story .append (Paragraph ("Matched Keywords",styles ["Heading3"]))
    story .append (Paragraph (_safe_paragraph (", ".join (matched ))if matched else "Not available",styles ["Normal"]))
    story .append (Spacer (1 ,10 ))

    story .append (Paragraph ("Missing Keywords",styles ["Heading3"]))
    story .append (Paragraph (_safe_paragraph (", ".join (missing ))if missing else "Not available",styles ["Normal"]))
    story .append (Spacer (1 ,12 ))


    for heading ,key in [
    ("Strengths","strengths"),
    ("Weaknesses","weaknesses"),
    ("Suggestions to Improve","suggestions"),
    ]:
        story .append (Paragraph (heading ,styles ["Heading3"]))
        text =format_list_or_text (scan_info .get (key ))
        story .append (Paragraph (_safe_paragraph (text ),styles ["Normal"]))
        story .append (Spacer (1 ,10 ))

    doc .build (story )
    buffer .seek (0 )
    return buffer .getvalue ()
