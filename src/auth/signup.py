

import streamlit as st 
from database .config import supabase 
from utils .helper import hash_password ,new_id 


def show_signup_form ():


    st .subheader ("Create a new account")

    with st .form ("signup_form"):
        name =st .text_input ("Full Name",key ="signup_name",placeholder ="Your Name")
        email =st .text_input ("Email",key ="signup_email",placeholder ="you@example.com")
        password =st .text_input ("Password",type ="password",key ="signup_password",placeholder ="At least 6 characters")
        confirm_password =st .text_input ("Confirm Password",type ="password",key ="signup_confirm")
        submitted =st .form_submit_button ("Sign Up",use_container_width =True ,type ="primary")

    if submitted :
        create_new_user (name ,email ,password ,confirm_password )


def create_new_user (name ,email ,password ,confirm_password ):



    if not name or not email or not password or not confirm_password :
        st .error ("Please fill in all the fields.")
        return 

    if password !=confirm_password :
        st .error ("Passwords do not match.")
        return 

    if len (password )<6 :
        st .error ("Password should be at least 6 characters long.")
        return 


    existing =supabase .table ("users").select ("*").eq ("email",email ).execute ()
    if len (existing .data )>0 :
        st .error ("An account with this email already exists.")
        return 


    user_id =new_id ()
    hashed_pw =hash_password (password )

    supabase .table ("users").insert ({
    "id":user_id ,
    "name":name ,
    "email":email ,
    "password":hashed_pw ,
    }).execute ()

    st .success ("Account created successfully! Please login now.")
