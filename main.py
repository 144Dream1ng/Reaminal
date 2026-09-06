# main.py
import os
import nextcord
import itertools
import yaml
from nextcord.ext import commands, tasks
from rich.console import Console
from rich.panel import Panel
from rich.rule import Rule
from pathlib import Path
from dotenv import load_dotenv


class Reaminal(commands.AutoShardedBot):
    def __init__(self, *args, **kwargs):
        """리미널의 초기화 메서드."""
        super().__init__(*args, **kwargs)
        self.console = Console()
        self.status_cycle = None
    
    async def load_exts(self):
        """리미널 실행 시 모든 명령어를 로드함."""
        def load_extension_with_logging(extension_name: str):
            try:
                self.load_extension(extension_name)
                self.console.print(f"[INFO] Loaded extension: [bold blue]{extension_name}[/bold blue]")
            except Exception as e:
                self.console.print(f"[EROR] Failed to load extension: [bold red]{extension_name}[/bold red] - [bold red]{e}[/bold red]", style="bold red")
        
        self.console.print(Rule(title="[INFO] Loading Cogs", style="bold blue", characters="="))
        commands_dir = Path("./commands")
        
        for file in commands_dir.rglob("*.py"):
            if file.name == "__init__.py": continue
            
            relative_path = file.relative_to(commands_dir.parent)
            module_path = ".".join(relative_path.with_suffix("").parts)
            
            load_extension_with_logging(module_path)
        else:
            await self.sync_application_commands()
            self.console.print(Rule(title=f"[INFO] All Cogs Loaded (Cogs: [bold purple]{len(self.extensions)}[/bold purple])", style="bold blue", characters="="))
            print()
    
    @tasks.loop(seconds=10)
    async def change_status(self):
        """10초마다 상태 메시지를 변경함."""
        try:
            with open('./data/status.txt', 'r', encoding='utf-8') as f:
                status_list = f.read().splitlines()
            
            if self.status_cycle is None:
                self.status_cycle = itertools.cycle(status_list)
            
            status_msg = next(self.status_cycle).format(guild_count=len(self.guilds))
            
            await self.change_presence(
                activity=nextcord.CustomActivity(status_msg),
                status=nextcord.Status.idle
            )
        except Exception as e:
            self.console.print(f"[EROR] Failed to change status: [bold red]{e}[/bold red]", style="bold red")
    
    async def on_ready(self):
        """리미널이 준비되었을 때 호출됨."""
        if not self.user:
            raise Exception("'self.user' is not defined.")
        
        owner = await self.fetch_user(int(str(os.environ.get("OWNER"))))
        
        self.console.print(Rule(title="[INFO] Reaminal is now online!", style="bold blue", characters="="))
        
        self.console.print(Panel(
            f"""\
            Logged in as: [bold blue]{self.user.name}#{self.user.discriminator}[/bold blue] [blue]({self.user.id})[/blue]
            Owner:        [bold blue]{owner.name}[/bold blue] [blue]({owner.id})[/blue]""",
            title = "[INFO] Reaminal Information",
            title_align = "left",
            border_style = "bold blue",
        ))
        print()
        
        self.console.print(Panel(
            f"""\
            Guilds: [bold blue]{len(self.guilds)}[/bold blue]
            {"\n".join([f"  [bold blue]{guild.name}[/bold blue] [blue]({guild.id})[/blue]" for guild in self.guilds[:10]])}""",
            title = "[INFO] Guilds Information",
            title_align = "left",
            border_style = "bold blue",
        ))
        print()
        
        if not self.extensions:
            await self.load_exts()
        
        if not self.change_status.is_running():
            self.change_status.start()

if __name__ == "__main__":
    load_dotenv()
    
    intents = nextcord.Intents.default()
    intents.members = True
    intents.message_content = True
    reaminal = Reaminal(command_prefix=' ', intents=intents, status=nextcord.Status.dnd)
    
    with open('config.yml', 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    
    if config['settings']['debug']:
        reaminal.console.print("[INFO] Debug mode is enabled.", style="bold yellow")
        print()
        token = os.environ.get("DEBUG_TOKEN")
    else:
        token = os.environ.get("TOKEN")
    
    if not token: raise ValueError("[EROR] TOKEN environment variable is not set.")
    
    reaminal.run(token)