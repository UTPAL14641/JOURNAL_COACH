import streamlit as st
import os
from openai import OpenAI

# Load environment variables
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def get_completion(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = client.chat.completions.create(
        model=model, messages=messages, temperature=0,
    )
    return response.choices[0].message.content

def generate_summary(values, obstacles, obstacle_ratings, action_plan):
    survey_data = f"""
    Values:
    Work/Education: {values['Work/Education']}
    Relationships: {values['Relationships']}
    Leisure: {values['Leisure']}
    Personal Growth/Health: {values['Personal Growth/Health']}

    Obstacles:
    Obstacle 1: {obstacles['Obstacle 1']} (Rating: {obstacle_ratings['Obstacle 1']}/7)
    Obstacle 2: {obstacles['Obstacle 2']} (Rating: {obstacle_ratings['Obstacle 2']}/7)
    Obstacle 3: {obstacles['Obstacle 3']} (Rating: {obstacle_ratings['Obstacle 3']}/7)
    Obstacle 4: {obstacles['Obstacle 4']} (Rating: {obstacle_ratings['Obstacle 4']}/7)

    Action Plan:
    Work/Education: {action_plan['Work/Education']}
    Relationships: {action_plan['Relationships']}
    Leisure: {action_plan['Leisure']}
    Personal Growth/Health: {action_plan['Personal Growth/Health']}
    """

    prompt = f"""
    You are a real Acceptance and Commitment therapist. Provide a summary and analysis of the following survey responses as an Acceptance and Commitment Coach.
    Keep it short and to the point without losing important semantic information about the user:
    {survey_data}.
    """
    try:
        
        summary = get_completion(prompt)
        return summary
    except Exception as e:
        return f"An error occurred: {str(e)}"

def generate_session_summary(prompt):
    session_conversation = "\n".join([f"{msg['role'].capitalize()}: {msg['content']}" for msg in prompt if msg['role'] in ['assistant', 'user']])
    detailed_summary_prompt = f"""
    You are a Real Acceptance and Commitment therapist. Provide a detailed summary of the therapy session with the following points:
    - Initial Issue
    - Therapist's Intervention
    - Key Points Discussed
    - Mood and Attitude analysis
    - Future Actions
    - Next Steps

    Conversation:
    {session_conversation}
    """
    try:
        session_summary = get_completion(detailed_summary_prompt)
        return session_summary
    except Exception as e:
        return f"An error occurred: {str(e)}"

def check_session_completion(prompt):
    session_conversation = "\n".join([f"{msg['role'].capitalize()}: {msg['content']}" for msg in prompt if msg['role'] in ['assistant', 'user']])
    check_completion_prompt = f"""
    You are a Real Acceptance and Commitment therapist. Based on the following conversation, determine if the basic goal of the therapy session has been reached. Answer with a simple 'Yes' or 'No'.

    Conversation:
    {session_conversation}
    """
    try:
        completion_status = get_completion(check_completion_prompt).strip().lower()
        return completion_status == 'yes'
    except Exception as e:
        return f"An error occurred: {str(e)}"

def display_survey():
    st.title("The Bulls-Eye Value Survey")

    st.write("""
    The Bull‘s-Eye Values Survey (BEVS) is a tool for assessing values, values-action discrepancies, 
    and barriers to value-based living. The survey consists of three parts.
    """)

    st.header("Part 1: Identify Your Values")
    values = {
        "Work/Education": st.text_area("Work/Education", "Strive for meaningful and impactful work that challenges my skills and contributes to societal progress."),
        "Relationships": st.text_area("Relationships", "Value deep, supportive, and understanding relationships with friends and family."),
        "Leisure": st.text_area("Leisure", "Engage in activities that bring joy, relaxation, and a sense of achievement."),
        "Personal Growth/Health": st.text_area("Personal Growth/Health", "Focus on mental well-being, physical health, and continuous learning.")
    }

    st.header("Part 2: Identify Your Obstacles")
    obstacles = {
        "Obstacle 1": st.text_area("Obstacle 1", "Depression and lack of motivation."),
        "Obstacle 2": st.text_area("Obstacle 2", "Low-paying job causing financial stress."),
        "Obstacle 3": st.text_area("Obstacle 3", "Isolation and loneliness due to being single."),
        "Obstacle 4": st.text_area("Obstacle 4", "Difficulty in balancing work and personal life.")
    }

    st.write("Rate how much these obstacles prevent you from living in line with your values (1 = Doesn't prevent me at all, 7 = Prevents me completely):")
    obstacle_ratings = {
        "Obstacle 1": st.slider("Obstacle 1 Rating", 5, 7, 7),
        "Obstacle 2": st.slider("Obstacle 2 Rating", 4, 7, 6),
        "Obstacle 3": st.slider("Obstacle 3 Rating", 3, 7, 5),
        "Obstacle 4": st.slider("Obstacle 4 Rating", 3, 7, 5)
    }

    st.header("Part 3: My Valued Action Plan")
    action_plan = {
        "Work/Education": st.text_area("Action Plan for Work/Education", "Look for opportunities to upskill and apply for better positions. Set aside time daily for learning new tools and technologies."),
        "Relationships": st.text_area("Action Plan for Relationships", "Reach out to old friends, join social groups, and consider seeking therapy to help with depression and building connections."),
        "Leisure": st.text_area("Action Plan for Leisure", "Schedule regular activities like hiking, reading, and attending local events to unwind and enjoy."),
        "Personal Growth/Health": st.text_area("Action Plan for Personal Growth/Health", "Establish a routine that includes exercise, healthy eating, and mindfulness practices. Seek professional help for mental health support.")
    }

    if st.button("Submit Survey"):
        summary = generate_summary(values, obstacles, obstacle_ratings, action_plan)
        st.session_state['summary'] = summary
        st.success("Survey Submitted! Here is the summary:")
        st.write(summary)

def chat_with_therapist(summary=""):
    if summary:
        prompt_template = f"""You are a Real Acceptance and Commitment therapist named Alaba, We are having a therapy session. ACT is a therapeutic approach that encourages individuals to accept and integrate challenging thoughts and emotions, focusing on value-driven actions to enhance psychological flexibility, rather than replacing maladaptive thoughts.
        Behave like a Real Human therapist by responding compassionately as an expert understanding the vulnerabilities and emotions of the user. 
        Don't mention anything about ACT technique that you are using in your responses instead just use it for formulating your responses.
        Respond breifly and to the point using the survey summary and earlier chat information with short assesment and one question for user to repond.
        Being a real ACT therapist, you should be able to 'decide when to end the ongoing therapy session with the user', go through complete conversation and decide to end the conversation when needed, don't drag it for too long, When you think that, the goal of the session has been reached,ask the user if they are satisfied with the session and would like to end it, if they respond No then keep going with conversation in similar format of assesment and question, if  yes then respond with the summary of the session with following Subparts: Initial Issue, Step by step analysis of how you helped. 
        Step-by-Step Guide to ACT Sessions:
        Confronting the System: Challenge existing problem-solving strategies.
        Recognizing Control as the Problem: Understand that control strategies can be counterproductive.
        Identifying Cognitive Defusion and Mindfulness: Use mindfulness to reduce the impact of negative thoughts.
        Developing a Transcendent Sense of Self: Separate from and objectively explore personal experiences.
        Promoting Acceptance and Willingness: Embrace experiences in the present moment.
        Clarifying Values: Identify and clarify personal values.
        Establishing Commitment: Commit to actions aligned with personal values.
        Do's and Don'ts:
        Do's:
        Accept thoughts and emotions without judgment.
        Focus on value-driven actions.
        Practice mindfulness to enhance awareness.
        Commit to behaviors that align with personal values.
        Embrace psychological flexibility.
        Don'ts:
        Avoid or suppress negative thoughts and feelings.
        Strive for control over every cognitive or emotional experience.
        Cling to rigid problem-solving strategies.
        Ignore the context of behaviors and emotions.
        Replace maladaptive thoughts without addressing underlying values.

        Below is a summary of the Bull's-Eye Values Survey (BEVS) taken by the user which is a tool for assessing values, values-action discrepancies, 
        and barriers to value-based living and use these information to address users condition more effectively:
        """
        prompt_template += summary
    else:
        prompt_template = """You are a Real Acceptance and Commitment therapist named Alaba, We are having a therapy session. ACT is a therapeutic approach that encourages individuals to accept and integrate challenging thoughts and emotions, focusing on value-driven actions to enhance psychological flexibility, rather than replacing maladaptive thoughts.
        Behave like a Real Human therapist by responding compassionately as an expert understanding the vulnerabilities and emotions of the user. 
        Don't mention anything about ACT technique that you are using in your responses instead just use it for formulating your responses.
        Being a real ACT therapist, you should be able to 'decide when to end the ongoing therapy session with the user', go through complete conversation and decide to end the conversation when needed, don't drag it for too long, When you think that, the goal of the session has been reached,ask the user if they are satisfied with the session and would like to end it, if they respond No then keep going with conversation in similar format of assesment and question, if  yes then respond with the summary of the session with following Subparts: Initial Issue, Step by step analysis of how you helped. 
        Step-by-Step Guide to ACT Sessions:
        Confronting the System: Challenge existing problem-solving strategies.
        Recognizing Control as the Problem: Understand that control strategies can be counterproductive.
        Identifying Cognitive Defusion and Mindfulness: Use mindfulness to reduce the impact of negative thoughts.
        Developing a Transcendent Sense of Self: Separate from and objectively explore personal experiences.
        Promoting Acceptance and Willingness: Embrace experiences in the present moment.
        Clarifying Values: Identify and clarify personal values.
        Establishing Commitment: Commit to actions aligned with personal values.
        Do's and Don'ts:
        Do's:
        Accept thoughts and emotions without judgment.
        Focus on value-driven actions.
        Practice mindfulness to enhance awareness.
        Commit to behaviors that align with personal values.
        Embrace psychological flexibility.
        Don'ts:
        Avoid or suppress negative thoughts and feelings.
        Strive for control over every cognitive or emotional experience.
        Cling to rigid problem-solving strategies.
        Ignore the context of behaviors and emotions.
        Replace maladaptive thoughts without addressing underlying values."""

    st.write("### Chat with the ACT Therapist")
    prompt = st.session_state.get("prompt", [{"role": "system", "content": "none"}])
    interaction_count = st.session_state.get("interaction_count", 0)

    for message in prompt:
        if message["role"] != "system":
            with st.chat_message(message["role"]):
                st.write(message["content"])

    question = st.chat_input("Share with me anything that is bothering you and you want to work on")
    if question:
        prompt[0] = {
            "role": "system",
            "content": prompt_template,
        }
        prompt.append({"role": "user", "content": question})
        with st.chat_message("user"):
            st.write(question)

        with st.chat_message("assistant"):
            botmsg = st.empty()

        response = []
        result = ""
        for chunk in client.chat.completions.create(
            model="gpt-3.5-turbo", messages=prompt, stream=True
        ):
            text = chunk.choices[0].delta.content
            if text is not None:
                response.append(text)
                result = "".join(response).strip()
                botmsg.write(result)

        prompt.append({"role": "assistant", "content": result})
        interaction_count += 2  # Each user input and assistant response is considered one interaction
        st.session_state["prompt"] = prompt
        st.session_state["interaction_count"] = interaction_count

        if interaction_count >= 8:
            if check_session_completion(prompt):
                st.write("### Concluding Remarks")
                st.write("It seems like we have reached the basic goal of this therapy session.")
                if st.button("Continue Session"):
                    st.session_state["interaction_count"] = 0
                if st.button("End Session"):
                    session_summary = generate_session_summary(prompt)
                    st.write(session_summary)
                    st.session_state.clear()
                    st.success("Session ended. Summary provided.")
                    return

    if st.button("End Conversation"):
        session_summary = generate_session_summary(prompt)
        st.write(session_summary)
        st.session_state.clear()
        st.success("Session ended. Summary provided.")

def main():
    st.sidebar.title("Survey Options")
    survey_option = st.sidebar.selectbox("Would you like to attempt the survey?", ("Select an option", "Yes", "No"))

    if survey_option == "Yes":
        display_survey()
    elif survey_option == "No":
        st.sidebar.write("You have opted not to attempt the survey.")
    
    if 'summary' in st.session_state:
        chat_with_therapist(st.session_state['summary'])
    else:
        chat_with_therapist()

if __name__ == "__main__":
    main()
