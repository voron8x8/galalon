#TO DO:
#Loading animation
#Stream messages
#Hebrew texts
#RTL layout
#Repo on github and share with Ron and Alec

import streamlit as st
import anthropic
from dotenv import load_dotenv
import os
import time

# Set page configuration
st.set_page_config(layout="wide", page_title="Almabot")
st.header("AlmaBot - Lesson Planner")

# Load environment variables (e.g., API key)
load_dotenv()
api_key = os.getenv("ANTHROPIC_API_KEY")

# Initialize Anthropic client
client = anthropic.Anthropic(api_key=api_key)

# Define system prompt
system_prompt = """You are AlmaBot, a professional lesson planner for elementary school education in Israel. You adhere to the needs of elementary school teachers in Israel by planning lessons according to a specific paradigm that caters to the diverse needs, knowledge, and skills of individual learners. By planning lessons and encouraging active learning, teachers can support the needs of each individual student. This is achieved by creating a diverse and challenging learning environment adapted to the various learners. The lesson should be integrated into the physical environment of the class, allowing and encouraging students to make choices and elicit active learning, cooperation, and enablement of learning through creation, construction, and play.

Here is the outline of an ideal lesson that will apply this paradigm in class:

Opening (5 minutes) - Lay the background of the lesson by connecting the lesson topic to previous lessons and highlight its relevance for the students.

Plenary session (15 minutes) - This part of the lesson focuses on the acquisition of skills and new knowledge facilitated by the teacher.

Groups session (20 minutes) - The class is divided into groups according to each student's level:

- Group 1 ("with the teacher") contains the students who are struggling to acquire the skills and/or new knowledge. The teacher repeats concepts from the plenary session and establishes what was learned.

- Group 2 ("next to the teacher") and Group 3 ("in the space") contain intermediate and strong students who apply the knowledge and skills through independent learning activities, such as worksheets, projects, or inquiry-based tasks.

Summary (5 minutes) - The entire class convenes, summarizes the acquired knowledge, reflects on the lesson objectives, and provides feedback through various means (e.g., worksheet, discussion, visual/auditory aids)."""

# Define user prompt template
initial_user_prompt = """Hi, my name is {teacher_name}. I'm planning a lesson for {class_grade} on {lesson_topic}. The main goals are:
- {generic_goals}
- {content_specific_goals}

The lesson will span {number_of_lessons} sessions, each 45 minutes long. I prefer to open the lesson with {opening_session_preferences}. Here are some ideas for the plenary session:
- {plenary_session_ideas}

For Group 1 (struggling students), the students are: {group_1_students_first_names}. The skills/knowledge they should acquire are: {group1_skills}. Some ideas for Group 1 activities:
- {group1_activity_ideas}
Their understanding should be assessed by: {group1_assessment}

For Group 2 (intermediate students), the students are: {group_2_students_first_names}. Some ideas for Group 2 activities:
- {group2_activity_ideas}

For Group 3 (strong students), they should work as {group3_learning_type}. Some ideas for Group 3 activities:
- {group3_activity_ideas}

Some ideas for the summary session:
- {summary_session_ideas}

Please provide a detailed lesson plan in {preferred_language}."""

