#!/usr/bin/env python3

import json
import os
import sys
import subprocess
import platform
import time
import random
import shutil
import threading
import queue
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
import hashlib

from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeRemainingColumn
from rich.prompt import Prompt, Confirm
from rich.syntax import Syntax
from rich.text import Text
from rich.align import Align
from rich.traceback import install
from rich.status import Status

from prompt_toolkit import prompt

import pyfiglet
from colorama import init, Fore, Back, Style
import curses
import itertools

install(show_locals=True)
init(autoreset=True)

console = Console()

class MatrixRain:
    def __init__(self, speed=0.05):
        self.speed = speed
        self.chars = "01"
        self.running = False
        
    def run(self, duration=3):
        self.running = True
        columns = shutil.get_terminal_size().columns
        lines = shutil.get_terminal_size().lines
        
        end_time = time.time() + duration
        while time.time() < end_time and self.running:
            os.system('clear' if os.name == 'posix' else 'cls')
            for _ in range(lines):
                line = ''.join(random.choice(self.chars) for _ in range(columns))
                print(Fore.GREEN + line)
            time.sleep(self.speed)
        
        self.running = False
        os.system('clear' if os.name == 'posix' else 'cls')


class TypeWriter:
    @staticmethod
    def print(text: str, delay: float = 0.03, color: str = Fore.GREEN):
        for char in text:
            print(color + char, end='', flush=True)
            time.sleep(delay)
        print()
    
    @staticmethod
    def animate_banner(text: str, delay: float = 0.01):
        lines = text.split('\n')
        for line in lines:
            for char in line:
                if char in ['█', '╔', '╗', '╚', '╝', '═', '║']:
                    print(Fore.RED + char, end='', flush=True)
                elif char in ['V', 'E', 'N', 'O', 'M', 'X']:
                    print(Fore.YELLOW + char, end='', flush=True)
                else:
                    print(Fore.WHITE + char, end='', flush=True)
                time.sleep(delay)
            print()
            time.sleep(delay * 2)


class Spinner:
    SPINNERS = {
        'dots': ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏'],
        'snake': ['=', '=', '=', '=', '=', '='],
        'matrix': ['0', '1', '0', '1', '0', '1', '0', '1'],
        'arrow': ['->', '-->', '--->', '---->', '----->', '---->', '--->', '-->', '->'],
    }
    
    @staticmethod
    def run(message: str, duration: float = 2, style: str = 'snake'):
        spinner_chars = Spinner.SPINNERS.get(style, Spinner.SPINNERS['dots'])
        end_time = time.time() + duration
        i = 0
        
        while time.time() < end_time:
            print(f'\r{Fore.YELLOW}{spinner_chars[i % len(spinner_chars)]}{Style.RESET_ALL} {message}', end='', flush=True)
            time.sleep(0.1)
            i += 1
        print('\r' + ' ' * (len(message) + 10) + '\r', end='')


class GlitchEffect:
    @staticmethod
    def glitch(text: str, intensity: int = 3):
        chars = "!@#$%^&*()_+{}|:<>?~"
        result = []
        
        for char in text:
            if random.random() < 0.1:
                result.append(random.choice(chars))
            else:
                result.append(char)
        
        return ''.join(result)


@dataclass
class Tool:
    name: str
    full_name: str
    url: str
    clone_url: str
    description: str
    stars: int
    language: str
    category: str
    installed: bool = False
    install_command: str = ""
    
    def __post_init__(self):
        if 'github.com' in self.clone_url:
            self.install_command = f"git clone {self.clone_url}"
        elif 'pypi' in self.url or 'python' in self.language.lower():
            self.install_command = f"pip3 install {self.name}"
        elif self.language.lower() == 'go':
            self.install_command = f"go install {self.clone_url}@latest"
        elif self.language.lower() == 'ruby':
            self.install_command = f"gem install {self.name}"
        elif self.language.lower() == 'npm' or 'javascript' in self.language.lower():
            self.install_command = f"npm install -g {self.name}"
        else:
            self.install_command = f"git clone {self.clone_url} && cd {self.name} && make install"


