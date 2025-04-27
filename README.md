# 📖 PlotWeaver

**PlotWeaver** is an AI-powered story generator that lets users craft unique and engaging stories with just a few prompts. Built using **Streamlit**, **PyMongo**, and **Groq**, it combines smooth user interaction with powerful AI capabilities and a MongoDB backend for storing story data.

## ✨ Features

- 🖋️ AI Story Generation using Groq LLM
- 🎨 Generate Images for stories using Stability API
- 🔍 Search and Fetch Images from Google using SerpAPI
- 🔑 Password Reset Functionality with Resend API
- 📚 Save & Manage Stories with MongoDB (PyMongo)
- 🎨 Simple & Intuitive UI built with Streamlit
- 🔄 Regenerate Stories with fresh twists
- 🧠 Smart Prompt Handling for creative control

## 🛠️ Tech Stack

- Frontend/UI: Streamlit
- Backend: Python, PyMongo
- AI Model: Groq LLM
- Database: MongoDB
- Image Generation: Stability API
- Image Search: SerpAPI
- Email Services: Resend API

## 🚀 Installation and Setup

First, clone the repository:

```bash
git clone https://github.com/yshbtw/plotweaver.git
cd plotweaver
Install the required Python packages:

bash
Copy
Edit
pip install -r requirements.txt
Create a .env file in the project root and add the following environment variables:

bash
Copy
Edit
MONGO_URI=your_mongodb_connection_uri
GROQ_API_KEY=your_groq_api_key
STABILITY_API_KEY=your_stability_api_key
SERPAPI_API_KEY=your_serpapi_key
RESEND_API_KEY=your_resend_api_key
Now, run the application:

bash
Copy
Edit
streamlit run app.py
