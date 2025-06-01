from langchain_openai import ChatOpenAI
from langchain_openai import OpenAI
from browser_use import Agent
from dotenv import load_dotenv
load_dotenv()
import os
import asyncio

llm = ChatOpenAI(model="deepseek/deepseek-chat-v3-0324:free",
                 base_url=os.getenv("OPEN_ROUTER_ENDPOINT"),
                 api_key=os.getenv("OPEN_ROUTER_API_KEY")
                 )



async def main():
    agent = Agent(
        task="Compare the price of gpt-4o and DeepSeek-V3",
        llm=llm,
        use_vision=False,
        save_conversation_path="logs/conversation",
    )
    result = await agent.run()
    print("result:", result)
asyncio.run(main())