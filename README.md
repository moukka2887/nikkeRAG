# NIKKE RAG 文檔系統

將 NIKKE 遊戲劇情 YouTube 影片轉換為結構化 RAG 文檔的自動化系統。

## 項目簡介

本項目處理了 **NIKKE: Goddess of Victory** 遊戲的主線劇情（42章）及特殊活動內容，將日文、韓文遊戲錄屏轉換為結構化的 RAG（Retrieval-Augmented Generation）文檔，供 AI 助手進行劇情查詢和分析。

### 數據來源

本項目的劇情內容來自：
- 📺 **YouTube 遊戲錄屏**：日文版和韓文版的遊戲劇情錄屏
- 📖 **參考資料**：[巴哈姆特 NIKKE 劇情討論串](https://forum.gamer.com.tw/C.php?bsn=36390&snA=8753)
- 🎮 **官方內容**：遊戲內原始對話和劇情

### 已處理內容

✅ **主線劇情**（42章）：
- 第00章-第41章完整劇情
- 雙語言版本（RAG文檔 + 原文記錄）

✅ **特殊活動**：
- RED ASH（一周年活動）
- Old Tales（二周年活動）
- Dorothy 與 Ark 危機
- Queen 攻防戰

✅ **分析文檔**：
- 完整故事時間線
- 角色檔案（按章節）
- 世界觀設定
- 時間流逝分析

### 文檔結構

```
docs/
├── videos/              # 劇情文檔（按章節）
│   ├── NIKKE 第XX章 - RAG文档.md     # AI查詢優化版
│   └── NIKKE 第XX章 - 原文記錄.md    # 完整原始對話
├── characters/          # 角色檔案
├── worldbuilding/       # 世界觀設定
└── *.md                # 時間線分析等
```

## 功能特色

- ✅ 從 YouTube 提取字幕/轉錄文本
- ✅ 獲取帶時間戳的字幕（方便定位內容）
- ✅ 提取影片元數據（標題、時長等）
- ✅ 支持多語言字幕
- ✅ 自動分頁處理長內容

## 快速開始

### 1. 安裝 MCP 服務器

首先確保您已安裝 `uvx`：

```bash
# 方式一：使用 pip
pip install uv

# 方式二：使用官方安裝腳本（推薦）
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows PowerShell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### 2. 配置 Claude Desktop

將以下配置添加到您的 Claude Desktop 配置文件：

**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
**Linux**: `~/.config/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "youtube-transcript": {
      "command": "uvx",
      "args": ["mcp-youtube-transcript"]
    },
    "yt-dlp": {
      "command": "npx",
      "args": ["-y", "@kevinwatt/yt-dlp-mcp"],
      "env": {
        "YTDLP_DOWNLOADS_DIR": "./downloads"
      }
    }
  }
}
```

**配置說明：**
- `YTDLP_DOWNLOADS_DIR`: 下載目錄路徑，可使用相對路徑 `./downloads` 或絕對路徑
- Windows 用戶可能需要使用 Windows 路徑格式，如 `C:\\Users\\YourName\\downloads`
- Linux/WSL 用戶使用 Unix 路徑格式

### 3. 重啟 Claude Desktop

配置完成後重啟 Claude Desktop，您將看到新的 MCP 工具可用。

## 使用方式

### 方式一：自動化腳本（推薦）

使用自動化 Python 腳本，一鍵生成結構化的 Markdown 文檔：

#### 1. 安裝依賴

```bash
pip install -r requirements.txt
```

**requirements.txt 內容：**
```
anthropic>=0.18.0
youtube-transcript-api>=0.6.0
requests>=2.31.0
```

#### 2. 設置 API 金鑰

```bash
# Linux/macOS
export ANTHROPIC_API_KEY='your-api-key-here'

# Windows CMD
set ANTHROPIC_API_KEY=your-api-key-here

# Windows PowerShell
$env:ANTHROPIC_API_KEY='your-api-key-here'
```

#### 3. 運行腳本

```bash
python scripts/process_youtube.py "https://youtu.be/VIDEO_ID"
```

腳本會自動完成：
- ✅ 提取 YouTube 字幕（帶時間戳）
- ✅ 使用 Claude API 分析內容
- ✅ 識別章節、角色、對話
- ✅ 生成結構化的 Markdown 文檔
- ✅ 保存到 `docs/videos/` 目錄

#### 輸出格式

生成的文檔包含：
- 📋 影片元數據（標題、ID、時長、標籤）
- 📖 章節時間軸（場景 + 時間戳）
- 💬 對話記錄（角色 + 台詞 + 時間）
- 🎬 場景描述（發生了什麼事）
- 👤 角色檔案（自動提取）
- 🔍 搜索關鍵詞（便於 RAG 檢索）

生成的文檔可直接作為 Claude Code 項目的參考資料。

---

### 方式二：在 Claude 中手動使用

配置完成後，您可以直接在 Claude 對話中請求：

```
請幫我提取這個 YouTube 影片的字幕：https://www.youtube.com/watch?v=VIDEO_ID
```

Claude 會自動調用 MCP 工具獲取字幕。

### 可用的 MCP 工具

本項目配置了兩個 MCP 服務器，提供不同功能：

**來自 `youtube-transcript` 服務器：**

#### 1. `get_transcript`
獲取影片字幕（純文本）

```
參數：
- url: YouTube 影片網址
- language: 語言代碼（可選，如 'zh', 'en', 'ja', 'ko'）
- cursor: 分頁游標（可選）
```

#### 2. `get_timed_transcript`
獲取帶時間戳的字幕

```
參數：
- url: YouTube 影片網址
- language: 語言代碼（可選）
- cursor: 分頁游標（可選）

