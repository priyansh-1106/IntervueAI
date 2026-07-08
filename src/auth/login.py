

import streamlit as st 
from database .config import supabase 
from utils .helper import check_password 


def show_login_form ():


    st .subheader ("Login to your account")

    with st .form ("login_form"):
        email =st .text_input ("Email",key ="login_email",placeholder ="you@example.com")
        password =st .text_input ("Password",type ="password",key ="login_password",placeholder ="Your password")
        submitted =st .form_submit_button ("Login",use_container_width =True ,type ="primary")

    if submitted :
        login_user (email ,password )


def login_user (email ,password ):


    if not email or not password :
        st .error ("Please enter both email and password.")
        return 

    result =supabase .table ("users").select ("*").eq ("email",email ).execute ()

    if len (result .data )==0 :
        st .error ("No account found with this email.")
        return 

    user =result .data [0 ]

    if check_password (password ,user ["password"]):

        st .session_state ["logged_in"]=True 
        st .session_state ["user_id"]=user ["id"]
        st .session_state ["user_name"]=user ["name"]
        st .session_state ["user_email"]=user ["email"]

        st .success (f"Welcome back, {user ['name']}!")
        st .rerun ()
    else :
        st .error ("Incorrect password. Please try again.")


def logout_user ():

    for key in ["logged_in","user_id","user_name","user_email"]:
        if key in st .session_state :
            del st .session_state [key ]
    st .rerun ()
