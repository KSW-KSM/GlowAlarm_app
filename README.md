# 🌟 Gemini-Powered Smart Alarm App

Welcome to our cutting-edge Gemini-Powered Smart Alarm App! This innovative application leverages the power of Google's Gemini AI to provide you with an intelligent and adaptive alarm experience.

## 🚀 Features

- 🧠 AI-Optimized Wake-Up Times: Utilizes Gemini AI to suggest the best wake-up time based on your sleep patterns.
- 🔊 Voice-Controlled Alarm Management: Stop your alarm using voice commands.
- 😴 Smart Snooze Function: Intelligently adjusts snooze duration based on your habits.
- 🔄 Adaptive Alarm Settings: Learns from your preferences to improve over time.

## 🛠 Tech Stack

- Backend: FastAPI
- AI Integration: LangChain with Google Gemini
- Testing: Pytest
- API Requests: HTTPX

## 🏗 Project Structure

alarm-app/
│
├── app/
│   ├── init.py
│   ├── main.py        # Main application logic
│   ├── models.py      # Data models
│   └── utils.py       # Utility functions
│
├── tests/
│   ├── init.py
│   ├── test_main.py   # Unit tests
│   └── test_server_requests.py  # Integration tests
│
├── .env               # Environment variables (not in version control)
├── .gitignore
├── requirements.txt
└── README.md

## 🚀 Getting Started

1. Clone the repository:

```
git clone https://github.com/yourusername/alarm-app.git
cd alarm-app
```

2. Set up a virtual environment:

```
python -m venv venv
source venv/bin/activate  # On Windows use venv\Scripts\activate
```

3. Install dependencies:
```
pip install -r requirements.txt
```

4. Set up your environment variables:
```
Create a `.env` file in the root directory and add:
GOOGLE_API_KEY=your_google_api_key_here
```

5. Run the application:
```
uvicorn app.main:app --reload
```

6. Run tests:
```
pytest
```

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for more details.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgements

- Google Gemini AI
- FastAPI
- LangChain

Happy Waking Up! 🌞