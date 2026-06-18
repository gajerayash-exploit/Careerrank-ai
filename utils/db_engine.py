import os
from supabase import create_client, Client
import streamlit as st
import uuid
import json

def get_supabase_client():
    url = st.session_state.get('supabase_url', '')
    key = st.session_state.get('supabase_key', '')
    if not url or not key:
        return None
    try:
        supabase: Client = create_client(url, key)
        return supabase
    except Exception as e:
        print("Supabase connection error:", e)
        return None

def save_analysis_to_db(jd_text, results):
    supabase = get_supabase_client()
    if not supabase:
        return False
        
    try:
        # Create a safe JSON payload
        payload = {
            "id": str(uuid.uuid4()),
            "job_description": jd_text,
            "results": json.dumps([{
                "name": r.get("Candidate Name"),
                "email": r.get("Email"),
                "score": r.get("Match Score"),
                "rank": r.get("Rank"),
                "recommendation": r.get("Recommendation")
            } for r in results])
        }
        # Assuming table name is 'analysis_history'
        response = supabase.table('analysis_history').insert(payload).execute()
        return True
    except Exception as e:
        print("Error saving to Supabase:", e)
        return False

def get_analysis_history():
    supabase = get_supabase_client()
    if not supabase:
        return []
    try:
        response = supabase.table('analysis_history').select("*").execute()
        return response.data
    except Exception as e:
        print("Error fetching from Supabase:", e)
        return []
