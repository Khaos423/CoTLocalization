import os

# --- API and Game Config ---
# API_KEY可以通过环境变量ITCH_API_KEY设置，或使用默认值
API_KEY = os.environ.get("ITCH_API_KEY", "")

STABLE_GAME_ID = "2151565"
EARLY_ACCESS_GAME_ID = "2499529"

# --- Paths and Directories ---
# 使用绝对路径以避免歧义
DESTINATION_DIR = r"D:\Game\CourseOfTemptation_desktop_v0.5.2d"
# 将临时文件放在项目结构中，便于管理
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
TEMP_DIR = os.path.join(BASE_DIR, "temp_update_files")
TEMP_HTML_PATH = os.path.join(TEMP_DIR, "index.html")
SOURCE_DIR = os.path.join(BASE_DIR, "source")
FETCH_DIR = os.path.join(BASE_DIR, "fetch")

# --- File Names ---
VERSION_UPDATE_SCRIPT_PATH = os.path.join(BASE_DIR, "versionUpdate.py")
# 优先使用仓库中的story-export.js，如果不存在则使用本地目标目录中的
STORY_EXPORT_JS_PATH_REPO = os.path.join(BASE_DIR, "story-export.js")
STORY_EXPORT_JS_PATH_LOCAL = os.path.join(DESTINATION_DIR, "story-export.js")
STORY_EXPORT_JS_PATH = STORY_EXPORT_JS_PATH_REPO if os.path.exists(STORY_EXPORT_JS_PATH_REPO) else STORY_EXPORT_JS_PATH_LOCAL
FINAL_EXPORT_ZIP_NAME = "story_export.zip"
# Selenium默认会将文件下载到项目根目录
FINAL_EXPORT_ZIP_PATH = os.path.join(BASE_DIR, FINAL_EXPORT_ZIP_NAME)

# --- API Endpoints ---
# 获取游戏上传列表的API - 使用Header认证
UPLOADS_URL_TEMPLATE = "https://api.itch.io/games/{game_id}/uploads"
# 直接访问HTML的URL模板 - 使用upload_id和build_id
HTML_URL_TEMPLATE = "https://html-classic.itch.zone/html/{upload_id}-{build_id}/index.html"

# --- Selenium Config ---
BROWSER_DOWNLOAD_DIR = BASE_DIR # Selenium将下载到此目录
BROWSER_TIMEOUT = 60 # 秒