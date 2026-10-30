🤖 AI ChatBOT – Your Personal Gemini AI Assistant

A modern, interactive AI chatbot built with Python, Streamlit, and Google Gemini AI. This application provides an intelligent conversational experience with support for multiple chat sessions, persistent chat history, voice input, text-to-speech, and an enhanced Think Mode for detailed responses.

✨ Features
🤖 AI-Powered Conversations: Get intelligent and helpful responses using Google's Gemini AI.
💬 Multiple Chat Sessions: Create and manage multiple conversations independently.
🕘 Chat History: Automatically save conversations locally in a JSON file.
🎙️ Voice Input: Ask questions using your microphone with speech-to-text functionality.
🔊 Read Aloud: Listen to AI-generated responses using browser text-to-speech.
🧠 Think Mode: Enable more detailed and carefully structured responses for complex questions.
🎨 Modern UI: Enjoy a clean, dark-themed interface with a responsive layout.
🗑️ Chat Management: Create new chats, switch between conversations, and clear or delete chats.
⚙️ Configurable AI Model: Choose a Gemini model through environment variables.
🔐 Environment Variables: Keep your Gemini API key outside your source code.
🛠️ Technologies Used
Technology	Purpose
Python	Backend programming
Streamlit	Web application and user interface
Google Gemini AI	AI-powered chatbot responses
Google Generative AI SDK	Gemini API integration
streamlit-mic-recorder	Voice input and speech recognition
Python-dotenv	Environment variable management
JSON	Local chat history storage
JavaScript	Browser-based text-to-speech
HTML & CSS	UI customization and styling
📂 Project Structure
text
AI-ChatBOT/
│
├── app.py                  # Main Streamlit application
├── chat_history.json       # Automatically generated chat history
├── .env                    # Environment variables (API key)
├── .gitignore              # Files excluded from Git
├── requirements.txt        # Python dependencies
└── README.md               # Project documentation

🚀 Getting Started

Follow these steps to run the project on your local machine.

1. Clone the Repository
bash
git clone https://github.com/your-username/AI-ChatBOT.git

2. Navigate to the Project Directory
bash
cd AI-ChatBOT

3. Create a Virtual Environment (Recommended)
bash
python -m venv venv


Activate the virtual environment:

Windows:

bash
venv\Scripts\activate


macOS / Linux:

bash
source venv/bin/activate

4. Install Dependencies
bash
pip install -r requirements.txt


Alternatively, install the required packages directly:

bash
pip install streamlit google-generativeai python-dotenv streamlit-mic-recorder

5. Configure Your Gemini API Key

Get your API key from Google AI Studio.

Create a .env file in the root directory and add:

env
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-3.5-flash


Note: Replace your_gemini_api_key_here with your actual Gemini API key. Make sure the configured model is available to your API key.

6. Run the Application
bash
streamlit run app.py


The application will open automatically in your browser.

Default local URL:

text
http://localhost:8501

📦 Requirements

Create a requirements.txt file with the following dependencies:

text
streamlit
google-generativeai
python-dotenv
streamlit-mic-recorder

🧠 How It Works
Launch the application using Streamlit.
Enter your message in the chat input or use the microphone.
Your message is sent to the Google Gemini API.
Gemini processes the prompt and generates an AI response.
The response appears in the chat window.
Use the Read Aloud button to listen to the response.
Your conversations are automatically stored in chat_history.json.
Enable Think Mode whenever you need more detailed and structured answers.
🎙️ Voice Features

The chatbot includes two voice-related features:

Speech-to-Text: Convert spoken questions into text using your microphone.
Text-to-Speech: Convert AI-generated responses into spoken audio using your browser's built-in speech synthesis.

Note: Microphone access must be allowed in your browser. Speech recognition availability may depend on your browser and environment.

🔒 Security
Store your Gemini API key in the .env file.
Never upload your API key to GitHub.
Add .env and other sensitive files to .gitignore.
Avoid sharing your chat_history.json file if it contains private conversations.

Example .gitignore:

gitignore
.env
venv/
__pycache__/
*.pyc
chat_history.json
.streamlit/secrets.toml

🔮 Future Improvements

Some possible enhancements for future versions:

Image and document upload support.
Export conversations as PDF or TXT.
User authentication and account management.
Database integration for chat storage.
Multiple AI model support.
Customizable chatbot themes.
Improved voice interaction.
Deploy the application online.
👨‍💻 Author

Navjot Singh

Python Developer | AI & Machine Learning Enthusiast

I enjoy building AI-powered applications and exploring modern technologies to create useful and interactive software solutions.

Connect With Me
GitHub: Your GitHub Profile
LinkedIn: Your LinkedIn Profile
⭐ Support

If you like this project, consider giving it a ⭐ on GitHub. Your support and feedback are appreciated!

<p align="center">
Made with ❤️ by <strong>Navjot Singh</strong>
</p>