@dataclass
class Category:
    id: str
    name: str
    color: str
    tools: List[Tool] = field(default_factory=list)
    
    @property
    def count(self) -> int:
        return len(self.tools)
    
    @property
    def installed_count(self) -> int:
        return sum(1 for t in self.tools if t.installed)


class VenomTheme:
    THEMES = {
        'venom': {
            'primary': Fore.RED,
            'secondary': Fore.YELLOW,
            'accent': Fore.GREEN,
            'danger': Fore.MAGENTA,
            'info': Fore.CYAN,
            'success': Fore.LIGHTGREEN_EX,
            'warning': Fore.LIGHTYELLOW_EX,
            'error': Fore.LIGHTRED_EX,
            'border': '-',
        },
        'matrix': {
            'primary': Fore.GREEN,
            'secondary': Fore.LIGHTGREEN_EX,
            'accent': Fore.LIGHTWHITE_EX,
            'danger': Fore.RED,
            'info': Fore.CYAN,
            'success': Fore.LIGHTGREEN_EX,
            'warning': Fore.YELLOW,
            'error': Fore.RED,
            'border': '=',
        },
        'dark': {
            'primary': Fore.WHITE,
            'secondary': Fore.LIGHTBLACK_EX,
            'accent': Fore.CYAN,
            'danger': Fore.RED,
            'info': Fore.BLUE,
            'success': Fore.GREEN,
            'warning': Fore.YELLOW,
            'error': Fore.RED,
            'border': '*',
        },
    }
    
    def __init__(self, theme: str = 'venom'):
        self.current = self.THEMES.get(theme, self.THEMES['venom'])
        self.name = theme
    
    def color(self, key: str) -> str:
        return self.current.get(key, Fore.WHITE)
    
    def styled(self, text: str, style: str) -> str:
        return f"{self.color(style)}{text}{Style.RESET_ALL}"


