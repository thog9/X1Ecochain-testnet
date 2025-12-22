import os
import sys
import asyncio
from colorama import init, Fore, Style
import inquirer

# Khởi tạo colorama
init(autoreset=True)

# Độ rộng viền cố định
BORDER_WIDTH = 80

# Hàm hiển thị viền đẹp mắt
def print_border(text: str, color=Fore.CYAN, width=BORDER_WIDTH):
    text = text.strip()
    if len(text) > width - 4:
        text = text[:width - 7] + "..."  # Cắt dài và thêm "..."
    padded_text = f" {text} ".center(width - 2)
    print(f"{color}┌{'─' * (width - 2)}┐{Style.RESET_ALL}")
    print(f"{color}│{padded_text}│{Style.RESET_ALL}")
    print(f"{color}└{'─' * (width - 2)}┘{Style.RESET_ALL}")

# Hàm hiển thị banner
def _banner():
    banner = r"""


██╗░░██╗░░███╗░░  ███████╗░█████╗░░█████╗░░█████╗░██╗░░██╗░█████╗░██╗███╗░░██╗
╚██╗██╔╝░████║░░  ██╔════╝██╔══██╗██╔══██╗██╔══██╗██║░░██║██╔══██╗██║████╗░██║
░╚███╔╝░██╔██║░░  █████╗░░██║░░╚═╝██║░░██║██║░░╚═╝███████║███████║██║██╔██╗██║
░██╔██╗░╚═╝██║░░  ██╔══╝░░██║░░██╗██║░░██║██║░░██╗██╔══██║██╔══██║██║██║╚████║
██╔╝╚██╗███████╗  ███████╗╚█████╔╝╚█████╔╝╚█████╔╝██║░░██║██║░░██║██║██║░╚███║
╚═╝░░╚═╝╚══════╝  ╚══════╝░╚════╝░░╚════╝░░╚════╝░╚═╝░░╚═╝╚═╝░░╚═╝╚═╝╚═╝░░╚══╝


    """
    print(f"{Fore.GREEN}{banner:^80}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}{'═' * BORDER_WIDTH}{Style.RESET_ALL}")
    print_border("X1ECOCHAIN TESTNET", Fore.GREEN)
    print(f"{Fore.YELLOW}│ {'Website'}: {Fore.CYAN}https://thogtoolhub.com/{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}│ {'Discord'}: {Fore.CYAN}https://discord.gg/MnmYBKfHQf{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}│ {'Channel Telegram'}: {Fore.CYAN}https://t.me/thogairdrops{Style.RESET_ALL}")
    print(f"{Fore.GREEN}{'═' * BORDER_WIDTH}{Style.RESET_ALL}")

# Hàm xóa màn hình
def _clear():
    os.system('cls' if os.name == 'nt' else 'clear')

# Các hàm giả lập cho các lệnh mới
async def run_deploytoken(language: str):
    from scripts.deploytoken import run_deploytoken as deploytoken_run
    await deploytoken_run(language)

async def run_sendtoken(language: str):
    from scripts.sendtoken import run_sendtoken as sendtoken_run
    await sendtoken_run(language)

async def run_nftcollection(language: str):
    from scripts.nftcollection import run_nftcollection as nftcollection_run
    await nftcollection_run(language)

async def run_sendtx(language: str):
    from scripts.sendtx import run_sendtx as sendtx_run
    await sendtx_run(language)

async def run_x1faucet(language: str):
    from scripts.x1faucet import run_x1faucet as x1faucet_run
    await x1faucet_run(language)

async def run_daily(language: str):
    from scripts.daily import run_daily as daily_run
    await daily_run(language)

async def run_social(language: str):
    from scripts.social import run_social as social_run
    await social_run(language)
    
async def cmd_exit(language: str):
    messages = {"vi": "Đang thoát...", "en": "Exiting..."}
    print_border(messages[language], Fore.GREEN)
    sys.exit(0)

# Danh sách lệnh menu
SCRIPT_MAP = {
    "sendtx": run_sendtx,
    "deploytoken": run_deploytoken,
    "sendtoken": run_sendtoken,
    "nftcollection": run_nftcollection,
    "x1faucet": run_x1faucet,
    "daily": run_daily,
    "social": run_social,
    "exit": cmd_exit
}


# Danh sách script và thông báo theo ngôn ngữ
def get_available_scripts(language):
    scripts = {
        'vi': [
            {"name": "1. Faucet X1T → X1 EcoChain", "value": "x1faucet", "locked": True},
            {"name": "2. Tự động hoàn thành nhiệm vụ Daily", "value": "daily", "locked": True},
            {"name": "3. Tự động hoàn thành nhiệm vụ Linking & Social", "value": "social", "locked": True},
            
            {"name": "4. Deploy Token smart-contract", "value": "deploytoken"},
            {"name": "5. Gửi Token ERC20 ngẫu nhiên hoặc File (addressERC20.txt)", "value": "sendtoken"},
            {"name": "6. Deploy NFT smart-contract", "value": "nftcollection"},
            {"name": "7. Gửi TX ngẫu nhiên hoặc File (address.txt)", "value": "sendtx"},
            
            {"name": "X. Thoát", "value": "exit"},
        ],
        'en': [
            {"name": "1. Faucet X1T → X1 EcoChain", "value": "faucet", "locked": True},
            {"name": "2. Automatic task Daily completion", "value": "daily", "locked": True},
            {"name": "3. Automatic task Linking & Social completion", "value": "social", "locked": True},
            
            {"name": "4. Deploy Token smart-contract", "value": "deploytoken"},
            {"name": "5. Send Token ERC20 random or File (addressERC20.txt)", "value": "sendtoken"},
            {"name": "6. Deploy NFT smart-contract", "value": "nftcollection"},
            {"name": "7. Send TX random or File (address.txt)", "value": "sendtx"},

            {"name": "X. Thoát", "value": "exit"},
        ]
    }
    return scripts[language]

