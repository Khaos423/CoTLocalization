#!/usr/bin/env python3
"""
生成 GameOriginalImagePack 的 boot.json 文件（适用于 Course of Temptation）

用法:
    python generate_image_pack_boot.py <img_dir> <version> [output_file]

参数:
    img_dir: 包含图片文件的目录路径（工作流中应该是 res）
    version: 游戏版本号
    output_file: 输出的 boot.json 路径 (默认: boot.json)

CoT 的图片路径格式为 res/img/xxx.png
"""

import json
import os
import sys
from pathlib import Path


def find_image_files(base_dir: str) -> list[str]:
    """
    查找目录中的所有图片文件
    返回相对于当前工作目录的路径列表
    
    例如：base_dir="res"，会返回 ["res/img/xxx.png", "res/img/yyy.png", ...]
    """
    image_extensions = {'.png', '.jpg', '.jpeg', '.gif', '.webp'}
    image_files = []
    
    base_path = Path(base_dir)
    if not base_path.exists():
        print(f"错误: 目录不存在: {base_dir}")
        sys.exit(1)
    
    # 遍历目录
    for file_path in base_path.rglob('*'):
        if file_path.is_file() and file_path.suffix.lower() in image_extensions:
            # 使用 POSIX 路径格式（正斜杠），保持从 base_dir 开始的完整路径
            # 例如：res/img/xxx.png
            full_path = str(file_path).replace('\\', '/')
            image_files.append(full_path)
    
    image_files.sort()
    return image_files


def generate_boot_json(base_dir: str, version: str, output_file: str = 'boot.json',
                       include_extras: bool = False):
    """
    生成 boot.json 文件
    
    Args:
        base_dir: 图片基础目录（如 "res"），生成的路径会保持此前缀
        version: 版本号
        output_file: 输出文件路径
        include_extras: 是否包含额外的样式和脚本文件
    """
    print(f"扫描目录: {base_dir}")
    print(f"游戏版本: {version}")
    
    image_files = find_image_files(base_dir)
    print(f"找到 {len(image_files)} 个图片文件")
    
    if len(image_files) == 0:
        print("警告: 未找到任何图片文件")
    else:
        print(f"示例文件: {image_files[:5]}")
    
    # 基础 boot.json 结构
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
    
    # 如果需要包含额外文件（完整版 GameOriginalImagePack）
    if include_extras:
        boot_data["styleFileList"] = ["Roschild.ttf.css"]
        boot_data["scriptFileList_inject_early"] = ["dist/GameOriginalImagePack.js"]
        boot_data["scriptFileList_preload"] = ["dist/preload/preload.js"]
        boot_data["additionFile"] = ["README.md", "Roschild.ttf.base64"]
        boot_data["dependenceInfo"].extend([
            {
                "modName": "ModuleCssReplacer",
                "version": "^1.0.0"
            },
            {
                "modName": "ReplacePatcher",
                "version": "^1.2.1"
            }
        ])
    
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
    print(f"dependenceInfo: {len(boot_data['dependenceInfo'])} 个依赖")


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        print("\n额外参数（可选）:")
        print("  --extras           包含额外的样式和脚本文件（完整版 GameOriginalImagePack）")
        print("  <output_file>      输出文件名（默认: boot.json）")
        print("\n示例:")
        print("  python generate_image_pack_boot.py res 0.7.3 boot.json --extras")
        sys.exit(1)
    
    base_dir = sys.argv[1]
    version = sys.argv[2]
    output_file = 'boot.json'
    include_extras = False
    
    # 解析额外参数
    i = 3
    while i < len(sys.argv):
        if sys.argv[i] == '--extras':
            include_extras = True
            i += 1
        else:
            output_file = sys.argv[i]
            i += 1
    
    generate_boot_json(base_dir, version, output_file, include_extras)


if __name__ == '__main__':
    main()