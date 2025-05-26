# Midjourney 自動化生成圖片

這個專案用於自動化生成任何類型的圖片，使用 Midjourney 通過 Discord 進行圖片生成。您可以輕鬆替換成自己的數據來生成所需的圖片。

## 功能特點

- 自動登入 Discord
- 自動發送 /imagine 指令
- 自動監控 Midjourney 回應
- 自動下載並保存圖片
- 根據項目編號和名稱建立對應資料夾
- 支持多種數據類型和自定義格式
- 自動檢測已完成任務，避免重複生成
- 智能錯誤處理和重試機制

## 安裝需求

- Python 3.8+
- Chrome 瀏覽器
- Discord 帳號
- Midjourney 訂閱

## 安裝步驟

1. 克隆此專案
2. 安裝依賴包：
   ```bash
   pip install -r requirements.txt
   ```
3. 在專案根目錄創建 .env 文件，並設置以下環境變數：
   ```
   DISCORD_TOKEN=你的Discord令牌
   DISCORD_CHANNEL_ID=目標頻道ID
   DISCORD_EMAIL=你的Discord郵箱
   DISCORD_PASSWORD=你的Discord密碼
   ```

## 如何替換成您自己的圖片數據

### 1. 準備數據文件

在 `data/` 目錄中創建您的 JSON 數據文件，格式如下：

```json
[
  {
    "編號欄位": "1",
    "名稱欄位": "您的項目名稱",
    "prompt": "您的 Midjourney 提示詞..."
  },
  {
    "編號欄位": "2", 
    "名稱欄位": "另一個項目名稱",
    "prompt": "另一個 Midjourney 提示詞..."
  }
]
```

### 2. 修改配置文件

編輯 `config.py` 文件，設置您的數據類型：

```python
# 數據類型配置
DATA_TYPES = {
    "your_type": {  # 替換成您的類型名稱
        "file": "data/your_data.json",  # 您的數據文件路徑
        "number_field": "編號欄位",      # JSON 中的編號欄位名稱
        "name_field": "名稱欄位",        # JSON 中的名稱欄位名稱
        "folder_prefix": "您的前綴"      # 輸出資料夾前綴
    }
}

# 預設數據類型
DEFAULT_TYPE = "your_type"  # 設置為您的類型
```

### 3. 運行程式

```bash
# 使用預設類型生成圖片
python src/main.py

# 或指定特定類型
python src/main.py --type your_type
```

## 數據文件範例

### 基本格式
```json
[
  {
    "項目編號": "001",
    "項目名稱": "範例項目",
    "prompt": "a beautiful landscape, digital art, highly detailed --ar 16:9"
  }
]
```

### 進階格式（支援更多欄位）
```json
[
  {
    "編號": "001",
    "標題": "範例標題",
    "描述": "詳細描述",
    "prompt": "detailed prompt for midjourney --ar 16:9 --v 6",
    "標籤": ["tag1", "tag2"]
  }
]
```

## 輸出結構

程式會自動創建以下結構：
```
output/
├── 您的前綴_001_項目名稱/
│   ├── image_1.png
│   ├── image_2.png
│   ├── image_3.png
│   └── image_4.png
└── 您的前綴_002_另一個項目/
    ├── image_1.png
    └── ...
```

## 注意事項

- 請確保您的 Discord 帳號已經加入目標伺服器
- 請確保您有足夠的 Midjourney 使用額度
- 建議在運行過程中不要手動操作瀏覽器
- 標記為「缺」的 prompt 會自動跳過處理
- 程式會自動檢測已完成的項目，從未完成的地方繼續

## 錯誤處理

如果遇到問題，請檢查：
1. 環境變數是否正確設置
2. 網絡連接是否正常
3. Discord 帳號狀態是否正常
4. Midjourney 是否可用
5. JSON 數據格式是否正確

## 更新日誌

查看 [changelog.md](../changelog.md) 了解最新更新。

## 開發計畫

查看 [開發計畫.md](../開發計畫.md) 了解未來功能計畫。 