輸出格式：
[00:00:15] 第一段文本
[00:00:32] 第二段文本
```

#### 3. `get_video_info`
獲取影片元數據

```
參數：
- url: YouTube 影片網址

輸出：標題、作者、時長、描述等信息
```

**來自 `yt-dlp` 服務器：**

提供更強大的視頻下載和元數據提取功能，可繞過部分 IP 封鎖問題。具體工具請參考 [@kevinwatt/yt-dlp-mcp](https://github.com/kevinwatt/yt-dlp-mcp) 文檔。

## 輸出格式建議

### Markdown 格式（推薦）

```markdown
# 影片標題

**來源**: [YouTube 連結](https://youtube.com/...)
**時長**: XX:XX
**日期**: YYYY-MM-DD

## 摘要
[影片摘要]

## 完整內容

### 段落1 標題
[00:00:00] 內容...

### 段落2 標題
[00:05:30] 內容...
```

### 純文本格式

適合直接作為 AI 參考資料，移除時間戳和格式化。

## 使用場景

### 1. 學習筆記整理

```
請提取這個教程影片的字幕，並整理成結構化的學習筆記
```

### 2. 內容摘要

```
請獲取這個影片的字幕，並生成 3-5 點的重點摘要
```

### 3. 引用定位

```
請獲取帶時間戳的字幕，我需要引用特定段落
```

### 4. AI 助手上下文

```
請提取這個技術講座的內容，我後續會基於這些內容提問
```

## 注意事項

- 需要影片有可用的字幕（自動生成或上傳者提供）
- 長影片會自動分頁（超過 50,000 字符）
- 支持多語言字幕，可指定語言代碼
- 私人影片或受限影片無法提取

## 進階配置

### 自定義分頁大小

可以在配置中添加 `--response-limit` 參數：

```json
{
  "mcpServers": {
    "youtube-transcript": {
      "command": "uvx",
      "args": ["mcp-youtube-transcript", "--response-limit", "100000"]
    }
  }
}
```

### Docker 部署

```bash
docker run -p 3000:3000 ghcr.io/jkawamoto/mcp-youtube-transcript
```

## 疑難排解

### 使用 MCP 提取字幕遇到問題

**IP 封鎖問題**
- YouTube 有爬蟲協議限制，頻繁請求可能導致 IP 被暫時封鎖
- 建議：使用 `yt-dlp` MCP 服務器替代，更穩定可靠
- 或者：適當控制請求頻率，避免短時間內大量請求

**YouTube 爬蟲協議限制**
- 部分地區或網絡環境可能無法正常訪問 YouTube API
- 某些影片可能有地區限制或版權保護
- 建議：使用 VPN 或代理服務器，或直接使用 `yt-dlp` 下載字幕文件

### 字幕被截斷
- 使用 `cursor` 參數獲取後續內容
- 或增加 `response-limit` 設置（見「進階配置」部分）
- 示例：`get_transcript(url, cursor="next_page_token")`
- 長視頻（超過50,000字符）會自動分頁，需要多次調用獲取完整內容

## 數據來源聲明

### 劇情內容來源

本項目的 NIKKE 劇情內容來自以下公開資源：

1. **YouTube 遊戲錄屏**
   - 日文版遊戲劇情錄屏
   - 韓文版遊戲劇情錄屏
   - 所有影片均為公開可訪問的內容

2. **社群參考資料**
   - [巴哈姆特 NIKKE 哈拉板劇情討論串](https://forum.gamer.com.tw/C.php?bsn=36390&snA=8753)
   - 玩家社群的劇情整理和討論

3. **內容處理**
   - 使用 MCP YouTube Transcript 工具提取字幕
   - 使用 Claude AI 進行劇情分析和結構化
   - 生成 RAG 優化格式供 AI 查詢使用

### 版權聲明

- 遊戲內容版權歸 SHIFT UP Corporation 所有
- 本項目僅用於學習和非商業用途
- 不提供遊戲資源的下載或分發
- 僅整理公開可訪問的劇情文本內容

## 資源連結

- [YouTube Transcript MCP](https://github.com/jkawamoto/mcp-youtube-transcript)
- [MCP 協議說明](https://modelcontextprotocol.io/)
- [NIKKE 官方網站](https://nikke-kr.com/)
- [巴哈姆特 NIKKE 討論區](https://forum.gamer.com.tw/B.php?bsn=36390)

## 授權

本項目代碼使用 MIT 授權。
遊戲內容版權歸 SHIFT UP Corporation 所有。
