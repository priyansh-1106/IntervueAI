

import streamlit as st 
import streamlit .components .v1 as components 
from streamlit_javascript import st_javascript 
from pypdf import PdfReader 

from model .llm import extract_resume_info ,extract_job_description_info ,evaluate_answer ,transcribe_audio 
from model .interview import (
build_question_set ,create_interview_record ,save_answer_feedback ,
finish_interview ,add_proctoring_flag ,
)
from model .live_view import build_pip_html ,build_tab_switch_tracker_html ,build_auto_speak_html 
from utils .helper import page_header 
from utils .report_pdf import build_report_pdf 

AI_PHOTO_URL ="https://thumbs.dreamstime.com/b/stylized-faceless-person-illustration-modern-hair-plain-backdrop-minimalist-featuring-fashionable-haircut-simple-381062473.jpg"
DIFFICULTY_OPTIONS =["Mixed (40% Easy / 40% Medium / 20% Hard)","Easy","Medium","Hard"]


def render ():


    if "interview_stage"not in st .session_state :
        st .session_state ["interview_stage"]="setup"

    stage =st .session_state ["interview_stage"]

    if stage =="setup":
        page_header ("🎯 Set Up Your Interview","Upload your resume and a job description to begin")
        render_setup_stage ()
    elif stage =="live":
        page_header ("🎥 Live Interview","Answer each question as if this were the real thing")
        render_live_stage ()
    elif stage =="feedback":
        page_header ("📝 Answer Feedback","Here's how you did on that question")
        render_feedback_stage ()
    elif stage =="report":
        page_header ("📊 Your Interview Report","Full breakdown of your performance")
        render_report_stage ()






def render_setup_stage ():


    resume_file =st .file_uploader ("Upload your Resume (PDF)",type =["pdf"])
    job_description =st .text_area ("Paste the Job Description",height =180 )

    col1 ,col2 ,col3 =st .columns (3 )
    with col1 :
        interview_type =st .selectbox ("Interview Type",["HR","Technical"])
    with col2 :
        job_role =st .text_input ("Job Role",placeholder ="e.g. Python Developer")
    with col3 :
        num_questions =st .number_input (
        "Number of Questions",min_value =1 ,max_value =25 ,value =5 ,step =1 ,
        )

    difficulty_choice =st .selectbox ("Difficulty",DIFFICULTY_OPTIONS )
    difficulty ="Mixed"if difficulty_choice .startswith ("Mixed")else difficulty_choice 

    st .info ("📷 Your webcam will show as a small self-view during the interview, and 🎙️ your microphone "
    "will be used to answer questions by voice. Please allow camera and microphone access when asked.")

    if st .button ("Generate Interview Questions",use_container_width =True ):
        start_new_interview (resume_file ,job_description ,interview_type ,job_role ,num_questions ,difficulty )


def start_new_interview (resume_file ,job_description ,interview_type ,job_role ,num_questions ,difficulty ):


    if resume_file is None or not job_description or not job_role :
        st .error ("Please upload a resume, paste a job description and enter a job role.")
        return 

    with st .spinner ("Reading your resume and job description..."):
        resume_text =read_pdf_text (resume_file )
        resume_info =extract_resume_info (resume_text )
        jd_info =extract_job_description_info (job_description )


    combined_skills =(
    resume_info .get ("skills",[])
    +resume_info .get ("languages",[])
    +resume_info .get ("frameworks",[])
    +jd_info .get ("required_skills",[])
    +jd_info .get ("technologies",[])
    )
    combined_skills_text =", ".join (combined_skills )if combined_skills else job_role 

    with st .spinner ("Preparing your interview questions..."):
        questions =build_question_set (interview_type ,job_role ,num_questions ,combined_skills_text ,difficulty )

    if not questions :
        st .error ("Could not retrieve questions. Please make sure the ChromaDB vector store has been built.")
        return 


    user_id =st .session_state .get ("user_id")
    interview_id =create_interview_record (user_id ,job_role ,interview_type ,num_questions ,difficulty )


    st .session_state ["interview_id"]=interview_id 
    st .session_state ["job_role"]=job_role 
    st .session_state ["interview_type"]=interview_type 
    st .session_state ["questions"]=questions 
    st .session_state ["current_question_index"]=0 
    st .session_state ["all_feedback"]=[]
    st .session_state ["proctoring_flags"]=0 
    st .session_state ["last_tab_switch_count"]=0 
    st .session_state ["interview_stage"]="live"
    st .rerun ()


