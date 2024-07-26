import discord
from discord.ext import commands
import requests
import asyncio
import os
from dotenv import load_dotenv
import logging
from typing import Dict, Any, Optional
import aiohttp 

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()
DISCORD_BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')
API_KEY = os.getenv('WEATHER_API_KEY')
BASE_URL = "http://api.weatherapi.com/v1"

# Bot setup
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

# Language codes mapping
LANG_CODES = {
    "ar": "Arabic", "bn": "Bengali", "bg": "Bulgarian", "zh": "Chinese Simplified",
    "zh_tw": "Chinese Traditional", "cs": "Czech", "da": "Danish", "nl": "Dutch",
    "fi": "Finnish", "fr": "French", "de": "German", "el": "Greek", "hi": "Hindi",
    "hu": "Hungarian", "it": "Italian", "ja": "Japanese", "jv": "Javanese",
    "ko": "Korean", "zh_cmn": "Mandarin", "mr": "Marathi", "pl": "Polish",
    "pt": "Portuguese", "pa": "Punjabi", "ro": "Romanian", "ru": "Russian",
    "sr": "Serbian", "si": "Sinhalese", "sk": "Slovak", "es": "Spanish",
    "sv": "Swedish", "ta": "Tamil", "te": "Telugu", "tr": "Turkish",
    "uk": "Ukrainian", "ur": "Urdu", "vi": "Vietnamese", "zh_wuu": "Wu (Shanghainese)",
    "zh_hsn": "Xiang", "zh_yue": "Yue (Cantonese)", "zu": "Zulu", "en": "English"
}

