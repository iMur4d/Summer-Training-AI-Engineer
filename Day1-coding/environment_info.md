PS C:\Users\Dvs\Desktop\AI-Engineering-Training\coding> python --version
Python 3.14.6
PS C:\Users\Dvs\Desktop\AI-Engineering-Training\coding> pip show google-genai
Name: google-genai
Version: 2.10.0
Summary: GenAI Python SDK
Home-page: https://github.com/googleapis/python-genai
Author:
License-Expression: Apache-2.0
Location: C:\Users\Dvs\AppData\Local\Python\pythoncore-3.14-64\Lib\site-packages
Requires: anyio, distro, google-auth, httpx, pydantic, requests, sniffio, tenacity, typing-extensions, websockets
Required-by:
Name: python-dotenv
Version: 1.2.2
Summary: Read key-value pairs from a .env file and set them as environment variables
Author:
Author-email: Saurabh Kumar <me+github@saurabh-kumar.com>
License: BSD-3-Clause
Location: C:\Users\Dvs\AppData\Local\Python\pythoncore-3.14-64\Lib\site-packages
Requires:
Required-by:
On branch main
Your branch is up to date with 'origin/main'.

nothing to commit, working tree clean
PS C:\Users\Dvs\Desktop\AI-Engineering-Training\coding> git remote -v
origin https://github.com/iMur4d/Summer-Training-AI-Engineer.git (fetch)
origin https://github.com/iMur4d/Summer-Training-AI-Engineer.git (push)
PS C:\Users\Dvs\Desktop\AI-Engineering-Training\coding> git log --oneline --decorate
aee6d7d (HEAD -> main, origin/main) implement AI(Gemini) chatbot with context window with high & low temperature
27f75dd Implement working Gemini API client with system instruction and configs
bcb50e3 Testing a test key to ensure .env is hide
60c8e74 Remove .env from tracking and update gitignore
1ad01ec Create LLM-API.ipynb file and write test code
5e786a3 first commit
PS C:\Users\Dvs\Desktop\AI-Engineering-Training\coding> git ls-files
.gitignore
Day1-coding/HighTempOutput.png
Day1-coding/LLM-API.ipynb
Day1-coding/LLM-Answer-HighTemp.py
Day1-coding/LLM-Answer-LowTemp.py
Day1-coding/LowTempOutput.png
README.md
PS C:\Users\Dvs\Desktop\AI-Engineering-Training\coding> cat .gitignore
.env
