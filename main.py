import os
import requests
import schedule
import time
import threading
import subprocess
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

# Load environment variables
load_dotenv()
running = False


# --- Fetch latest news articles ---
def fetch_news_text(query: str):
    api_key = os.getenv("NEWS_API_KEY")
    if not api_key:
        return ["Missing NEWS_API_KEY in .env file."]

    url = f"https://newsapi.org/v2/everything?q={query}&sortBy=publishedAt&pageSize=3&apiKey={api_key}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            articles = response.json().get('articles', [])
            return [
                f"{article['title']}: {article.get('description', '') or 'No description.'}"
                for article in articles
            ]
        else:
            return [f"Error fetching news: {response.status_code}"]
    except Exception as e:
        return [f"Exception occurred while fetching news: {e}"]


# --- Summarize articles using OpenAI ---
def analyze_articles(articles):
    try:
        model = ChatOpenAI()
        prompt = (
                "Summarize the key takeaways from these AI news headlines:\n\n"
                + "\n\n".join(articles)
        )
        messages = [HumanMessage(content=prompt)]
        summary = model.invoke(messages).content
        return summary
    except Exception as e:
        return f"Error generating summary: {e}"


# --- macOS native notification using terminal-notifier ---
def show_notification():
    articles = fetch_news_text("AI")
    summary = analyze_articles(articles)

    # Clean and trim summary for notification
    short_summary = summary.replace('"', "'")
    if len(short_summary) > 180:
        short_summary = short_summary[:180] + "..."

    # Save full summary to a local file
    full_path = os.path.abspath("latest_summary.txt")
    with open(full_path, "w") as f:
        f.write(summary)

    try:
        subprocess.run([
            "terminal-notifier",
            "-title", "AI News Summary",
            "-message", short_summary,
            "-open", f"file://{full_path}"  # Opens full summary in default text editor
        ])
    except Exception as e:
        print(f"Notification error: {e}")



# --- Schedule runner in background ---
def schedule_runner():
    while running:
        schedule.run_pending()
        time.sleep(60)


# --- Start the agent ---
def start_agent():
    global running
    running = True
    schedule.every().day.at("09:00").do(show_notification)

    thread = threading.Thread(target=schedule_runner)
    thread.start()

    print("Agent started. Press 'q' to quit.\n")
    while running:
        cmd = input().strip().lower()
        if cmd == 'q':
            running = False
            print("Agent stopped.")
            break


# --- Entry point ---
if __name__ == "__main__":
    show_notification()
    print("Type 'start' to run the desktop agent:")
    user_input = input().strip().lower()
    if user_input == 'start':
        show_notification()  # Run immediately once
        start_agent()
    else:
        print("Exiting without starting agent.")
