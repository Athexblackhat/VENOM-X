#!/usr/bin/env python3

import time
import random
import os
import sys
import shutil
import threading
from colorama import Fore, Back, Style, init

init(autoreset=True)

class MatrixRain:
    def __init__(self, speed: float = 0.03):
        self.speed = speed
        self.chars = "0123456789ABCDEF"
        self.running = False
        self.thread = None
    
    def _animate(self):
        try:
            columns = shutil.get_terminal_size().columns
            lines = shutil.get_terminal_size().lines
            
            while self.running:
                for _ in range(lines):
                    line = ''
                    for _ in range(columns):
                        char = random.choice(self.chars)
                        color = random.choice([Fore.GREEN, Fore.LIGHTGREEN_EX, Fore.WHITE])
                        line += f"{color}{char}"
                    print(line, end='\r')
                time.sleep(self.speed)
                
                print(f"\033[{lines}A", end='')
        except:
            pass
    
    def run(self, duration: float = 3):
        self.running = True
        self.thread = threading.Thread(target=self._animate)
        self.thread.daemon = True
        self.thread.start()
        time.sleep(duration)
        self.running = False
        os.system('clear' if os.name == 'posix' else 'cls')
    
    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join(timeout=1)


class TypeWriter:
    @staticmethod
    def write(text: str, delay: float = 0.03, color: str = Fore.GREEN):
        for char in text:
            sys.stdout.write(f"{color}{char}")
            sys.stdout.flush()
            time.sleep(delay)
        print()
    
    @staticmethod
    def write_line(text: str, delay: float = 0.02, color: str = Fore.WHITE):
        for char in text:
            sys.stdout.write(f"{color}{char}")
            sys.stdout.flush()
            time.sleep(delay)
        print()
    
    @staticmethod
    def animate_banner(text: str, delay: float = 0.01):
        lines = text.split('\n')
        for line in lines:
            for char in line:
                if char in ['=', '-', '+', '*', '#', '|', '/', '\\']:
                    print(Fore.RED + char, end='', flush=True)
                elif char in ['V', 'E', 'N', 'O', 'M', 'X', 'A', 'T', 'H', 'B', 'L', 'C', 'K']:
                    print(Fore.YELLOW + char, end='', flush=True)
                elif char.isdigit():
                    print(Fore.CYAN + char, end='', flush=True)
                else:
                    print(Fore.WHITE + char, end='', flush=True)
                time.sleep(delay)
            print()
            time.sleep(delay * 2)


class GlitchEffect:
    @staticmethod
    def glitch(text: str, intensity: int = 3) -> str:
        chars = "!@#$%^&*()_+{}|:<>?~[]\\;',./`"
        result = []
        
        for char in text:
            if random.random() < 0.15:
                result.append(random.choice(chars))
            else:
                result.append(char)
        
        result = [c.upper() if random.random() < 0.05 else c for c in result]
        
        return ''.join(result)
    
    @staticmethod
    def print_glitch(text: str, delay: float = 0.5):
        for _ in range(3):
            sys.stdout.write(f"\r{Fore.RED}{GlitchEffect.glitch(text)}")
            sys.stdout.flush()
            time.sleep(0.1)
            sys.stdout.write(f"\r{Fore.GREEN}{GlitchEffect.glitch(text)}")
            sys.stdout.flush()
            time.sleep(0.1)
            sys.stdout.write(f"\r{Fore.YELLOW}{GlitchEffect.glitch(text)}")
            sys.stdout.flush()
            time.sleep(0.1)
        print(f"\r{Fore.WHITE}{text}")


