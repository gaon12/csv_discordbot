import csv
import discord
from discord.ext import commands
import asyncio
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import openpyxl
import xlrd
import os

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

def read_csv_or_tsv(file_path, delimiter=','):
    try:
        with open(file_path, mode='r', encoding='utf-8') as f:
            reader = csv.reader(f, delimiter=delimiter)
            next(reader)  # 첫 번째 행(헤더) 건너뛰기
            return {row[0]: row[1] for row in reader}
    except Exception as e:
        logging.error(f"Error reading CSV/TSV file: {e}")
        return {}

def read_xls(file_path):
    try:
        workbook = xlrd.open_workbook(file_path)
        sheet = workbook.sheet_by_index(0)
        return {sheet.cell_value(row, 0): sheet.cell_value(row, 1) for row in range(1, sheet.nrows)}
    except Exception as e:
        logging.error(f"Error reading XLS file: {e}")
        return {}

def read_xlsx(file_path):
    try:
        workbook = openpyxl.load_workbook(file_path, data_only=True)
        sheet = workbook.active
        return {sheet.cell(row=row, column=1).value: sheet.cell(row=row, column=2).value for row in range(2, sheet.max_row + 1)}
    except Exception as e:
        logging.error(f"Error reading XLSX file: {e}")
        return {}

async def load_qa_data():
    file_path = 'qa_data'  # 파일 이름(확장자 제외)
    if os.path.exists(f"{file_path}.tsv"):
        return read_csv_or_tsv(f"{file_path}.tsv", delimiter='\t')
    elif os.path.exists(f"{file_path}.xlsx"):
        return read_xlsx(f"{file_path}.xlsx")
    elif os.path.exists(f"{file_path}.xls"):
        return read_xls(f"{file_path}.xls")
    elif os.path.exists(f"{file_path}.csv"):
        return read_csv_or_tsv(f"{file_path}.csv")
    else:
        logging.error("No suitable QA data file found.")
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
