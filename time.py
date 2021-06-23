import datetime
import discord
import asyncio
from discord.ext import commands


def setup(bot):
    bot.add_cog(Time(bot))


class Time(commands.Cog, name='Time'):
    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    async def time(self, ctx):
        # If no subcommand is used, displays commands in an embed
        if ctx.invoked_subcommand is None:
            embed = discord.Embed(title="Time", description="Returns timezones of other people in your local time.",
                                  color=0x00ff00)
            embed.add_field(name="Command", value='''
            time help
        
            time register [diff]
        
        
            time convert @user''', inline=True)
            embed.add_field(name="Description", value='''
            Returns this message.
        
            Adds your timezone. diff is the difference between your timezone and UTC. For example, CEST would be +02:00. 
        
            Retrieves time of other person in your timezone. You have to ping them.''', inline=True)
            await ctx.channel.send(embed=embed)

    @time.command()
    async def help(self, ctx):
        # Displays commands in an embed
        embed = discord.Embed(title="Time", description="Returns timezones of other people in your local time.",
                              color=0x00ff00)
        embed.add_field(name="Command", value='''
            time help

            time register [diff]


            time convert @user''', inline=True)
        embed.add_field(name="Description", value='''
            Returns this message.

            Adds your timezone. diff is the difference between your timezone and UTC. For example, CEST would be +02:00. 

            Retrieves time of other person in your timezone. You have to ping them.''', inline=True)
        await ctx.channel.send(embed=embed)

    @time.command()
    async def register(self, ctx, timezone: str):
        flag = 0

        def check(author):
            def inner_check(message):
                if message.author != author:
                    return False
                if message.content == 'y':
                    return True
                if message.content == 'n':
                    return True
                return False

            return inner_check

        with open('timezones.txt', 'r') as timezones:
            for line in timezones:
                if line == str(ctx.author.id) + '\n':
                    flag = 1
                    break
        if timezone.find('+', 0, 1) == -1 and timezone.find('-', 0, 1) == -1:
            await ctx.channel.send('Remember to put a + or - in front of the time')
        elif len(timezone) != 6:
            await ctx.channel.send('Timezone isn\'t the correct length. Maybe you forgot to pad 0s?')
        elif int(timezone[5:7]) > 14:
            await ctx.channel.send('Not a valid timezone.')
        elif flag == 1:
            await ctx.channel.send('It appears you have registered already. Would you like to re-register? (y/n)')
            try:
                msg = await self.bot.wait_for('message', check=check(ctx.author), timeout=10)
            except asyncio.TimeoutError:
                await ctx.channel.send('You didn\'t respond in time.')
            else:
                if msg.content == 'y':
                    index = 0
                    with open('timezones.txt', 'r') as timezones:
                        for i, line in enumerate(timezones):
                            if line == str(ctx.author.id) + '\n':
                                index = i + 1
                                break
                    with open('timezones.txt', 'r') as timezones:
                        data = timezones.readlines()
                    with open('timezones.txt', 'w') as timezones:
                        for i, line in enumerate(data):
                            if i == index:
                                timezones.writelines(timezone + '\n')
                            else:
                                timezones.writelines(line)
                    await ctx.channel.send('You have been re-registered.')
                elif msg.content == 'n':
                    await ctx.channel.send('Keeping old timezone.')
        else:
            file = open("timezones.txt", "a")
            file.write(str(ctx.author.id) + "\n")
            file.write(timezone + "\n")
            file.close()
            await ctx.channel.send('You have been registered.')

    @time.command()
    async def convert(self, ctx, member: discord.Member):
        memberdiff = ""
        index = 0
        with open('timezones.txt', 'r') as timezones:
            for i, line in enumerate(timezones):
                if line == str(member.id) + '\n':
                    index = i + 1
                    break
        timezones = open("timezones.txt", 'r')
        for i, line in enumerate(timezones):
            if i == index:
                memberdiff = line
        if memberdiff == "":
            await ctx.channel.send(
                'It looks like they have not registered yet. Tell them to register using time register.')
        memberh = 0
        memberm = 0
        if memberdiff[0] == "-":
            if memberdiff[1] == "0":
                memberh = 0 - int(memberdiff[2])
                memberm = int(memberdiff[4:])
            else:
                memberh = 0 - int(memberdiff[1:3])
                memberm = int(memberdiff[4:])
        else:
            if memberdiff[1] == "0":
                memberh = int(memberdiff[2])
                memberm = int(memberdiff[4:])
            else:
                memberh = int(memberdiff[1:3])
                memberm = int(memberdiff[4:])
        currenttime = datetime.datetime.utcnow()
        hour = int(currenttime.strftime('%H')) + memberh
        minute = int(currenttime.strftime('%M')) + memberm
        year = int(currenttime.strftime('%Y'))
        monthnow = int(currenttime.strftime('%m')) - 1
        day = int(currenttime.strftime('%d'))
        weekdaynow = int(currenttime.strftime('%w'))
        weekdays = ['Sun ', 'Mon ', 'Tue ', 'Wed ', 'Thu ', 'Fri ', 'Sat ']
        months = ['Jan ', 'Feb ', 'Mar ', 'Apr ', 'May ', 'Jun ', 'Jul ', 'Aug ', 'Sep ', 'Oct ', 'Nov ', 'Dec ']
        monthday = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        if year % 4 == 0:
            if year % 100 == 0:
                if year % 400 == 0:
                    monthday[1] = 29
                else:
                    monthday[1] = 28
            else:
                monthday[1] = 29
        else:
            monthday[1] = 28
        if minute > 59:
            minute %= 60
            hour += 1
        if hour > 23:
            hour %= 24
            weekdaynow += 1
            day += 1
        if day > monthday[monthnow]:
            day %= monthday[monthnow]
            day += 1
            monthnow += 1
        if monthnow > 11:
            monthnow %= 12
            year += 1
        strhour = ''
        strminute = ''
        if hour < 10:
            strhour = '0' + str(hour)
        else:
            strhour = str(hour)
        if minute < 10:
            strminute = '0' + str(minute)
        else:
            strminute = str(minute)
        await ctx.channel.send(
            weekdays[weekdaynow] + months[monthnow] + str(day) + ' ' + str(year) + ' ' + strhour + ':' + strminute)
