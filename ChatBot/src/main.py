import asyncio
import sys
import os

# Chuyển working directory về thư mục gốc của project (ChatBot) để tránh lỗi đường dẫn relative
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(project_root)
# Thêm ChatBot root vào path để import modules (do chạy file này từ src/)
sys.path.insert(0, project_root)

from langchain_core.messages import HumanMessage
from src.graph.graph import graph
from src.config.configs import config_object
from src.log import logger

# ─────────────── ANSI colors ───────────────
RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"
CYAN = "\033[36m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
MAGENTA = "\033[35m"
RED = "\033[31m"
BLUE = "\033[34m"


def print_banner():
    # Sử dụng config_models.OPENAI_LLM_MODEL vì bạn đã sửa trong models.yaml
    llm_name = getattr(config_object, "OPENAI_LLM_MODEL", getattr(config_object, "GROQ_LLM_MODEL", None))
    model_name = llm_name.MODEL_NAME if llm_name else "Unknown Model"
    
    banner = f"""
{CYAN}{BOLD}╔══════════════════════════════════════════════════════════════╗
║               🤖  CHATBOT HỒ SƠ LƯU TRỮ  🤖               ║
║──────────────────────────────────────────────────────────────║
║  LLM  : {model_name:<44}║
║  Tools : MCP via {config_object.MCP.BASE_MCP_SERVER_URL:<42}║
╚══════════════════════════════════════════════════════════════╝{RESET}
"""
    print(banner)


async def run_chat():
    print_banner()
    print(f"{GREEN}✅ ChatBot sẵn sàng (dựa trên kiến trúc chatbot_homepage){RESET}")
    print(f"{DIM}Gõ 'quit' hoặc 'exit' để thoát{RESET}\n")

    while True:
        try:
            user_input = input(f"{CYAN}{BOLD}👤 Bạn: {RESET}").strip()
        except (EOFError, KeyboardInterrupt):
            print(f"\n{DIM}Tạm biệt! 👋{RESET}")
            break

        if not user_input:
            continue

        if user_input.lower() in ("quit", "exit", "thoát"):
            print(f"\n{DIM}Tạm biệt! 👋{RESET}")
            break

        print(f"\n{DIM}Đang xử lý...{RESET}")

        try:
            from src.graph.configuration import Context, LLMConfig
            
            result = await graph.ainvoke(
                {"messages": [HumanMessage(content=user_input)]},
                context=Context(llm_config=LLMConfig())
            )
            
            ai_message = result["messages"][-1]
            print(f"\n{GREEN}{BOLD}🤖 Bot:{RESET} {ai_message.content}\n")

        except Exception as e:
            import traceback
            traceback.print_exc()
            logger.error(f"Lỗi khi xử lý: {e}")
            print(f"\n{RED}❌ Lỗi: {e}{RESET}\n")

if __name__ == "__main__":
    asyncio.run(run_chat())
