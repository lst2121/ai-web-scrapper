from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from browser_use import Agent, BrowserSession
from dotenv import load_dotenv
import asyncio
import os

load_dotenv()

# llm = ChatOpenAI(model="gpt-3.5-turbo")

llm = ChatGoogleGenerativeAI(model='gemini-2.0-flash')

chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

async def main():
    browser_session = BrowserSession(
        executable_path=chrome_path,
        headless=False,
        # No user_data_dir here — browser-use manages the profile automatically
    )

    agent = Agent(
        task="Go to LinkedIn and login with email:lokender2121@gmail.com, password:Deepak@21 then check my account information",
        llm=llm,
        use_vision=False,
        save_conversation_path="logs/conversation",
        browser_session=browser_session,
    )

    result = await agent.run()
    print(result)

    if browser_session.browser:
        await browser_session.browser.close()

asyncio.run(main())
