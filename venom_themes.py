#!/usr/bin/env python3

from colorama import Fore, Back, Style, init
import json
import os
from pathlib import Path

init(autoreset=True)

class VenomTheme:
    THEMES = {
        'venom': {
            'name': 'VENOM',
            'primary': Fore.RED,
            'secondary': Fore.YELLOW,
            'accent': Fore.GREEN,
            'danger': Fore.MAGENTA,
            'info': Fore.CYAN,
            'success': Fore.LIGHTGREEN_EX,
            'warning': Fore.LIGHTYELLOW_EX,
            'error': Fore.LIGHTRED_EX,
            'border': '-',
            'bg': Back.BLACK,
            'description': 'Red and Black - Deadly Venom Theme'
        },
        'matrix': {
            'name': 'MATRIX',
            'primary': Fore.GREEN,
            'secondary': Fore.LIGHTGREEN_EX,
            'accent': Fore.LIGHTWHITE_EX,
            'danger': Fore.RED,
            'info': Fore.CYAN,
            'success': Fore.LIGHTGREEN_EX,
            'warning': Fore.YELLOW,
            'error': Fore.RED,
            'border': '=',
            'bg': Back.BLACK,
            'description': 'Green and Black - Matrix Theme'
        },
        'dark': {
            'name': 'DARK',
            'primary': Fore.WHITE,
            'secondary': Fore.LIGHTBLACK_EX,
            'accent': Fore.CYAN,
            'danger': Fore.RED,
            'info': Fore.BLUE,
            'success': Fore.GREEN,
            'warning': Fore.YELLOW,
            'error': Fore.RED,
            'border': '*',
            'bg': Back.BLACK,
            'description': 'White and Gray - Minimal Dark Theme'
        },
        'neon': {
            'name': 'NEON',
            'primary': Fore.MAGENTA,
            'secondary': Fore.LIGHTMAGENTA_EX,
            'accent': Fore.CYAN,
            'danger': Fore.RED,
            'info': Fore.BLUE,
            'success': Fore.GREEN,
            'warning': Fore.YELLOW,
            'error': Fore.RED,
            'border': '+',
            'bg': Back.BLACK,
            'description': 'Cyan and Magenta - Cyberpunk Neon Theme'
        },
        'blood': {
            'name': 'BLOOD',
            'primary': Fore.RED,
            'secondary': Fore.LIGHTRED_EX,
            'accent': Fore.WHITE,
            'danger': Fore.MAGENTA,
            'info': Fore.YELLOW,
            'success': Fore.GREEN,
            'warning': Fore.YELLOW,
            'error': Fore.RED,
            'border': '#',
            'bg': Back.BLACK,
            'description': 'Blood Red - Dark Vampire Theme'
        }
    }
    
    def __init__(self, theme_name: str = 'venom'):
        self.config_path = Path.home() / '.venomx' / 'theme.json'
        self.current_theme = self.load_theme()
        self._theme = self.THEMES.get(self.current_theme, self.THEMES['venom'])
    
    def load_theme(self) -> str:
        if self.config_path.exists():
            try:
                with open(self.config_path, 'r') as f:
                    data = json.load(f)
                    return data.get('theme', 'venom')
            except:
                return 'venom'
        return 'venom'
    
    def save_theme(self, theme_name: str):
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.config_path, 'w') as f:
            json.dump({'theme': theme_name}, f, indent=4)
        self.current_theme = theme_name
        self._theme = self.THEMES.get(theme_name, self.THEMES['venom'])
    
    def get(self, key: str) -> str:
        return self._theme.get(key, Fore.WHITE)
    
    def set_theme(self, theme_name: str):
        if theme_name in self.THEMES:
            self._theme = self.THEMES[theme_name]
            self.save_theme(theme_name)
            return True
        return False
    
    def styled(self, text: str, style: str) -> str:
        return f"{self.get(style)}{text}{Style.RESET_ALL}"
    
    def border_line(self, text: str = "", length: int = 80) -> str:
        border_char = self.get('border')
        if text:
            padding = length - len(text) - 4
            return f"{self.get('primary')}{border_char * 2} {text} {border_char * padding}{Style.RESET_ALL}"
        return f"{self.get('primary')}{border_char * length}{Style.RESET_ALL}"
    
    def header(self, text: str) -> str:
        separator = "=" * 60
        return f"\n{self.get('danger')}{separator}\n{self.get('warning')}{text.center(60)}\n{self.get('danger')}{separator}{Style.RESET_ALL}"
    
    def menu_option(self, number: str, text: str) -> str:
        return f"  {self.get('accent')}[{self.get('primary')}{number}{self.get('accent')}]{self.get('secondary')} {text}{Style.RESET_ALL}"
    
    def status_icon(self, status: str) -> str:
        icons = {
            'success': f"{self.get('success')}OK",
            'error': f"{self.get('error')}FAIL",
            'warning': f"{self.get('warning')}WARN",
            'info': f"{self.get('info')}INFO",
            'install': f"{self.get('accent')}INSTALL",
            'remove': f"{self.get('danger')}REMOVE",
            'search': f"{self.get('info')}SEARCH",
            'settings': f"{self.get('secondary')}CONFIG",
            'back': f"{self.get('warning')}BACK",
            'exit': f"{self.get('danger')}EXIT"
        }
        return icons.get(status, "-")
    
    def print_banner(self, text: str):
        banner = self.header(text)
        print(banner)
    
    def list_themes(self) -> dict:
        return self.THEMES
    
    def get_current_theme(self) -> str:
        return self.current_theme
    
    def theme_preview(self, theme_name: str) -> str:
        theme = self.THEMES.get(theme_name, self.THEMES['venom'])
        preview = f"""
{theme['primary']}========================================
{theme['primary']}{theme['name']} THEME PREVIEW
{theme['primary']}========================================
{theme['primary']}Primary: {theme['primary']}████████
{theme['secondary']}Secondary: {theme['secondary']}████████
{theme['accent']}Accent: {theme['accent']}████████
{theme['danger']}Danger: {theme['danger']}████████
{theme['success']}Success: {theme['success']}████████
{theme['primary']}========================================{Style.RESET_ALL}
"""
        return preview


if __name__ == "__main__":
    theme = VenomTheme()
    print(theme.header("VENOM-X THEME TEST"))
    print(theme.menu_option("1", "Install Tools"))
    print(theme.status_icon('success'), "Success message")
