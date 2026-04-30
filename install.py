from textual.app import App, ComposeResult
from textual.widgets import Static, ProgressBar, Log, Input
from textual.containers import Vertical, Center
from textual.screen import Screen
import asyncio
import os
import httpx
import sys
import subprocess

class WelcomeScreen(Screen):
    async def on_mount(self) -> None:
        for msg in ["Hello", "Privet", "Nihao", "Hi", "Zdorova"]:
            self.query_one("#welcome_text").update(f"[bold green]{msg}[/]")
            await asyncio.sleep(0.6)
        self.app.push_screen(WifiScreen())

    def compose(self) -> ComposeResult:
        yield Center(Static("", id="welcome_text"))

class WifiScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Center(Vertical(
            Static(">> SELECT WIFI NETWORK", classes="label"),
            Input(placeholder="SSID...", id="wifi_name"),
            Input(placeholder="Password...", password=True),
            Static("Press ENTER to connect", classes="hint"),
            id="dialog"
        ))
    def on_input_submitted(self) -> None:
        self.app.push_screen(UserScreen())

class UserScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Center(Vertical(
            Static(">> CREATE NEW OPERATOR", classes="label"),
            Input(placeholder="Enter Username...", id="username"),
            Static("Press ENTER to confirm", classes="hint"),
            id="dialog"
        ))
    def on_input_submitted(self, event: Input.Submitted) -> None:
        self.app.user_name = event.value if event.value else "Operator"
        self.app.push_screen(InstallScreen())

class InstallScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Center(Vertical(
            Static(">> ISHOS CORE DEPLOYMENT <<", id="title"),
            ProgressBar(total=100, show_percentage=True, id="pbar"),
            Log(id="install_log"),
            id="main_container"
        ))

    async def on_mount(self) -> None:
        log = self.query_one("#install_log")
        pbar = self.query_one("#pbar")
        path = "system"
        
        if not os.path.exists(path): os.makedirs(path)
        log.write_line("[+] System folder ready.")
        
        # Список файлов для загрузки
        base_url = "https://raw.githubusercontent.com/samrat1games/ISHosRepo/main"
        files_to_get = ["main.py", "person.txt", "boot.py"] 

        async with httpx.AsyncClient() as client:
            for file in files_to_get:
                log.write_line(f"[*] Downloading {file}...")
                try:
                    response = await client.get(f"{base_url}/{file}")
                    content = response.text if response.status_code == 200 else f"print('ISHos Booting...')\nprint('User: {self.app.user_name}')"
                    
                    with open(os.path.join(path, file), "w", encoding="utf-8") as f:
                        f.write(content)
                    log.write_line(f"[OK] {file} saved.")
                except:
                    log.write_line(f"[!] {file} fallback created.")
                pbar.advance(33)

        log.write_line("\n[DONE] Press 'Q' to REBOOT into ISHos.")

class ISHosInstaller(App):
    user_name = "Admin"
    CSS = """
    Screen { background: #000000; color: #00FF00; }
    #dialog { width: 45; border: double #00FF00; padding: 1; }
    #main_container { width: 75; height: 25; border: heavy #00FF00; padding: 1; }
    .label { margin-bottom: 1; text-style: bold; }
    .hint { color: #004400; text-align: right; }
    Input { background: #001100; border: tall #004400; color: #00FF00; margin-bottom: 1; }
    Log { height: 12; background: #000500; border: solid #003300; }
    ProgressBar { width: 100%; }
    ProgressBar > .bar--complete { color: #00FF00; }
    """
    def on_mount(self) -> None:
        self.push_screen(WelcomeScreen())

    def action_quit(self) -> None:
        # Автоматический запуск boot.py после выхода
        boot_path = os.path.join("system", "boot.py")
        if os.path.exists(boot_path):
            subprocess.Popen([sys.executable, boot_path], creationflags=subprocess.CREATE_NEW_CONSOLE)
        self.exit()

    BINDINGS = [("q", "quit", "Quit & Boot")]

if __name__ == "__main__":
    ISHosInstaller().run()