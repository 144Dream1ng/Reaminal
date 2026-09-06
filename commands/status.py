# commands/ping.py
import nextcord
import os
import psutil
from nextcord.ext import commands
from utils.localizer import get, gwl


class StatusCog(commands.Cog):
    """리미널의 상태를 확인하는 명령어"""
    def __init__(self, reaminal: commands.Bot):
        self.reaminal = reaminal
    
    def status_color(self, latency: int) -> nextcord.Color:
        max_latency = 500
        ratio = min(latency / max_latency, 1.0)
        
        if ratio < 0.5: r, g = int(255 * ratio * 2), 255
        else: r, g = 255, int(255 * (1 - (ratio - 0.5) * 2)) 
        
        return nextcord.Color.from_rgb(r, g, 25)
    
    @nextcord.slash_command(
        name=get("status_name1")["en-US"],
        name_localizations=get("status_name1"),
    )
    async def status_first(self, interaction: nextcord.Interaction): pass
    
    @status_first.subcommand(
        name=get("status_name2")["en-US"],
        description=get("status_desc")["en-US"],
        name_localizations=get("status_name2"),
        description_localizations=get("status_desc")
    )
    async def status(self, interaction: nextcord.Interaction):
        if not self.reaminal.user: return
        
        locale = interaction.locale
        latency = round(self.reaminal.latency * 1000)
        process = psutil.Process(os.getpid())
        memory_usage = process.memory_info().rss / (1024 ** 2)
        
        embed = nextcord.Embed(
            title=gwl('status_emb_title', locale),
            color=self.status_color(latency)
        )
        embed.add_field(
            name=gwl('status_emb_lat_title', locale), 
            value=gwl('status_emb_lat', locale).format(latency=latency), 
            inline=False
        )
        embed.add_field(
            name=gwl('status_emb_mem_title', locale), 
            value=gwl('status_emb_mem', locale).format(memory=memory_usage), 
            inline=False
        )
        embed.set_thumbnail(url=self.reaminal.user.display_avatar.url)
        await interaction.response.send_message(embed=embed)

def setup(reaminal: commands.Bot):
    reaminal.add_cog(StatusCog(reaminal))