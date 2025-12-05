import requests
from . import config


def get_html_channel_info(game_id, password=None):
    """
    获取HTML channel的上传信息，包括upload_id、build_id和版本号。
    通过查找channel_name为"html"的记录获取所需信息。
    
    返回: (upload_id, build_id, version) 或 (None, None, None) 如果失败
    """
    print("  - 正在请求上传列表...")
    
    url = config.UPLOADS_URL_TEMPLATE.format(game_id=game_id)
    params = {}
    if password:
        params['password'] = password

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        if "uploads" not in data or len(data["uploads"]) == 0:
            print("  - 错误: 未找到任何上传记录。")
            return None, None, None

        # 查找channel_name为"html"的记录
        html_upload = None
        for upload in data["uploads"]:
            if upload.get("channel_name") == "html":
                html_upload = upload
                break
        
        if not html_upload:
            print("  - 错误: 未找到channel_name为'html'的上传记录。")
            return None, None, None

        # 获取upload_id
        upload_id = html_upload.get("id")
        if not upload_id:
            print("  - 错误: 上传记录中缺少 'id'。")
            return None, None, None
        
        # 获取build_id
        build_info = html_upload.get("build")
        if not build_info:
            print("  - 错误: 上传记录中缺少 'build' 信息。")
            return None, None, None
        
        build_id = build_info.get("id")
        if not build_id:
            print("  - 错误: build信息中缺少 'id'。")
            return None, None, None
        
        # 获取版本号 (user_version)
        version = build_info.get("user_version")
        if not version:
            print("  - 警告: build信息中缺少 'user_version'，使用build version作为后备。")
            version = str(build_info.get("version", "unknown"))
        
        print(f"  - 成功获取 Upload ID: {upload_id}")
        print(f"  - 成功获取 Build ID: {build_id}")
        print(f"  - 成功获取版本号: {version}")

        return upload_id, build_id, version

    except requests.exceptions.RequestException as e:
        print(f"  - 错误: API请求失败: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"  - 响应内容: {e.response.text}")
        return None, None, None


def build_html_url(upload_id, build_id):
    """
    根据upload_id和build_id构建HTML访问URL。
    """
    return config.HTML_URL_TEMPLATE.format(upload_id=upload_id, build_id=build_id)