class Spinner:
    SPINNERS = {
        'snake': ['-', '\\', '|', '/'],
        'matrix': ['0', '1', '0', '1', '0', '1', '0', '1'],
        'arrow': ['>', 'v', '<', '^'],
        'hack': ['H', 'A', 'C', 'K', 'I', 'N', 'G'],
        'binary': ['0', '1', '0', '1', '0', '1'],
        'dots': ['.', '..', '...', '....'],
        'box': ['[  ]', '[*  ]', '[** ]', '[***]', '[ **]', '[  *]']
    }
    
    def __init__(self, style: str = 'snake'):
        self.style = style
        self.spinner_chars = self.SPINNERS.get(style, self.SPINNERS['dots'])
        self.running = False
        self.thread = None
        self.message = ""
    
    def _spin(self):
        i = 0
        while self.running:
            char = self.spinner_chars[i % len(self.spinner_chars)]
            color = random.choice([Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.CYAN])
            sys.stdout.write(f"\r{color}{char}{Style.RESET_ALL} {self.message}")
            sys.stdout.flush()
            time.sleep(0.1)
            i += 1
    
    def start(self, message: str = "Loading..."):
        self.message = message
        self.running = True
        self.thread = threading.Thread(target=self._spin)
        self.thread.daemon = True
        self.thread.start()
    
    def stop(self, final_message: str = None):
        self.running = False
        if self.thread:
            self.thread.join(timeout=0.5)
        if final_message:
            sys.stdout.write(f"\r{Fore.GREEN}[OK] {final_message}{' ' * 20}\n")
        else:
            sys.stdout.write(f"\r{' ' * 50}\r")
        sys.stdout.flush()
    
    def run(self, message: str, duration: float = 2):
        self.start(message)
        time.sleep(duration)
        self.stop()


class ProgressBar:
    def __init__(self, total: int, width: int = 50):
        self.total = total
        self.width = width
        self.current = 0
    
    def update(self, current: int, message: str = ""):
        self.current = current
        percent = self.current / self.total
        filled = int(self.width * percent)
        empty = self.width - filled
        
        bar = f"{Fore.RED}[{Fore.YELLOW}{'=' * filled}{Fore.DIM}{'-' * empty}{Fore.RED}]{Style.RESET_ALL}"
        percent_text = f"{Fore.CYAN}{percent * 100:>5.1f}%{Style.RESET_ALL}"
        
        sys.stdout.write(f"\r{bar} {percent_text} {message}")
        sys.stdout.flush()
    
    def finish(self, message: str = "Complete!"):
        self.update(self.total, message)
        print()


class LoadingEffect:
    @staticmethod
    def dots(message: str, duration: float = 2):
        for i in range(int(duration * 10)):
            dots = '.' * (i % 4)
            sys.stdout.write(f"\r{message}{dots}{' ' * 3}")
            sys.stdout.flush()
            time.sleep(0.1)
        print()
    
    @staticmethod
    def pulse(message: str, duration: float = 2):
        colors = [Fore.RED, Fore.YELLOW, Fore.GREEN, Fore.CYAN, Fore.MAGENTA]
        end_time = time.time() + duration
        
        while time.time() < end_time:
            for color in colors:
                sys.stdout.write(f"\r{color}{message}{Style.RESET_ALL}")
                sys.stdout.flush()
                time.sleep(0.1)
        print()
    
    @staticmethod
    def countdown(seconds: int, message: str = "Starting in"):
        for i in range(seconds, 0, -1):
            sys.stdout.write(f"\r{Fore.YELLOW}{message} {i}{' ' * 5}{Style.RESET_ALL}")
            sys.stdout.flush()
            time.sleep(1)
        print(f"\r{Fore.GREEN}{message} GO!{' ' * 10}{Style.RESET_ALL}")


class ScreenEffect:
    @staticmethod
    def clear():
        os.system('clear' if os.name == 'posix' else 'cls')
    
    @staticmethod
    def flash(duration: float = 0.1, times: int = 3):
        for _ in range(times):
            print(f"{Back.WHITE}{' ' * shutil.get_terminal_size().columns}")
            time.sleep(duration)
            print(f"{Back.BLACK}{' ' * shutil.get_terminal_size().columns}")
            time.sleep(duration)
    
    @staticmethod
    def shake(duration: float = 0.5):
        end_time = time.time() + duration
        while time.time() < end_time:
            sys.stdout.write(f"\033[{random.randint(0, 2)};{random.randint(0, 2)}H")
            time.sleep(0.05)
        sys.stdout.write("\033[0;0H")


if __name__ == "__main__":
    print("Testing VENOM-X Animations...")
    
    TypeWriter.write("VENOM-X Loading...", 0.05, Fore.RED)
    
    spinner = Spinner('snake')
    spinner.run("Injecting Venom...", 2)
    
    pb = ProgressBar(100)
    for i in range(0, 101, 10):
        pb.update(i, f"Installing... {i}%")
        time.sleep(0.2)
    pb.finish()
    
    print("\n[OK] All animations working!")
