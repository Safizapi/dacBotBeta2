from nextcord import slash_command, Interaction, SlashOption, Member, Embed
from nextcord.ext.commands import Cog, Bot
from additional import on_member_join
import json


class User(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    # Displays information about member of the server in embed
    @slash_command(name="user_info", description="Displays information about user")
    async def user_info(self, interaction: Interaction, user: Member = SlashOption(name="user")):
        embed = Embed(color=0xc93c3e)
        embed.set_author(name=user, icon_url=user.avatar.url)

        with open("users.json", "r") as users:
            try:
                user_data = json.load(users)[str(user.id)]
            except KeyError:
                await interaction.send(f"There's no info about {user.name} yet. Registered {user.name}")
                await on_member_join(user)
                return None

        embed.add_field(name="Alt accounts", value="\n".join(user_data["alts"]))
        embed.add_field(name="Won tournaments", value=", ".join(user_data["won_tourneys"]))
        embed.add_field(name="Won games", value=user_data["won_games"])
        embed.add_field(name="Lost games", value=user_data["lost_games"])
        embed.add_field(name="Total games", value=user_data["won_games"] + user_data["lost_games"])

        if user_data["won_games"] + user_data["lost_games"] != 0:
            embed.add_field(name="Win rate",
                            value=f'{user_data["won_games"] / (user_data["won_games"] + user_data["lost_games"]) * 100:.2f}%')
        else:
            embed.add_field(name="Win rate", value="N/A")

        embed.set_image(user.avatar.url)

        await interaction.send(embed=embed)


def setup(bot: Bot):
    bot.add_cog(User(bot))
