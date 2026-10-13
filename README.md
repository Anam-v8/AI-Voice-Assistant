\# AI Voice Assistant



A beginner-friendly desktop voice assistant built using Python. It listens to voice commands, responds through speech, provides weather information, and opens useful websites and desktop applications.



\## Features



\- Voice recognition and spoken responses

\- Greeting, name, date, and time commands

\- Current weather information using OpenWeatherMap

\- Open Google, YouTube, and other useful websites

\- Search Google using voice commands

\- Play music or videos on YouTube

\- Open desktop applications such as Notepad, Calculator, and Paint

\- Exit the assistant using a voice command



\## Technologies Used



\- Python

\- SpeechRecognition

\- PyAudio

\- pyttsx3

\- Requests

\- OpenWeatherMap API

\- Python modules such as `webbrowser`, `datetime`, and `os`



\## Requirements



\- Python 3.12 or a compatible Python version

\- A working microphone

\- An internet connection

\- An OpenWeatherMap API key for the weather feature



\## Installation and Setup



\### 1. Clone the repository



```bash

git clone https://github.com/Anam-v8/AI-Voice-Assistant.git

cd AI-Voice-Assistant

```



\### 2. Create a virtual environment



```bash

python -m venv .venv

```



\### 3. Activate the virtual environment on Windows



```cmd

.venv\\Scripts\\activate

```



\### 4. Install the required packages



```bash

pip install SpeechRecognition PyAudio pyttsx3 requests

```



\### 5. Configure the weather API key



Get an API key from \[OpenWeatherMap](https://openweathermap.org/api).



In Windows Command Prompt, set the key for the current terminal session:



```cmd

set OPENWEATHER\_API\_KEY=YOUR\_API\_KEY

```



Replace `YOUR\_API\_KEY` with your own API key. Keep your API key private and never upload it to GitHub.



\*\*Note:\*\* This command sets the key only for the current Command Prompt session. If you open a new terminal, set it again before running the assistant.



\### 6. Run the assistant



```bash

python main.py

```



Speak a supported command into your microphone and listen to the assistant's response.



\## Project Structure



```text

AI-Voice-Assistant/

├── main.py

├── .gitignore

└── README.md

```



\## Security Note



The weather API key is read from the `OPENWEATHER\_API\_KEY` environment variable instead of being hardcoded in the source code. Keep API keys private and do not commit them to version control.



\## Future Improvements



\- Improve voice recognition and command handling

\- Add more useful voice commands

\- Improve error handling

\- Add more features in future versions



\## Author



GitHub: \[Anam-v8](https://github.com/Anam-v8)



