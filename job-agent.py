from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from browser_use import Agent
from browser_use.browser import BrowserProfile, BrowserSession
from dotenv import load_dotenv
import asyncio
import os
load_dotenv()

# llm = ChatOpenAI(model="gpt-3.5-turbo")

# llm = ChatGoogleGenerativeAI(model='gemini-2.0-flash')
# llm = ChatOpenAI(model="gpt-4o-mini")

llm = ChatOpenAI(model="deepseek/deepseek-chat-v3-0324:free",
                 base_url=os.getenv("OPEN_ROUTER_ENDPOINT"),
                 api_key=os.getenv("OPEN_ROUTER_API_KEY")
                 )
task_prompt = """
You are automating LinkedIn Easy Apply for QA Automation Engineer jobs in Noida, India.

After you click the "Easy Apply" button on a job:
- Check if an application form/modal appears.
- If yes, fill in all required fields:
  - If the phone number field is empty or missing, enter the phone number +91-8946975401.
  - If there is a resume upload field and it is empty, upload the resume from the path "C:/Users/You/Documents/resume.pdf". Otherwise, skip uploading since my resume is already saved in my profile.
  - For dropdowns or multiple choice questions, select the first available valid option.
  - For any text input fields, provide reasonable answers or placeholders.
- Before clicking any "Next", "Continue", "Review", or "Submit" buttons, **scroll slowly and fully through the form** until the buttons become active.
- Proceed through all steps by clicking "Next" or "Continue".
- Uncheck any optional checkboxes such as "Follow [Company] to stay up to date with their page." before proceeding.
- When you reach the **review step**, carefully scroll through the entire review page.
- After reviewing, click the "Submit" or "Done" button to send the application.
- If at any point required information is missing or the form cannot be submitted, skip this job.
- Apply only to jobs with the "Easy Apply" tag.
- Do not apply to jobs that do not have the "Easy Apply" option.
- Stop applying after successfully applying to 2 jobs.
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
        task=task_prompt,
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
