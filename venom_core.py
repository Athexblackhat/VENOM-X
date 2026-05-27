#!/usr/bin/env python3

import json
import os
import sys
import time
import shutil
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field, asdict
from datetime import datetime

from venom_themes import VenomTheme
from venom_animations import Spinner, TypeWriter, MatrixRain


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
    install_date: str = ""
    version: str = "latest"
    
    def to_dict(self) -> dict:
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Tool':
        return cls(**data)


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
    
    @property
    def install_percentage(self) -> float:
        if self.count == 0:
            return 0
        return (self.installed_count / self.count) * 100


class VenomCore:
    def __init__(self, json_path: str = 'hacking_tools_ultimate.json'):
        self.json_path = Path(json_path)
        self.config_path = Path.home() / '.venomx' / 'config.json'
        self.tools_path = Path.home() / 'venomx-tools'
        self.tools: List[Tool] = []
        self.categories: Dict[str, Category] = {}
        self.config: dict = {}
        self.theme = VenomTheme()
        self.loaded = False
        
        self.tools_path.mkdir(parents=True, exist_ok=True)
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        
        self.load_config()
    
    def load_config(self) -> dict:
        default_config = {
            'theme': 'venom',
            'install_path': str(self.tools_path),
            'auto_update': True,
            'animations': True,
            'sound_effects': False,
            'first_run': True,
            'last_updated': datetime.now().isoformat(),
            'installed_tools': [],
            'selected_tools': []
        }
        
        if self.config_path.exists():
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    self.config = json.load(f)
            except:
                self.config = default_config
        else:
            self.config = default_config
            self.save_config()
        
        return self.config
    
    def save_config(self):
        with open(self.config_path, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, indent=4, ensure_ascii=False)
    
    def load_tools(self) -> bool:
        if not self.json_path.exists():
            if not Path(self.json_path).is_absolute():
                script_dir = Path(__file__).parent
                json_path = str(script_dir / self.json_path)
                self.json_path = Path(json_path)
        
        if not self.json_path.exists():
            print(f"Error: {self.json_path} not found!")
            return False
        
        try:
            spinner = Spinner('snake')
            spinner.start("Loading VENOM-X database...")
            time.sleep(1)
            
            with open(self.json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            self.tools = []
            self.categories = {}
            
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
            
            for tool_data in data.get('tools', []):
                tool = Tool(
                    name=tool_data.get('name', 'Unknown'),
                    full_name=tool_data.get('full_name', ''),
                    url=tool_data.get('url', ''),
                    clone_url=tool_data.get('clone_url', ''),
                    description=tool_data.get('description', 'No description'),
                    stars=tool_data.get('stars', 0),
                    language=tool_data.get('language', 'Unknown'),
                    category=tool_data.get('category', 'default'),
                    installed=False
                )
                self.tools.append(tool)
                
                cat_id = tool.category
                if cat_id not in self.categories:
                    meta_name = category_meta.get(cat_id, category_meta['default'])
                    self.categories[cat_id] = Category(
                        id=cat_id,
                        name=meta_name,
                        color='red'
                    )
                self.categories[cat_id].tools.append(tool)
            
            spinner.stop(f"Loaded {len(self.tools)} tools across {len(self.categories)} categories")
            self.loaded = True
            return True
            
        except json.JSONDecodeError as e:
            print(f"JSON Parse Error: {e}")
            return False
        except Exception as e:
            print(f"Error loading tools: {e}")
            return False
    
    def check_installed_tools(self):
        if not self.loaded:
            return
        
        installed_count = 0
        for tool in self.tools:
            tool_path = self.tools_path / tool.name.lower().replace(' ', '-')
            if tool_path.exists():
                tool.installed = True
                installed_count += 1
            elif self._check_system_command(tool.name.lower()):
                tool.installed = True
                installed_count += 1
        
        self.config['installed_tools'] = [t.name for t in self.tools if t.installed]
        self.save_config()
        
        return installed_count
    
    def _check_system_command(self, command: str) -> bool:
        return shutil.which(command) is not None
    
    def search_tools(self, query: str) -> List[Tool]:
        query = query.lower()
        results = []
        
        for tool in self.tools:
            if (query in tool.name.lower() or 
                query in tool.description.lower() or
                query in tool.language.lower() or
                query in tool.category.lower()):
                results.append(tool)
        
        return results
    
    def get_tools_by_category(self, category_id: str) -> List[Tool]:
        if category_id in self.categories:
            return self.categories[category_id].tools
        return []
    
    def get_tool_by_name(self, name: str) -> Optional[Tool]:
        for tool in self.tools:
            if tool.name.lower() == name.lower():
                return tool
        return None
    
    def get_categories(self) -> Dict[str, Category]:
        return self.categories
    
    def get_statistics(self) -> dict:
        total = len(self.tools)
        installed = sum(1 for t in self.tools if t.installed)
        categories = len(self.categories)
        languages = {}
        
        for tool in self.tools:
            lang = tool.language if tool.language else 'Unknown'
            languages[lang] = languages.get(lang, 0) + 1
        
        return {
            'total_tools': total,
            'installed_tools': installed,
            'pending_tools': total - installed,
            'categories': categories,
            'languages': languages,
            'install_percentage': (installed / total * 100) if total > 0 else 0
        }
    
    def get_install_command(self, tool: Tool) -> str:
        if 'github.com' in tool.clone_url:
            repo_name = tool.name.lower().replace(' ', '-')
            return f"git clone {tool.clone_url} {self.tools_path / repo_name}"
        elif tool.language.lower() in ['python', 'python3']:
            return f"pip3 install {tool.name.lower().replace(' ', '-')}"
        elif tool.language.lower() == 'go':
            return f"go install {tool.clone_url}@latest"
        elif tool.language.lower() == 'ruby':
            return f"gem install {tool.name.lower()}"
        elif tool.language.lower() in ['javascript', 'node', 'npm']:
            return f"npm install -g {tool.name.lower()}"
        else:
            return f"git clone {tool.clone_url} {self.tools_path / tool.name.lower().replace(' ', '-')}"
    
    def get_category_summary(self) -> str:
        summary = []
        for cat_id, category in self.categories.items():
            summary.append(f"{category.name}: {category.installed_count}/{category.count}")
        return '\n'.join(summary)
    
    def export_installed_list(self) -> str:
        installed = [tool.name for tool in self.tools if tool.installed]
        return '\n'.join(sorted(installed))
    
    def export_tools_json(self) -> dict:
        return {
            'total_tools': len(self.tools),
            'export_date': datetime.now().isoformat(),
            'tools': [tool.to_dict() for tool in self.tools]
        }


if __name__ == "__main__":
    core = VenomCore()
    print("VENOM-X Core Test")