class VenomX:
    def __init__(self):
        self.tools: List[Tool] = []
        self.categories: Dict[str, Category] = {}
        self.config = self.load_config()
        self.theme = VenomTheme(self.config.get('theme', 'venom'))
        self.selected_tools: List[Tool] = []
        self.install_queue: queue.Queue = queue.Queue()
        
    def load_config(self) -> dict:
        config_file = Path.home() / '.venomx' / 'config.json'
        
        default_config = {
            'theme': 'venom',
            'install_path': str(Path.home() / 'venomx-tools'),
            'auto_update': True,
            'animations': True,
            'sound_effects': False,
            'last_updated': time.time()
        }
        
        if config_file.exists():
            with open(config_file, 'r') as f:
                return json.load(f)
        else:
            config_file.parent.mkdir(parents=True, exist_ok=True)
            with open(config_file, 'w') as f:
                json.dump(default_config, f, indent=4)
            return default_config
    
    def save_config(self):
        config_file = Path.home() / '.venomx' / 'config.json'
        with open(config_file, 'w') as f:
            json.dump(self.config, f, indent=4)
    
    def load_tools(self, json_path: str = 'hacking_tools_ultimate.json'):
        console.print(f"{Fore.YELLOW}Loading tools from {json_path}...{Style.RESET_ALL}")
        
        try:
            Spinner.run("Loading database...", 1.5, 'matrix')
            if not Path(json_path).is_absolute():
                script_dir = Path(__file__).parent
                json_path = str(script_dir / json_path)
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            category_tools: Dict[str, List[Tool]] = {}
            
            for tool_data in data.get('tools', []):
                tool = Tool(
                    name=tool_data.get('name', 'Unknown'),
                    full_name=tool_data.get('full_name', ''),
                    url=tool_data.get('url', ''),
                    clone_url=tool_data.get('clone_url', ''),
                    description=tool_data.get('description', 'No description'),
                    stars=tool_data.get('stars', 0),
                    language=tool_data.get('language', 'Unknown'),
                    category=tool_data.get('category', 'uncategorized')
                )
                self.tools.append(tool)
                
                cat = tool.category
                if cat not in category_tools:
                    category_tools[cat] = []
                category_tools[cat].append(tool)
            
            category_meta = {
                'hacking-tool': 'Hacking Tools',
                'penetration-testing': 'Penetration Testing',
                'cybersecurity': 'Cybersecurity',
                'reconnaissance': 'Reconnaissance',
                'osint-tool': 'OSINT Tools',
                'password-cracker': 'Password Cracking',
                'vulnerability-scanner': 'Vulnerability Scanners',
                'exploit-database': 'Exploit Database',
                'default': 'Security Tools'
            }
            
            for cat_id, tools in category_tools.items():
                meta_name = category_meta.get(cat_id, category_meta['default'])
                self.categories[cat_id] = Category(
                    id=cat_id,
                    name=meta_name,
                    color='red',
                    tools=tools
                )
            
            console.print(f"{Fore.GREEN}Loaded {len(self.tools)} tools across {len(self.categories)} categories{Style.RESET_ALL}")

        except FileNotFoundError:
            console.print(f"{Fore.RED}Error: {json_path} not found!{Style.RESET_ALL}")
            sys.exit(1)
        except json.JSONDecodeError:
            console.print(f"{Fore.RED}Error: Invalid JSON in {json_path}!{Style.RESET_ALL}")
            sys.exit(1)
    
    def check_installed_tools(self):
        install_path = Path(self.config['install_path'])
        
        if not install_path.exists():
            install_path.mkdir(parents=True)
            return
        
        console.print(f"{Fore.CYAN}Checking installed tools...{Style.RESET_ALL}")
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        ) as progress:
            task = progress.add_task("[cyan]Scanning...", total=len(self.tools))
            
            for tool in self.tools:
                tool_path = install_path / tool.name
                if tool_path.exists() or self._check_system_tool(tool.name):
                    tool.installed = True
                progress.update(task, advance=1)
        
        installed_count = sum(1 for t in self.tools if t.installed)
        console.print(f"{Fore.GREEN}Found {installed_count} installed tools{Style.RESET_ALL}")
    
    def _check_system_tool(self, tool_name: str) -> bool:
        return shutil.which(tool_name.lower()) is not None
    
    def display_banner(self):
        os.system('clear' if os.name == 'posix' else 'cls')
        
        venom_banner = """
██╗   ██╗███████╗███╗   ██╗ ██████╗ ███╗   ███╗     ██╗  ██╗
██║   ██║██╔════╝████╗  ██║██╔═══██╗████╗ ████║     ╚██╗██╔╝
██║   ██║█████╗  ██╔██╗ ██║██║   ██║██╔████╔██║█████╗╚███╔╝ 
╚██╗ ██╔╝██╔══╝  ██║╚██╗██║██║   ██║██║╚██╔╝██║╚════╝██╔██╗ 
 ╚████╔╝ ███████╗██║ ╚████║╚██████╔╝██║ ╚═╝ ██║     ██╔╝ ██╗
  ╚═══╝  ╚══════╝╚═╝  ╚═══╝ ╚═════╝ ╚═╝     ╚═╝     ╚═╝  ╚═╝
"""
        console.print(venom_banner)
    
    def display_main_menu(self):
        while True:
            os.system('clear' if os.name == 'posix' else 'cls')
            self.display_banner()
            
            console.print(f"{Fore.CYAN}========== VENOM-X STATISTICS =========={Style.RESET_ALL}")
            console.print(f"Total Tools     : {len(self.tools):,}")
            console.print(f"Categories      : {len(self.categories)}")
            console.print(f"Installed       : {sum(1 for t in self.tools if t.installed):,}")
            console.print(f"Pending         : {sum(1 for t in self.tools if not t.installed):,}")
            console.print(f"Selected        : {len(self.selected_tools)}")
            console.print(f"{Fore.CYAN}========================================{Style.RESET_ALL}\n")
            
            console.print(f"{Fore.YELLOW}Menu Options:{Style.RESET_ALL}")
            console.print("1. Install Tools")
            console.print("2. Browse Categories")
            console.print("3. Search Tools")
            console.print("4. View Selections")
            console.print("5. Change Theme")
            console.print("6. Settings")
            console.print("7. About")
            console.print("8. Exit")
            console.print()
            
            choice = Prompt.ask(
                f"{self.theme.color('accent')}[VENOM-X] Select option",
                choices=["1", "2", "3", "4", "5", "6", "7", "8"],
                default="1"
            )
            
            if choice == "1":
                self.install_workflow()
            elif choice == "2":
                self.browse_categories()
            elif choice == "3":
                self.search_tools()
            elif choice == "4":
                self.view_selections()
            elif choice == "5":
                self.change_theme()
            elif choice == "6":
                self.settings_menu()
            elif choice == "7":
                self.about()
            elif choice == "8":
                if Confirm.ask("Exit VENOM-X?", default=True):
                    self.exit_animation()
                    break
    
    def browse_categories(self):
        while True:
            os.system('clear' if os.name == 'posix' else 'cls')
            
            console.print(f"{Fore.YELLOW}VENOM-X CATEGORIES{Style.RESET_ALL}\n")
            
            for idx, (cat_id, category) in enumerate(self.categories.items(), 1):
                installed = category.installed_count
                total = category.count
                console.print(f"{idx}. {category.name} ({installed}/{total})")
            
            console.print(f"\nPress 0 to go back, or enter category number to view tools\n")
            
            choice = Prompt.ask(
                f"{self.theme.color('accent')}[VENOM-X] Select category",
                default="0"
            )
            
            if choice == "0":
                break
            elif choice.isdigit() and 1 <= int(choice) <= len(self.categories):
                cat_list = list(self.categories.values())
                selected_cat = cat_list[int(choice) - 1]
                self.view_category_tools(selected_cat)
    
    def view_category_tools(self, category: Category):
        while True:
            os.system('clear' if os.name == 'posix' else 'cls')
            
            console.print(f"{Fore.YELLOW}{category.name} - {category.count} Tools{Style.RESET_ALL}\n")
            
            for idx, tool in enumerate(category.tools, 1):
                status = "Installed" if tool.installed else "Not Installed"
                status_color = Fore.GREEN if tool.installed else Fore.RED
                selected_mark = "[X]" if tool in self.selected_tools else "[ ]"
                
                console.print(f"{selected_mark} {idx}. {tool.name} ({tool.language}) - {status_color}{status}{Style.RESET_ALL}")
            
            console.print(f"\nCommands: [number] to toggle selection | 0 to go back | i to install selected\n")
            
            choice = Prompt.ask(
                f"{self.theme.color('accent')}[{category.name}]"
            )
            
            if choice == "0":
                break
            elif choice.lower() == "i":
                selected = [t for t in category.tools if t in self.selected_tools]
                if selected:
                    self.install_tools(selected)
                else:
                    console.print(f"{Fore.RED}No tools selected!{Style.RESET_ALL}")
                    time.sleep(1)
            elif choice.isdigit():
                idx = int(choice) - 1
                if 0 <= idx < len(category.tools):
                    tool = category.tools[idx]
                    if tool in self.selected_tools:
                        self.selected_tools.remove(tool)
                        console.print(f"{Fore.YELLOW}Removed {tool.name}{Style.RESET_ALL}")
                    else:
                        self.selected_tools.append(tool)
                        console.print(f"{Fore.GREEN}Added {tool.name}{Style.RESET_ALL}")
                    time.sleep(0.5)
    
    def search_tools(self):
        os.system('clear' if os.name == 'posix' else 'cls')
        
        search_term = Prompt.ask(
            f"{self.theme.color('accent')}Enter search term"
        ).lower()
        
        if not search_term:
            return
        
        results = []
        for tool in self.tools:
            if (search_term in tool.name.lower() or 
                search_term in tool.description.lower() or
                search_term in tool.language.lower()):
                results.append(tool)
        
        if not results:
            console.print(f"{Fore.RED}No tools found matching '{search_term}'{Style.RESET_ALL}")
            time.sleep(1)
            return
        
        while True:
            os.system('clear' if os.name == 'posix' else 'cls')
            
            console.print(f"{Fore.YELLOW}Search Results: '{search_term}' - {len(results)} tools{Style.RESET_ALL}\n")
            
            for idx, tool in enumerate(results, 1):
                status = "Installed" if tool.installed else "Not Installed"
                status_color = Fore.GREEN if tool.installed else Fore.RED
                selected_mark = "[X]" if tool in self.selected_tools else "[ ]"
                
                console.print(f"{selected_mark} {idx}. {tool.name} - {tool.category} ({tool.language}) - {status_color}{status}{Style.RESET_ALL}")
            
            console.print(f"\nCommands: [number] to toggle selection | 0 to go back | i to install selected\n")
            
            choice = Prompt.ask(
                f"{self.theme.color('accent')}[SEARCH]"
            )
            
            if choice == "0":
                break
            elif choice.lower() == "i":
                selected = [t for t in results if t in self.selected_tools]
                if selected:
                    self.install_tools(selected)
                else:
                    console.print(f"{Fore.RED}No tools selected!{Style.RESET_ALL}")
                    time.sleep(1)
            elif choice.isdigit():
                idx = int(choice) - 1
                if 0 <= idx < len(results):
                    tool = results[idx]
                    if tool in self.selected_tools:
                        self.selected_tools.remove(tool)
                        console.print(f"{Fore.YELLOW}Removed {tool.name}{Style.RESET_ALL}")
                    else:
                        self.selected_tools.append(tool)
                        console.print(f"{Fore.GREEN}Added {tool.name}{Style.RESET_ALL}")
                    time.sleep(0.5)
    
    def view_selections(self):
        os.system('clear' if os.name == 'posix' else 'cls')
        
        if not self.selected_tools:
            console.print(f"{Fore.RED}No tools selected!{Style.RESET_ALL}")
            time.sleep(1)
            return
        
        console.print(f"{Fore.CYAN}Selected Tools ({len(self.selected_tools)}){Style.RESET_ALL}\n")
        
        for idx, tool in enumerate(self.selected_tools, 1):
            console.print(f"{idx}. {tool.name} - {tool.category}")
            console.print(f"   Command: {tool.install_command[:60]}")
        
        console.print()
        
        if Confirm.ask(f"Install {len(self.selected_tools)} selected tools?", default=True):
            self.install_tools(self.selected_tools)
        elif Confirm.ask("Clear all selections?", default=False):
            self.selected_tools.clear()
            console.print(f"{Fore.GREEN}Selections cleared{Style.RESET_ALL}")
            time.sleep(1)
    
    def install_tools(self, tools: List[Tool]):
        os.system('clear' if os.name == 'posix' else 'cls')
        
        install_path = Path(self.config['install_path'])
        install_path.mkdir(parents=True, exist_ok=True)
        
        console.print(f"{Fore.YELLOW}========== INSTALLATION ENGINE =========={Style.RESET_ALL}")
        console.print(f"Preparing to install {len(tools)} tools...")
        console.print(f"Target Directory: {install_path}")
        console.print(f"{Fore.YELLOW}=========================================={Style.RESET_ALL}\n")
        
        time.sleep(1)
        
        success_count = 0
        fail_count = 0
        
        with Progress(
            SpinnerColumn(spinner_name="dots12"),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            TimeRemainingColumn(),
            console=console,
            transient=False,
        ) as progress:
            
            task = progress.add_task(f"{Fore.GREEN}Installing tools...{Style.RESET_ALL}", total=len(tools))
            
            for tool in tools:
                progress.update(task, description=f"{Fore.YELLOW}Installing {tool.name}...{Style.RESET_ALL}")
                
                try:
                    os.chdir(install_path)
                    
                    if 'git clone' in tool.install_command:
                        repo_name = tool.name.lower().replace(' ', '-')
                        if not (install_path / repo_name).exists():
                            result = subprocess.run(
                                tool.install_command.split(),
                                capture_output=True,
                                text=True
                            )
                            if result.returncode == 0:
                                success_count += 1
                                tool.installed = True
                            else:
                                fail_count += 1
                        else:
                            success_count += 1
                            tool.installed = True
                    
                    elif 'pip' in tool.install_command:
                        result = subprocess.run(
                            tool.install_command.split(),
                            capture_output=True,
                            text=True
                        )
                        if result.returncode == 0:
                            success_count += 1
                            tool.installed = True
                        else:
                            fail_count += 1
                    
                    elif 'gem' in tool.install_command:
                        result = subprocess.run(
                            tool.install_command.split(),
                            capture_output=True,
                            text=True
                        )
                        if result.returncode == 0:
                            success_count += 1
                            tool.installed = True
                        else:
                            fail_count += 1
                    
                    else:
                        result = subprocess.run(
                            tool.install_command,
                            shell=True,
                            capture_output=True,
                            text=True
                        )
                        if result.returncode == 0:
                            success_count += 1
                            tool.installed = True
                        else:
                            fail_count += 1
                    
                except Exception as e:
                    fail_count += 1
                    console.print(f"{Fore.RED}Failed to install {tool.name}: {str(e)}{Style.RESET_ALL}")
                
                progress.update(task, advance=1)
                time.sleep(0.1)
        
        os.system('clear' if os.name == 'posix' else 'cls')
        
        console.print(f"{Fore.CYAN}========= INSTALLATION COMPLETE ========={Style.RESET_ALL}")
        console.print(f"Successfully Installed: {success_count} tools")
        console.print(f"Failed: {fail_count} tools")
        console.print(f"Location: {install_path}")
        console.print(f"{Fore.CYAN}=========================================={Style.RESET_ALL}\n")
        
        self.selected_tools = [t for t in self.selected_tools if not t.installed]
        
        input(f"\n{self.theme.color('accent')}Press Enter to continue...")
    
    def change_theme(self):
        themes = list(VenomTheme.THEMES.keys())
        
        console.print(f"{Fore.CYAN}Available Themes:{Style.RESET_ALL}\n")
        
        for idx, theme in enumerate(themes, 1):
            console.print(f"{idx}. {theme.capitalize()}")
        
        choice = Prompt.ask(
            f"Select theme (1-{len(themes)})",
            default="1"
        )
        
        if choice.isdigit() and 1 <= int(choice) <= len(themes):
            selected_theme = themes[int(choice) - 1]
            self.config['theme'] = selected_theme
            self.theme = VenomTheme(selected_theme)
            self.save_config()
            console.print(f"{Fore.GREEN}Theme changed to {selected_theme.upper()}{Style.RESET_ALL}")
            time.sleep(1)
    
    def settings_menu(self):
        while True:
            os.system('clear' if os.name == 'posix' else 'cls')
            
            console.print(f"{Fore.CYAN}VENOM-X Settings{Style.RESET_ALL}\n")
            console.print("1. Theme")
            console.print("2. Install Path")
            console.print("3. Auto Update")
            console.print("4. Animations")
            console.print("0. Back")
            console.print()
            
            console.print(f"Theme: {self.config.get('theme', 'venom')}")
            console.print(f"Install Path: {self.config.get('install_path', '~/venomx-tools')}")
            console.print(f"Auto Update: {'Enabled' if self.config.get('auto_update') else 'Disabled'}")
            console.print(f"Animations: {'Enabled' if self.config.get('animations') else 'Disabled'}")
            console.print()
            
            choice = Prompt.ask(
                "Select option",
                choices=["1", "2", "3", "4", "0"],
                default="0"
            )
            
            if choice == "0":
                break
            elif choice == "2":
                new_path = Prompt.ask("Enter new install path", default=self.config['install_path'])
                self.config['install_path'] = new_path
                self.save_config()
                console.print(f"{Fore.GREEN}Install path updated to {new_path}{Style.RESET_ALL}")
                time.sleep(1)
            elif choice == "3":
                self.config['auto_update'] = not self.config.get('auto_update', True)
                self.save_config()
                console.print(f"{Fore.GREEN}Auto update set to {self.config['auto_update']}{Style.RESET_ALL}")
                time.sleep(1)
            elif choice == "4":
                self.config['animations'] = not self.config.get('animations', True)
                self.save_config()
                console.print(f"{Fore.GREEN}Animations set to {self.config['animations']}{Style.RESET_ALL}")
                time.sleep(1)
    
    def about(self):
        os.system('clear' if os.name == 'posix' else 'cls')
        
        about_text = """
========================================================
                 VENOM-X 
           The Ultimate Hacking Toolkit
========================================================

Created & Developed by: ATHEX BLACK HAT
Version: 1.0.0 (Black Hat Edition)
Release Date: May 2026
Tools Database: 5,268+ Hacking Tools
Categories: 15+
License: MIT

FEATURES:
  - 5,268+ Hacking Tools Database
  - Category-wise Tool Organization
  - One-click Batch Installation
  - Professional Animated UI
  - Real-time Installation Progress
  - Cross-platform Support
  - Auto-detect Installed Tools
  - Custom Themes

DISCLAIMER:
  This tool is for EDUCATIONAL PURPOSES only.
  The developer is NOT responsible for any misuse.
  Use responsibly and only on systems you own or have
  explicit permission to test.

GitHub: https://github.com/Athexblackhat/VENOM-X
TikTok: @team.athex1
YouTube: @inziXploit444

========================================================
"""
        console.print(about_text)
        input("\nPress Enter to continue...")
    
    def exit_animation(self):
        os.system('clear' if os.name == 'posix' else 'cls')
        
        exit_banner = """
           VENOM-X IS LEAVING...
           Stay Lethal. Stay Anonymous.
           
           Created by ATHEX BLACK HAT
"""
        TypeWriter.animate_banner(exit_banner, 0.01)
        time.sleep(1)
        
        matrix = MatrixRain()
        matrix.run(2)
        
        console.print(f"\n{Fore.GREEN}Thank you for using VENOM-X!{Style.RESET_ALL}\n")
    
    def install_workflow(self):
        if not self.selected_tools:
            console.print(f"{Fore.RED}No tools selected! Browse categories and select tools first.{Style.RESET_ALL}")
            time.sleep(1)
            return
        
        self.install_tools(self.selected_tools)
    
    def run(self):
        matrix = MatrixRain()
        matrix.run(2)
        
        self.load_tools()
        self.check_installed_tools()
        
        self.display_main_menu()


def check_dependencies():
    required = ['rich', 'prompt_toolkit', 'pyfiglet', 'colorama']
    missing = []
    
    for package in required:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing.append(package)
    
    if missing:
        console.print(f"[yellow]Missing dependencies: {', '.join(missing)}[/yellow]")
        if Confirm.ask("Install missing dependencies?", default=True):
            subprocess.run([sys.executable, '-m', 'pip', 'install'] + missing)
            console.print("[green]Dependencies installed! Please restart VENOM-X.[/green]")
            sys.exit(0)


def main():
    if sys.version_info < (3, 8):
        print("VENOM-X requires Python 3.8 or higher!")
        sys.exit(1)
    
    check_dependencies()
    
    try:
        venom = VenomX()
        venom.run()
    except KeyboardInterrupt:
        console.print(f"\n{Fore.RED}Interrupted by user{Style.RESET_ALL}")
        sys.exit(0)
    except Exception as e:
        console.print(f"{Fore.RED}Error: {str(e)}{Style.RESET_ALL}")
        sys.exit(1)


if __name__ == "__main__":
    main()
