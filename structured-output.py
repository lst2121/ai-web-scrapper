from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel
from browser_use import Agent, Controller
from dotenv import load_dotenv
load_dotenv()
import os

import asyncio

class Job(BaseModel):
    title: str
    company: str
    location: str
    posted: str

class Jobs(BaseModel):
    jobs: list[Job]

controller = Controller(output_model=Jobs)

# llm = ChatOpenAI(model="gpt-3.5-turbo")
# llm = ChatOpenAI(model="deepseek/deepseek-chat-v3-0324:free",
#                  base_url=os.getenv("OPEN_ROUTER_ENDPOINT"),
#                  api_key=os.getenv("OPEN_ROUTER_API_KEY")
#                  )
llm = ChatGoogleGenerativeAI(model='gemini-2.0-flash')

async def main():
    agent = Agent(
        task="Go to linkedIn and do not login and grab 5 most recent jobs in the India",
        llm=llm,
        use_vision=False,
        controller=controller,
        save_conversation_path="logs/conversation",
    )
    result = await agent.run()
    print("jobs:", result.final_result())

asyncio.run(main())