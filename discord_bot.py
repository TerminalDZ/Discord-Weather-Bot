import discord
from discord.ext import commands
import requests
import asyncio
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
DISCORD_BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')
API_KEY = os.getenv('WEATHER_API_KEY')
BASE_URL = "http://api.weatherapi.com/v1"

# Bot setup
intents = discord.Intents.default()
intents.message_content = True  # Enable message content intent
bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

# Help command to assist users
@bot.command(name="help")
async def help_command(ctx):
    help_text = """
    **Weather Bot Commands:**
    `!weather` - Get the current weather for a specified city.
    `!setlanguage` - Set the language for the weather information.
    """
    await ctx.send(help_text)

# Command to set language
@bot.command(name="setlanguage")
async def set_language(ctx, lang_code):
    if lang_code in LANG_CODES:
        bot.language = lang_code
        await ctx.send(f"Language set to {LANG_CODES[lang_code]}")
    else:
        await ctx.send("Invalid language code. Please try again.")

# Command to get weather for a specified city
@bot.command(name="weather")
async def weather(ctx):
    await ctx.send("Please enter the city name to get the current weather:")

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    try:
        msg = await bot.wait_for("message", check=check, timeout=30)
        city = msg.content
        weather_data = get_weather(city, bot.language if hasattr(bot, 'language') else 'en')
        if weather_data:
            embed = discord.Embed(title=f"Weather in {city}", color=discord.Color.blue())
            embed.add_field(name="Temperature", value=f"{weather_data['temp_c']} °C / {weather_data['temp_f']} °F")
            embed.add_field(name="Condition", value=weather_data['condition']['text'])
            embed.add_field(name="Wind", value=f"{weather_data['wind_kph']} kph / {weather_data['wind_mph']} mph")
            embed.add_field(name="Humidity", value=f"{weather_data['humidity']}%")
            embed.add_field(name="Cloud Coverage", value=f"{weather_data['cloud']}%")
            embed.add_field(name="Feels Like", value=f"{weather_data['feelslike_c']} °C / {weather_data['feelslike_f']} °F")
            embed.add_field(name="Pressure", value=f"{weather_data['pressure_mb']} mb / {weather_data['pressure_in']} in")
            embed.add_field(name="Visibility", value=f"{weather_data['vis_km']} km / {weather_data['vis_miles']} miles")
            embed.add_field(name="UV Index", value=f"{weather_data['uv']}")
            embed.add_field(name="Gust", value=f"{weather_data['gust_kph']} kph / {weather_data['gust_mph']} mph")
            embed.set_thumbnail(url=f"http:{weather_data['condition']['icon']}")
            await ctx.send(embed=embed)
        else:
            await ctx.send("Could not find the weather for this city. Please try again.")
    except asyncio.TimeoutError:
        await ctx.send("Time limit exceeded for entering the city name.")

def get_weather(city, lang):
    url = f"{BASE_URL}/current.json"
    params = {
        "key": API_KEY,
        "q": city,
        "lang": lang
    }
    response = requests.get(url, params=params)

    print(f"Requesting weather data: {response}")

    try:
        data = response.json()
        return data['current']
    except requests.exceptions.JSONDecodeError:
        print(f"Failed to decode JSON. Response text: {response.text}")
        return None

# Language codes mapping
LANG_CODES = {
    "ar": "Arabic",
    "bn": "Bengali",
    "bg": "Bulgarian",
    "zh": "Chinese Simplified",
    "zh_tw": "Chinese Traditional",
    "cs": "Czech",
    "da": "Danish",
    "nl": "Dutch",
    "fi": "Finnish",
    "fr": "French",
    "de": "German",
    "el": "Greek",
    "hi": "Hindi",
    "hu": "Hungarian",
    "it": "Italian",
    "ja": "Japanese",
    "jv": "Javanese",
    "ko": "Korean",
    "zh_cmn": "Mandarin",
    "mr": "Marathi",
    "pl": "Polish",
    "pt": "Portuguese",
    "pa": "Punjabi",
    "ro": "Romanian",
    "ru": "Russian",
    "sr": "Serbian",
    "si": "Sinhalese",
    "sk": "Slovak",
    "es": "Spanish",
    "sv": "Swedish",
    "ta": "Tamil",
    "te": "Telugu",
    "tr": "Turkish",
    "uk": "Ukrainian",
    "ur": "Urdu",
    "vi": "Vietnamese",
    "zh_wuu": "Wu (Shanghainese)",
    "zh_hsn": "Xiang",
    "zh_yue": "Yue (Cantonese)",
    "zu": "Zulu",
    "en": "English"
}

# Run the bot
bot.run(DISCORD_BOT_TOKEN)
