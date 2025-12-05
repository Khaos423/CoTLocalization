// 引入JSZip库
let script = document.createElement('script');
script.src = 'https://cdnjs.cloudflare.com/ajax/libs/jszip/3.7.1/jszip.min.js';
document.head.appendChild(script);
function addBOM(content) {
    return '\ufeff' + content;
}

script.onload = function() {
    console.log("[Step] JSZip library loaded successfully.");
    let zip = new JSZip();

    // 处理脚本
    console.log("[Step] Processing scripts...");
    let scriptContent = SugarCube.Story.getAllScript()[0].text;
    let jsFolder = zip.folder("js");
    let jsFiles = scriptContent.split(/\/\* twine-user-script #\d+: \"(.+?)\" \*\//).slice(1);
    for (let i = 0; i < jsFiles.length; i += 2) {
        let fileName = jsFiles[i];
        let content = jsFiles[i + 1].trim();
        jsFolder.file(fileName, addBOM(content));
    }
    console.log("[Step] Scripts processed.");

    // 处理样式表
    console.log("[Step] Processing stylesheets...");
    let stylesheetContent = SugarCube.Story.getAllStylesheet()[0].text;
    let cssFolder = zip.folder("css");
    let cssFiles = stylesheetContent.split(/\/\* twine-user-stylesheet #\d+: \"(.+?)\" \*\//).slice(1);
    for (let i = 0; i < cssFiles.length; i += 2) {
        let fileName = cssFiles[i];
        let content = cssFiles[i + 1].trim();
        cssFolder.file(fileName, content);
    }
    console.log("[Step] Stylesheets processed.");

    // 导出所有常规段落
    console.log("[Step] Exporting passages...");
    let passages = SugarCube.Story.getAllRegular();
    let passageFolder = zip.folder("Passages");
    for (let name in passages) {
        let content = `:: ${name}\n${passages[name].text}`;
        passageFolder.file(`${name}.twee`, content);
    }
    console.log("[Step] Passages exported.");

    // 导出所有小部件
    console.log("[Step] Exporting widgets...");
    let widgets = SugarCube.Story.getAllWidget();
    let widgetFolder = zip.folder("Widgets");
    widgets.forEach(widget => {
        let content = `:: ${widget.title} [widget]\n${widget.text}`;
        widgetFolder.file(`${widget.title}.twee`, content);
    });
    console.log("[Step] Widgets exported.");

    // 生成并下载ZIP文件
    console.log("[Step] Generating zip file...");
    zip.generateAsync({ type: "blob" }).then(function(content) {
        console.log("[Step] Zip file generated.");
        let url = URL.createObjectURL(content);
        let a = document.createElement('a');
        a.href = url;
        a.download = 'story_export.zip';
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
        console.log("[Step] Download initiated.");
    });
};

script.onerror = function() {
    console.error("[Error] Failed to load JSZip library.");
};