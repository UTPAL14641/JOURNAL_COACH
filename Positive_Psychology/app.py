import streamlit as st
import openai
from dotenv import load_dotenv
import os
from openai import OpenAI
# Load environment variables
load_dotenv()
client = OpenAI(
    # defaults to os.environ.get("OPENAI_API_KEY")
    api_key=os.environ.get("OPENAI_API_KEY"),
)
# Survey Questions and Details
questions = [
    ("To what extent is your work purposeful and meaningful?", "0 = not at all, 10 = completely", "M1"),
    ("How often do you feel you are making progress towards accomplishing your work-related goals?", "0 = never, 10 = always", "A1"),
    ("At work, how often do you become absorbed in what you are doing?", "0 = never, 10 = always", "E1"),
    ("In general, how would you say your health is?", "0 = terrible, 10 = excellent", "H1"),
    ("At work, how often do you feel joyful?", "0 = never, 10 = always", "P1"),
    ("To what extent do you receive help and support from coworkers when you need it?", "0 = not at all, 10 = completely", "R1"),
    ("At work, how often do you feel anxious?", "0 = never, 10 = always", "N1"),
    ("How often do you achieve the important work goals you have set for yourself?", "0 = never, 10 = always", "A2"),
    ("In general, to what extent do you feel that what you do at work is valuable and worthwhile?", "0 = not at all, 10 = completely", "M2"),
    ("At work, how often do you feel positive?", "0 = never, 10 = always", "P2"),
    ("To what extent do you feel excited and interested in your work?", "0 = not at all, 10 = completely", "E2"),
    ("How lonely do you feel at work?", "0 = not at all, 10 = completely", "Lon"),
    ("How satisfied are you with your current physical health?", "0 = not at all, 10 = completely", "H2"),
    ("At work, how often do you feel angry?", "0 = never, 10 = always", "N2"),
    ("To what extent do you feel appreciated by your coworkers?", "0 = not at all, 10 = completely", "R2"),
    ("How often are you able to handle your work-related responsibilities?", "0 = never, 10 = always", "A3"),
    ("To what extent do you generally feel that you have a sense of direction in your work?", "0 = not at all, 10 = completely", "M3"),
    ("Compared to others of your same age and sex, how is your health?", "0 = terrible, 10 = excellent", "H3"),
    ("How satisfied are you with your professional relationships?", "0 = not at all, 10 = completely", "R3"),
    ("At work, how often do you feel sad?", "0 = never, 10 = always", "N3"),
    ("At work, how often do you lose track of time while doing something you enjoy?", "0 = never, 10 = always", "E3"),
    ("At work, to what extent do you feel contented?", "0 = not at all, 10 = completely", "P3"),
    ("Taking all things together, how happy would you say you are with your work?", "0 = not at all, 10 = completely", "hap")
]

# Initialize session state variables
if 'responses' not in st.session_state:
    st.session_state.responses = [None] * len(questions)
if 'current_question' not in st.session_state:
    st.session_state.current_question = 0
if 'submitted' not in st.session_state:
    st.session_state.submitted = False
if 'summary' not in st.session_state:
    st.session_state.summary = ""

# Function to save response and navigate
def save_response(response):
    st.session_state.responses[st.session_state.current_question] = response
    if st.session_state.current_question < len(questions) - 1:
        st.session_state.current_question += 1
    else:
        st.session_state.submitted = True

