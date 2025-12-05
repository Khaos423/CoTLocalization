#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.parseTweev2 import TweeParserV2

def test_container_macro():
    """测试容器宏的识别和提取功能"""
    
    # 在这里放置您的测试用例
    with open("text.twee", "r", encoding="utf-8") as f:
        test_content = f.read()
    print("=== 容器宏测试 ===")
    parser = TweeParserV2()
    parser.parse(test_content)

    import json
    with open("test_macro_output.json", "w", encoding="utf-8") as f:
        json.dump(parser.extracted_texts, f, ensure_ascii=False, indent=4)
    # for item in parser.extracted_texts:
    #     print(f"类型: {item['type']}")
    #     print(f"文本: {item['text']}")
    #     print(f"位置: {item['position']}")
    #     print("---")
    pzdata = []

    for i in range(len(parser.extracted_texts)):
        if parser.extracted_texts[i]['type'] == 'passage_name':continue
        d = parser.extracted_texts[i]
        pzdata.append({
            "key":d['id'],
            "original":d['text'],
            "context":d['context'],
            "position":d['position']
        })
    with open("test_macro_output_pz.json", "w", encoding="utf-8") as f:
        json.dump(pzdata, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    test_container_macro()