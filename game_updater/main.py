import subprocess
import sys
from . import itch_api, file_handler, browser_automation, config

def run_post_export_tasks(version):
    """执行导出后的所有任务"""
    print("\n--- 步骤 3.1: 执行导出后任务 ---")
    
    if not file_handler.unzip_story_export(version):
        print("流程终止：解压 'story_export.zip' 失败。")
        return

    last_fetch_dir = file_handler.sync_fetch_dirs()
    if not last_fetch_dir:
        print("流程终止：同步 'fetch' 目录失败。")
        return

    print("  - 正在运行 versionUpdate.py 脚本...")
    try:
        args = [sys.executable, config.VERSION_UPDATE_SCRIPT_PATH, last_fetch_dir, version]
        result = subprocess.run(args, check=True, capture_output=True, text=True)
        print("  - versionUpdate.py 输出:")
        print(result.stdout)
        if result.stderr:
            print("  - versionUpdate.py 错误输出:")
            print(result.stderr)
        print("  - versionUpdate.py 脚本成功执行。")
    except FileNotFoundError:
        print(f"  - 错误: 未找到脚本 {config.VERSION_UPDATE_SCRIPT_PATH}")
    except subprocess.CalledProcessError as e:
        print(f"  - 错误: versionUpdate.py 执行失败，返回码 {e.returncode}")
        print(f"  - 输出: \n{e.stdout}")
        print(f"  - 错误: \n{e.stderr}")


def run_update_and_export(game_id, password=None, headless=False, js_path=None):
    """
    执行完整的游戏更新和故事导出流程。
    通过API获取HTML channel信息，直接下载HTML文件。
    
    :param game_id: 要更新的游戏的ID。
    :param password: (可选) EA版所需的密码。
    :param headless: (可选) 是否使用headless模式（CI环境）。
    :param js_path: (可选) JS脚本路径。
    """
    mode = "抢先体验版" if password else "稳定版"
    print(f"开始为 {mode} 执行游戏更新和导出流程...")
    if headless:
        print("  (使用headless模式)")

    # 步骤 1: 从itch.io获取HTML channel信息
    print("\n--- 步骤 1: 获取API信息 ---")
    upload_id, build_id, version = itch_api.get_html_channel_info(game_id, password)
    if not upload_id or not build_id or not version:
        print("流程终止：未能获取HTML channel信息。")
        return None

    # 步骤 2: 构建HTML URL并直接下载
    print("\n--- 步骤 2: 下载HTML文件 ---")
    html_url = itch_api.build_html_url(upload_id, build_id)
    print(f"  - 构建的HTML URL: {html_url}")
    
    new_html_path = file_handler.download_html(html_url, version)
    if not new_html_path:
        print("流程终止：下载HTML文件失败。")
        file_handler.cleanup_temp_files()
        return None

    # 步骤 3: 浏览器自动化
    print("\n--- 步骤 3: 执行浏览器自动化 ---")
    if browser_automation.export_story_from_html(new_html_path, headless=headless, js_path=js_path):
        run_post_export_tasks(version)

    # 步骤 4: 清理
    print("\n--- 清理临时文件 ---")
    file_handler.cleanup_temp_files()

    print("\n所有操作已完成！")
    return version