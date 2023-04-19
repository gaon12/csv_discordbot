import csv
import discord
from discord.ext import commands

def read_token_from_file(file_path):
    with open(file_path, 'r') as f:
        token = f.read().strip()
    return token

TOKEN = read_token_from_file('token.txt')

def load_qa_data():
    with open('qa_data.csv', mode='r', encoding='utf-8') as f:
        reader = csv.reader(f, quotechar='"', quoting=csv.QUOTE_ALL)
        next(reader)
        qa_data = {row[0]: row[1] for row in reader}
    return qa_data

qa_data = load_qa_data()

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
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

bot.run(TOKEN)
