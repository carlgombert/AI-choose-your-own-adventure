from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from langchain.memory import CassandraChatMessageHistory, ConversationBufferMemory
from langchain_openai import OpenAI
from langchain.chains import LLMChain
from langchain_core.prompts import PromptTemplate

import json

cloud_config= {
    'secure_connect_bundle': "secure-connect-choose-your-own-adventure.zip"
}

with open("application_token.json") as f:
    secrets = json.load(f)

CLIENT_ID = secrets["clientId"]
CLIENT_SECRET = secrets["secret"]
ASTRA_DB_KEYSPACE = "default_keyspace"
OPENAI_API_KEY = secrets["openAIKey"]

auth_provider = PlainTextAuthProvider(CLIENT_ID, CLIENT_SECRET)
cluster = Cluster(
    cloud=cloud_config,
    auth_provider=auth_provider,
)
session = cluster.connect()

row = session.execute("select release_version from system.local").one()

if row:
    print(row[0])
    print("no error")
else:
    print("error")

message_history = CassandraChatMessageHistory(
    session_id="session id",
    session=session,
    keyspace=ASTRA_DB_KEYSPACE,
    ttl_seconds=3600
)

message_history.clear()

cass_buff_memory = ConversationBufferMemory(
    memory_key="chat_history",
    chat_memory=message_history
)

template = """
You are now the guide of a dangerous journey in the Fallout Wasteland. 
A traveler named Carl seeks to find Vault City, the high-tech settlement in Northern Nevada. 
You must navigate him through challenges, choices, and consequences, 
dynamically adapting the tale based on the traveler's decisions. 
Your goal is to create a branching narrative experience where each choice 
leads to a new path, ultimately determining Carl's fate. 

Here are some rules to follow:
1. Start by asking the player to choose some kind of weapons that will be used later in the game
2. Have a few paths that lead to success
3. Have some paths that lead to death. If the user dies generate a response that explains the death and ends in the text: "The End.", I will search for this text to end the game

Here is the chat history, use this to understand what to say next: {chat_history}
Human: {human_input}
AI:"""

prompt = PromptTemplate(
    input_variables=["chat_history", "human_input"],
    template = template
)

llm = OpenAI(openai_api_key=OPENAI_API_KEY)
llm_chain = LLMChain(
    llm=llm,
    prompt= prompt,
    memory = cass_buff_memory
)

llm_chain.invoke(input="start the game")
response = llm_chain.predict()
print(response)