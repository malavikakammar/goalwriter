from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai

# Load environment variables from .env
load_dotenv()

# Configure the Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Initialize Streamlit app
st.set_page_config(page_title="Goal Writer Application")
st.header("Goal Writer Application")

# Initialize session state if it doesn't exist
if 'step' not in st.session_state:
    st.session_state.step = 0  # Track the current step of the conversation
    st.session_state.reason = None
    st.session_state.salary_hike = None
    st.session_state.role_change = None
    st.session_state.other_reason = None
    st.session_state.relocation_location = None  # Added for relocation option
    st.session_state.change_timing = None
    st.session_state.final_statement = None  # To store the final statement

# Function to generate responses from Gemini
def get_gemini_response(input_text):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(input_text)
    return response.text

# Step-based conversation for goal writer
if st.session_state.step == 0:
    # Input section for goals
    goal_input = st.text_input("Input your goal: ", key="goal_input")
    goal_submit = st.button("Submit Goal")
    if goal_submit:
        goal_response = get_gemini_response(goal_input)
        st.subheader("AI Response:")
        #st.write(goal_response)
        if "I want to change my job" in goal_input:
            st.session_state.step = 1
            st.subheader("Why do you want to change your job?")
            # Use radio buttons to display the options in bullet point (dot) format
            reasons = [
                "Seeking better salary",
                "Looking for more growth opportunities",
                "Wanting a better work-life balance",
                "Relocation for personal reasons",
                "Other"
            ]
            st.session_state.reason = st.radio("Select an option:", reasons)

elif st.session_state.step == 1:
    # Ensure that the salary, role, other reason, and location fields are reset on each step to avoid overlap.
    st.session_state.salary_hike = None
    st.session_state.role_change = None
    st.session_state.other_reason = None
    st.session_state.relocation_location = None

    if st.session_state.reason == "Seeking better salary":
        st.subheader("How much salary are you looking for?")
        st.session_state.salary_hike = st.text_input("Enter the expected salary hike (%):")
        if st.button("Submit Salary"):
            st.write(f"Got it! You're looking for a salary hike of: {st.session_state.salary_hike}%.")
            st.session_state.step = 3
    elif st.session_state.reason == "Looking for more growth opportunities":
        st.subheader("What role are you looking for?")
        st.session_state.role_change = st.text_input("Enter the desired role:")
        if st.button("Submit Role"):
            st.write(f"Great choice! You're looking for a role in: {st.session_state.role_change}.")
            st.session_state.step = 3
    elif st.session_state.reason == "Relocation for personal reasons":
        st.subheader("Which location do you want to relocate to?")
        st.session_state.relocation_location = st.text_input("Enter the location:")
        if st.button("Submit Location"):
            st.write(f"Got it! You're considering relocating to: {st.session_state.relocation_location}.")
            st.session_state.step = 3
    elif st.session_state.reason == "Other":
        st.subheader("Please state your reason:")
        st.session_state.other_reason = st.text_input("Enter the reason:")
        if st.button("Submit Reason"):
            st.write(f"Thanks for sharing! Your reason for wanting to change is: {st.session_state.other_reason}.")
            st.session_state.step = 3

elif st.session_state.step == 3:
    st.subheader("When do you want to change?")
    change_timing = st.selectbox("Select a timeframe:", ["Immediately", "Within 3 months", "Within 6 months", "Unsure"])
    if st.button("Submit Timing"):
        st.session_state.change_timing = change_timing
        # Create a summary statement based on the selected reason and inputs
        summary = "I want to change my job"
        if st.session_state.reason == "Seeking better salary" and st.session_state.salary_hike:
            summary += f" because of a salary hike of {st.session_state.salary_hike}%."
        elif st.session_state.reason == "Looking for more growth opportunities" and st.session_state.role_change:
            summary += f" to pursue a role in {st.session_state.role_change}."
        elif st.session_state.reason == "Relocation for personal reasons" and st.session_state.relocation_location:
            summary += f" to relocate to {st.session_state.relocation_location}."
        elif st.session_state.reason == "Other" and st.session_state.other_reason:
            summary += f" because: {st.session_state.other_reason}."

        # Adjust wording for "Immediately"
        if st.session_state.change_timing == "Immediately":
            summary += " You want to change your job immediately."
        else:
            summary += f" You want to change your job by {st.session_state.change_timing}."

        st.session_state.final_statement = summary
        st.subheader("Your Summary:")
        st.write(st.session_state.final_statement)

# Optionally, include a reset button to clear session state
if st.button("Reset"):
    st.session_state.clear()