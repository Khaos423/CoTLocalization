import requests
import zipfile
import os
import shutil
from . import config

def download_html(html_url, version):
    """
    直接从HTML URL下载HTML文件，并保存到目标目录。
    
    参数:
        html_url: HTML文件的完整URL
        version: 版本号，用于重命名文件
    
    返回:
        成功时返回HTML文件的目标路径，失败时返回None
    """
    print(f"  - 正在从 {html_url} 下载HTML文件...")
    
    # 确保临时目录存在
    os.makedirs(config.TEMP_DIR, exist_ok=True)
    
    try:
        # 下载HTML文件
        response = requests.get(html_url, stream=True)
        response.raise_for_status()
        
        # 先保存到临时位置
        with open(config.TEMP_HTML_PATH, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"  - HTML文件已下载到临时位置: {config.TEMP_HTML_PATH}")
        
        # 构建目标文件名和路径
        new_filename = f"index{version}.html"
        destination_path = os.path.join(config.DESTINATION_DIR, new_filename)
        
        # 确保目标目录存在
        os.makedirs(config.DESTINATION_DIR, exist_ok=True)
        
        # 移动文件到目标位置
        shutil.move(config.TEMP_HTML_PATH, destination_path)
        print(f"  - HTML文件已移动到: {destination_path}")
        
        return destination_path
        
    except requests.exceptions.RequestException as e:
        print(f"  - 错误: 下载HTML文件失败: {e}")
        return None
    except Exception as e:
        print(f"  - 错误: 处理HTML文件时发生错误: {e}")
        return None

def cleanup_temp_files():
    """清理临时文件和文件夹"""
    print("  - 清理临时文件...")
    if os.path.exists(config.TEMP_DIR):
        shutil.rmtree(config.TEMP_DIR)
        print(f"  - 已删除临时目录: {config.TEMP_DIR}")
    
    # 清理下载的zip文件
    if os.path.exists(config.FINAL_EXPORT_ZIP_PATH):
        os.remove(config.FINAL_EXPORT_ZIP_PATH)
        print(f"  - 已删除导出的zip文件: {config.FINAL_EXPORT_ZIP_PATH}")
    print("  - 清理完成。")

def unzip_story_export(version):
    """解压 story_export.zip 到 source/version 目录"""
    target_dir = os.path.join(config.SOURCE_DIR, version)
    print(f"  - 正在解压 '{config.FINAL_EXPORT_ZIP_NAME}' 到 '{target_dir}'...")
    
    if not os.path.exists(config.FINAL_EXPORT_ZIP_PATH):
        print(f"  - 错误: 未找到 '{config.FINAL_EXPORT_ZIP_NAME}'。")
        return False
        
    try:
        with zipfile.ZipFile(config.FINAL_EXPORT_ZIP_PATH, 'r') as zip_ref:
            zip_ref.extractall(target_dir)
        print("  - 解压完成。")
        return True
    except Exception as e:
        print(f"  - 错误: 解压失败: {e}")
        return False

def sync_fetch_dirs():
    """同步fetch目录，并返回最后一个目录名"""
    print("  - 正在同步 'fetch' 目录...")
    try:
        # 获取所有子目录并排序
        dirs = sorted([d for d in os.listdir(config.FETCH_DIR) if os.path.isdir(os.path.join(config.FETCH_DIR, d))])
        if len(dirs) < 2:
            print("  - 错误: 'fetch' 目录中没有足够的子目录进行同步。")
            return None

        last_dir_name = dirs[-1]
        second_last_dir_name = dirs[-2]
        
        source_path = os.path.join(config.FETCH_DIR, second_last_dir_name)
        dest_path = os.path.join(config.FETCH_DIR, last_dir_name)
        
        print(f"  - 源目录: {source_path}")
        print(f"  - 目标目录: {dest_path}")

        # 复制文件，跳过已存在的
        shutil.copytree(source_path, dest_path, dirs_exist_ok=True)
        print("  - 同步完成。")
        return last_dir_name
        
    except Exception as e:
        print(f"  - 错误: 同步 'fetch' 目录失败: {e}")
        return None