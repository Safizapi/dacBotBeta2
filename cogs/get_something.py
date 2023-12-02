from nextcord.ext.commands import Cog, Bot
from nextcord import slash_command, Interaction
import cooldowns
import random


class GetSomething(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    # ???
    @slash_command(name="get_something", description="???")
    @cooldowns.cooldown(1, 900, bucket=cooldowns.SlashBucket.author)
    async def get_something(self, interaction: Interaction):
        if random.randint(1, 100) == 67:
            role = self.bot.get_guild(1164872244078579712).get_role(1178772828967940298)
            await interaction.user.add_roles(role)
            await interaction.send(f"You got {role.mention}")
        else:
            await interaction.send("You got nothing")


def setup(bot: Bot):
    bot.add_cog(GetSomething(bot))
