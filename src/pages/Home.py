

import streamlit as st 
from model .interview import get_dashboard_stats 
from utils .helper import page_header 


def render ():


    page_header ("🏠 Dashboard","Your interview practice overview")

    user_id =st .session_state .get ("user_id")
    user_name =st .session_state .get ("user_name","User")

    total_interviews ,average_score =get_dashboard_stats (user_id )

    st .markdown (f"### Welcome, {user_name } 👋")
    st .write ("Here is a quick summary of your interview practice so far.")

    col1 ,col2 =st .columns (2 )
    with col1 :
        st .metric ("📊 Total Interviews",total_interviews )
    with col2 :
        st .metric ("⭐ Average Score",f"{average_score } / 10")

    st .markdown ("---")

    with st .container (border =True ):
        st .markdown ("#### 🎯 Ready to practice?")
        st .write ("Start a new mock interview based on your resume and a job description.")
        if st .button ("🚀 Start Interview",use_container_width =True ):
            st .session_state ["current_page"]="Interview"
            st .rerun ()
