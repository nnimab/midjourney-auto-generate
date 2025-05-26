# Midjourney 自動化生成圖片

這個專案用於自動化生成易經卦象和人物卡的圖片，使用 Midjourney 通過 Discord 進行圖片生成。

## 功能特點

- 自動登入 Discord
- 自動發送 /imagine 指令
- 自動監控 Midjourney 回應
- 自動下載並保存圖片
- 根據卦象/卡牌編號和名稱建立對應資料夾
- 支持多種數據類型 (卦象、人物卡)

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

## 使用方法

1. 確保 data 目錄中有正確格式的 JSON 文件
2. 運行主程序：

   ```bash
   # 生成卦象圖片 (預設)
   python src/main.py
   
   # 或指定生成卦象圖片
   python src/main.py --type hexagram
   
   # 生成人物卡圖片
   python src/main.py --type character
   ```

### 數據文件格式

1. 卦象數據 (hexagrams.json):
   ```json
   [
     {
       "卦象編號": "1",
       "卦象名稱": "乾卦（天）",
       "prompt": "圖片生成提示..."
     }
   ]
   ```

2. 人物卡數據 (character_cards.json):
   ```json
   [
     {
       "卡牌編號": "1",
       "卡牌名稱": "國王",
       "prompt": "圖片生成提示..."
     }
   ]
   ```

## 注意事項

- 請確保您的 Discord 帳號已經加入目標伺服器
- 請確保您有足夠的 Midjourney 使用額度
- 建議在運行過程中不要手動操作瀏覽器
- 標記為「缺」的 prompt 會自動跳過處理

## 錯誤處理

如果遇到問題，請檢查：
1. 環境變數是否正確設置
2. 網絡連接是否正常
3. Discord 帳號狀態是否正常
4. Midjourney 是否可用

## 更新日誌

查看 [changelog.md](../changelog.md) 了解最新更新。

## 開發計畫

查看 [開發計畫.md](../開發計畫.md) 了解未來功能計畫。 