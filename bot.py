import csv
import discord
from discord.ext import commands
import asyncio
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# 로깅 설정
logging.basicConfig(level=logging.INFO)

def read_token_from_file(file_path):
    try:
        with open(file_path, 'r') as f:
            token = f.read().strip()
        return token
    except Exception as e:
        logging.error(f"Token file read error: {e}")
        return None

TOKEN = read_token_from_file('token.txt')

async def load_qa_data():
    try:
        with open('qa_data.csv', mode='r', encoding='utf-8') as f:
            reader = csv.reader(f, quotechar='"', quoting=csv.QUOTE_ALL)
            next(reader)
            qa_data = {row[0]: row[1] for row in reader}
        return qa_data
    except Exception as e:
        logging.error(f"QA data file read error: {e}")
        return {}

class FileChangeHandler(FileSystemEventHandler):
    def __init__(self, bot, filename, callback):
        self.bot = bot
        self.filename = filename
        self.callback = callback

    def on_modified(self, event):
        if event.src_path == self.filename:
            asyncio.run_coroutine_threadsafe(self.callback(), self.bot.loop)

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    global qa_data
    qa_data = await load_qa_data()
    print(f'{bot.user} has connected to Discord!')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    await bot.process_commands(message)

@bot.command()
async def cmdname(ctx, *args):
    question = ' '.join(args)
    if question in qa_data:
        await ctx.send(qa_data[question])
    else:
        await ctx.send('Sorry, no answer values were found for the question you entered.')

@bot.command()
async def help_cmd(ctx):
    await ctx.send("Usage: !cmdname [question]")

async def update_qa_data():
    global qa_data
    qa_data = await load_qa_data()
    logging.info("QA data updated.")

if TOKEN:
    event_handler = FileChangeHandler(bot, 'qa_data.csv', update_qa_data)
    observer = Observer()
    observer.schedule(event_handler, path='.', recursive=False)
    observer.start()
    try:
        bot.run(TOKEN)
    finally:
        observer.stop()
        observer.join()
else:
    logging.error("No valid token found.")