def read_pdf_text (uploaded_file ):

    reader =PdfReader (uploaded_file )
    text =""
    for page in reader .pages :
        page_text =page .extract_text ()
        if page_text :
            text +=page_text +"\n"
    return text 






def render_live_stage ():


    questions =st .session_state ["questions"]
    index =st .session_state ["current_question_index"]
    total =len (questions )

    current_question =questions [index ]["question"]
    difficulty =questions [index ]["difficulty"]
    progress_percent =int ((index /total )*100 )

    check_tab_switches ()

    left_col ,right_col =st .columns ([7 ,3 ])


    with left_col :
        with st .container (border =True ):
            header_col ,badge_col =st .columns ([3 ,1 ])
            with header_col :
                st .markdown ("#### 🎥 Interview Session")
            with badge_col :
                st .markdown (
                "<div style='text-align:right;'><span class='ia-badge-live'>"
                "<span class='dot'></span>Live</span></div>",
                unsafe_allow_html =True ,
                )



            components .html (build_pip_html (AI_PHOTO_URL ),height =420 )



        components .html (build_auto_speak_html (current_question ),height =0 )


    with right_col :
        with st .container (border =True ):
            st .markdown ("###### 📈 Real-time AI Performance")
            st .markdown (
            f"<div class='ia-ring' style='--pct:{progress_percent };'>"
            f"<div class='ia-ring-inner'>{progress_percent }%</div></div>",
            unsafe_allow_html =True ,
            )
            st .caption (f"Question {index +1 } of {total } \u2022 Difficulty: {difficulty }")
            st .progress (index /total )

        st .markdown (
        f"<p style='font-weight:600; margin-top:14px;'>\u201c{current_question }\u201d</p>",
        unsafe_allow_html =True ,
        )

        st .caption ("🎙️ Record your answer")
        recording =st .audio_input ("Record your answer",key =f"audio_{index }",label_visibility ="collapsed")
        transcribe_recorded_answer (recording ,index )

        answer_text =st .session_state .get (f"answer_{index }","")
        if answer_text :
            st .markdown (
            f"<div class='ia-card' style='padding:12px 14px; margin-top:8px;'>"
            f"<strong>You said:</strong> {answer_text }</div>",
            unsafe_allow_html =True ,
            )

        col_next ,col_finish =st .columns (2 )
        with col_next :
            if st .button ("Next ➡️",use_container_width =True ):
                submit_answer (current_question ,answer_text ,is_last =False )
        with col_finish :
            if st .button ("✅ Finish Interview",use_container_width =True ):
                submit_answer (current_question ,answer_text ,is_last =True )


def transcribe_recorded_answer (recording ,index ):


    if recording is None :
        return 

    recording_id =recording .file_id if hasattr (recording ,"file_id")else recording .name 
    if st .session_state .get (f"last_transcribed_{index }")==recording_id :
        return 

    with st .spinner ("Transcribing your answer..."):
        try :
            transcript =transcribe_audio (recording .getvalue ())
        except Exception :
            transcript =""
            st .error ("Could not transcribe that recording. Please try again.")

    st .session_state [f"answer_{index }"]=transcript 
    st .session_state [f"last_transcribed_{index }"]=recording_id 


def check_tab_switches ():

    components .html (build_tab_switch_tracker_html (),height =0 )

    try :
        current_count =st_javascript ("window.localStorage.getItem('ia_tab_switches') || '0'")
        current_count =int (current_count )if current_count is not None else 0 
    except Exception :
        current_count =st .session_state .get ("last_tab_switch_count",0 )

    previous_count =st .session_state .get ("last_tab_switch_count",0 )
    if current_count >previous_count :
        new_switches =current_count -previous_count 
        for _ in range (new_switches ):
            st .session_state ["proctoring_flags"]=add_proctoring_flag (
            st .session_state ["interview_id"],st .session_state .get ("proctoring_flags",0 )
            )
        st .session_state ["last_tab_switch_count"]=current_count 


def submit_answer (question ,answer ,is_last ):


    if not answer :
        st .warning ("Please speak your answer using the mic before continuing.")
        return 

    with st .spinner ("Evaluating your answer..."):
        feedback =evaluate_answer (question ,answer )

    save_answer_feedback (st .session_state ["interview_id"],question ,answer ,feedback )

    feedback_record =dict (feedback )
    feedback_record ["question"]=question 
    feedback_record ["answer"]=answer 
    st .session_state ["all_feedback"].append (feedback_record )

    st .session_state ["last_answer_feedback"]=feedback_record 
    st .session_state ["is_last_question"]=is_last or (
    st .session_state ["current_question_index"]>=len (st .session_state ["questions"])-1 
    )
    st .session_state ["interview_stage"]="feedback"
    st .rerun ()






