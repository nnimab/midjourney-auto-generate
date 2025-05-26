import os
from dotenv import load_dotenv

# 載入環境變數
load_dotenv()

# Discord 設置
DISCORD_EMAIL = os.getenv('DISCORD_EMAIL')
DISCORD_PASSWORD = os.getenv('DISCORD_PASSWORD')
DISCORD_CHANNEL_ID = os.getenv('DISCORD_CHANNEL_ID')

# 檔案路徑設置
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
OUTPUT_DIR = os.path.join(BASE_DIR, 'output')

# Selenium 設置
DISCORD_URL = 'https://discord.com/login'
# 處理包含伺服器 ID 和頻道 ID 的格式
CHANNEL_URL = f'https://discord.com/channels/{DISCORD_CHANNEL_ID}'

# 等待時間設置（秒）
WAIT_TIME = 30  # 頁面加載等待時間
IMAGE_WAIT_TIME = 120  # 圖片生成等待時間
UPSCALE_WAIT_TIME = 180  # 放大圖片等待時間

# 創建必要的目錄
os.makedirs(OUTPUT_DIR, exist_ok=True) 