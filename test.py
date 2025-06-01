import asyncio
from langchain_openai import ChatOpenAI
from browser_use import Agent, BrowserSession
from dotenv import load_dotenv
load_dotenv()
import os

llm = ChatOpenAI(model="deepseek/deepseek-chat-v3-0324:free",
                 base_url=os.getenv("OPEN_ROUTER_ENDPOINT"),
                 api_key=os.getenv("OPEN_ROUTER_API_KEY")
                 )


browser_session = BrowserSession(
    executable_path='C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
    user_data_dir='C:\\Users\\lokender.singh\\AppData\\Local\\browseruse\\profiles\\default',  # your dedicated profile folder
    headless=False,
)

async def main():
    agent = Agent(
        task="Go to LinkedIn and grab 5 most recent jobs in India",
        llm=llm,
        browser_session=browser_session,
        use_vision=False,
        save_conversation_path="logs/conversation.json",
    )
    result = await agent.run()
    print(result.final_result())
    await browser_session.close()

asyncio.run(main())
