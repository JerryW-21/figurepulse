# FigurePulse — 人物动态脉搏

> 追踪关键人物的24小时动态。已覆盖埃隆·马斯克。未来将扩展更多科技/金融人物。
> *Track key figures' 24H activities. Currently covering Elon Musk. More figures coming.*

[🌐 在线访问 Live Site](https://468023a4c812420da1305300684b580e.app.codebuddy.work)

---

## 功能 Features

- **24H 动态追踪** — X平台推文、公司动态、市场影响，一站式汇总
- **数据驱动渲染** — DATA 对象在 HTML 中，自动化脚本每日注入最新数据
- **PWA 支持** — 可安装到手机桌面，离线可用
- **Android APK** — 原生 WebView 壳，Android Studio 一键打包
- **中国投资者视角** — A股联动分析、QDII 持仓参考、红涨绿跌
- **多人物架构** — 当前追踪马斯克，DATA.figures 支持未来扩展

## 项目结构 Project Structure

```
figurepulse/
├── index.html          # PWA 主程序（数据驱动）
├── manifest.json       # PWA 配置
├── sw.js               # Service Worker（离线+推送）
├── icons/              # App 图标
├── android/            # Android 原生壳（Gradle 项目）
├── build-android.bat   # Windows 一键构建
├── build-android.sh    # macOS/Linux 构建脚本
├── run-tracker.py      # 独立搜索脚本（WorkBuddy/Cursor 通用）
├── .cursorrules        # Cursor AI 配置
└── README.md
```

## 快速开始 Quick Start

### 方式 1：浏览器直接访问
打开 [在线地址](https://468023a4c812420da1305300684b580e.app.codebuddy.work)

### 方式 2：PWA 安装到手机
1. 用手机 Chrome 打开上述链接
2. 菜单 → 「添加到主屏幕」
3. 像原生 App 一样使用

### 方式 3：Android APK
```bash
# 用 Android Studio 打开 android/ 目录
# Build → Build APK
# 或运行：
./build-android.sh   # macOS/Linux
build-android.bat     # Windows
```

## 在 AI 助手中运行 Run with AI Assistants

### WorkBuddy（腾讯 CodeBuddy）
已内置 `musk-24h-tracker` Skill，自动每日 8:00 触发。

### Cursor / Codex
```bash
# 独立运行
python run-tracker.py

# 或让 Cursor 执行
# 将 .cursorrules 放入项目根目录，然后告诉 Cursor：
# "Run the musk tracker update"
```

---

## 扩展更多人物 Add New Figures

在 `index.html` 的 `DATA.figures` 数组中添加：

```javascript
{ id: 'jensen-huang', name: '黄仁勋', nameEn: 'Jensen Huang', role: 'NVIDIA CEO', active: true }
```

然后在 `DATA.content` 中添加对应内容即可。

---

## 技术栈 Tech Stack

- **前端**: 纯 HTML/CSS/JS（零依赖）
- **离线**: Service Worker + Cache API
- **移动端**: PWA Manifest + WebView APK
- **自动化**: WorkBuddy 定时任务 + Python 脚本
- **部署**: CloudStudio / GitHub Pages

---

## License

MIT — 自由使用、修改、分发。
