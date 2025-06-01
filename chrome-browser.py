import asyncio
from typing import List
from pydantic import BaseModel
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from browser_use import Agent, Controller, BrowserSession
from playwright.async_api import async_playwright

load_dotenv()

# Define Pydantic models for output parsing
class Post(BaseModel):
    post_title: str
    post_url: str
    num_comments: int
    hours_since_post: int

class Posts(BaseModel):
    posts: List[Post]

controller = Controller(output_model=Posts)

async def main():
    task = 'Go to hackernews show hn and give me the first 5 posts'
    model = ChatGoogleGenerativeAI(model='gemini-1.5-flash')  # or 'gemini-2.0-pro' based on your access

    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()

        browser_session = BrowserSession(page=page)

        agent = Agent(
            task=task,
            llm=model,
            controller=controller,
            browser_session=browser_session,
            use_vision=False,
            save_conversation_path="logs/conversation"
        )

        history = await agent.run()

        result = history.final_result()
        if result:
            parsed: Posts = Posts.model_validate_json(result)

            for post in parsed.posts:
                print('\n--------------------------------')
                print(f'Title:            {post.post_title}')
                print(f'URL:              {post.post_url}')
                print(f'Comments:         {post.num_comments}')
                print(f'Hours since post: {post.hours_since_post}')
        else:
            print('No result')

if __name__ == '__main__':
    asyncio.run(main())
