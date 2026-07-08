

import json 
import streamlit as st 
from groq import Groq 


GROQ_MODEL ="llama-3.1-8b-instant"


def get_groq_client ():

    api_key =st .secrets ["GROQ_API_KEY"]
    return Groq (api_key =api_key )


def ask_groq (prompt ,system_message ="You are a helpful assistant."):

    client =get_groq_client ()

    response =client .chat .completions .create (
    model =GROQ_MODEL ,
    messages =[
    {"role":"system","content":system_message },
    {"role":"user","content":prompt },
    ],
    temperature =0.3 ,
    )

    return response .choices [0 ].message .content 


def extract_resume_info (resume_text ):


    prompt =f"""
    Read the resume text below and extract the candidate's details.
    Return ONLY valid JSON with these exact keys:
    "skills", "languages", "frameworks", "projects", "education"
    Each value should be a list of short strings.

    Resume Text:
    {resume_text }
    """

    reply =ask_groq (prompt ,system_message ="You extract structured data from resumes and reply only in JSON.")
    return safe_json_parse (reply )


def extract_job_description_info (jd_text ):


    prompt =f"""
    Read the job description below and extract the requirements.
    Return ONLY valid JSON with these exact keys:
    "required_skills", "technologies", "experience"
    "required_skills" and "technologies" should be lists of short strings.
    "experience" should be a short string (for example "2-4 years").

    Job Description:
    {jd_text }
    """

    reply =ask_groq (prompt ,system_message ="You extract structured data from job descriptions and reply only in JSON.")
    return safe_json_parse (reply )


def refine_question_with_context (raw_question ,skills_text ,job_role ):


    prompt =f"""
    Rewrite the interview question below so it is relevant to a
    candidate applying for the role of "{job_role }" who has these skills: {skills_text }.
    Keep the meaning of the original question. Keep it short, one question only.
    Output ONLY the rewritten question itself, with no preamble, no introduction,
    no label like "Here's the rewritten question", no quotation marks, and no
    explanation before or after it.

    Original Question:
    {raw_question }
    """

    reply =ask_groq (prompt ,system_message ="You are an experienced technical interviewer.")
    return clean_question_text (reply )


def clean_question_text (text ):


    cleaned =text .strip ().strip ('"').strip ("'").strip ()

    lines =[line .strip ()for line in cleaned .split ("\n")if line .strip ()]
    if len (lines )>1 :
        cleaned =lines [-1 ]
    else :
        cleaned =lines [0 ]if lines else cleaned 

    preamble_starts =("here's","here is","sure","certainly","okay","ok,","rewritten question")
    if cleaned .lower ().startswith (preamble_starts )and ":"in cleaned :
        cleaned =cleaned .split (":",1 )[1 ].strip ()

    return cleaned .strip ('"').strip ("'").strip ()


def evaluate_answer (question ,answer ):


    prompt =f"""
    Question: {question }
    Candidate Answer: {answer }

    Evaluate the answer carefully and in detail. Return ONLY valid JSON
    with these exact keys:

    "score" (overall score, a number from 0 to 10),
    "technical_accuracy" (a number from 0 to 10, how factually correct the answer is),
    "communication" (a number from 0 to 10, how clearly it was explained),
    "relevance" (a number from 0 to 10, how directly it answers the question),
    "strengths" (2-3 sentences describing specifically what was good about the answer),
    "weaknesses" (2-3 sentences describing specifically what was missing or wrong),
    "tips" (1-2 concrete, actionable tips to improve this exact answer),
    "model_answer" (a short 2-4 sentence example of a strong answer to this question)
    """

    reply =ask_groq (
    prompt ,
    system_message =(
    "You are a fair, detail-oriented interview evaluator. "
    "Be specific and reference the candidate's actual words where useful. "
    "Reply only in JSON."
    ),
    )
    return safe_json_parse (reply )


def generate_final_report (all_feedback ,job_role ,interview_type ):


    feedback_text =json .dumps (all_feedback ,indent =2 )

    prompt =f"""
    Below is the detailed feedback for every question of a {interview_type } interview
    for the role of "{job_role }".

    {feedback_text }

    Based on this, write a detailed final report. Return ONLY valid JSON
    with these exact keys:

    "overall_score" (a number from 0 to 10, the average performance),
    "technical_score" (a number from 0 to 10),
    "communication_score" (a number from 0 to 10),
    "skill_analysis" (a detailed paragraph on how well the candidate's
        skills matched the role, mentioning specific topics from the answers),
    "strengths" (a detailed paragraph listing the candidate's strongest points,
        with specific examples from their answers),
    "weaknesses" (a detailed paragraph listing the candidate's weak points,
        with specific examples from their answers),
    "improvements" (a detailed paragraph with concrete next steps the
        candidate should work on before their real interview),
    "recommendation" (one of: "Strongly Recommended", "Recommended", "Needs Improvement", "Not Recommended")
    """

    reply =ask_groq (
    prompt ,
    system_message =(
    "You are a senior hiring manager writing a detailed, specific final "
    "interview report based on real evidence from the answers. Reply only in JSON."
    ),
    )
    return safe_json_parse (reply )


def transcribe_audio (audio_bytes ):

    client =get_groq_client ()

    transcription =client .audio .transcriptions .create (
    file =("answer.wav",audio_bytes ),
    model ="whisper-large-v3-turbo",
    response_format ="text",
    language ="en",
    )
    return str (transcription ).strip ()


def analyze_resume_ats (resume_text ,job_description =""):


    jd_block =(
    f"Target Job Description:\n{job_description }\n"
    if job_description else 
    "No specific job description was provided, so score this resume "
    "generically against strong ATS and recruiter practices for its "
    "apparent field.\n"
    )

    prompt =f"""
    You are an ATS (Applicant Tracking System) resume scoring engine.
    Evaluate the resume below{" against the job description"if job_description else ""}.

    {jd_block }

    Resume Text:
    {resume_text }

    Return ONLY valid JSON with these exact keys:

    "ats_score" (overall ATS compatibility score, a number from 0 to 100),
    "keyword_match_score" (0 to 100, how well the resume's keywords/skills
        match the target role or field),
    "formatting_score" (0 to 100, how ATS-friendly the formatting/structure is:
        standard section headers, no tables/columns issues, parseable text),
    "structure_score" (0 to 100, presence of key sections like contact info,
        summary, skills, experience, education, and clear reverse-chronological order),
    "matched_keywords" (a list of important skills/keywords found in the resume),
    "missing_keywords" (a list of important skills/keywords that are missing
        or under-represented, based on the job description or the resume's field),
    "strengths" (2-4 sentences on what the resume does well),
    "weaknesses" (2-4 sentences on what is holding the ATS score back),
    "suggestions" (3-5 concrete, actionable bullet-style improvements,
        as a single string with each suggestion on its own line)
    """

    reply =ask_groq (
    prompt ,
    system_message =(
    "You are a precise, detail-oriented ATS resume scoring engine. "
    "Be specific and reference the resume's actual content. Reply only in JSON."
    ),
    )
    return safe_json_parse (reply )


def safe_json_parse (text ):


    cleaned =text .strip ()
    cleaned =cleaned .replace ("```json","").replace ("```","")

    try :
        return json .loads (cleaned )
    except json .JSONDecodeError :

        start =cleaned .find ("{")
        end =cleaned .rfind ("}")
        if start !=-1 and end !=-1 :
            try :
                return json .loads (cleaned [start :end +1 ])
            except json .JSONDecodeError :
                return {}
        return {}
