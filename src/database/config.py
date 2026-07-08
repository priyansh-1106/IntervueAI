

import streamlit as st 
from supabase import create_client 


def get_supabase_client ():

    url =st .secrets ["SUPABASE_URL"]
    key =st .secrets ["SUPABASE_KEY"]



    if "your-project-id"in url or "your-supabase"in key :
        st .error (
        "Supabase is not configured yet. Open .streamlit/secrets.toml "
        "and replace SUPABASE_URL and SUPABASE_KEY with the real values "
        "from your Supabase project's Settings > API page, then restart the app."
        )
        st .stop ()

    client =create_client (url ,key )
    return client 



supabase =get_supabase_client ()
