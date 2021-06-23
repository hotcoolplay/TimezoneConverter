import os
import discord
from dotenv import load_dotenv
from discord.ext import commands
from discord.ext.commands import CommandNotFound

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.typing = True

bot = commands.Bot(command_prefix=".", intents=intents)
bot.remove_command('help')
bot.remove_command('invite')

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')


@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        return
    raise error


@bot.command()
async def help(ctx):
    embed = discord.Embed(title="Help", description="General commands.",
                              color=0x00ff00)
    embed.add_field(name="Commands", value='''
        help
        
        invite
        
        categories''', inline=True)
    embed.add_field(name="Description", value='''
        Returns this message.
        
        Displays the invite link for this bot.
        
        Displays categories of things this bot can do; use .[category] to look at their commands.''', inline=True)
    await ctx.channel.send(embed=embed)


@bot.command()
async def invite(ctx):
    await ctx.channel.send(
        'https://discord.com/api/oauth2/authorize?client_id=851830140702818304&permissions=0&scope=bot')


@bot.command()
async def categories(ctx):
    embed = discord.Embed(title="Categories", description="Categories of commands.",
                          color=0x00ff00)
    embed.add_field(name="Categories", value='''
          time''', inline=True)
    embed.add_field(name="Description", value='''
          Allows the user to convert timezones.''', inline=True)
    await ctx.channel.send(embed=embed)

bot.run(TOKEN)
