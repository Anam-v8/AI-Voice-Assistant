
import speech_recognition as sr
import pyttsx3
import webbrowser
from datetime import datetime
import os
import requests
import subprocess
from urllib.parse import quote_plus


# ---------------- WIKIPEDIA ----------------

def get_wikipedia_summary(topic):
    url = "https://en.wikipedia.org/w/api.php"

    headers = {
        "User-Agent": "AI-Voice-Assistant/1.0"
    }

    try:
        # Step 1: Search Wikipedia
        search_params = {
            "action": "query",
            "format": "json",
            "list": "search",
            "srsearch": topic
        }

        response = requests.get(
            url,
            params=search_params,
            headers=headers,
            timeout=15
        )

        response.raise_for_status()

        search_data = response.json()
        results = search_data["query"]["search"]

        if not results:
            return None

        # Step 2: Get the best matching page title
        title = results[0]["title"]
        print("Wikipedia page found:", title)

        # Step 3: Fetch the page summary
        summary_params = {
            "action": "query",
            "format": "json",
            "prop": "extracts",
            "exintro": True,
            "explaintext": True,
            "titles": title
        }

        response = requests.get(
            url,
            params=summary_params,
            headers=headers,
            timeout=15
        )

        response.raise_for_status()

        data = response.json()
        pages = data["query"]["pages"]

        for page in pages.values():
            extract = page.get("extract", "")

            if extract.strip():
                # Keep the spoken summary reasonably short
                sentences = extract.split(". ")
                summary = ". ".join(sentences[:3])

                if summary and not summary.endswith((".", "!", "?")):
                    summary += "."

                return summary

        return None

    except (
        requests.RequestException,
        ValueError,
        KeyError,
        TypeError
    ) as error:
        print("Wikipedia error:", error)
        return None


# ---------------- WEATHER ----------------

def get_weather(city):
    url = "https://api.openweathermap.org/data/2.5/weather"

    params = {
        "q": city,
        "appid": os.getenv("OPENWEATHER_API_KEY"),
        "units": "metric"
    }

    try:
        response = requests.get(
            url,
            params=params,
            timeout=15
        )

        if response.status_code != 200:
            print("Weather API error:", response.status_code)
            return None

        data = response.json()

        temperature = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        description = data["weather"][0]["description"]

        return temperature, humidity, description

    except (
        requests.RequestException,
        ValueError,
        KeyError,
        IndexError,
        TypeError
    ) as error:
        print("Weather error:", error)
        return None


# ---------------- SPEAK ----------------

def speak(text):
    engine = pyttsx3.init()
    engine.say(str(text))
    engine.runAndWait()


# ---------------- LISTEN ----------------

def listen():
    recognizer = sr.Recognizer()

    try:
        with sr.Microphone() as source:
            print("Listening...")
            audio = recognizer.listen(source, timeout=5)

        print("Recognizing...")
        text = recognizer.recognize_google(audio)

        return text.lower().strip()

    except sr.WaitTimeoutError:
        return ""

    except sr.UnknownValueError:
        speak("Sorry, I didn't understand that.")
        return ""

    except sr.RequestError:
        speak("Sorry, there is a problem with the speech recognition service.")
        return ""

    except OSError:
        speak("Sorry, I could not access the microphone.")
        return ""


# ---------------- PROCESS COMMAND ----------------

def process_command(command):

    if command == "":
        return True

    # Hello
    if command == "hello":
        speak("Hello! How can I help you?")

    # Name
    elif command == "what is your name":
        speak("I am your desktop voice assistant.")

    # Time
    elif command in ("what is the time", "tell me the time"):
        current_time = datetime.now().strftime("%I:%M %p")
        speak("The current time is " + current_time)

    # Date
    elif command in (
        "what is today's date",
        "what is the date",
        "tell me today's date"
    ):
        current_date = datetime.now().strftime("%d %B %Y")
        speak("Today's date is " + current_date)

    # Weather
    elif command.startswith("weather in "):
        city = command.replace("weather in ", "", 1).strip()

        if not city:
            speak("Please tell me a city name.")
        else:
            speak("Checking the weather in " + city + ".")

            result = get_weather(city)

            if result is None:
                speak("Sorry, I could not get the weather information.")
            else:
                temperature, humidity, description = result

                speak(
                    "The temperature in "
                    + city
                    + " is "
                    + str(round(temperature))
                    + " degrees Celsius. Humidity is "
                    + str(humidity)
                    + " percent. The weather is "
                    + description
                )

    # Wikipedia
    elif command.startswith("wikipedia "):
        topic = command.replace("wikipedia ", "", 1).strip()

        if not topic:
            speak("Please tell me what you want to search on Wikipedia.")
        else:
            speak("Searching Wikipedia for " + topic + ".")

            result = get_wikipedia_summary(topic)

            if result is None:
                speak("Sorry, I could not get information from Wikipedia.")
            else:
                print("Wikipedia result:", result)
                speak(result)

    # Open YouTube
    elif command in ("open youtube", "youtube"):
        speak("Opening YouTube.")
        webbrowser.open("https://www.youtube.com")

    # Open Google
    elif command in ("open google", "google"):
        speak("Opening Google.")
        webbrowser.open("https://www.google.com")

    # Google Search
    elif command.startswith("search for "):
        search_query = command.replace("search for ", "", 1).strip()

        if search_query:
            speak("Searching for " + search_query)
            search_url = (
                "https://www.google.com/search?q="
                + quote_plus(search_query)
            )
            webbrowser.open(search_url)
        else:
            speak("Please tell me what you want to search for.")

    # Play Music
    elif command in ("play music", "play some music"):
        speak("Opening music.")
        webbrowser.open(
            "https://www.youtube.com/results?search_query=music"
        )

    # Open Chrome
    elif command == "open chrome":
        chrome_paths = [
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
            os.path.expandvars(
                r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe"
            )
        ]

        chrome_path = next(
            (path for path in chrome_paths if os.path.exists(path)),
            None
        )

        if chrome_path:
            speak("Opening Chrome.")
            subprocess.Popen([chrome_path])
        else:
            speak("Sorry, Chrome was not found on this computer.")

    # Open Notepad
    elif command in ("open notepad", "start notepad"):
        try:
            subprocess.Popen(["notepad.exe"])
            speak("Opening Notepad.")
        except OSError as error:
            print("Notepad error:", error)
            speak("Sorry, I could not open Notepad.")

    # Open Calculator
    elif command in ("open calculator", "start calculator"):
        try:
            subprocess.Popen(["calc.exe"])
            speak("Opening Calculator.")
        except OSError as error:
            print("Calculator error:", error)
            speak("Sorry, I could not open Calculator.")

    # Open Paint
    elif command in ("open paint", "start paint"):
        try:
            subprocess.Popen(["mspaint.exe"])
            speak("Opening Paint.")
        except OSError as error:
            print("Paint error:", error)
            speak("Sorry, I could not open Paint.")

    # Exit
    elif command in ("exit", "quit", "stop assistant"):
        speak("Goodbye!")
        return False

    # Unknown command
    else:
        speak("Sorry, I didn't understand that command.")

    return True


# ---------------- MAIN ----------------

def main():
    speak(
        "Hello! I am your desktop voice assistant. "
        "How can I help you?"
    )

    while True:
        command = listen()

        if command:
            print("You said:", command)

        if not process_command(command):
            break


# ---------------- START PROGRAM ----------------

if __name__ == "__main__":
    main()
