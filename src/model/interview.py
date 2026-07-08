

import random 
from database .config import supabase 
from utils .helper import new_id ,current_timestamp 
from model .rag import retrieve_questions 
from model .llm import refine_question_with_context ,evaluate_answer ,generate_final_report 


def build_question_set (interview_type ,job_role ,num_questions ,combined_skills_text ,difficulty ="Mixed"):


    raw_questions =retrieve_questions (interview_type ,combined_skills_text ,num_questions )

    if difficulty =="Mixed":

        num_easy =round (num_questions *0.4 )
        num_medium =round (num_questions *0.4 )
        num_hard =num_questions -num_easy -num_medium 
        difficulty_labels =(["Easy"]*num_easy )+(["Medium"]*num_medium )+(["Hard"]*num_hard )
        random .shuffle (difficulty_labels )
    else :

        difficulty_labels =[difficulty ]*num_questions 

    final_questions =[]
    for index ,raw_question in enumerate (raw_questions ):
        refined =refine_question_with_context (raw_question ,combined_skills_text ,job_role )
        question_difficulty =difficulty_labels [index ]if index <len (difficulty_labels )else "Medium"
        final_questions .append ({
        "question":refined ,
        "difficulty":question_difficulty ,
        })

    return final_questions 


def save_answer_feedback (interview_id ,question ,answer ,feedback ):

    supabase .table ("interview_answers").insert ({
    "id":new_id (),
    "interview_id":interview_id ,
    "question":question ,
    "answer":answer ,
    "score":feedback .get ("score",0 ),
    "technical_accuracy":feedback .get ("technical_accuracy",0 ),
    "communication":feedback .get ("communication",0 ),
    "relevance":feedback .get ("relevance",0 ),
    "strengths":feedback .get ("strengths",""),
    "weaknesses":feedback .get ("weaknesses",""),
    "tips":feedback .get ("tips",""),
    "model_answer":feedback .get ("model_answer",""),
    "created_at":current_timestamp (),
    }).execute ()


def create_interview_record (user_id ,job_role ,interview_type ,num_questions ,difficulty ="Mixed"):

    interview_id =new_id ()

    supabase .table ("interviews").insert ({
    "id":interview_id ,
    "user_id":user_id ,
    "job_role":job_role ,
    "interview_type":interview_type ,
    "num_questions":num_questions ,
    "difficulty":difficulty ,
    "overall_score":None ,
    "proctoring_flags":0 ,
    "created_at":current_timestamp (),
    }).execute ()

    return interview_id 


def add_proctoring_flag (interview_id ,current_flag_count ):

    new_count =current_flag_count +1 
    supabase .table ("interviews").update ({
    "proctoring_flags":new_count ,
    }).eq ("id",interview_id ).execute ()
    return new_count 


def finish_interview (interview_id ,job_role ,interview_type ,all_feedback ):


    report =generate_final_report (all_feedback ,job_role ,interview_type )

    supabase .table ("interviews").update ({
    "overall_score":report .get ("overall_score",0 ),
    "technical_score":report .get ("technical_score",0 ),
    "communication_score":report .get ("communication_score",0 ),
    "skill_analysis":report .get ("skill_analysis",""),
    "strengths":report .get ("strengths",""),
    "weaknesses":report .get ("weaknesses",""),
    "improvements":report .get ("improvements",""),
    "recommendation":report .get ("recommendation",""),
    }).eq ("id",interview_id ).execute ()

    return report 


def get_user_interviews (user_id ):

    result =(
    supabase .table ("interviews")
    .select ("*")
    .eq ("user_id",user_id )
    .order ("created_at",desc =True )
    .execute ()
    )
    return result .data 


def get_interview_answers (interview_id ):

    result =(
    supabase .table ("interview_answers")
    .select ("*")
    .eq ("interview_id",interview_id )
    .execute ()
    )
    return result .data 


def get_dashboard_stats (user_id ):

    interviews =get_user_interviews (user_id )

    total_interviews =len (interviews )

    scores =[i ["overall_score"]for i in interviews if i .get ("overall_score")is not None ]
    average_score =round (sum (scores )/len (scores ),1 )if scores else 0 

    return total_interviews ,average_score 