def run_script(script_func, language):
    """Chạy script bất kể nó là async hay không."""
    if asyncio.iscoroutinefunction(script_func):
        asyncio.run(script_func(language))
    else:
        script_func(language)

def select_language():
    while True:
        _clear()
        _banner()
        print(f"{Fore.GREEN}{'═' * BORDER_WIDTH}{Style.RESET_ALL}")
        print_border("CHỌN NGÔN NGỮ / SELECT LANGUAGE", Fore.YELLOW)
        questions = [
            inquirer.List('language',
                          message=f"{Fore.CYAN}Vui lòng chọn / Please select:{Style.RESET_ALL}",
                          choices=[("1. Tiếng Việt", 'vi'), ("2. English", 'en')],
                          carousel=True)
        ]
        answer = inquirer.prompt(questions)
        if answer and answer['language'] in ['vi', 'en']:
            return answer['language']
        print(f"{Fore.RED}❌ {'Lựa chọn không hợp lệ / Invalid choice':^76}{Style.RESET_ALL}")

def main():
    _clear()
    _banner()
    language = select_language()

    messages = {
        "vi": {
            "running": "Đang thực thi: {}",
            "completed": "Đã hoàn thành: {}",
            "error": "Lỗi: {}",
            "press_enter": "Nhấn Enter để tiếp tục...",
            "menu_title": "MENU CHÍNH",
            "select_script": "Chọn script để chạy",
            "locked": "🔒 Script này bị khóa! Vui lòng vào group hoặc donate để mở khóa."
        },
        "en": {
            "running": "Running: {}",
            "completed": "Completed: {}",
            "error": "Error: {}",
            "press_enter": "Press Enter to continue...",
            "menu_title": "MAIN MENU",
            "select_script": "Select script to run",
            "locked": "🔒 This script is locked! Please join our group or donate to unlock."
        }
    }

    while True:
        _clear()
        _banner()
        print(f"{Fore.YELLOW}{'═' * BORDER_WIDTH}{Style.RESET_ALL}")
        print_border(messages[language]["menu_title"], Fore.YELLOW)
        print(f"{Fore.CYAN}│ {messages[language]['select_script'].center(BORDER_WIDTH - 4)} │{Style.RESET_ALL}")

        available_scripts = get_available_scripts(language)
        questions = [
            inquirer.List('script',
                          message=f"{Fore.CYAN}{messages[language]['select_script']}{Style.RESET_ALL}",
                          choices=[script["name"] for script in available_scripts],
                          carousel=True)
        ]
        answers = inquirer.prompt(questions)
        if not answers:
            continue

        selected_script_name = answers['script']
        selected_script = next(script for script in available_scripts if script["name"] == selected_script_name)
        selected_script_value = selected_script["value"]

        if selected_script.get("locked"):
            _clear()
            _banner()
            print_border("SCRIPT BỊ KHÓA / LOCKED", Fore.RED)
            print(f"{Fore.YELLOW}{messages[language]['locked']}")
            print('')
            print(f"{Fore.CYAN}→ Telegram: https://t.me/thogairdrops")
            print(f"{Fore.CYAN}→ Donate: https://buymecafe.vercel.app{Style.RESET_ALL}")
            print('')
            input(f"{Fore.YELLOW}⏎ {messages[language]['press_enter']}{Style.RESET_ALL:^76}")
            continue

        script_func = SCRIPT_MAP.get(selected_script_value)
        if script_func is None:
            print(f"{Fore.RED}{'═' * BORDER_WIDTH}{Style.RESET_ALL}")
            print_border(f"{'Chưa triển khai / Not implemented'}: {selected_script_name}", Fore.RED)
            input(f"{Fore.YELLOW}⏎ {messages[language]['press_enter']}{Style.RESET_ALL:^76}")
            continue

        try:
            print(f"{Fore.CYAN}{'═' * BORDER_WIDTH}{Style.RESET_ALL}")
            print_border(messages[language]["running"].format(selected_script_name), Fore.CYAN)
            run_script(script_func, language)
            print(f"{Fore.GREEN}{'═' * BORDER_WIDTH}{Style.RESET_ALL}")
            print_border(messages[language]["completed"].format(selected_script_name), Fore.GREEN)
            input(f"{Fore.YELLOW}⏎ {messages[language]['press_enter']}{Style.RESET_ALL:^76}")
        except Exception as e:
            print(f"{Fore.RED}{'═' * BORDER_WIDTH}{Style.RESET_ALL}")
            print_border(messages[language]["error"].format(str(e)), Fore.RED)
            print('')
            input(f"{Fore.YELLOW}⏎ {messages[language]['press_enter']}{Style.RESET_ALL:^76}")

if __name__ == "__main__":
    main()