# Translations for weather fields
WEATHER_TRANSLATIONS = {
    "ar": {"Temperature": "درجة الحرارة", "Condition": "الحالة", "Wind": "الرياح", "Humidity": "الرطوبة", "Cloud Coverage": "تغطية السحب", "Feels Like": "الإحساس", "Pressure": "الضغط", "Visibility": "الرؤية", "UV Index": "مؤشر الأشعة فوق البنفسجية", "Gust": "هبوب الرياح"},
    "bn": {"Temperature": "তাপমাত্রা", "Condition": "অবস্থা", "Wind": "বাতাস", "Humidity": "আর্দ্রতা", "Cloud Coverage": "মেঘের আচ্ছাদন", "Feels Like": "অনুভূত", "Pressure": "চাপ", "Visibility": "দৃশ্যমানতা", "UV Index": "ইউভি সূচক", "Gust": "ঝোঁক"},
    "bg": {"Temperature": "Температура", "Condition": "Състояние", "Wind": "Вятър", "Humidity": "Влажност", "Cloud Coverage": "Облачно покритие", "Feels Like": "Усеща се като", "Pressure": "Налягане", "Visibility": "Видимост", "UV Index": "UV индекс", "Gust": "Порив"},
    "zh": {"Temperature": "温度", "Condition": "状况", "Wind": "风", "Humidity": "湿度", "Cloud Coverage": "云量", "Feels Like": "体感温度", "Pressure": "气压", "Visibility": "能见度", "UV Index": "紫外线指数", "Gust": "阵风"},
    "zh_tw": {"Temperature": "溫度", "Condition": "狀況", "Wind": "風", "Humidity": "濕度", "Cloud Coverage": "雲量", "Feels Like": "體感溫度", "Pressure": "氣壓", "Visibility": "能見度", "UV Index": "紫外線指數", "Gust": "陣風"},
    "cs": {"Temperature": "Teplota", "Condition": "Stav", "Wind": "Vítr", "Humidity": "Vlhkost", "Cloud Coverage": "Oblačnost", "Feels Like": "Pocitová teplota", "Pressure": "Tlak", "Visibility": "Viditelnost", "UV Index": "UV index", "Gust": "Poryv větru"},
    "da": {"Temperature": "Temperatur", "Condition": "Tilstand", "Wind": "Vind", "Humidity": "Luftfugtighed", "Cloud Coverage": "Skydække", "Feels Like": "Føles som", "Pressure": "Tryk", "Visibility": "Sigtbarhed", "UV Index": "UV-indeks", "Gust": "Vindstød"},
    "nl": {"Temperature": "Temperatuur", "Condition": "Toestand", "Wind": "Wind", "Humidity": "Luchtvochtigheid", "Cloud Coverage": "Bewolking", "Feels Like": "Gevoelstemperatuur", "Pressure": "Luchtdruk", "Visibility": "Zichtbaarheid", "UV Index": "UV-index", "Gust": "Windstoot"},
    "fi": {"Temperature": "Lämpötila", "Condition": "Tila", "Wind": "Tuuli", "Humidity": "Kosteus", "Cloud Coverage": "Pilvipeite", "Feels Like": "Tuntuu kuin", "Pressure": "Paine", "Visibility": "Näkyvyys", "UV Index": "UV-indeksi", "Gust": "Puuska"},
    "fr": {"Temperature": "Température", "Condition": "Condition", "Wind": "Vent", "Humidity": "Humidité", "Cloud Coverage": "Couverture nuageuse", "Feels Like": "Ressenti", "Pressure": "Pression", "Visibility": "Visibilité", "UV Index": "Indice UV", "Gust": "Rafale"},
    "de": {"Temperature": "Temperatur", "Condition": "Zustand", "Wind": "Wind", "Humidity": "Luftfeuchtigkeit", "Cloud Coverage": "Bewölkung", "Feels Like": "Gefühlt wie", "Pressure": "Luftdruck", "Visibility": "Sichtweite", "UV Index": "UV-Index", "Gust": "Windböe"},
    "el": {"Temperature": "Θερμοκρασία", "Condition": "Κατάσταση", "Wind": "Άνεμος", "Humidity": "Υγρασία", "Cloud Coverage": "Νεφοκάλυψη", "Feels Like": "Αίσθηση", "Pressure": "Πίεση", "Visibility": "Ορατότητα", "UV Index": "Δείκτης UV", "Gust": "Ριπή"},
    "hi": {"Temperature": "तापमान", "Condition": "स्थिति", "Wind": "हवा", "Humidity": "नमी", "Cloud Coverage": "बादल छाया", "Feels Like": "महसूस होता है", "Pressure": "दबाव", "Visibility": "दृश्यता", "UV Index": "यूवी सूचकांक", "Gust": "हवा का झोंका"},
    "hu": {"Temperature": "Hőmérséklet", "Condition": "Állapot", "Wind": "Szél", "Humidity": "Páratartalom", "Cloud Coverage": "Felhőborítottság", "Feels Like": "Hőérzet", "Pressure": "Légnyomás", "Visibility": "Látótávolság", "UV Index": "UV index", "Gust": "Széllökés"},
    "it": {"Temperature": "Temperatura", "Condition": "Condizione", "Wind": "Vento", "Humidity": "Umidità", "Cloud Coverage": "Copertura nuvolosa", "Feels Like": "Percepita", "Pressure": "Pressione", "Visibility": "Visibilità", "UV Index": "Indice UV", "Gust": "Raffica"},
    "ja": {"Temperature": "気温", "Condition": "状態", "Wind": "風", "Humidity": "湿度", "Cloud Coverage": "雲量", "Feels Like": "体感温度", "Pressure": "気圧", "Visibility": "視界", "UV Index": "UV指数", "Gust": "突風"},
    "jv": {"Temperature": "Suhu", "Condition": "Kahanan", "Wind": "Angin", "Humidity": "Kelembaban", "Cloud Coverage": "Tutupan Awan", "Feels Like": "Krasa Kaya", "Pressure": "Tekanan", "Visibility": "Visibilitas", "UV Index": "Indeks UV", "Gust": "Angin Kencang"},
    "ko": {"Temperature": "온도", "Condition": "상태", "Wind": "바람", "Humidity": "습도", "Cloud Coverage": "구름 덮임", "Feels Like": "체감 온도", "Pressure": "기압", "Visibility": "가시성", "UV Index": "자외선 지수", "Gust": "돌풍"},
    "zh_cmn": {"Temperature": "温度", "Condition": "状况", "Wind": "风", "Humidity": "湿度", "Cloud Coverage": "云量", "Feels Like": "体感温度", "Pressure": "气压", "Visibility": "能见度", "UV Index": "紫外线指数", "Gust": "阵风"},
    "mr": {"Temperature": "तापमान", "Condition": "स्थिती", "Wind": "वारा", "Humidity": "आर्द्रता", "Cloud Coverage": "ढग आच्छादन", "Feels Like": "जाणवते", "Pressure": "दाब", "Visibility": "दृश्यता", "UV Index": "यूव्ही निर्देशांक", "Gust": "वाऱ्याचा झोत"},
    "pl": {"Temperature": "Temperatura", "Condition": "Stan", "Wind": "Wiatr", "Humidity": "Wilgotność", "Cloud Coverage": "Zachmurzenie", "Feels Like": "Odczuwalna", "Pressure": "Ciśnienie", "Visibility": "Widoczność", "UV Index": "Indeks UV", "Gust": "Podmuch"},
    "pt": {"Temperature": "Temperatura", "Condition": "Condição", "Wind": "Vento", "Humidity": "Humidade", "Cloud Coverage": "Cobertura de Nuvens", "Feels Like": "Sensação Térmica", "Pressure": "Pressão", "Visibility": "Visibilidade", "UV Index": "Índice UV", "Gust": "Rajada"},
    "pa": {"Temperature": "ਤਾਪਮਾਨ", "Condition": "ਹਾਲਤ", "Wind": "ਹਵਾ", "Humidity": "ਨਮੀ", "Cloud Coverage": "ਬੱਦਲ ਛਾਏ", "Feels Like": "ਮਹਿਸੂਸ ਹੁੰਦਾ ਹੈ", "Pressure": "ਦਬਾਅ", "Visibility": "ਦ੍ਰਿਸ਼ਟੀ", "UV Index": "ਯੂਵੀ ਸੂਚਕਾਂਕ", "Gust": "ਝੋਕਾ"},
    "ro": {"Temperature": "Temperatură", "Condition": "Condiție", "Wind": "Vânt", "Humidity": "Umiditate", "Cloud Coverage": "Acoperire cu nori", "Feels Like": "Se simte ca", "Pressure": "Presiune", "Visibility": "Vizibilitate", "UV Index": "Index UV", "Gust": "Rafală"},
    "ru": {"Temperature": "Температура", "Condition": "Состояние", "Wind": "Ветер", "Humidity": "Влажность", "Cloud Coverage": "Облачность", "Feels Like": "Ощущается как", "Pressure": "Давление", "Visibility": "Видимость", "UV Index": "УФ-индекс", "Gust": "Порыв ветра"},
    "sr": {"Temperature": "Температура", "Condition": "Стање", "Wind": "Ветар", "Humidity": "Влажност", "Cloud Coverage": "Облачност", "Feels Like": "Осећај", "Pressure": "Притисак", "Visibility": "Видљивост", "UV Index": "УВ индекс", "Gust": "Удар ветра"},
    "si": {"Temperature": "උෂ්ණත්වය", "Condition": "තත්ත්වය", "Wind": "සුළඟ", "Humidity": "ආර්ද්රතාව", "Cloud Coverage": "වලාකුළු ආවරණය", "Feels Like": "දැනෙන", "Pressure": "පීඩනය", "Visibility": "දර්ශනය", "UV Index": "UV දර්ශකය", "Gust": "සුළං රළ"},
    "sk": {"Temperature": "Teplota", "Condition": "Stav", "Wind": "Vietor", "Humidity": "Vlhkosť", "Cloud Coverage": "Oblačnosť", "Feels Like": "Pocitovo", "Pressure": "Tlak", "Visibility": "Viditeľnosť", "UV Index": "UV index", "Gust": "Náraz vetra"},
    "es": {"Temperature": "Temperatura", "Condition": "Condición", "Wind": "Viento", "Humidity": "Humedad", "Cloud Coverage": "Nubosidad", "Feels Like": "Sensación térmica", "Pressure": "Presión", "Visibility": "Visibilidad", "UV Index": "Índice UV", "Gust": "Ráfaga"},
    "sv": {"Temperature": "Temperatur", "Condition": "Tillstånd", "Wind": "Vind", "Humidity": "Luftfuktighet", "Cloud Coverage": "Molntäcke", "Feels Like": "Känns som", "Pressure": "Lufttryck", "Visibility": "Sikt", "UV Index": "UV-index", "Gust": "Vindby"},
    "ta": {"Temperature": "வெப்பநிலை", "Condition": "நிலைமை", "Wind": "காற்று", "Humidity": "ஈரப்பதம்", "Cloud Coverage": "மேக மூட்டம்", "Feels Like": "உணர்கிறது", "Pressure": "அழுத்தம்", "Visibility": "தெரிவுநிலை", "UV Index": "UV குறியீடு", "Gust": "காற்று வீச்சு"},
    "te": {"Temperature": "ఉష్ణోగ్రత", "Condition": "పరిస్థితి", "Wind": "గాలి", "Humidity": "తేమ", "Cloud Coverage": "మేఘాచ్ఛాదనం", "Feels Like": "అనిపిస్తోంది", "Pressure": "ఒత్తిడి", "Visibility": "దృశ్యమానత", "UV Index": "UV సూచిక", "Gust": "గాలి దుమారం"},
    "en": {"Temperature": "Temperature", "Condition": "Condition", "Wind": "Wind", "Humidity": "Humidity", "Cloud Coverage": "Cloud Coverage", "Feels Like": "Feels Like", "Pressure": "Pressure", "Visibility": "Visibility", "UV Index": "UV Index", "Gust": "Gust"},

}

