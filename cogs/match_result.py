from nextcord import slash_command, Interaction, SlashOption, Embed, Member
from nextcord.ext.commands import Cog, Bot
from additional import on_member_join
import json


class MatchResult(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    # Logs the results in member profiles
    @slash_command(name="match_result", description="Result of tournament match", default_member_permissions=8)
    async def match_result(self, interaction: Interaction,
                           winner: Member = SlashOption(name="winner"),
                           winner_score: int = SlashOption("winner_score"),
                           loser: Member = SlashOption(name="loser"),
                           loser_score: int = SlashOption(name="loser_score"),
                           final_match: bool = SlashOption(name="final_match")):
        channel = self.bot.get_guild(1164872244078579712).get_channel(1168993435164889269)
        embed = Embed(color=0xc93c3e)
        embed.title = "Match results"

        embed.add_field(name=winner.name, value=winner_score)
        embed.add_field(name=loser.name, value=loser_score)
        embed.description = f"{winner.mention} has won the match"
        embed.set_image(winner.avatar.url)

        with open("users.json", "r") as users:
            users_data = json.load(users)

        if not str(winner.id) in users_data.keys():
            await on_member_join(winner)
        if not str(loser.id) in users_data.keys():
            await on_member_join(loser)

        users_data[str(winner.id)]["won_games"] += winner_score
        users_data[str(winner.id)]["lost_games"] += loser_score
        users_data[str(loser.id)]["won_games"] += loser_score
        users_data[str(loser.id)]["lost_games"] += winner_score

        if final_match:
            embed.description = f"{winner.mention} has won the tournament :trophy:"

            guild = self.bot.get_guild(1164872244078579712)
            role = guild.get_role(1178399001771516015)
            await guild.get_member(winner.id).add_roles(role)

        with open("users.json", "w") as users:
            users.write(json.dumps(users_data, indent=2))

        await interaction.send(f"Sent embed in channel {channel.name}")
        await channel.send(embed=embed)


def setup(bot: Bot):
    bot.add_cog(MatchResult(bot))
