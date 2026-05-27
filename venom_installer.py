#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
VENOM-X Installation Handler
Created by ATHEX BLACK HAT
"""

import subprocess
import os
import sys
import time
import shutil
from pathlib import Path
from typing import List, Tuple, Optional
from datetime import datetime

from venom_core import VenomCore, Tool
from venom_animations import ProgressBar, Spinner, TypeWriter, MatrixRain
from venom_themes import VenomTheme


class VenomInstaller:
    """VENOM-X Installation Handler"""
    
    def __init__(self, core: VenomCore):
        self.core = core
        self.theme = core.theme
        self.install_path = Path(core.config.get('install_path', Path.home() / 'venomx-tools'))
        self.install_path.mkdir(parents=True, exist_ok=True)
        
        # Statistics
        self.success_count = 0
        self.fail_count = 0
        self.skipped_count = 0
        self.failed_tools: List[Tuple[Tool, str]] = []
    
    def _run_command(self, command: str, cwd: Path = None) -> Tuple[bool, str]:
        """Run shell command and return result"""
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                cwd=cwd or self.install_path,
                timeout=300  # 5 minute timeout
            )
            if result.returncode == 0:
                return True, result.stdout
            else:
                return False, result.stderr
        except subprocess.TimeoutExpired:
            return False, "Command timed out"
        except Exception as e:
            return False, str(e)
    
    def install_git_tool(self, tool: Tool) -> Tuple[bool, str]:
        """Install tool from GitHub"""
        repo_name = tool.name.lower().replace(' ', '-')
        target_path = self.install_path / repo_name
        
        # Check if already installed
        if target_path.exists():
            return True, "Already installed"
        
        # Clone repository
        command = f"git clone {tool.clone_url} {repo_name}"
        success, output = self._run_command(command)
        
        if success:
            # Try to run install if Makefile exists
            makefile = target_path / 'Makefile'
            if makefile.exists():
                self._run_command("make install", target_path)
            
            # Update tool status
            tool.installed = True
            tool.install_date = datetime.now().isoformat()
            
            return True, "Installed successfully"
        
        return False, output
    
    def install_pip_tool(self, tool: Tool) -> Tuple[bool, str]:
        """Install tool via pip"""
        package_name = tool.name.lower().replace(' ', '-')
        command = f"pip3 install {package_name}"
        success, output = self._run_command(command)
        
        if success:
            tool.installed = True
            tool.install_date = datetime.now().isoformat()
            return True, "Installed via pip"
        
        return False, output
    
    def install_go_tool(self, tool: Tool) -> Tuple[bool, str]:
        """Install tool via go install"""
        command = f"go install {tool.clone_url}@latest"
        success, output = self._run_command(command)
        
        if success:
            tool.installed = True
            tool.install_date = datetime.now().isoformat()
            return True, "Installed via go"
        
        return False, output
    
    def install_gem_tool(self, tool: Tool) -> Tuple[bool, str]:
        """Install tool via gem"""
        gem_name = tool.name.lower()
        command = f"gem install {gem_name}"
        success, output = self._run_command(command)
        
        if success:
            tool.installed = True
            tool.install_date = datetime.now().isoformat()
            return True, "Installed via gem"
        
        return False, output
    
    def install_npm_tool(self, tool: Tool) -> Tuple[bool, str]:
        """Install tool via npm"""
        package_name = tool.name.lower()
        command = f"npm install -g {package_name}"
        success, output = self._run_command(command)
        
        if success:
            tool.installed = True
            tool.install_date = datetime.now().isoformat()
            return True, "Installed via npm"
        
        return False, output
    
    def install_tool(self, tool: Tool) -> Tuple[bool, str]:
        """Install a single tool based on its type"""
        
        # Check if already installed
        if tool.installed:
            return True, "Already installed"
        
        # Determine installation method
        if 'github.com' in tool.clone_url:
            return self.install_git_tool(tool)
        elif tool.language.lower() in ['python', 'python3', '']:
            return self.install_pip_tool(tool)
        elif tool.language.lower() == 'go':
            return self.install_go_tool(tool)
        elif tool.language.lower() == 'ruby':
            return self.install_gem_tool(tool)
        elif tool.language.lower() in ['javascript', 'node', 'npm', 'typescript']:
            return self.install_npm_tool(tool)
        else:
            # Default to git clone
            return self.install_git_tool(tool)
    
    def install_tools(self, tools: List[Tool], show_progress: bool = True) -> dict:
        """Install multiple tools"""
        
        self.success_count = 0
        self.fail_count = 0
        self.skipped_count = 0
        self.failed_tools = []
        
        if not tools:
            return {'success': 0, 'failed': 0, 'skipped': 0}
        
        if show_progress:
            print(f"\n{self.theme.header('INSTALLATION IN PROGRESS')}")
            print(f"{self.theme.get('info')}📦 Installing {len(tools)} tools...{self.theme.get('reset')}\n")
            
            pb = ProgressBar(len(tools))
        
        for i, tool in enumerate(tools):
            if show_progress:
                pb.update(i, f"⚡ Installing {tool.name}...")
            
            success, message = self.install_tool(tool)
            
            if success:
                if "Already" in message:
                    self.skipped_count += 1
                else:
                    self.success_count += 1
            else:
                self.fail_count += 1
                self.failed_tools.append((tool, message))
            
            time.sleep(0.1)
        
        if show_progress:
            pb.finish()
        
        # Save updated config
        self.core.save_config()
        
        return {
            'success': self.success_count,
            'failed': self.fail_count,
            'skipped': self.skipped_count,
            'total': len(tools),
            'failed_tools': self.failed_tools
        }
    
    def uninstall_tool(self, tool: Tool) -> Tuple[bool, str]:
        """Uninstall a tool"""
        repo_name = tool.name.lower().replace(' ', '-')
        tool_path = self.install_path / repo_name
        
        if not tool_path.exists():
            # Try to find via pip
            check_cmd = f"pip3 show {tool.name.lower()}"
            success, _ = self._run_command(check_cmd)
            if success:
                uninstall_cmd = f"pip3 uninstall -y {tool.name.lower()}"
                success, output = self._run_command(uninstall_cmd)
                if success:
                    tool.installed = False
                    return True, "Uninstalled via pip"
        
        # Remove directory
        if tool_path.exists():
            try:
                shutil.rmtree(tool_path)
                tool.installed = False
                return True, "Removed successfully"
            except Exception as e:
                return False, str(e)
        
        return False, "Tool not found"
    
    def update_tool(self, tool: Tool) -> Tuple[bool, str]:
        """Update a tool"""
        repo_name = tool.name.lower().replace(' ', '-')
        tool_path = self.install_path / repo_name
        
        if tool_path.exists() and (tool_path / '.git').exists():
            command = f"git -C {repo_name} pull"
            success, output = self._run_command(command)
            if success:
                return True, "Updated successfully"
            return False, output
        
        # Reinstall if not git repo
        return self.install_tool(tool)
    
    def update_all_tools(self) -> dict:
        """Update all installed tools"""
        installed_tools = [t for t in self.core.tools if t.installed]
        
        if not installed_tools:
            return {'success': 0, 'failed': 0}
        
        print(f"\n{self.theme.header('UPDATING TOOLS')}")
        print(f"{self.theme.get('info')}🔄 Updating {len(installed_tools)} tools...{self.theme.get('reset')}\n")
        
        success_count = 0
        fail_count = 0
        
        pb = ProgressBar(len(installed_tools))
        
        for i, tool in enumerate(installed_tools):
            pb.update(i, f"🔄 Updating {tool.name}...")
            success, _ = self.update_tool(tool)
            if success:
                success_count += 1
            else:
                fail_count += 1
            time.sleep(0.1)
        
        pb.finish()
        
        return {'success': success_count, 'failed': fail_count}
    
    def get_install_report(self) -> str:
        """Generate installation report"""
        report = f"""
{self.theme.header('INSTALLATION REPORT')}

