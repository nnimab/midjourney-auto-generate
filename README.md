# Midjourney 自動產生圖片工具

這是一個自動化工具集，用於生成各種類型的圖片，包括易經卦象、人物卡等。主要使用 Midjourney 通過 Discord 進行圖片生成。

## 專案結構

```
├── midjourney-automation/     # 主要自動化程式
├── 易經卡.json               # 易經卦象數據
├── 人物卡.json               # 人物卡數據
├── 時空卡.json               # 時空卡數據
├── 22人物卡.pdf              # 人物卡參考文件
├── changelog.md              # 更新日誌
├── 開發計畫.md               # 開發計畫
└── README.md                 # 本文件
```

## 主要功能

- 🤖 自動化 Discord 登入和操作
- 🎨 自動發送 Midjourney `/imagine` 指令
- 📥 自動監控和下載生成的圖片
- 📁 智能文件夾管理和圖片分類
- 🔄 支持多種數據類型（卦象、人物卡、時空卡）
- ⚡ 批量處理和錯誤恢復

## 快速開始

1. **克隆專案**
   ```bash
   git clone https://github.com/nnimab/midjourney-auto-generate.git
   cd midjourney-auto-generate
   ```

2. **安裝依賴**
   ```bash
   cd midjourney-automation
   pip install -r requirements.txt
   ```

3. **設置環境變數**
   在 `midjourney-automation` 目錄中創建 `.env` 文件：
   ```env
   DISCORD_TOKEN=你的Discord令牌
   DISCORD_CHANNEL_ID=目標頻道ID
   DISCORD_EMAIL=你的Discord郵箱
   DISCORD_PASSWORD=你的Discord密碼
   ```

4. **運行程式**
   ```bash
   # 生成卦象圖片
   python src/main.py --type hexagram
   
   # 生成人物卡圖片
   python src/main.py --type character
   ```

## 詳細文檔

更多詳細信息請查看：
- [midjourney-automation/README.md](midjourney-automation/README.md) - 詳細使用說明
- [changelog.md](changelog.md) - 更新日誌
- [開發計畫.md](開發計畫.md) - 開發計畫

## 系統需求

- Python 3.8+
- Chrome 瀏覽器
- Discord 帳號
- Midjourney 訂閱

## 注意事項

- 請確保您的 Discord 帳號已加入目標伺服器
- 請確保有足夠的 Midjourney 使用額度
- 運行時請勿手動操作瀏覽器
- 私人資訊（如 `.env` 文件）已被 `.gitignore` 排除

## 授權

本專案僅供學習和個人使用。

## 貢獻

歡迎提交 Issue 和 Pull Request！ 