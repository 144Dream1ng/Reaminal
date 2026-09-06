# commands/large.py
import nextcord
import re
import io
import aiohttp
from PIL import Image, ImageSequence
from utils import localizer
from nextcord.ext import commands


class LargeCog(commands.Cog):
    """메시지의 이모지를 확대하는 명령어"""
    def __init__(self, reaminal: commands.Bot):
        self.reaminal = reaminal
        self.EMOJI_PATTERN = re.compile(
            r"<(?P<animated>a?):(?P<name>\w+):(?P<id>\d+)>"
        )
        self.UPSCALE_SIZE = 256
        self.RESAMPLE_METHOD = Image.Resampling.BICUBIC
    
    @nextcord.message_command(
        name=localizer.default("large_name"),
        name_localizations=localizer.all("large_name"),
        integration_types=[
            nextcord.IntegrationType.guild_install,
            nextcord.IntegrationType.user_install,
        ],
        contexts=[
            nextcord.InteractionContextType.guild,
            nextcord.InteractionContextType.bot_dm,
            nextcord.InteractionContextType.private_channel,
        ],
        force_global=True,
    )
    async def large(
            self,
            interaction: nextcord.Interaction,
            message: nextcord.Message
        ):
        if not self.reaminal.user:
            return
        
        emojis = list(self.EMOJI_PATTERN.finditer(message.content))
        
        if not emojis:
            await interaction.response.send_message(
                localizer.get("large_no_emoji", interaction.locale),
                ephemeral=True
            )
            return
        
        if len(emojis) != 1:
            await interaction.response.send_message(
                localizer.get("large_multiple_emojis", interaction.locale),
                ephemeral=True
            )
            return
        
        if not self.EMOJI_PATTERN.fullmatch(message.content.strip()):
            await interaction.response.send_message(
                localizer.get("large_only_emoji", interaction.locale),
                ephemeral=True
            )
            return
        
        emoji = emojis[0]
        
        animated = emoji.group("animated") == "a"
        name = emoji.group("name")
        emoji_id = emoji.group("id")
        
        extension = "gif" if animated else "png"
        emoji_url = f"https://cdn.discordapp.com/emojis/{emoji_id}.{extension}"
        
        async with aiohttp.ClientSession() as session:
            async with session.get(emoji_url) as response:
                if response.status != 200:
                    await interaction.response.send_message(
                        localizer.get("large_failed", interaction.locale),
                        ephemeral=True
                    )
                    return
                data = await response.read()
        
        if animated:
            buffer = self.upscale_gif(data)
            filename = f"{name}.gif"
        else:
            buffer = self.upscale_png(data)
            filename = f"{name}.png"
        
        file = nextcord.File(buffer, filename=filename)
        
        embed = nextcord.Embed()
        embed.set_image(url=f"attachment://{filename}")
        
        await interaction.response.send_message(
            file=file,
            embed=embed
        )
    
    def upscale_png(self, data: bytes) -> io.BytesIO:
        image = Image.open(io.BytesIO(data)).convert("RGBA")
        
        image = image.resize(
            (self.UPSCALE_SIZE, self.UPSCALE_SIZE),
            self.RESAMPLE_METHOD
        )
        
        buffer = io.BytesIO()
        image.save(buffer, format="PNG")
        buffer.seek(0)
        
        return buffer
    
    def upscale_gif(self, data: bytes) -> io.BytesIO:
        source = Image.open(io.BytesIO(data))
        
        frames = []
        durations = []
        
        for frame in ImageSequence.Iterator(source):
            new_frame = frame.convert("RGBA").resize(
                (self.UPSCALE_SIZE, self.UPSCALE_SIZE),
                self.RESAMPLE_METHOD
            )
            frames.append(new_frame)
            durations.append(frame.info.get("duration", 80))
        
        buffer = io.BytesIO()
        frames[0].save(
            buffer,
            format="GIF",
            save_all=True,
            append_images=frames[1:],
            duration=durations,
            loop=source.info.get("loop", 0),
            disposal=2
        )
        buffer.seek(0)
        
        return buffer


def setup(reaminal: commands.Bot):
    reaminal.add_cog(LargeCog(reaminal))