# 更新日誌

## 2024-12-19 - README 通用化更新

### 修改
- 更新根目錄和 midjourney-automation 目錄的 README.md
- 改為通用格式，不再特定提到 hexagram 和 character
- 新增詳細的「如何替換成您自己的圖片數據」說明
- 提供 JSON 數據格式範例和配置步驟
- 說明輸出結構和文件夾命名規則
- 讓專案更容易被其他用戶理解和使用

## 2024-12-19 - GitHub 推送

### 新增
- 創建 .gitignore 文件，排除私人資訊和不需要的文件
- 新增根目錄 README.md，提供專案概覽和快速開始指南
- 成功推送專案到 GitHub：https://github.com/nnimab/midjourney-auto-generate
- 排除 .env 文件、output 開頭的資料夾、舊圖片等私人資訊
- 設置完整的 Git 版本控制，包含適當的 .gitignore 規則

## 2024-12-19

### 新增
- 創建 .gitignore 文件，排除私人資訊和不需要的文件
- 新增根目錄 README.md，提供專案概覽和快速開始指南
- 成功推送專案到 GitHub：https://github.com/nnimab/midjourney-auto-generate
- 排除 .env 文件、output 開頭的資料夾、舊圖片等私人資訊
- 設置完整的 Git 版本控制，包含適當的 .gitignore 規則

## 2024-12-19

### 新增
- 新增自動檢測已完成任務功能
- 程式現在會自動掃描 output 資料夾，檢測已完成的任務編號
- 支援從未完成的編號開始繼續處理，避免重複生成已完成的圖片
- 新增 `get_last_completed_number()` 方法，可自動識別 hexagram、character、timespace 三種類型的最大完成編號
- 優化任務處理邏輯，顯示將要處理的項目數量和起始編號
- 改善日誌輸出，清楚顯示從哪個編號開始繼續處理

### 優化
- 大幅強化瀏覽器彈窗禁用功能
- 禁用密碼保存提示、自動填充建議、安全性警告等所有干擾性彈窗
- 新增多層次的彈窗禁用機制：Chrome 啟動參數、用戶偏好設置、JavaScript 腳本
- 在登入過程中額外執行彈窗禁用腳本，確保自動化流程不被中斷
- 禁用通知、翻譯提示、同步建議等各種瀏覽器功能
- 提升腳本運行的穩定性和可靠性

## 2023-04-11

### 修復
- 解決多個卡牌共用同一 UUID 的嚴重問題
- 添加 scroll_to_bottom 方法，確保總是獲取最新圖片
- 優化 get_midjourney_image_urls 方法，更精確地區分新舊 UUID
- 增加項目處理之間的等待時間，避免任務間相互干擾
- 添加重複項目檢查，防止同一卡牌被重複處理
- 改進頁面滾動策略，確保能獲取完整的預覽圖集

## 2023-04-10

### 修復
- 修復 Midjourney 圖片 URL 順序混亂的問題
- 改進 get_midjourney_image_urls 方法，使用 Discord 預覽圖的原始順序來確定正確的圖片順序
- 更新 _get_current_attachments 方法，保持 DOM 中的圖片順序
- 解決不同卡牌獲取到相同圖片 UUID 的問題
- 增強圖片 URL 獲取過程的日誌記錄
- 添加重試機制，提高圖片獲取的成功率
- 改進 download_all_variations 方法，添加更多檢查確保 UUID 是唯一的

## 2023-03-25

### 新增
- 添加人物卡生成功能
- 創建 character_cards.json 數據文件，支持人物卡數據
- 修改主程序支持選擇數據類型 (卦象或人物卡)
- 更新圖片處理器以支持多種數據類型
- 將人物卡提示詞全部修改為中國風格，增加中式元素及畫風
- 添加時空卡生成功能
- 創建 timespace_cards.json 數據文件，支持時空卡數據

### 修改
- 重構 process_hexagram 方法為 process_item 方法，增加靈活性
- 更新圖片保存邏輯，支持不同類型的命名規則
- 添加命令行參數支持，可以使用 --type 參數選擇處理類型
- 添加 DATA_TYPE 全局變數，只需修改一個參數即可切換生成類型
- 補充完成原先缺少的祭司和孤兒角色提示詞
- 擴展 process_item 和 run 方法，支持時空卡類型
- 將 DATA_TYPE 默認值更改為 "timespace"，以生成時空卡圖片

## 2023-02-11

### 新增
- 初始項目創建
- 自動生成易經卦象圖片功能
- Discord 自動登入和控制
- Midjourney 圖片生成和下載