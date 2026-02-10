# import warnings
# warnings.filterwarnings('ignore')

# import streamlit as st
# from pathlib import Path
# from langchain_community.agent_toolkits import create_sql_agent
# from langchain_community.utilities import SQLDatabase
# from langchain_classic.agents import AgentType
# from langchain_community.callbacks.streamlit import StreamlitCallbackHandler
# from langchain_community.agent_toolkits import SQLDatabaseToolkit
# from sqlalchemy import create_engine
# import sqlite3
# from langchain_groq import ChatGroq






# st.set_page_config(page_title="Langchain : chat with SQL db", page_icon="g")
# st.title("Langchain : chat with sql")



# INJECTION_WARNING = """
#                     SQL agent can be vulnerable to prompt injection . Use a DB role with Limit,
#                     Read more here(https://python.langchain.com/docs/security)"""





# LOCALDB = "USE_LOCALDB"
# MYSQL = "USE_MYSQL"



# #### radio
# radio_opt = ["USE SQLITE # databse Student.db","connect to your SQL database"]
# selected_opt = st.sidebar.radio(label="choose the db which you want to use", options=radio_opt)

# if radio_opt.index(selected_opt)==1:
#     db_uri = MYSQL
#     mysql_host = st.sidebar.text_input("provide my sql host")
#     mysql_user = st.sidebar.text_input("provide user name of mysql")
#     mysql_password = st.sidebar.text_input("mysql password",type="password")
#     mysql_db = st.sidebar.text_input("mysql database")
# else:
#     db_uri =LOCALDB


# api_key = st.sidebar.text_input(label="groq api key ",type="password")

# if not db_uri :
#     st.info("please enter the databse info and uri")
    

# if not api_key:
#     st.info("please add the groq api key")
    



# ###llm model
# llm =ChatGroq(groq_api_key=api_key,model="llama-3.1-8b-instant",streaming=True)


# @st.cache_resource(ttl="2h")
# def configure_db(db_uri,mysql_host=None,mysql_user = None,mysql_password =None,mysql_db =None):
#     if db_uri == LOCALDB:
#         dbfilepath = (Path(__file__).parent/"student.db").absolute()
#         print(dbfilepath)
#         creator = lambda: sqlite3.connect(f"file:{dbfilepath}?mode=ro",uri = True)
#         return SQLDatabase(create_engine("sqlite:///",creator=creator))
#     elif db_uri == MYSQL:
#         if not(mysql_user and mysql_db and mysql_host and mysql_password):
#             st.error("please provide all mysql connection details")
#             st.stop()
        
#         return SQLDatabase(create_engine(f"mysql+mysqlconnector://{mysql_user}:{mysql_password}@m{mysql_host}/{mysql_db}"))
        


# if db_uri == MYSQL:
#     db = configure_db(db_uri,mysql_host,mysql_user,mysql_password,mysql_db)
# else:
#     db= configure_db(db_uri)


# ###toolkit
# toolkit = SQLDatabaseToolkit(db=db,llm=llm)
# toolkit = SQLDatabaseToolkit(db=db, llm=llm)

# agent = create_sql_agent(
#     llm=llm,
#     toolkit=toolkit,
#     verbose=True,
#     handle_parsing_errors=True
# )



# if "messages" not in st.session_state or st.sidebar.button("clear message history"):
#     st.session_state["messages"] = [{"role":"assistant","content":"how can i  help you ?"}]


# for msg in st.session_state.messages:
#     st.chat_message(msg["role"]).write(msg["content"])


# user_query = st.chat_input(placeholder="ask anything from database")


# if user_query:
#     st.session_state.messages.append({"role":"user","content": user_query})
#     st.chat_message("user").write(user_query)

#     with st.chat_message("assistant"):
#         streamlit_callback = StreamlitCallbackHandler(st.container())
#         response = agent.run(user_query,callbacks=[streamlit_callback])
#         st.session_state.messages.append({"role":"assitant","content":response})
#         st.write(response)