# Streamlit app
def main():

    # Initialize chat history
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

    # Initialize form submission state
    if 'form_submitted' not in st.session_state:
        st.session_state.form_submitted = False

    # Collect form data
    with st.form("test_form"):
        st.write("Please fill out the form:")

        teacher_name = st.text_input("Teacher's Name", value="שרה כהן")
        class_grade = st.text_input("Class Grade", value="כיתה ג'")
        lesson_topic = st.text_input("Lesson Topic", value="מחזור המים בטבע")
        generic_goals = st.text_area("Generic Goals", value="התלמידים יבינו את חשיבות המים לחיים ויכירו את שלבי מחזור המים בטבע.")
        content_specific_goals = st.text_area("Content Specific Goals", value="התלמידים יוכלו לתאר את תהליך האידוי, העיבוי והמשקעים. התלמידים יבינו כיצד מחזור המים משפיע על הסביבה.")
        number_of_lessons = st.number_input("Number of Lessons (45 minutes each)", min_value=1, step=1, value=1)
        opening_session_preferences = st.text_area("Preferences for Opening Session", value="הצגת סרטון קצר על מחזור המים בטבע")
        plenary_session_ideas = st.text_area("Ideas for Plenary Session", value="הסבר על שלבי מחזור המים תוך שימוש באיורים ותמונות")
        group_1_students_first_names = st.text_input("Group 1 Students' First Names", value="דוד, יעל, רון, דניאל")
        group_2_students_first_names = st.text_input("Group 2 Students' First Names", value="מאיה, יונתן, שירה, אלון")
        group1_skills = st.text_area("Skills for Group 1", value="זיהוי שלבי מחזור המים, הבנת חשיבות המים לחיים")
        group1_activity_ideas = st.text_area("Group 1 Activity Ideas", value="אין לי רעיונות")
        group1_assessment = st.text_area("Group 1 Assessment", value="אין לי רעיונות")
        group2_activity_ideas = st.text_area("Group 2 Activity Ideas", value="אין לי רעיונות")
        group3_learning_type = st.text_input("Group 3 Learning Type", value="זוגות")
        group3_activity_ideas = st.text_area("Group 3 Activity Ideas", value="אין לי רעיונות")
        summary_session_ideas = st.text_area("Summary Session Ideas", value="אין לי רעיונות")
        preferred_language = st.selectbox("Preferred Language", options=["Hebrew", "English"], index=0)

        submitted = st.form_submit_button("Generate Lesson Plan", disabled=st.session_state.form_submitted)

    if submitted:
        st.session_state.form_submitted = True

        # Format user prompt with form data
        user_prompt = initial_user_prompt.format(
            teacher_name=teacher_name,
            class_grade=class_grade,
            lesson_topic=lesson_topic,
            generic_goals=generic_goals,
            content_specific_goals=content_specific_goals,
            number_of_lessons=number_of_lessons,
            opening_session_preferences=opening_session_preferences,
            plenary_session_ideas=plenary_session_ideas,
            group_1_students_first_names=group_1_students_first_names,
            group_2_students_first_names=group_2_students_first_names,
            group1_skills=group1_skills,
            group1_activity_ideas=group1_activity_ideas,
            group1_assessment=group1_assessment,
            group2_activity_ideas=group2_activity_ideas,
            group3_learning_type=group3_learning_type,
            group3_activity_ideas=group3_activity_ideas,
            summary_session_ideas=summary_session_ideas,
            preferred_language=preferred_language,
        )

        # Add user prompt to chat history
        st.session_state.chat_history.append({"role": "user", "content": user_prompt})

        # Get initial response from Anthropic API
        initial_response = client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=2000,
            system=system_prompt,
            messages=st.session_state.chat_history
        )

        # Extract text content from API response
        initial_response_text = initial_response.content[0].text
        print("initial response text is:")
        print(initial_response_text)

        # Add initial response to chat history
        st.session_state.chat_history.append({"role": "assistant", "content": initial_response_text})

    # Display chat messages
    for message in st.session_state.chat_history:
        if message["role"] == "user":
            with st.chat_message("user"):
                st.markdown(message["content"])
        else:
            with st.chat_message("assistant"):
                st.markdown(message["content"])
        print("role: " + message["role"])
        print("message content: " + message["content"])

    # Get user input from chat
    user_input = st.chat_input("Enter your message:")

    if user_input:
        # Add user input to chat history
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        # Display new chat messages
        with st.chat_message("user"):
            st.markdown(user_input)

        # Show loading animation
        with st.chat_message("assistant"):
            loading_placeholder = st.empty()
            loading_placeholder.markdown("אני חושב.ת...")

            # Get response from Anthropic API based on user input
            following_response = client.messages.create(
                model="claude-3-opus-20240229",
                max_tokens=1024,
                system=system_prompt,
                messages=st.session_state.chat_history
            )

            # Extract text content from API response
            following_response_text = following_response.content[0].text
            print("following response text is:")
            print(following_response_text)

            # Add response to chat history
            st.session_state.chat_history.append({"role": "assistant", "content": following_response_text})

            # Clear the loading animation and display the response
            loading_placeholder.empty()
            st.markdown(following_response_text)

        print('chat history thus far:')
        print(st.session_state.chat_history)

if __name__ == "__main__":
    main()