# Default language
bot.language = 'en'

@bot.event
async def on_ready():
    logger.info(f'Bot is ready. Logged in as {bot.user.name}')

@bot.command(name="help")
async def help_command(ctx):
    help_text = """
    **Weather Bot Commands:**
    `!weather` - Get the current weather for a specified city.
    `!setlanguage [code]` - Set the language for the weather information.
    `!listlanguages` - List all available languages.
    """
    await ctx.send(help_text)

@bot.command(name="setlanguage")
async def set_language(ctx, lang_code: str):
    if lang_code in LANG_CODES:
        bot.language = lang_code
        await ctx.send(f"Language set to {LANG_CODES[lang_code]}")
    else:
        await ctx.send("Invalid language code. Please try again.")

@bot.command(name="listlanguages")
async def list_languages(ctx):
    languages = '\n'.join([f"{code}: {name}" for code, name in LANG_CODES.items()])
    await ctx.send(f"Available languages:\n{languages}")

@bot.command(name="weather")
async def weather(ctx):
    await ctx.send("Please enter the city name to get the current weather:")

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    try:
        msg = await bot.wait_for("message", check=check, timeout=30)
        city = msg.content
        weather_data = await get_weather(city, bot.language)
        if weather_data:
            await send_weather_embed(ctx, city, weather_data)
        else:
            await ctx.send("Could not find the weather for this city. Please try again.")
    except asyncio.TimeoutError:
        await ctx.send("Time limit exceeded for entering the city name.")

