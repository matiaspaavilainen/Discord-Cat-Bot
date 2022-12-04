import discord
import praw
import random

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

reddit = praw.Reddit(
    client_id="CLIENT_ID",
    client_secret="CLIENT_SECRET",
    user_agent="USER_AGENT",
    check_for_async=False
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


def getSubmissions(n):
    for sub in subs:
        for submission in reddit.subreddit(sub).hot(limit=n):
            # Filter crossposts and videos out
            if submission.is_reddit_media_domain and submission.url.startswith("https://i"):
                submissions.append(submission.url)
            else:
                continue
        print(len(submissions))


def randomPost():
    if len(submissions) == 0:
        getSubmissions(10)
    post = random.choice(submissions)
    submissions.remove(post)
    return post


@client.event
async def on_ready():
    print("Getting submissions...")
    getSubmissions(10)
    print("Logged in as {0.user}".format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('/cat'):
        await message.channel.send(randomPost())

client.run("DISCORD_TOKEN")
