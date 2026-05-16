import os
import discord
from dotenv import load_dotenv
from src.analysis.edge_finder import find_edges

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_BOT_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f"{client.user} has connected to Discord!")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.lower() == "!ping":
        await message.channel.send(
        "Pong. Betting engine is online."
    )

    if message.content.lower() == "!bets":

        await message.channel.send(
            "Running betting analysis..."
        )

        edge_reports = find_edges()

        top_reports = edge_reports[:5]

        if not top_reports:
            await message.channel.send(
                "No betting edges found."
            )
            return

        for report in top_reports:

            message_text = (
                f"🏆 {report['team']}\n"
                f"Signal: {report['signal']}\n"
                f"Edge Score: {report['edge_score']:+.2f}\n"
                f"Odds: {report['odds']}\n"
                f"Sportsbook: {report['sportsbook']}\n"
                f"Pitcher: {report['pitcher_name']}\n"
            )

            await message.channel.send(message_text)

client.run(DISCORD_TOKEN)