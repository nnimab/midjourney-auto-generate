# Midjourney 自動產生圖片工具

這是一個自動化工具集，用於生成各種類型的圖片。主要使用 Midjourney 通過 Discord 進行圖片生成。您可以輕鬆替換成自己的數據來生成所需的圖片。

## 專案結構

```
├── midjourney-automation/           # 主要自動化程式目錄
│   ├── data/                       # 數據文件目錄
│   │   ├── character_cards.json    # 人物卡數據
│   │   ├── character_cards copy.json
│   │   ├── hexagrams.json          # 易經卦象數據
│   │   ├── hexagrams copy.json
│   │   ├── timespace_cards.json    # 時空卡數據
│   │   └── timespace_cards copy.json
│   ├── output/                     # 生成圖片輸出目錄
│   ├── output_temp/                # 臨時輸出目錄
│   ├── src/                        # 源代碼目錄
│   ├── 舊圖片/                     # 舊圖片備份
│   ├── .env                        # 環境變數配置（需自行創建）
│   ├── config.py                   # 配置文件
│   ├── README.md                   # 詳細使用說明
│   └── requirements.txt            # Python 依賴包
├── 易經卡.json                     # 範例：易經卦象數據
├── 人物卡.json                     # 範例：人物卡數據
├── 時空卡.json                     # 範例：時空卡數據
├── 22人物卡.pdf                    # 範例：人物卡參考文件
└── README.md                       # 本文件
```

## 主要功能

- 🤖 自動化 Discord 登入和操作
- 🎨 自動發送 Midjourney `/imagine` 指令
- 📥 自動監控和下載生成的圖片
- 📁 智能文件夾管理和圖片分類
- 🔄 支持多種數據類型和自定義格式
- ⚡ 批量處理和錯誤恢復
- 🎯 自動檢測已完成任務，避免重複生成

## 快速開始

1. **克隆專案**
   ```bash
   git clone https://github.com/nnimab/midjourney-auto-generate.git
   cd midjourney-auto-generate
   ```

2. **進入主程式目錄**
   ```bash
   cd midjourney-automation
   ```

3. **安裝依賴**
   ```bash
   pip install -r requirements.txt
   ```

4. **設置環境變數**
   在 `midjourney-automation` 目錄中創建 `.env` 文件：
   ```env
   DISCORD_TOKEN=你的Discord令牌
   DISCORD_CHANNEL_ID=目標頻道ID
   DISCORD_EMAIL=你的Discord郵箱
   DISCORD_PASSWORD=你的Discord密碼
   ```

5. **準備您的數據**
   - 在 `data/` 目錄中創建或修改您的 JSON 數據文件
   - 修改 `config.py` 設置您的數據類型
   - 詳細說明請參考 [midjourney-automation/README.md](midjourney-automation/README.md)

6. **運行程式**
   ```bash
   # 使用預設類型生成圖片
   python src/main.py
   
   # 或指定特定類型
   python src/main.py --type your_type
   ```

## 如何替換成您的數據

### JSON 數據格式範例
```json
[
  {
    "編號": "001",
    "名稱": "您的項目名稱", 
    "prompt": "您的 Midjourney 提示詞 --ar 16:9"
  }
]
```

### 配置步驟
1. 在 `midjourney-automation/data/` 目錄中創建您的 JSON 數據文件
2. 修改 `midjourney-automation/config.py` 中的數據類型設置
3. 運行程式開始生成圖片

詳細配置說明請查看 [midjourney-automation/README.md](midjourney-automation/README.md)

## 輸出結構

生成的圖片會保存在 `midjourney-automation/output/` 目錄中：
```
midjourney-automation/output/
├── 前綴_001_項目名稱/
│   ├── image_1.png
│   ├── image_2.png
│   ├── image_3.png
│   └── image_4.png
└── 前綴_002_另一個項目/
    ├── image_1.png
    └── ...
```

## 詳細文檔

更多詳細信息請查看：
- [midjourney-automation/README.md](midjourney-automation/README.md) - 詳細使用說明和配置

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
- 所有生成的圖片會保存在 `midjourney-automation/output/` 目錄中

## 授權

本專案僅供學習和個人使用。

## 貢獻

歡迎提交 Issue 和 Pull Request！ 