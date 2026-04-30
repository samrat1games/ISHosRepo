import random
import datetime
import os
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Static, Digits, Input
from textual.containers import Grid, Vertical, Container

LOGO = """
 [bold cyan]
  _    _ 
 | |  | |
 | |__| |
 |  __  |
 | |  | |
 |_|  |_|
 [/bold cyan]
"""

class HackerOS(App):
    CSS = """
    Grid {
        grid-size: 2 2;
        grid-columns: 1fr 2fr;
        grid-rows: 1fr 1fr;
        padding: 1;
        grid-gutter: 1;
    }
    .box {
        border: double green;
        background: black;
        padding: 1;
        color: lime;
    }
    #logo-box { border: double cyan; color: cyan; content-align: center middle; }
    #time-box { border: double magenta; color: white; content-align: center middle; }
    #terminal-box { border: double yellow; }
    
    #term-output {
        height: 70%;
        color: #00FF00;
        margin-bottom: 1;
    }

    Input {
        background: #001a00;
        border: tall #004400;
        color: #00FF00;
        width: 100%;
    }
    Input:focus {
        border: tall lime;
    }
    """

    log_lines = ["[bold]CORE SYSTEM READY[/]"]

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        with Grid():
            yield Static(LOGO, classes="box", id="logo-box")
            yield Vertical(
                Static(self.log_lines[0], id="logs"),
                classes="box"
            )
            # Секция терминала
            with Vertical(classes="box", id="terminal-box"):
                yield Static("DATABASE TERMINAL v2.0\n[grey37]Commands: find [name], list, clear[/]", id="term-output")
                yield Input(placeholder="enter command...", id="term-input")
                
            yield Vertical(
                Digits("00:00:00", id="clock"),
                classes="box", id="time-box"
            )
        yield Footer()

    def on_mount(self) -> None:
        self.set_interval(1, self.update_time)
        self.set_interval(0.15, self.update_logs)

    def update_time(self) -> None:
        now = datetime.datetime.now().strftime("%H:%M:%S")
        try: self.query_one("#clock", Digits).update(now)
        except: pass

    def update_logs(self) -> None:
        prefix = random.choice(["SEC", "NET", "SRV", "DB"])
        addr = hex(random.randint(0x1000, 0xFFFF))
        self.log_lines.append(f"[{prefix}] {addr} -> [green]OK[/]")
        if len(self.log_lines) > 13: self.log_lines.pop(0)
        try: self.query_one("#logs", Static).update("\n".join(self.log_lines))
        except: pass

    async def on_input_submitted(self, event: Input.Submitted) -> None:
        raw_cmd = event.value.strip()
        cmd = raw_cmd.lower()
        output = self.query_one("#term-output", Static)
        
        if cmd.startswith("find "):
            target = raw_cmd[5:].strip()
            result = self.db_query(target)
            output.update(f"[bold yellow]SEARCHING DATABASE FOR:[/] {target}...\n\n{result}")
        
        elif cmd == "list":
            people = self.get_all_people()
            output.update(f"[bold cyan]TOTAL RECORDS FOUND:[/]\n{people}")
            
        elif cmd == "clear":
            output.update("TERMINAL READY")
            
        else:
            output.update(f"[red]ERROR:[/] Command '{cmd}' not recognized.")
        
        self.query_one("#term-input", Input).value = ""

    def db_query(self, name):
        if not os.path.exists("person.txt"):
            return "[red]CRITICAL ERROR: DATABASE FILE MISSING[/]"
        
        found = []
        with open("person.txt", "r", encoding="utf-8") as f:
            for line in f:
                if name.lower() in line.lower():
                    found.append(f"[bold green]▶[/] {line.strip()}")
        
        return "\n".join(found) if found else "[red]NO RESULTS IN DATABASE[/]"

    def get_all_people(self):
        if not os.path.exists("person.txt"): return "Empty"
        with open("person.txt", "r", encoding="utf-8") as f:
            lines = [f"[cyan]•[/] {line.split(':')[0].strip()}" for line in f if ":" in line]
        return "\n".join(lines) if lines else "No formatted data found."

if __name__ == "__main__":
    app = HackerOS()
    app.run()