# Function to process data
def get_completion(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = client.chat.completions.create(
        model=model,messages=messages,temperature=0,)
    return response.choices[0].message.content

def process_data(responses):
    prompt = "Here are the responses to the survey:\n"
    for i, response in enumerate(responses):
        question_text = questions[i][0]
        prompt += f"Q{i+1}: {question_text}\nResponse: {response}/10\n"

    prompt += """\nYou are a real journaling coach that follow positive psychology in your session specifically the PERMA model.
      provide an extensive summary and analysis of the following survey responses. The ratings are based out of 10.
        keep it short and to the point without loosing important semantic information about the user.Understand the points where the patient needs helps and where he is doing good."""
    
    try:
        print(prompt)
        summary = get_completion(prompt)
        return summary
    except Exception as e:
        return f"An error occurred: {str(e)}"

# Display survey or summary based on submission status
if not st.session_state.submitted:
    question, anchors, label = questions[st.session_state.current_question]
    st.write(f"Q{st.session_state.current_question + 1}: {question}")
    st.write(f"Response Anchors: {anchors}")
    response = st.slider(label, 0, 10, 3, key=st.session_state.current_question)
    st.button("Next", on_click=save_response, args=(response,))
else:
    st.write("Thank you for completing the survey!")
    st.write("Here are your responses:")
    for i, response in enumerate(st.session_state.responses):
        st.write(f"Q{i+1}: {questions[i][0]}")
        st.write(f"Response: {response}")

    if not st.session_state.summary:
        st.session_state.summary = process_data(st.session_state.responses)

    st.write("Summary of responses:")
    st.write(st.session_state.summary)

# Chatbot section
st.title("PERMA Model for Positive Psychology")
form_summary = st.session_state.summary
prompt_template= """
You are a Real Journaling coach named Kingsley that does Positive Psychology-based therapy using PERMA model. 
Behave like a Real Human therapist by responding compassionately as an expert understanding the vulnerabilities and emotions of the user. 
Coaches apply the PERMA model to enhance well-being in personal and workplace settings. Don't mention anything about PERMA model in your responses. Respond breifly and to the point using the survey summary and earlier chat information with short assesment and one question for user to repond.
The PERMA Model identifies five elements essential for happiness and well-being:
Positive Emotion (P)
Description: Experiencing joy, gratitude, and other positive emotions.
Application Steps:
Daily Gratitude Exercise: Encourage listing three things they are grateful for.
Positive Visualization: Guide users to visualize positive future events.
Savoring Exercises: Teach individuals to fully engage in and reflect on joyful experiences.
Example: Suggest keeping a gratitude journal noting positive work experiences.

Engagement (E)
Description: Being deeply involved in activities that induce a state of "flow."
Application Steps:
Identify Strengths: Help find strengths and interests.
Flow Activities: Promote activities that fully absorb individuals.
Example: Create an engagement room with resources for hobbies.

Relationships (R)
Description: Building and maintaining supportive and positive connections.
Application Steps:
Foster Teamwork: Encourage team-building activities.
Social Support Networks: Help build support networks.
Regular Check-ins: Implement regular one-on-one meetings.
Example: Organize monthly team-building activities.

Meaning (M)
Description: Having a sense of purpose and being part of something greater.
Application Steps:
Define Values: Assist in identifying core values.
Purpose-Driven Projects: Encourage participation in meaningful projects.
Volunteer Opportunities: Provide opportunities for community service.
Example: Launch corporate social responsibility initiatives.

Accomplishments (A)
Description: Achieving goals and feeling competent.
Application Steps:
Set Goals: Help set realistic goals.
Regular Feedback: Provide constructive feedback.
Celebrate Successes: Foster a culture of celebrating achievements.
Example: Establish a “Kudos Wall” for recognizing achievements.

Applying the PERMA Model in the Workplace
Positive Emotion: Encourage appreciation. Example: Send thank-you notes for good work.
Engagement: Provide hobby resources. Example: Set up a creative space.
Relationships: Foster community. Example: Organize team lunches.
Meaning: Connect to larger purposes. Example: Engage in community service.
Accomplishments: Recognize success. Example: Implement an employee recognition program.
Do's and Don'ts
Do's:
Encourage regular gratitude exercises and positive visualization.
Identify and promote activities that fully engage individuals.
Foster teamwork and build supportive social networks.
Help individuals find and participate in meaningful projects.
Set realistic goals and provide regular, constructive feedback.
Don'ts:
Don't expect individuals to be happy 100% of the time.
Don't neglect the importance of personal strengths and interests.
Don't overlook the need for regular check-ins and support.
Don't ignore the need for purpose and meaning in activities.
Don't delay recognition of accomplishments to annual events only.
Below is the summary of the survey form based on PERMA model taken by user which you can use to address users condition more effectively:
"""
prompt_template+=form_summary
prompt = st.session_state.get("prompt", [{"role": "system", "content": "none"}])

# Display previous chat messages
for message in prompt:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.write(message["content"])

question = st.chat_input("Share with me anything that is bothering you and you want to work on")

if question:
    # search_results
    pdf_extract = ""
    # Update the prompt with the pdf extract
    prompt[0] = {
        "role": "system",
        "content": prompt_template.format(pdf_extract=pdf_extract),
    }
    # Add the user's question to the prompt and display it
    prompt.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.write(question)

    # Display an empty assistant message while waiting for the response
    with st.chat_message("assistant"):
        botmsg = st.empty()

    # Call ChatGPT with streaming and display the response as it comes
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

    # Add the assistant's response to the prompt
    prompt.append({"role": "assistant", "content": result})

    # Store the updated prompt in the session state
    st.session_state["prompt"] = prompt
    prompt.append({"role": "assistant", "content": result})

    # Store the updated prompt in the session state
    st.session_state["prompt"] = prompt

