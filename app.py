import os 
import sys 

sys .path .insert (0 ,os .path .join (os .path .dirname (os .path .abspath (__file__ )),"src"))

import streamlit as st 
from auth .login import show_login_form ,logout_user 
from auth .signup import show_signup_form 
from utils .helper import load_css 

from pages import Home ,Interview ,History ,Tips ,ResumeAnalyzer ,ResumeHistory 

st .set_page_config (page_title ="IntervueAI",page_icon ="📸",layout ="wide",initial_sidebar_state ="expanded")

st .markdown (f"<style>{load_css ('src/css/style.css')}</style>",unsafe_allow_html =True )

NAV_ITEMS =[
("Home","🏠","Home"),
("Take Interview","📸","Interview"),
("Resume Analyzer","📄","ResumeAnalyzer"),
("Resume History","🗐","ResumeHistory"),
("Interview History","📜","History"),
("Tips","💡","Tips"),
]


def show_auth_screen ():
    st .markdown (
    "<div class='auth-brand'>"
    "<h1>IntervueAI 📄</h1>"
    "<p>AI Powered RAG Interview Assistant</p>"
    "</div>",
    unsafe_allow_html =True ,
    )

    col1 ,col2 ,col3 =st .columns ([1 ,1.2 ,1 ])
    with col2 :
        with st .container (border =True ):
            login_tab ,signup_tab =st .tabs (["Login","Sign Up"])
            with login_tab :
                show_login_form ()
            with signup_tab :
                show_signup_form ()


def show_sidebar ():
    if "current_page"not in st .session_state :
        st .session_state ["current_page"]="Home"

    with st .sidebar :
        st .markdown (
        "<div class='sidebar-brand'>"
        "<h1 class='sidebar-brand-name' style = 'margin-bottom : 20px; font-size: 36px;'>IntervueAI 📄</h1>"
        "</div>",
        unsafe_allow_html =True ,
        )

        st .markdown ("---")
        st .space ()

        for label ,icon ,page_name in NAV_ITEMS :
            is_active =st .session_state ["current_page"]==page_name 
            wrapper_class ="active-nav"if is_active else ""
            st .markdown (f"<div class='{wrapper_class }'>",unsafe_allow_html =True )
            if st .button (f"{icon }  {label }",use_container_width =True ,key =f"nav_{page_name }"):
                st .session_state ["current_page"]=page_name 
                st .rerun ()
            st .markdown ("</div>",unsafe_allow_html =True )

        st .markdown ("<div class='sidebar-logout' style='margin-top: 180px;'>",unsafe_allow_html =True )
        st .markdown ("---")
        if st .button ("↙️ Logout",use_container_width =True ):
            logout_user ()
        st .markdown ("</div>",unsafe_allow_html =True )

    return st .session_state ["current_page"]


def main ():
    if not st .session_state .get ("logged_in",False ):
        show_auth_screen ()
        return 

    page =show_sidebar ()

    if page =="Home":
        Home .render ()
    elif page =="Interview":
        Interview .render ()
    elif page =="ResumeAnalyzer":
        ResumeAnalyzer .render ()
    elif page =="ResumeHistory":
        ResumeHistory .render ()
    elif page =="History":
        History .render ()
    elif page =="Tips":
        Tips .render ()


if __name__ =="__main__":
    main ()
