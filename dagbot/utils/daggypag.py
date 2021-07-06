from dagbot.utils.context import MyContext
from typing import List
import discord
from datetime import datetime

class PagViewButton(discord.ui.Button['DaggyPaginator']):

	def __init__(self, label: str, num: int):
	    super().__init__(style=discord.ButtonStyle.blurple, label=label)
	    self.num = num

	async def callback(self, interaction: discord.Interaction):
		assert self.view is not None
		await self.view.process_callback(self, interaction)





class DaggyPaginator(discord.ui.View):

	children: List[PagViewButton]

	def __init__(self, ctx: MyContext,embeds: List[discord.Embed]):
	    super().__init__(timeout=60.0)
	    self.ctx = ctx
	    self.embeds = embeds
	    for i, embed in enumerate(self.embeds):
	    	embed.set_footer(text=f"{i + 1}/{len(self.embeds)}")
	    	embed.timestamp = datetime.utcnow()
	    for i in range(1, len(embeds) + 1):
	    	self.add_item(PagViewButton(str(i), i-1))

	async def on_timeout(self) -> None:
	    return await super().on_timeout()

	async def interaction_check(self, interaction: discord.Interaction) -> bool:
	    assert interaction.user is not None
	    return interaction.user.id == self.ctx.author.id

	async def process_callback(self, button: PagViewButton, interaction: discord.Interaction):
		embed_to_use = self.embeds[button.num]
		await interaction.response.edit_message(embed=embed_to_use)