{self.theme.get('success')}✅ Successfully installed: {self.success_count}{self.theme.get('reset')}
{self.theme.get('warning')}⏭️  Skipped (already installed): {self.skipped_count}{self.theme.get('reset')}
{self.theme.get('error')}❌ Failed: {self.fail_count}{self.theme.get('reset')}

"""
        if self.failed_tools:
            report += f"{self.theme.get('danger')}⚠️ Failed Tools:{self.theme.get('reset')}\n"
            for tool, error in self.failed_tools:
                report += f"  - {tool.name}: {error[:50]}...\n"
        
        return report
    
    def cleanup_temp_files(self):
        """Cleanup temporary installation files"""
        temp_dirs = [
            self.install_path / 'tmp',
            self.install_path / '__pycache__',
            self.install_path / 'build',
            self.install_path / 'dist'
        ]
        
        for temp_dir in temp_dirs:
            if temp_dir.exists():
                try:
                    shutil.rmtree(temp_dir)
                except:
                    pass
    
    def verify_installation(self, tool: Tool) -> bool:
        """Verify if tool is properly installed"""
        # Check directory
        repo_name = tool.name.lower().replace(' ', '-')
        tool_path = self.install_path / repo_name
        
        if tool_path.exists():
            # Check if it has files
            if any(tool_path.iterdir()):
                return True
        
        # Check system command
        if self.core._check_system_command(tool.name.lower()):
            return True
        
        # Check pip package
        check_cmd = f"pip3 show {tool.name.lower()}"
        success, _ = self._run_command(check_cmd)
        if success:
            return True
        
        return False


# Test installer
if __name__ == "__main__":
    core = VenomCore()
    core.load_tools()
    
    installer = VenomInstaller(core)
    
    print("VENOM-X Installer Test")
    print("-" * 40)
    
    # Test install first tool
    if core.tools:
        test_tool = core.tools[0]
        print(f"Testing install for: {test_tool.name}")
        success, message = installer.install_tool(test_tool)
        print(f"Result: {success} - {message}")