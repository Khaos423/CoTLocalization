import asyncio
import os
import contextlib
from zipfile import ZipFile, BadZipfile
import httpx
import shutil
from pathlib import Path
from typing import Optional
from src.consts import DIR_ROOT, DIR_TRANS
from src.replacer import Replacer
from src.log import logger

PARATRANZ_BASE_URL = "https://paratranz.cn/api"
DIR_PARATRANZ = DIR_ROOT / "paratranz"
DIR_TEMP_ROOT = DIR_ROOT / "paratranz_tmp"

class ParatranzClient:
    def __init__(self, project_id: int = 11363, mention_name: str = "COT", type_dir: str = "cot", token: Optional[str] = None):
        self._project_id = project_id
        self._mention_name = mention_name
        self._type = type_dir
        self._token = token or os.environ.get("PARATRANZ_TOKEN", "")

    @property
    def headers(self):
        return {"Authorization": f"Bearer {self._token}"} if self._token else {}

    async def download_from_paratranz(self) -> bool:
        os.makedirs(DIR_PARATRANZ, exist_ok=True)
        os.makedirs(DIR_TEMP_ROOT, exist_ok=True)
        with contextlib.suppress(httpx.TimeoutException):
            await self.trigger_export()

        async with httpx.AsyncClient(verify=False) as client:
            flag = False
            for _ in range(3):
                try:
                    await self.download_export(client)
                    await self.unzip_export()
                except (httpx.ConnectError, httpx.TimeoutException, BadZipfile) as e:
                    logger.warning(f"下载/解压失败，重试: {e}")
                    continue
                else:
                    flag = True
                    break
            if not flag:
                logger.error(f"***** 无法正常下载 Paratranz {self._mention_name}汉化包！请检查网络连接情况，以及是否填写了正确的 TOKEN！")
                return False
            return True

    async def trigger_export(self):
        logger.info(f"===== 开始导出{self._mention_name}汉化文件 ...")
        url = f"{PARATRANZ_BASE_URL}/projects/{self._project_id}/artifacts"
        httpx.post(url, headers=self.headers, verify=False)
        logger.info(f"##### {self._mention_name}汉化文件已导出 !")

    async def download_export(self, client: httpx.AsyncClient):
        logger.info(f"===== 开始下载{self._mention_name}汉化文件 ...")
        url = f"{PARATRANZ_BASE_URL}/projects/{self._project_id}/artifacts/download"
        content = (await client.get(url, headers=self.headers, follow_redirects=True)).content
        zip_path = DIR_TEMP_ROOT / f"paratranz_export{self._mention_name}.zip"
        with open(zip_path, "wb") as fp:
            fp.write(content)
        logger.info(f"##### {self._mention_name}汉化文件已下载 !")

    async def unzip_export(self):
        logger.info(f"===== 开始解压{self._mention_name}汉化文件 ...")
        zip_path = DIR_TEMP_ROOT / f"paratranz_export{self._mention_name}.zip"
        with ZipFile(zip_path) as zfp:
            zfp.extractall(DIR_PARATRANZ / self._type)
        logger.info(f"##### {self._mention_name}汉化文件已解压 !")

def sync_to_trans(version: str, type_dir: str = "cot") -> Path:
    src_dir = DIR_PARATRANZ / type_dir / "utf8" / version
    if not src_dir.exists():
        raise FileNotFoundError(f"未找到解压目录: {src_dir}")
    dest_dir = DIR_TRANS / version
    if dest_dir.exists():
        shutil.rmtree(dest_dir)
    shutil.copytree(src_dir, dest_dir)
    logger.info(f"已将 Paratranz 导出同步到 trans: {dest_dir}")
    return dest_dir

def detect_version(type_dir: str = "cot") -> str:
    base = DIR_PARATRANZ / type_dir / "utf8"
    if not base.exists():
        raise FileNotFoundError(f"未找到目录: {base}")
    candidates = [p for p in base.iterdir() if p.is_dir()]
    if not candidates:
        raise FileNotFoundError(f"未在 {base} 下找到版本目录")
    # 选择最近修改的版本目录
    candidates.sort(key=lambda p: p.stat().st_mtime, reverse=True)
    version = candidates[0].name
    logger.info(f"检测到版本: {version}")
    return version
async def run_workflow() -> int:
    token = os.environ.get("PARATRANZ_TOKEN", "")
    if not token:
        logger.error("未提供 PARATRANZ_TOKEN，请在环境变量中设置。")
        return 1

    client = ParatranzClient(project_id=11363, mention_name="COT", type_dir="cot", token=token)
    ok = await client.download_from_paratranz()
    if not ok:
        return 1

    version = detect_version("cot")
    sync_to_trans(version, "cot")

    replacer = Replacer(version)
    os.makedirs(replacer.translatedPath, exist_ok=True)
    replacer.convert_to_i18n()
    logger.info(f"已生成 i18n.json for {version}")
    return 0

def main():
    exit_code = asyncio.run(run_workflow())
    raise SystemExit(exit_code)

if __name__ == "__main__":
    main()