import json 
import uuid 
import datetime 
import bcrypt 
import streamlit as st 


def hash_password (plain_password ):
    password_bytes =plain_password .encode ("utf-8")
    hashed =bcrypt .hashpw (password_bytes ,bcrypt .gensalt ())
    return hashed .decode ("utf-8")


def check_password (plain_password ,hashed_password ):
    password_bytes =plain_password .encode ("utf-8")
    hashed_bytes =hashed_password .encode ("utf-8")
    return bcrypt .checkpw (password_bytes ,hashed_bytes )


def new_id ():
    return str (uuid .uuid4 ())


def current_timestamp ():
    return datetime .datetime .now ().strftime ("%Y-%m-%d %H:%M:%S")


def current_date ():
    return datetime .date .today ().strftime ("%Y-%m-%d")


def load_css (file_path ):
    with open (file_path ,"r")as css_file :
        return css_file .read ()


def format_list_or_text (value ,empty_message ="Not available"):


    if value is None :
        return empty_message 


    if isinstance (value ,str ):
        stripped =value .strip ()
        if stripped .startswith ("[")and stripped .endswith ("]"):
            try :
                parsed =json .loads (stripped )
                if isinstance (parsed ,list ):
                    value =parsed 
            except (json .JSONDecodeError ,ValueError ):
                pass 

    if isinstance (value ,(list ,tuple )):
        items =[str (item ).strip ()for item in value if str (item ).strip ()]
        if not items :
            return empty_message 
        return "\n".join (f"- {item }"for item in items )

    text =str (value ).strip ()
    return text if text else empty_message 


def page_header (title ,subtitle =""):
    subtitle_html =f"<p style='margin:0; color:#6b7280;'>{subtitle }</p>"if subtitle else ""

    st .markdown (
    f"""
        <div style='display:flex; justify-content:space-between; align-items:center;
                    padding-bottom:14px; margin-bottom:18px; border-bottom:1px solid #e4e9f5;'>
            <div>
                <h2 style='margin:0;'>{title }</h2>
                {subtitle_html }
            </div>
            <div style='color:#9aa4b8; font-size:14px;'>IntervueAI 📄</div>
        </div>
        """,
    unsafe_allow_html =True ,
    )
