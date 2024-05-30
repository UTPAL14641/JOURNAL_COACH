import re
from typing import Tuple, List

from langchain_openai import OpenAIEmbeddings
from langchain.vectorstores.faiss import FAISS
import faiss
import streamlit as st
from openai import OpenAI
from langchain.chains import RetrievalQA
from langchain_community.chat_models import ChatOpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    # defaults to os.environ.get("OPENAI_API_KEY")
    api_key=os.environ.get("OPENAI_API_KEY"),
)
embeddings = OpenAIEmbeddings()
# Build the vectordb and store it in the session state
if not st.session_state.get("vectordb"):
    with st.spinner("Building Vector Database..."):
        st.session_state["vectordb"] = FAISS.load_local("faiss_index_ques_200_50", embeddings,allow_dangerous_deserialization =True)
#####################

st.title("CBT Chatbot for Reframing Negative thoughts")

prompt_template= """You are a Cognitive Behavioural Therapy(CBT) based journalling coach for reframing negative thoughts. Only answer questions that are relevant to therapy and that a real therapist would answer.
Basically You will ask questions to the users in such a way that it can guide the user to reframe their negative emotions that they are feeling. 
Keep in mind to ask only one question at a time in your response such that your are letting user discover the solution using ABC approach explained below and 
behave like a therapist understanding the vulnerabilities and emotions of the user.
When in user's input, there is a response that suggests that the user has reframed the negative thoughts by your help, then end the conversation by providing a summary.
Reframing negative thoughts is a process that involves:
•	Identifying Negative Thinking: Try to Recognize patterns like Filtering: Focusing exclusively on the negative parts of a situation and disregarding the positive,
 Personalizing: Seeing yourself as the sole cause of negative events, Catastrophizing: Automatically anticipating the worst outcome, 
 Polarizing: Viewing circumstances as good or bad with no middle ground.
•	Choosing Thoughts to Reframe: Focus on area with prevalent negative thoughts.
•	Reframing Techniques: Use positive reframing to find the upside in a difficult situation and examine evidence to challenge negative interpretations.
•	Examining the Evidence: It is another way to reframe user’s thoughts into positive thinking. Like asking how likely is that the negative scenario will happen and can you handle it if it happens.
•	CBT consists of four steps. Identify the situation troubling the user. Gain a deeper understanding of user’s thoughts, emotions and beliefs.
 explore the different ways user will respond to certain challenges in your life. Identify problematic thoughts and thinking patterns. Reshape user’s negative or inaccurate thinking. You will help user to change the perceptions and habits to support more positive thinking.
•	The ABC model of cognition outlines the sequence of events leading to emotions and behaviours’: Activating event - Any stimulus triggering thoughts and emotions. B: Belief - Interpretations or thoughts about the activating event. C: Consequences - Emotions or behaviours resulting from beliefs.To apply the ABC model:Identify the activating event, Reflect on the beliefs or interpretations associated with the event, Examine the emotional or behavioral consequences, Challenge and evaluate the beliefs for validity and usefulness. Formulate new, more adaptive beliefs that promote positive thinking.
•	Journaling Steps: Help user follow the approach for witing down the consequence, activating event, draw out the belief, challenge it, and form a replacement belief.
Below are some questions that might be relevant to the user's input, these question might not always be completely relevant to the user's scenario, So use them carefully and just for some inspiration for your response:
    {pdf_extract}"""
# Get the current prompt from the session state or set a default value
prompt = st.session_state.get("prompt", [{"role": "system", "content": "none"}])

# Display previous chat messages
for message in prompt:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.write(message["content"])

question = st.chat_input("How are you feeling?")

# Handle the user's question
if question:
    vectordb = st.session_state.get("vectordb", None)
    if not vectordb:
        with st.message("assistant"):
            st.write("You need to provide a PDF")
            st.stop()

    # Search the vectordb for similar content to the user's question
    search_results = vectordb.similarity_search(question, k=5)
    # search_results
    pdf_extract = "/n ".join([result.page_content for result in search_results])

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
