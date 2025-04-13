## macOS Desktop Agent: AI News Summarizer

A lightweight Python desktop agent for macOS that fetches the latest AI news, summarizes it using OpenAI's GPT model, and shows a daily native macOS notification with a clickable link to the full summary.


### Features

- Fetches recent **AI news** articles using [NewsAPI](https://newsapi.org/)
- Summarizes news using **OpenAI GPT** via [LangChain](https://www.langchain.com/)
- Sends a **native macOS notification** with `terminal-notifier`
- **Click notification** to open full summary in a text file
- Scheduled to run **daily at 9:00 AM**
- Simple CLI to start and stop the agent


### Preview

- Daily notification at 9:00 AM
- View full summary by clicking the notification
- Runs silently in the background


## Requirements

- macOS (tested on Ventura/Sonoma)
- Python 3.11+
- [Homebrew](https://brew.sh/)
- OpenAI API Key
- NewsAPI Key


### Setup Instructions

#### 1. Clone the Repo

```bash
git clone https://github.com/yourusername/desktop-agent.git
cd desktop-agent
```

#### 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

#### 3. Install terminal-notifier (for macOS notifications)

```bash
brew install terminal-notifier
```

#### 4. Create `.env` File

```env
NEWS_API_KEY=your_news_api_key
OPENAI_API_KEY=your_openai_api_key
```


### How It Works

- `main.py` fetches the latest 3 articles about AI
- Passes the titles/descriptions to OpenAI via LangChain
- Trims the summary for notification display
- Saves full summary in `latest_summary.txt`
- Uses `terminal-notifier` to show notification with a "View Full Summary" action


### Usage

#### Run the Agent

```bash
python main.py
```

Then type:

```
start
```

You’ll see:

```
Agent started. Press 'q' to quit.
```

- `q` to quit and stop the agent


### Customization

- Change `"AI"` to another topic in `fetch_news_text()`
- Modify notification time in `schedule.every().day.at("09:00")`
- Extend with Slack alerts, email, or a GUI


### Troubleshooting

#### Notification not showing?

- Ensure `terminal-notifier` is installed:  
  `which terminal-notifier`
- Allow notifications in **System Settings > Notifications > Terminal**
- Disable **Do Not Disturb / Focus Mode**
- Run test notification:  
  ```bash
  terminal-notifier -title "Test" -message "This is a test"
  ```


### License

MIT License


### Contributing

Pull requests are welcome. For major changes, open an issue first to discuss what you would like to change.


### Credits

- [LangChain](https://www.langchain.com/)
- [OpenAI](https://platform.openai.com/)
- [NewsAPI](https://newsapi.org/)
- [terminal-notifier](https://github.com/julienXX/terminal-notifier)
