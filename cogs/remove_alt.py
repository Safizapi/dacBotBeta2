from nextcord import slash_command, Interaction, SlashOption
from nextcord.ext.commands import Cog, Bot
import json


class RemoveAlt(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    # Removes alt account from bot files
    @slash_command(name="remove_alt", description="Remove your alt account")
    async def remove_alt(self, interaction: Interaction, alt: str = SlashOption(name="alt_account")):
        with open("users.json", "r") as users:
            users_data = json.load(users)

        user_id = str(interaction.user.id)
        alt_list_lower = list(map(lambda name: name.lower(), users_data[user_id]["alts"]))

        if not alt.isascii() or len(alt) > 40:
            await interaction.send("Bro wtf are you trying to input???")
        elif alt.lower() not in list(map(lambda name: name.lower(), users_data[user_id]["alts"])):
            await interaction.send(f"No account {alt} was found in the list")
        elif alt.lower() in alt_list_lower:
            users_data[user_id]["alts"].pop(alt_list_lower.index(alt.lower()))

            with open("users.json", "w") as users:
                users.write(json.dumps(users_data, indent=2))

            await interaction.send(f"Account `{alt}` was removed from your account list")


def setup(bot: Bot):
    bot.add_cog(RemoveAlt(bot))
