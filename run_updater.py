import argparse
import getpass
import os
from game_updater import main
from game_updater.config import STABLE_GAME_ID, EARLY_ACCESS_GAME_ID

def run():
    parser = argparse.ArgumentParser(
        description="游戏更新和故事导出自动化工具。"
    )
    parser.add_argument(
        "--ea",
        action="store_true",
        help="如果设置此标志，将更新抢先体验版。否则，将更新稳定版。"
    )
    parser.add_argument(
        "--headless",
        action="store_true",
        help="使用headless模式（CI环境）。"
    )
    parser.add_argument(
        "--js-path",
        type=str,
        default=None,
        help="指定story-export.js脚本的路径。"
    )
    parser.add_argument(
        "--password",
        type=str,
        default=None,
        help="EA版所需的密码（CI环境中使用，避免交互式输入）。"
    )
    args = parser.parse_args()

    # 从环境变量获取密码（如果参数中未提供）
    password = args.password or os.environ.get("EA_PASSWORD")

    if args.ea:
        print("已选择抢先体验版更新流程。")
        if not password and not args.headless:
            password = getpass.getpass("请输入抢先体验版的密码: ")
        main.run_update_and_export(
            EARLY_ACCESS_GAME_ID,
            password=password,
            headless=args.headless,
            js_path=args.js_path
        )
    else:
        print("已选择稳定版更新流程。")
        main.run_update_and_export(
            STABLE_GAME_ID,
            headless=args.headless,
            js_path=args.js_path
        )

if __name__ == "__main__":
    run()