#!/usr/bin/env python3
"""
生成 GameOriginalImagePack 的 boot.json 文件

用法:
    python generate_image_pack_boot.py <res_dir> <version> [output_file]

参数:
    res_dir: 包含 res/img 目录的路径
    version: 游戏版本号
    output_file: 输出的 boot.json 路径 (默认: boot.json)
"""

import json
import os
import sys
from pathlib import Path


def find_image_files(res_dir: str) -> list[str]:
    """
    查找 res 目录中的所有图片文件
    返回相对路径列表，格式为 res/img/xxx.png
    """
    image_extensions = {'.png', '.jpg', '.jpeg', '.gif', '.webp'}
    image_files = []
    
    res_path = Path(res_dir)
    if not res_path.exists():
        print(f"错误: 目录不存在: {res_dir}")
        sys.exit(1)
    
    # 遍历 res 目录
    for file_path in res_path.rglob('*'):
        if file_path.is_file() and file_path.suffix.lower() in image_extensions:
            # 获取相对于 res_dir 父目录的路径
            # 如果 res_dir 是 ./res，则相对路径应该是 res/img/xxx.png
            try:
                rel_path = file_path.relative_to(res_path.parent)
                # 使用 POSIX 路径格式（正斜杠）
                image_files.append(str(rel_path).replace('\\', '/'))
            except ValueError:
                # 如果无法计算相对路径，使用从 res 开始的路径
                rel_path = file_path.relative_to(res_path)
                image_files.append('res/' + str(rel_path).replace('\\', '/'))
    
    image_files.sort()
    return image_files


def generate_boot_json(res_dir: str, version: str, output_file: str = 'boot.json'):
    """
    生成 boot.json 文件
    """
    print(f"扫描目录: {res_dir}")
    print(f"游戏版本: {version}")
    
    image_files = find_image_files(res_dir)
    print(f"找到 {len(image_files)} 个图片文件")
    
    if len(image_files) == 0:
        print("警告: 未找到任何图片文件")
    else:
        print(f"示例文件: {image_files[:5]}")
    
    boot_data = {
        "name": "GameOriginalImagePack",
        "version": version,
        "styleFileList": [],
        "scriptFileList": [],
        "tweeFileList": [],
        "imgFileList": image_files,
        "scriptFileList_inject_early": [],
        "scriptFileList_preload": [],
        "additionFile": [],
        "dependenceInfo": [
            {
                "modName": "ModLoader",
                "version": "^2.26.9"
            },
            {
                "modName": "ModLoader ImageLoaderHookCore",
                "version": "^2.18.0"
            }
        ]
    }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(boot_data, f, indent=2, ensure_ascii=False)
    
    print(f"boot.json 已生成: {output_file}")
    
    # 显示部分内容
    print("\n--- boot.json 内容预览 ---")
    print(f"name: {boot_data['name']}")
    print(f"version: {boot_data['version']}")
    print(f"imgFileList 数量: {len(boot_data['imgFileList'])}")
    if boot_data['imgFileList']:
        print(f"前3个文件: {boot_data['imgFileList'][:3]}")
        if len(boot_data['imgFileList']) > 3:
            print(f"后3个文件: {boot_data['imgFileList'][-3:]}")


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)
    
    res_dir = sys.argv[1]
    version = sys.argv[2]
    output_file = sys.argv[3] if len(sys.argv) > 3 else 'boot.json'
    
    generate_boot_json(res_dir, version, output_file)


if __name__ == '__main__':
    main()