import warnings
warnings.filterwarnings('ignore')

import streamlit as st
import sqlite3
from pathlib import Path
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_community.callbacks.streamlit import StreamlitCallbackHandler
from langchain_community.agent_toolkits import create_sql_agent
from sqlalchemy import create_engine
from langchain_groq import ChatGroq

st.set_page_config(page_title="Langchain: Chat with SQL DB", page_icon="🎯")
st.title("🗄️ Langchain: Chat with SQL Database")

LOCALDB = "USE_LOCALDB"
MYSQL = "USE_MYSQL"

# Sidebar - API Key
api_key = st.sidebar.text_input(label="Enter Groq API Key", type="password")

# Sidebar - DB Selection
radio_opt = ["Use SQLite (Student.db)", "Connect to MySQL Database"]
selected_opt = st.sidebar.radio(label="Choose your database", options=radio_opt)

mysql_host = mysql_user = mysql_password = mysql_db = None

if radio_opt.index(selected_opt) == 1:
    db_uri = MYSQL
    mysql_host = st.sidebar.text_input("MySQL Host")
    mysql_user = st.sidebar.text_input("MySQL User")
    mysql_password = st.sidebar.text_input("MySQL Password", type="password")
    mysql_db = st.sidebar.text_input("MySQL Database Name")
else:
    db_uri = LOCALDB

# Validation
if not api_key:
    st.info("⚠️ Please enter your Groq API key in the sidebar to continue.")
    st.stop()

if db_uri == MYSQL and not all([mysql_host, mysql_user, mysql_password, mysql_db]):
    st.info("⚠️ Please provide all MySQL connection details.")
    st.stop()

# Configure DB
@st.cache_resource(ttl="2h")
def configure_db(db_uri, mysql_host=None, mysql_user=None, mysql_password=None, mysql_db=None):
    if db_uri == LOCALDB:
        dbfilepath = (Path(__file__).parent / "student.db").absolute()
        creator = lambda: sqlite3.connect(f"file:{dbfilepath}?mode=ro", uri=True)
        return SQLDatabase(create_engine("sqlite:///", creator=creator))
    elif db_uri == MYSQL:
        return SQLDatabase(
            create_engine(f"mysql+mysqlconnector://{mysql_user}:{mysql_password}@{mysql_host}/{mysql_db}")
        )

db = configure_db(db_uri, mysql_host, mysql_user, mysql_password, mysql_db)

# LLM
llm = ChatGroq(groq_api_key=api_key, model="llama-3.3-70b-versatile", streaming=False, temperature=0)

# Agent
toolkit = SQLDatabaseToolkit(db=db, llm=llm)

agent = create_sql_agent(
    llm=llm,
    toolkit=toolkit,
    verbose=True,
    handle_parsing_errors=True,
    max_iterations=15,
    early_stopping_method="force",
    agent_executor_kwargs={"return_intermediate_steps": True}
)

# Chat History
if "messages" not in st.session_state or st.sidebar.button("🗑️ Clear Chat"):
    st.session_state["messages"] = [
        {"role": "assistant", "content": "Hello! I'm your SQL assistant. Ask me anything about your database."}
    ]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# User Input
user_query = st.chat_input(placeholder="Ask anything about your database...")

if user_query:
    st.session_state.messages.append({"role": "user", "content": user_query})
    st.chat_message("user").write(user_query)

    with st.chat_message("assistant"):
        streamlit_callback = StreamlitCallbackHandler(st.container())
        try:
            response = agent.invoke(
                {"input": user_query},
                config={"callbacks": [streamlit_callback]}
            )
            answer = response.get("output", "Sorry, I couldn't generate a response.")
        except Exception as e:
            answer = f"❌ Error: {str(e)}"

        st.session_state.messages.append({"role": "assistant", "content": answer})
        st.write(answer)