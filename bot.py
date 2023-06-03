import discord
from discord import app_commands
from discord.ext import commands
import re

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='/', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    synced = await bot.tree.sync()

@bot.command(name='top')
async def top(ctx, start_date:str, end_date:str, count: int = 1):
    # Specify the channel where messages should be searched
    channel_id = 1062672408747712542  #Channel ID for #retail-keys

    channel = bot.get_channel(channel_id)
    if channel is None:
        await ctx.send("Invalid channel ID.")
        return

    # Regular expression pattern to extract usernames
    pattern = r'\[(.*?)\]\(https:\/\/raider\.io\/characters\/[^\/]+\/([^?]+)\?.*?\)'

    # Fetch messages from the channel history
    messages = []
    async for message in channel.history(limit=1000, oldest_first=True):
        messages.append(message)

    # Iterate through the fetched messages
    mentioned_users = {}
    for message in messages:
        if message.created_at.strftime('%Y-%m-%d') >= start_date:
            if message.created_at.strftime('%Y-%m-%d') <= end_date:
                if message.embeds:
                    for embed in message.embeds:
                        message_content = embed.to_dict().get('description', '')

                        # Extract usernames using regex
                        matches = re.findall(pattern, message_content)
                        usernames = [match[1] for match in matches]
                        for username in usernames:
                            mentioned_users.setdefault(username, 0)
                            mentioned_users[username] += 1

    # Check if any mentioned usernames were found
    if not mentioned_users:
        await ctx.send("No mentioned usernames found in the specified date range.")
        return

    # Find the top mentioned usernames
    sorted_usernames = sorted(mentioned_users, key=lambda x: mentioned_users[x], reverse=True)
    top_usernames = sorted_usernames[:count]

    # Reply with the top mentioned usernames and their mention counts
    reply = f"The top {count} mentioned usernames between {start_date} and {end_date} are:\n"
    for i, username in enumerate(top_usernames, start=1):
        mention_count = mentioned_users[username]
        reply += f"{i}. '{username.split('/')[1]}' with {mention_count} mentions\n"
    await ctx.send(reply)

bot.run('MTEwMjQ0Njk5MDIxMTY5NDYxMg.GBtLeL.NZ1rK_P4ZGEGceD830rbKDONMg-imDdnfsg4GE')