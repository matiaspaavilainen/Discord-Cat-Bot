import discord
import asyncpraw
import random

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

reddit = asyncpraw.Reddit(
    client_id="CLIENT_ID",
    client_secret="CLIENT_SECRET",
    user_agent="USER_AGENT",
)

# Name of the subreddit as string

subs = [
    "OneOrangeBraincell",
    "Catswithjobs",
    "Catloaf",
    "WhatsWrongWithYourCat",
    "teefies",
    "CatsOnKeyboards",
    "blurrypicturesofcats",
]

submissions = []

async def getSubmissions(n):
    for sub in subs:
        subreddit = await reddit.subreddit(sub)
        async for submission in subreddit.hot(limit=n):
            # Filter crossposts and videos out
            if submission.is_reddit_media_domain and submission.url.startswith("https://i"):
                submissions.append(submission.url)
            else:
                continue
        print(len(submissions))


async def randomPost():
    if len(submissions) == 0:
        await getSubmissions(10)
    post = random.choice(submissions)
    submissions.remove(post)
    return post


@client.event
async def on_ready():
    print("Getting submissions...")
    await getSubmissions(10)
    print("Logged in as {0.user}".format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('/cat'):
        await message.channel.send(await randomPost())

client.run("DISCORD_TOKEN")