async def get_weather(city: str, lang: str) -> Optional[Dict[str, Any]]:
    url = f"{BASE_URL}/current.json"
    params = {"key": API_KEY, "q": city, "lang": lang}
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    return data['current']
                else:
                    logger.error(f"Error fetching weather data: {response.status}")
                    return None
    except Exception as e:
        logger.error(f"Exception occurred while fetching weather data: {e}")
        return None

async def send_weather_embed(ctx, city: str, weather_data: Dict[str, Any]):
    lang = bot.language
    translations = WEATHER_TRANSLATIONS.get(lang, WEATHER_TRANSLATIONS['en'])
    
    embed = discord.Embed(title=f"{translations['Condition']} in {city}", color=discord.Color.blue())
    embed.add_field(name=translations["Temperature"], value=f"{weather_data['temp_c']} °C / {weather_data['temp_f']} °F")
    embed.add_field(name=translations["Condition"], value=weather_data['condition']['text'])
    embed.add_field(name=translations["Wind"], value=f"{weather_data['wind_kph']} kph / {weather_data['wind_mph']} mph")
    embed.add_field(name=translations["Humidity"], value=f"{weather_data['humidity']}%")
    embed.add_field(name=translations["Cloud Coverage"], value=f"{weather_data['cloud']}%")
    embed.add_field(name=translations["Feels Like"], value=f"{weather_data['feelslike_c']} °C / {weather_data['feelslike_f']} °F")
    embed.add_field(name=translations["Pressure"], value=f"{weather_data['pressure_mb']} mb / {weather_data['pressure_in']} in")
    embed.add_field(name=translations["Visibility"], value=f"{weather_data['vis_km']} km / {weather_data['vis_miles']} miles")
    embed.add_field(name=translations["UV Index"], value=f"{weather_data['uv']}")
    embed.add_field(name=translations["Gust"], value=f"{weather_data['gust_kph']} kph / {weather_data['gust_mph']} mph")
    embed.set_thumbnail(url=f"http:{weather_data['condition']['icon']}")
    
    await ctx.send(embed=embed)

if __name__ == "__main__":
    bot.run(DISCORD_BOT_TOKEN)