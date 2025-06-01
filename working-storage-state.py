from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from browser_use import Agent
from browser_use.browser import BrowserProfile, BrowserSession
from dotenv import load_dotenv
import asyncio

load_dotenv()

# llm = ChatOpenAI(model="gpt-3.5-turbo")

llm = ChatGoogleGenerativeAI(model='gemini-2.0-flash')

task_prompt = """
Go to LinkedIn and search for 'QA Automation Engineer' jobs with 'Remote' option.
Filter jobs located in 'Noida, India' only.
From the search results, identify jobs that have the 'Easy Apply' tag.
Apply to only 2 such jobs with the 'Easy Apply' option.
Do NOT apply to any jobs that do not have the 'Easy Apply' option.
Make sure to complete the application process for these 2 jobs.
"""


# Point to your saved authenticated session
storage_state_path = "auth.json"  # Must match the file created by Playwright

# Create a reusable browser profile
shared_profile = BrowserProfile(
    executable_path=r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    headless=False,
    storage_state=storage_state_path,
    user_data_dir=None,  # Important: each session gets its own user data dir
    keep_alive=True,     # To keep browser alive after agent run
)

async def main():
    # Each agent gets its own browser window/session, but shares the same profile
    browser_session = BrowserSession(browser_profile=shared_profile)

    agent = Agent(
        task="Go to LinkedIn and get top 5 jobs for QA Automation post in Noida, India location.",
        llm=llm,
        use_vision=False,
        save_conversation_path="logs/conversation",
        browser_session=browser_session,
    )

    result = await agent.run()
    print(result)

    # Save updated cookies back to the file
    await browser_session.save_cookies()

    await browser_session.close()

asyncio.run(main())
