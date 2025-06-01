from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from browser_use import Agent, BrowserSession
import asyncio

llm = ChatGoogleGenerativeAI(model='gemini-2.0-flash')

# Domain-specific sensitive data
sensitive_data = {
    'x_email': 'lokender2121@gmail.com', 'x_pass': '*****'
}

# # Set browser session with allowed domains that match all domain patterns in sensitive_data
browser_session = BrowserSession(
    allowed_domains=[
    'https://www.linkedin.com/',
    'https://www.linkedin.com/*',
    'https://www.linkedin.com/in/*',
]
)

# Pass the sensitive data to the agent
agent = Agent(
    task="Go to LinkedIn and login with x_email, x_pass then check my account information",
    llm=llm,
    sensitive_data=sensitive_data,
    # browser_session=browser_session,
    use_vision=False,
)

async def main():
    await agent.run()

if __name__ == '__main__':
    asyncio.run(main())
