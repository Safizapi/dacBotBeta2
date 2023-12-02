import nextcord as nc
from nextcord.ext import commands
import cooldowns
import json

token = "TOKEN HERE"
bot = commands.Bot(intents=nc.Intents.all())

extensions = [
    "cogs.add_alt",
    "cogs.display_members",
    "cogs.match_result",
    "cogs.register_tournament",
    "cogs.remove_alt",
    "cogs.send_embed",
    "cogs.send_message",
    "cogs.tournaments",
    "cogs.user_info",
    "cogs.get_something"
]

bot.load_extensions(extensions)


@bot.event
async def on_ready():
    await bot.sync_all_application_commands()
    print("YEEE IT'S RUNNIN' BABY")


@bot.event
async def on_member_join(member):
    scratch_user_data = {
        "alts": [],
        "won_tourneys": [],
        "won_games": 0,
        "lost_games": 0
    }

    guild = bot.get_guild(1164872244078579712)
    role = guild.get_role(1178399001771516015)
    await guild.get_member(member.id).add_roles(role)

    with open("users.json", "r") as users:
        users_data = json.load(users)

    users_data[str(member.id)] = scratch_user_data

    with open("users.json", "w") as users:
        users.write(json.dumps(users_data, indent=2))


@bot.event
async def on_application_command_error(interaction: nc.Interaction, error):
    error = getattr(error, "original", error)

    if isinstance(error, cooldowns.CallableOnCooldown):
        minutes = int(error.retry_after // 60)
        seconds = int(error.retry_after % 60)
        await interaction.send(f"You're on cooldown ({minutes} minutes, {seconds} seconds)")


if __name__ == "__main__":
    bot.run(token)
