# Mr.Handly Telegram Bot

## Description

Mr.Handly Telegram Bot is a bot for task management created using aiogram and SQLAlchemy. The bot allows users to create
and manage tasks, track their status, manage notes and get currency exchange rates.

## Features

- Create and manage tasks.
- Track task status (completed/cancelled).
- Add notes with tags.
- Get currency exchange rates from various sources (Monobank, BestChange, Binance).
- Generate secure passwords.
- User-friendly interface with Inline keyboards.

## Installation

### Requirements

- Python 3.11+
- Dependencies listed in `requirements.txt`

### Installation Steps

#### Manual installation

1. Clone the repository:
   ```shell
   git clone https://github.com/Grister/telegram_bot.git
   cd telegram_bot
   ```
2. Create and activate a virtual environment:
   ```shell
   python -m venv venv
   source venv/bin/activate  # for Linux/Mac
   venv\Scripts\activate  # for Windows
   ```
3. Install dependencies:
   ```shell
   pip install -r requirements.txt
   ```
4. Set environment variables in the .env file:
   ```
   BOT_TOKEN=your_bot_token
   POSTGRES_USER=postgres_user
   POSTGRES_PASSWORD=postgres_password
   POSTGRES_NAME=db_name
   POSTGRES_HOST=localhost
   POSTGRES_PORT=5432
   BESTCHANCE_API_KEY=bestchance_api_key
   ```
5. Run the bot:
   ```shell
   python main.py
   ```

#### Installation with Doker

1. Clone the repository:
   ```shell
   git clone https://github.com/Grister/telegram_bot.git
   cd telegram_bot
   ```

2. Install [Docker for Desktop](https://docs.docker.com/desktop/install/windows-install/)

3. Run docker-compose in terminal
   ```shell
   docker-compose up
   ```

4. At the end you can stop the containers with the command:
   ```shell
   docker-compose down
   ```

## Usage

### Main Commands

- `/start` - Start interacting with the bot.
- `/help` - Get list of available commands.
- `/password [length]` - Generate a password of specified length (default is 8 characters).
- `/tags` - Show all user tags.
- `/currency` - Get currency rates.
- `/create_task` - Create a new task.
- `/tasks` - Check your daily tasks'.
- `/task_archive` - View completed or cancelled tasks.

### Task Management

- Create and manage tasks.
    - Use `/create_task` to create a new task. The bot will prompt you to enter the task name.
- Track task status.
    - Use `/tasks` to see list of tasks.
    - Tasks can be marked as completed or cancelled.
- View archived tasks.
    - Use `/task_archive` to view tasks that have been completed or cancelled.

### Notes

- Add notes with tags.
    - To add a note, use the format: #tag_name note_content. The bot will save the note with the specified tag.
- View notes by tags.
    - Use `/tags` to see all tags. Select a tag to view all notes associated with that tag.
- Edit or delete notes.
    - After viewing notes by tag, you can choose to edit or delete individual notes.

### Currency Exchange Rates

- Get currency exchange rates from Monobank, BestChange, and Binance.
    - Use `/currency` to get the latest exchange rates.
    - The bot will provide exchange rates for USD/UAH, EUR/UAH, USDT/UAH, USDT/RUB, BTC/USDT, and ETH/USDT.

### Password Generation

- Generate secure passwords.
    - Use `/password` to generate an 8-character password.
    - Use `/password [length]` to generate a password of specified length.

## Project Structure

```bash
    .
    ├── main.py                   # Entry point for running the bot
    ├── database
    │ ├── models.py               # Database model definitions
    │ ├── db.py                   # Script for creating database connection
    │ └── requests              
    │ ├── note.py                 # Database requests for Note models
    │ ├── task.py                 # Database requests for Task models
    │ └── user.py                 # Database requests for User models
    ├── handlers
    │ ├── __init__.py             # Handlers initialization
    │ ├── base.py                 # Handlers for main commands
    │ ├── tasks.py                # Handlers for task management
    │ ├── currency.py             # Handlers for getting currency rates
    │ └── notes.py                # Handlers for note management
    ├── keyboards
    │ ├── __init__.py             # Keyboards initialization
    │ ├── main.py                 # Keyboards for main handlers
    │ ├── notes.py                # Keyboards for note handlers
    │ └── tasks.py                # Keyboards for task handlers
    ├── services
    │ └── currency_service.py     # Parser for getting rates
    ├── utils
    │ ├── db_utils.py             # Database utility functions
    │ ├── password_generate.py    # Utility for password generation
    │ └── text_formater.py        # Text formater utility
    ├── docker-compose.yml        # File to run project in Docker 
    ├── Dockerfile                # Dockerfile for project 
    ├── .env                      # Configuration file
    └── README.md                 # Project documentation
```
### Contributing

If you would like to contribute to the project, please create a pull request or contact me via email.

### License

This project is licensed under the MIT License. See the LICENSE file for details.

### Contact

If you have any questions or suggestions, please contact me at carroll.lewi@gmail.com.
