# Discord Weather Bot

A multilingual Discord bot that provides current weather information for any city in the world. This bot uses the WeatherAPI.com API to fetch accurate and up-to-date weather data.

## Features

- Get current weather information for any city
- Multilanguage support
- Display detailed information such as temperature, humidity, wind speed, atmospheric pressure, and more
- User-friendly interface with simple commands

## Prerequisites

- Python 3.8 or newer
- A Discord account to get a bot token
- An account on WeatherAPI.com to get an API key

## Installation

1. Download or clone this repository:
   ```
   git clone https://github.com/TerminalDZ/discord-weather-bot.git
   cd discord-weather-bot
   ```

2. Install the required libraries:
   ```
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the root folder of the project and add your Discord bot token and WeatherAPI key:
   ```
   DISCORD_BOT_TOKEN=your_discord_bot_token_here
   WEATHER_API_KEY=your_weatherapi_key_here
   ```

## How to Get the Required Tokens

### Getting a Discord Bot Token

1. Visit the [Discord Developer Portal](https://discord.com/developers/applications)
2. Click on "New Application" and enter a name for your application
3. Go to the "Bot" section and click "Add Bot"
4. Customize your bot and copy the token

### Getting an API Key from WeatherAPI

1. Create an account on [WeatherAPI.com](https://www.weatherapi.com/)
2. After logging in, go to your dashboard
3. You'll find your API key in the "API Keys" section

## Running the Bot

To run the bot, execute the following command in the project's root directory:

```
python discord_bot.py
```

## Usage

Once the bot is running and added to your Discord server, you can use the following commands:

- `!help`: Display a list of all available commands
- `!weather`: Get weather information for a specific city
- `!setlanguage`: Set the language for weather information

## Contributing

Contributions are welcome! If you'd like to contribute, please follow these steps:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push the branch (`git push origin feature/AmazingFeature`)
5. Open a pull request

## License

This project is distributed under the MIT License. See the `LICENSE` file for more information.

## Contact

Project Link: [Discord Weather Bot](https://github.com/TerminalDZ/discord-weather-bot)

If you have any questions or suggestions, feel free to open an issue or contact us!