def render_feedback_stage ():


    feedback =st .session_state .get ("last_answer_feedback",{})

    with st .container (border =True ):
        st .markdown (f"**Q: {feedback .get ('question','')}**")
        st .write (f"Your Answer: {feedback .get ('answer','')}")

    col1 ,col2 ,col3 ,col4 =st .columns (4 )
    col1 .metric ("Overall",f"{feedback .get ('score','-')} / 10")
    col2 .metric ("Technical",f"{feedback .get ('technical_accuracy','-')} / 10")
    col3 .metric ("Communication",f"{feedback .get ('communication','-')} / 10")
    col4 .metric ("Relevance",f"{feedback .get ('relevance','-')} / 10")

    with st .container (border =True ):
        st .markdown ("###### ✅ Strengths")
        st .write (feedback .get ("strengths","Not available"))

    with st .container (border =True ):
        st .markdown ("###### ⚠️ Weaknesses")
        st .write (feedback .get ("weaknesses","Not available"))

    with st .container (border =True ):
        st .markdown ("###### 💡 Improvement Tip")
        st .write (feedback .get ("tips","Not available"))

    if feedback .get ("model_answer"):
        with st .container (border =True ):
            st .markdown ("###### 📝 Example of a Strong Answer")
            st .write (feedback .get ("model_answer"))

    button_label ="See Final Report ➡️"if st .session_state .get ("is_last_question")else "Next Question ➡️"
    if st .button (button_label ,use_container_width =True ):
        if st .session_state .get ("is_last_question"):
            st .session_state ["interview_stage"]="report"
        else :
            st .session_state ["current_question_index"]+=1 
            st .session_state ["interview_stage"]="live"
        st .rerun ()






def render_report_stage ():


    if "final_report"not in st .session_state :
        with st .spinner ("Preparing your final report..."):
            report =finish_interview (
            st .session_state ["interview_id"],
            st .session_state ["job_role"],
            st .session_state ["interview_type"],
            st .session_state ["all_feedback"],
            )
            st .session_state ["final_report"]=report 

    report =st .session_state ["final_report"]

    col1 ,col2 ,col3 =st .columns (3 )
    col1 .metric ("Overall Score",f"{report .get ('overall_score',0 )} / 10")
    col2 .metric ("Technical Score",f"{report .get ('technical_score',0 )} / 10")
    col3 .metric ("Communication Score",f"{report .get ('communication_score',0 )} / 10")

    flags =st .session_state .get ("proctoring_flags",0 )
    if flags >0 :
        st .warning (f"⚠️ Proctoring Summary: {flags } suspicious event(s) were flagged during this interview "
        f"(e.g. no face visible, more than one face, or leaving the browser tab).")
    else :
        st .success ("✅ Proctoring Summary: No suspicious activity was flagged during this interview.")

    for heading ,key ,icon in [
    ("Skill Analysis","skill_analysis","🧩"),
    ("Strengths","strengths","✅"),
    ("Weaknesses","weaknesses","⚠️"),
    ("Suggested Improvements","improvements","📈"),
    ("Hiring Recommendation","recommendation","🏁"),
    ]:
        with st .container (border =True ):
            st .markdown (f"#### {icon } {heading }")
            st .write (report .get (key ,"Not available"))


    interview_info =dict (report )
    interview_info ["job_role"]=st .session_state .get ("job_role","")
    interview_info ["interview_type"]=st .session_state .get ("interview_type","")
    interview_info ["proctoring_flags"]=flags 

    pdf_bytes =build_report_pdf (interview_info ,st .session_state .get ("all_feedback",[]))

    col_download ,col_new =st .columns (2 )
    with col_download :
        st .download_button (
        "⬇️ Export Report as PDF",
        data =pdf_bytes ,
        file_name ="IntervueAI_Report.pdf",
        mime ="application/pdf",
        use_container_width =True ,
        )
    with col_new :
        if st .button ("Start a New Interview",use_container_width =True ):
            reset_interview_session ()
            st .rerun ()


def reset_interview_session ():

    keys_to_clear =[
    "interview_stage","interview_id","job_role","interview_type",
    "questions","current_question_index","all_feedback","final_report",
    "proctoring_flags","last_tab_switch_count",
    "last_answer_feedback","is_last_question",
    ]
    for key in keys_to_clear :
        if key in st .session_state :
            del st .session_state [key ]
