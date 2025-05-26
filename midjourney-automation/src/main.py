import json
import logging
import os
import time
import sys
import re
from pathlib import Path

# 添加父目錄到 Python 路徑
sys.path.append(str(Path(__file__).parent.parent))

from src.selenium_handler import create_selenium_handler
from src.discord_client import create_discord_handler
from src.image_processor import create_image_processor
from config import DATA_DIR, IMAGE_WAIT_TIME, UPSCALE_WAIT_TIME, OUTPUT_DIR

# 設置日誌
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 設置數據類型：改變這個變數來切換生成的圖片類型
# "hexagram" - 生成卦象圖片
# "character" - 生成人物卡圖片
# "timespace" - 生成時空卡圖片
DATA_TYPE = "hexagram"

class MidjourneyAutomation:
    def __init__(self):
        self.selenium_handler = create_selenium_handler()
        self.discord_handler = create_discord_handler(self.selenium_handler)
        self.image_processor = create_image_processor()
        # 設置selenium_handler
        self.image_processor.set_selenium_handler(self.selenium_handler)
        
    def get_last_completed_number(self, data_type):
        """
        掃描output資料夾，找出指定類型的最大完成編號
        
        Args:
            data_type (str): 數據類型 ("hexagram", "character", "timespace")
            
        Returns:
            int: 最大完成編號，如果沒有找到則返回0
        """
        try:
            if not os.path.exists(OUTPUT_DIR):
                logger.info(f"Output資料夾不存在: {OUTPUT_DIR}")
                return 0
            
            max_number = 0
            pattern = rf"{data_type}_(\d+)_.*"
            
            # 掃描output資料夾中的所有子資料夾
            for folder_name in os.listdir(OUTPUT_DIR):
                folder_path = os.path.join(OUTPUT_DIR, folder_name)
                if os.path.isdir(folder_path):
                    match = re.match(pattern, folder_name)
                    if match:
                        number = int(match.group(1))
                        max_number = max(max_number, number)
            
            logger.info(f"找到 {data_type} 類型的最大完成編號: {max_number}")
            return max_number
            
        except Exception as e:
            logger.error(f"掃描已完成任務時發生錯誤: {str(e)}")
            return 0
        
    def process_item(self, item_data, item_type="hexagram"):
        """處理單個項目（卦象、人物卡或時空卡）"""
        try:
            if item_type == "hexagram":
                item_id = item_data['卦象編號']
                item_name = item_data['卦象名稱']
                logger.info(f"開始處理卦象: {item_id} - {item_name}")
            elif item_type == "character":
                item_id = item_data['卡牌編號']
                item_name = item_data['卡牌名稱']
                logger.info(f"開始處理人物卡: {item_id} - {item_name}")
            elif item_type == "timespace":
                item_id = item_data['卡牌編號']
                item_name = item_data['卡牌名稱']
                logger.info(f"開始處理時空卡: {item_id} - {item_name}")
            else:
                logger.error(f"未知的項目類型: {item_type}")
                return False
                
            # 檢查是否缺少 prompt
            if item_data.get('prompt') == "缺":
                logger.warning(f"{item_type} {item_id} 缺少 prompt，跳過處理")
                return True
                
            # 發送 imagine 指令
            if not self.discord_handler.send_imagine_command(item_data['prompt']):
                logger.error('發送 imagine 指令失敗')
                return False
                
            # 等待並獲取圖片URLs，加入重試機制
            logger.info('等待圖片生成並獲取URLs...')
            max_retries = 3
            image_urls = None
            
            for retry in range(max_retries):
                image_urls = self.selenium_handler.get_midjourney_image_urls(timeout=120)
                if image_urls:
                    break
                else:
                    logger.warning(f'第 {retry+1} 次獲取圖片URLs失敗，{retry+1 < max_retries and "重試中..." or "已達最大重試次數"}')
                    time.sleep(5)  # 短暫等待後重試
            
            if not image_urls:
                logger.error('多次獲取圖片URLs均失敗')
                return False
                
            # 記錄獲取到的URLs
            logger.info(f'成功獲取 {len(image_urls)} 個圖片URLs')
            
            # 為當前項目添加類型信息，確保正確處理
            if item_type != "hexagram":
                item_data['卡牌類型'] = item_type
                
            # 下載所有變體圖片
            logger.info('正在下載所有變體圖片...')
            if not self.image_processor.download_all_variations(image_urls, item_data, item_type):
                logger.error('下載變體圖片失敗')
                return False
                
            logger.info(f"{item_type} {item_id} 處理完成")
            return True
            
        except Exception as e:
            logger.error(f"處理{item_type}時發生錯誤: {str(e)}")
            return False
            
    def run(self, data_type="hexagram"):
        """運行主程序，支持不同數據類型"""
        try:
            # 根據數據類型選擇對應的 JSON 文件
            if data_type == "hexagram":
                json_path = os.path.join(DATA_DIR, 'hexagrams.json')
                logger.info("開始處理卦象圖片生成")
            elif data_type == "character":
                json_path = os.path.join(DATA_DIR, 'character_cards.json')
                logger.info("開始處理人物卡圖片生成")
            elif data_type == "timespace":
                json_path = os.path.join(DATA_DIR, 'timespace_cards.json')
                logger.info("開始處理時空卡圖片生成")
            else:
                logger.error(f"未支持的數據類型: {data_type}")
                return
            
            # 檢查已完成的任務編號
            last_completed = self.get_last_completed_number(data_type)
            start_from = last_completed + 1
            
            if last_completed > 0:
                logger.info(f"檢測到已完成的 {data_type} 任務到編號 {last_completed}，將從編號 {start_from} 開始繼續處理")
            else:
                logger.info(f"未找到已完成的 {data_type} 任務，將從編號 1 開始處理")
                
            # 讀取 JSON 文件
            with open(json_path, 'r', encoding='utf-8') as f:
                items = json.load(f)
                
            # 登入 Discord
            if not self.selenium_handler.login_discord():
                logger.error('Discord 登入失敗')
                return
                
            # 導航到目標頻道
            if not self.selenium_handler.navigate_to_channel():
                logger.error('導航到頻道失敗')
                return
                
            # 記錄已處理過的項目 ID，用於避免重複處理
            processed_ids = set()
            
            # 統計要處理的項目數量
            items_to_process = []
            for item in items:
                # 確定項目 ID
                if data_type == "hexagram":
                    id_key = "卦象編號"
                    item_number = int(item[id_key])
                else:
                    id_key = "卡牌編號"
                    item_number = int(item[id_key])
                
                # 只處理編號大於等於start_from的項目
                if item_number >= start_from:
                    items_to_process.append(item)
            
            logger.info(f"總共需要處理 {len(items_to_process)} 個 {data_type} 項目（從編號 {start_from} 開始）")
                
            # 處理每個項目
            for item in items_to_process:
                try:
                    # 確定項目 ID
                    if data_type == "hexagram":
                        id_key = "卦象編號"
                    else:
                        id_key = "卡牌編號"
                    
                    item_id = item[id_key]
                    
                    # 檢查是否已處理過
                    if item_id in processed_ids:
                        logger.warning(f"{data_type} {item_id} 已經處理過，跳過")
                        continue
                    
                    # 滾動到頁面底部，確保能夠看到最新消息
                    self.selenium_handler.scroll_to_bottom()
                    
                    # 等待一小段時間確保頁面更新
                    time.sleep(3)
                    
                    # 處理當前項目
                    success = self.process_item(item, item_type=data_type)
                    
                    # 記錄已處理的項目 ID
                    processed_ids.add(item_id)
                    
                    # 根據處理結果進行相應處理
                    if success:
                        logger.info(f"{data_type} {item_id} 處理成功")
                        # 成功處理後增加更長的等待時間，確保下一個項目的處理不受影響
                        wait_time = 10 if data_type == "hexagram" else 10  # 卡牌需要更長時間
                        logger.info(f"等待 {wait_time} 秒後處理下一個項目...")
                        time.sleep(wait_time)
                    else:
                        if data_type == "hexagram":
                            id_key = "卦象編號"
                        else:
                            id_key = "卡牌編號"
                        logger.warning(f"{data_type} {item[id_key]} 處理失敗，繼續下一個")
                        # 即使失敗也等待一段時間，避免請求過快
                        time.sleep(10)
                except Exception as e:
                    logger.error(f"處理項目時出錯: {str(e)}")
                    time.sleep(5)
                
        except Exception as e:
            logger.error(f"運行程序時發生錯誤: {str(e)}")
        finally:
            # 清理資源
            self.selenium_handler.close()
            
def main():
    """主函數"""
    automation = MidjourneyAutomation()
    automation.run(data_type=DATA_TYPE)
    
if __name__ == "__main__":
    main() 