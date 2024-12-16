import os
import time
import streamlit as st
import google.generativeai as genai

# CONFIG:
modelUsed = "gemini-2.0-flash-exp"
jsonData = {"Name":{"0":"ID_0","2":"ID_2","4":"ID_4","5":"ID_5","6":"ID_6","8":"ID_8","9":"ID_9","10":"ID_10 ","11":"ID_11","12":"ID_12","13":"ID_13","14":"ID_14","15":"ID_ 15","16":"ID_16","17":"ID_17","18":"ID_18","19":"ID_19","20":" ID_20","21":"ID_21","22":"ID_22","23":"ID_23","24":"ID_24","25":"ID_25","26":"ID_26 ","27":"ID_27","28":"ID_28","29":"ID_29","30":"ID_30","31":"ID_31","32":"ID_32","34":"ID_34","35":"ID_35","36":"ID_36","37":"ID_37","38":"ID_38","39":"ID_ 39","40":"ID_40","41":"ID_41","42":"ID_42","43":"ID_43","44":"ID_44","45":"ID_45","47":"ID_47","48":"ID_48","49":"ID_49"," 1":"ID_1"," 3":"ID_3"," 7":"ID_7","33 ":"ID_33"," 46":"ID_46"},"Source":{"0":"Dean","1":"Dean","2":"Dean","3":"Dean","4":"Dean","5":"Dean","6":"Dean","7":"Dean","8":"Dean","9":"Dean","10":"Dean","11":"Dean","12":"Dean","13":"Dean","14":"Dean","15":"Dean","16":"Dean","17":"Dean","18":"Dean","19":"Dean","20":"Dean","21":"Dean","22":" Dean","23":"Dean","24":"Dean","25":"Dean","26":"Dean","27":"Dean","28":"Dean","29":"Dean","30":"Dean","31":"Dean ","32":"Dean","33":"Dean","34":"Dean","35":"Dean","36":"Dean","37":"Dean","38":"Dean","39":"Dean","40":"Dean","41":"Dean","42":"Dean","43":"Dean","44":"Dean","45":"Dean","46":"Dean","47":"Dean","48":"Dean","49":"Dean"},"College":{"0":"JJ","1":"ARC","2":"AGR","3":"A&S","4":"ED","5":"A&S","6":"ARC","7":"AGR","8":"ENG","10":"ED","11":"NUR","12":"PAH","13":"AGR","14":"JJ","15":"ENG","16":"JJ","17":"A& S","18":"NUR","19":"ED","20":"ED","21":"A&S","22":"BUS","23":"ARC","24":"PAH","25":"A&S","26":"A&S","27":"A&S","28":"ENG","29":"ENG","30":"AGR","31":"AGR","32":"ENG","33":"NUR","35":"A&S","36":"AGR","37":"ED","38":"NUR","39":"AGR","40":"ENG","41":"A&S","43":"BUS","44":"ENG","45":"AGR","46":"A&S","47":"ED","48":"PAH","49":"ENG"," 9":"ED"," 34":"AGR"," 42":"A&S"},"Department ":{"0":"School Of Juvenile Justice","1":"School Of Architecture & Art","2":"Cooperative Agricultural Research Center","3":"College Admin. Arts & Science","4":"Curriculum & Instruction","5":"College Admin. Arts & Science","6":"School Of Architecture & Art","7":"Cooperative Agricultural Research Center","8":"Chemical Engineering","9":"Curriculum & Instruction","10":"College Admin - Education","11":"College Admin. - Nursing","12":"School Of Public And Allied  Health","13":"Cooperative Agricultural Research Center","14":"School Of Juvenile Justice","15":"College Of Engineering","16":"School Of Juvenile Justice","17":"Languages & Communication","18":"College Admin. - Nursing","20":"College Admin - Education","21":"Biology","22":"College Admin. - Business","23":"School Of Architecture & Art","24":"School Of Public And Allied Health","25":" Music & Drama","26":"Division Of Social Sciences","27":"Psychology Department","28":"Mechanical Engineering","29":"Electrical Engineering","30":"Cooperative Extension Program","31":"Cooperative Agricultural Research Center","32":"College Of Engineering","33":"Nursing","34":"Cooperative Extension Program","35":"Chemistry","36":"College Of Ag, Food & Natural Resources","37":"Curriculum & Instruction","38":"College Admin. - Nursing","39":"College Of Ag, Food & Natural Resources","40":"Computer Science","41":"Department Of Social Work","42":"Music & Drama","43":"College Admin. - Business","44":"College Of Engineering","46":"College Admin. Arts & Science","47":"College Admin - Education","48":"School Of Public And Allied Health","49":"Transportation Center","1 9":"Curriculum & Instruction","45 ":"College Of Ag, Food & Natural Resources"},"Title":{"0":"Budget Specialist III ","1":"Administrative Associate II","2":"Administrative Associate II","3":"Business Administrator II","4":"Administrative Associate III","5":"Research Program Coordinator","6":"Administrative Coordinator II","7":"Administrative Coordinator II","8":"Senior Administrative Associate ","9":"Program Coordinator I","10":"Senior Administrative Coordinator I","11":"Program Cordinator II","12":"Administrative Associate III","13":"Business Coordinator III","14":"Administrative Associate III","15":"Budget Specialist III ","16":"Administrative Associate III","17":"Administrative Associate V","18":"Administrative Coordinator II","19":"Program Coordinator II","20":"Administrative Associate III","21":"Administrative Associate III","22":"Budget Specialist III","23":"Administrative Coordinator I","24":"Administrative Associate IV","25":"Administrative Associate III","26":"Administrative Associate III (SBPS)","27":"Administrative Associate III","28":"Administrative Associate III","29":"Administrative Associate  III","30":"Business Coordinator III","31":"Administrative Coordinator II","32":"Administrative Associate III","33":"Administrative Associate II","34":"Budget Specialist III","35":"Administrative Associate III","36":"Director of Business  Operations ","37":"Administrative Coordinator I","38":"Budget Specialist III","39":"Senior Administrative Coordinator I","40":"Administrative Associate III","41":"Administrative Associate III","42":"Business Coordinator III","43":"Administrative Associate  IV","44":"Administrative Associate IV","45":"Business Coordinator II","46":"Senior Administrative Coordinator I","47":"Budget Specialist I","48":"Budget Specialist I","49":"Administrative Associate III"},"Function":{"0":"Both","1":"Admin","2":"Admin","3":"Admin","4":"Admin","5":"Both","6":"Both","7":"Admin","8":"Both","9":"Admin","10":"Admin","11":"Both","12":"Admin","13":"Both","14":"Both","15":"Both","16":"Admin","17":"Admin","18":"Admin","19":" Admin","20":"Admin","21":"Admin","22":"Bus","23":"Admin","24":"Admin","25":"Admin","26":"Admin","27":"Admin","28":"Both ","29":"Both","30":"Both","31":"Admin","32":"Admin","33":"Admin","34":"Bus","35":"Admin","36":"Both","37":"Admin","38":"Bus","39":"Admin","40":"Both","41":"Admin","42":"Admin","43":"Admin","44":"Admin","45":"Bus","46":"Admin","48":"Both","49":"Both"," 47":"Both"},"FTE":{"0":0.05,"1":0.15,"2":1,"3":0.05,"4":0.05,"5":0.9,"6":0.05,"7":1,"8":0.15,"9":1,"10":0.1,"11":1,"12":0.03,"13":0.98,"14":0.25,"15":0.5,"16":0.05,"17":0.05,"18":1,"19":1,"20":0.05,"21":0.05,"22":0.15,"23":0.05,"24":0.2,"26":0.05,"27":0.05,"28":0.5,"29":0.4,"30":0.09,"31":1,"32":0.05,"33":1,"34":0.45,"35":0.05,"36":0.5,"37":0.05,"38":1,"39":0.2,"40":0.3,"41":0.05,"42":0.05,"43":0.1,"44":0.05,"46":0.05,"47":0.25,"48":0.1,"49":1," 25":0.05,"4 5":0.5}}
instruction = ("You are a data scientist and a superb communicator. "
               "I will ask you a question about JSON data provided below. "
               "Use professional tone and easy to understand language. "
               "Prioritize clarity. "
               "Put an effort into your work, take your time, and do an excellent job. "
               "I will tip you $500."
               "[JSON DATA STARTS]" + 
               str(jsonData)
               )
