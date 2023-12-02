from nextcord import slash_command, Interaction, SlashOption
from nextcord.ext.commands import Cog, Bot
import json


class AddAlt(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    # Adds alt account in bot files
    @slash_command(name="add_alt", description="Add your alt account")
    async def add_alt(self, interaction: Interaction, alt: str = SlashOption(name="alt_account")):
        with open("users.json", "r") as users:
            users_data = json.load(users)
        user_id = str(interaction.user.id)

        if not alt.isascii() or len(alt) > 40:
            await interaction.send("Bro wtf are you trying to input???")
        elif len(users_data[user_id]["alts"]) > 50:
            await interaction.send("You have reached the limit of alt accounts amount (50)")
        elif alt.lower() in list(map(lambda name: name.lower(), users_data[user_id]["alts"])):
            await interaction.send("This account is already in your list!")
        else:
            users_data[user_id]["alts"].append(alt)

            with open("users.json", "w") as users:
                users.write(json.dumps(users_data, indent=2))

            await interaction.send(f"Added account `{alt}` to your list")


def setup(bot: Bot):
    bot.add_cog(AddAlt(bot))
