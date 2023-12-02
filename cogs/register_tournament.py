from nextcord import slash_command, Interaction, SlashOption, Member
from nextcord.ext.commands import Cog, Bot
import json


class RegisterTournament(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    # Adds tournament to tournaments file
    @slash_command(name="register_tournament", description="Add tournament to the list", default_member_permissions=8)
    async def register_tournament(self, interaction: Interaction,
                                  name: str = SlashOption(name="name", description="Tournament name"),
                                  link: str = SlashOption(name="link", description="Link to tournament brackets"),
                                  date: str = SlashOption(name="date", description="Tournament hosting period"),
                                  players: int = SlashOption(name="player_count", description="Amount of players"),
                                  winner: Member = SlashOption(name="winner", description="Tournament winner"),
                                  image_link: str = SlashOption(name="image_link")
                                  ):
        if name.isascii() and link.isascii() and date.isascii() and str(players).isdigit():
            with open("tournaments.json", "r") as tourneys:
                tourney_list = json.load(tourneys)

            with open("users.json", "r") as users:
                users_data = json.load(users)

            tourney_list.append({
                "name": name,
                "link": link,
                "date": date,
                "players": players,
                "winner": winner.mention,
                "image_link": image_link
            })
            users_data[str(winner.id)]["won_tourneys"].append(name)

            with open("tournaments.json", "w") as tourneys:
                tourneys.write(json.dumps(tourney_list, indent=2))

            with open("users.json", "w") as users:
                users.write(json.dumps(users_data, indent=2))

            await interaction.send(f"Registered {name}")
        else:
            await interaction.send("You did the inputs wrong")


def setup(bot: Bot):
    bot.add_cog(RegisterTournament(bot))
