/**
 * 修改 ModI18N 的 boot.json 中的版本信息
 *
 * 用法: node change_mod_version.js <boot.json路径> <chinese_version> <game_version>
 * 例如: node change_mod_version.js ModLoader/mod/i18n/boot.json auto-nightly 0.5.2.6
 */

const fs = require('fs');
const path = require('path');

/**
 * 将版本号格式化为带连字符的格式
 * 例如: 0.7.4c -> 0.7.4-c, 0.5.5.8 -> 0.5.5.8
 */
function formatVersionWithHyphen(version) {
    // 匹配版本号末尾的字母后缀（如 0.7.4c 中的 c）
    const match = version.match(/^([\d.]+)([a-zA-Z]+)$/);
    if (match) {
        return `${match[1]}-${match[2]}`;
    }
    return version;
}

function main() {
    // 检查参数
    if (process.argv.length < 5) {
        console.error('错误: 缺少必要参数');
        console.error('用法: node change_mod_version.js <boot.json路径> <chinese_version> <game_version>');
        console.error('例如: node change_mod_version.js ModLoader/mod/i18n/boot.json auto-nightly 0.5.2.6');
        process.exit(1);
    }

    const bootJsonPath = process.argv[2];
    const chineseVersion = process.argv[3];
    const gameVersion = process.argv[4];

    console.log(`Boot.json 路径: ${bootJsonPath}`);
    console.log(`Chinese 版本: ${chineseVersion}`);
    console.log(`游戏版本: ${gameVersion}`);

    // 检查文件是否存在
    if (!fs.existsSync(bootJsonPath)) {
        console.error(`错误: 文件不存在: ${bootJsonPath}`);
        process.exit(1);
    }

    try {
        // 读取 boot.json
        const content = fs.readFileSync(bootJsonPath, 'utf-8');
        const bootJson = JSON.parse(content);

        // 修改版本信息
        // 格式: v{gameVersion} (不再包含 chs-xxx 后缀)
        const newVersion = `v${gameVersion}`;
        
        if (bootJson.version) {
            console.log(`原版本: ${bootJson.version}`);
            bootJson.version = newVersion;
            console.log(`新版本: ${bootJson.version}`);
        } else {
            console.error('警告: boot.json 中未找到 version 字段');
            bootJson.version = newVersion;
            console.log(`已添加 version 字段: ${bootJson.version}`);
        }

        // 更新 dependenceInfo 中 GameVersion 的版本
        if (bootJson.dependenceInfo && Array.isArray(bootJson.dependenceInfo)) {
            const gameVersionDep = bootJson.dependenceInfo.find(dep => dep.modName === 'GameVersion');
            if (gameVersionDep) {
                console.log(`原 GameVersion 依赖版本: ${gameVersionDep.version}`);
                // 将版本号格式化为带连字符的格式 (如 0.7.4c -> 0.7.4-c)
                const formattedVersion = formatVersionWithHyphen(gameVersion);
                gameVersionDep.version = `=${formattedVersion}`;
                console.log(`新 GameVersion 依赖版本: ${gameVersionDep.version}`);
            } else {
                console.log('警告: dependenceInfo 中未找到 GameVersion 依赖');
            }
        }

        // 更新 imgFileList
        console.log(`原 imgFileList: ${JSON.stringify(bootJson.imgFileList)}`);
        bootJson.imgFileList = [
            "res/img/map_univ_big.png",
            "res/img/map_town_big.png"
        ];
        console.log(`新 imgFileList: ${JSON.stringify(bootJson.imgFileList)}`);

        // 写回文件
        fs.writeFileSync(bootJsonPath, JSON.stringify(bootJson, null, 2), 'utf-8');
        console.log(`✓ 已成功更新 ${bootJsonPath}`);

    } catch (error) {
        console.error(`错误: 处理文件时发生错误: ${error.message}`);
        process.exit(1);
    }
}

main();