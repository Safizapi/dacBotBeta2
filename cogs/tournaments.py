from nextcord import slash_command, Interaction, Embed
from nextcord.ext.commands import Cog, Bot
import json


class Tournaments(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    # Displays all tournaments in embeds
    @slash_command(name="tournaments", description="See information about tournament")
    async def tournaments(self, interaction: Interaction):
        with open("tournaments.json", "r") as tourneys:
            tourney_list = json.load(tourneys)

        if len(tourney_list) == 0:
            await interaction.send("There are no tournaments yet")
        else:
            embeds = list()
            for tourney in tourney_list:
                embed = Embed(color=0xc93c3e)
                embed.title = tourney["name"]

                embed.add_field(name="Link", value=tourney["link"])
                embed.add_field(name="Hosting period", value=tourney["date"])
                embed.add_field(name="Amount of players", value=tourney["players"])
                embed.add_field(name="Winner", value=tourney["winner"])
                embed.set_image(tourney["image_link"])

                embeds.append(embed)

            await interaction.send(embeds=embeds)


def setup(bot: Bot):
    bot.add_cog(Tournaments(bot))