os.environ['GEMINI_API_KEY'] = st.secrets['keys']['GEMINI_API_KEY']
# Show title and description.
st.title("Anonymized Grant Support Data Chatbot 💬")
st.write(
    "This chatbot uses Google Gemini AI 2.0 Flash Experimental model to "
    "answer questions about grant support staffing data."
)

# Ask user for their geminai API key via `st.text_input`.
# Alternatively, you can store the API key in `./.streamlit/secrets.toml` and access it
# via `st.secrets`, see https://docs.streamlit.io/develop/concepts/connections/secrets-management
#geminai_api_key = st.text_input("geminai API Key", type="password")
if not os.environ['GEMINI_API_KEY']:
    st.info("Please add your Gemini AI API key to continue.", icon="🗝️")
else:
    genai.configure(api_key=os.environ['GEMINI_API_KEY'])
    # Create an Gemini AI client.
    model = genai.GenerativeModel(modelUsed, system_instruction=instruction)

    # Create a session state variable to store the chat messages. This ensures that the
    # messages persist across reruns.
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display the existing chat messages via `st.chat_message`.
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Create a chat input field to allow the user to enter a message. This will display
    # automatically at the bottom of the page.
    if prompt := st.chat_input("Your message here..."):

        # Store and display the current prompt.
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate a response using the geminai API.
        chat = model.start_chat(
#            history=[{"role": "user", "parts": "Hello"},
#                     {"role": "model", "parts": "Great to meet you. What would you like to know?"},
#                    ]
        )
        #response = chat.send_message("I have 2 dogs in my house.", stream=True)
        #for chunk in response:
        #    print(chunk.text)
        #    print("_" * 80)

        #print(chat.history)

        response = chat.send_message(
            [
                 prompt
#                m["content"] for m in st.session_state.messages
#                {"role": m["role"], "content": m["content"]}
#                for m in st.session_state.messages
            ],
            stream=True,
        )

        # Display assistant response in chat message container
        with st.chat_message(
            name='ai',
#            avatar="🤖",
        ):
            message_placeholder = st.empty()
            full_response = ''
            assistant_response = response
            # Streams in a chunk at a time
            for chunk in response:
                # Simulate stream of chunk
                # TODO: Chunk missing `text` if API stops mid-stream ("safety"?)
                for ch in chunk.text.split(' '):
                    full_response += ch + ' '
                    time.sleep(0.05)
                    # Rewrites with a cursor at end
                    message_placeholder.write(full_response + '▌')
            # Write full message with placeholder
            message_placeholder.write(full_response)
            #st.session_state.messages.append({"role": "assistant", "content": response})


        # Stream the response to the chat using `st.write_stream`, then store it in 
        # session state.
        #with st.chat_message("assistant"):
        #    response = st.write_stream(response)
        #st.session_state.messages.append({"role": "assistant", "content": response})
