import os
import requests
import logging
from PIL import Image
from io import BytesIO
import base64
from config import OUTPUT_DIR
import time

# 設置日誌
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ImageProcessor:
    def __init__(self):
        self.output_dir = OUTPUT_DIR
        self.selenium_handler = None
        os.makedirs(self.output_dir, exist_ok=True)
        
    def set_selenium_handler(self, selenium_handler):
        """設置Selenium處理器"""
        self.selenium_handler = selenium_handler
        
    def create_item_directory(self, item_data, item_type="hexagram"):
        """創建目錄（適用於卦象或人物卡）"""
        if item_type == "hexagram":
            item_id = item_data['卦象編號']
            item_name = item_data['卦象名稱']
        elif item_type == "character":
            item_id = item_data['卡牌編號']
            item_name = item_data['卡牌名稱']
        elif item_type == "timespace":
            item_id = item_data['卡牌編號']
            item_name = item_data['卡牌名稱']
        else:
            raise ValueError(f"不支持的項目類型: {item_type}")
            
        dir_name = f"{item_type}_{item_id}_{item_name}"
        dir_path = os.path.join(self.output_dir, dir_name)
        os.makedirs(dir_path, exist_ok=True)
        return dir_path
        
    def create_hexagram_directory(self, hexagram_number, hexagram_name):
        """創建卦象目錄 (保留舊方法以維持向後兼容)"""
        dir_name = f"{hexagram_number}_{hexagram_name}"
        dir_path = os.path.join(self.output_dir, dir_name)
        os.makedirs(dir_path, exist_ok=True)
        return dir_path
        
    def download_image(self, image_url, save_path):
        """下載圖片"""
        try:
            if not self.selenium_handler:
                raise Exception("Selenium處理器未設置")
                
            # 從Selenium獲取所有cookies
            cookies = self.selenium_handler.driver.get_cookies()
            cookies_dict = {cookie['name']: cookie['value'] for cookie in cookies}
            
            # 設置headers
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
                'Accept-Language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7',
                'Referer': 'https://discord.com/',
                'Origin': 'https://discord.com',
                'Connection': 'keep-alive',
                'Sec-Fetch-Dest': 'image',
                'Sec-Fetch-Mode': 'no-cors',
                'Sec-Fetch-Site': 'cross-site',
                'Pragma': 'no-cache',
                'Cache-Control': 'no-cache'
            }
            
            # 使用session保持連接狀態
            with requests.Session() as session:
                # 設置cookies
                session.cookies.update(cookies_dict)
                
                # 下載圖片
                response = session.get(image_url, headers=headers, timeout=30)
                response.raise_for_status()
                
                # 保存圖片
                with open(save_path, 'wb') as f:
                    f.write(response.content)
                    
                logger.info(f'圖片已保存至: {save_path}')
                return True
            
        except requests.exceptions.RequestException as e:
            logger.error(f'下載圖片時發生錯誤: {str(e)}')
            return False
        except Exception as e:
            logger.error(f'處理圖片時發生錯誤: {str(e)}')
            return False
            
    def save_image_urls(self, image_urls, item_data, item_type="hexagram"):
        """保存圖片URLs到txt文件（適用於卦象或人物卡）"""
        try:
            # 創建目錄
            dir_path = self.create_item_directory(item_data, item_type)
            
            # 構建txt文件路徑
            file_name = f"{item_type}_{item_data.get('卦象編號', item_data.get('卡牌編號'))}_urls.txt"
            txt_path = os.path.join(dir_path, file_name)
            
            # 保存URLs到txt文件
            with open(txt_path, 'w', encoding='utf-8') as f:
                if item_type == "hexagram":
                    f.write(f"卦象編號: {item_data['卦象編號']}\n")
                    f.write(f"卦象名稱: {item_data['卦象名稱']}\n")
                elif item_type == "character":
                    f.write(f"卡牌編號: {item_data['卡牌編號']}\n")
                    f.write(f"卡牌名稱: {item_data['卡牌名稱']}\n")
                    
                f.write(f"生成時間: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("\n變體圖片URLs:\n")
                for i, url in enumerate(image_urls, 1):
                    f.write(f"{i}. {url}\n")
                    
            logger.info(f'圖片URLs已保存至: {txt_path}')
            return True
            
        except Exception as e:
            logger.error(f'保存圖片URLs時發生錯誤: {str(e)}')
            return False
            
    def download_all_variations(self, image_urls, item_data, item_type="hexagram"):
        """保存所有變體圖片的URLs（適用於卦象或人物卡）"""
        try:
            # 根據item_data的鍵判斷數據類型
            if '卡牌編號' in item_data:
                if '卡牌類型' in item_data:
                    item_type = item_data['卡牌類型']
                else:
                    item_type = "character"
            elif '卦象編號' in item_data:
                item_type = "hexagram"
            
            # 檢查URLs是否為空
            if not image_urls or len(image_urls) == 0:
                logger.error(f"沒有找到有效的圖片URLs用於{item_type}")
                return False
                
            # 驗證URLs格式，確保UUID唯一性
            first_url = image_urls[0]
            if "cdn.midjourney.com" in first_url:
                try:
                    # 從URL中提取UUID
                    uuid = first_url.split('/')[3]  # 例如 https://cdn.midjourney.com/UUID/0_0.png
                    
                    # 確保所有URL使用相同的UUID
                    for url in image_urls:
                        if uuid not in url:
                            logger.error(f"圖片URL中的UUID不一致: {url}")
                            return False
                            
                    # 記錄當前處理的UUID，添加到日誌中
                    if item_type == "hexagram":
                        id_name = f"卦象 {item_data['卦象編號']} ({item_data['卦象名稱']})"
                    else:
                        id_name = f"卡牌 {item_data['卡牌編號']} ({item_data['卡牌名稱']})"
                        
                    logger.info(f"為 {id_name} 獲取到有效的UUID: {uuid}")
                    
                except Exception as e:
                    logger.error(f"解析URL中的UUID時出錯: {str(e)}")
                    return False
            
            # 保存URLs到txt文件
            return self.save_image_urls(image_urls, item_data, item_type)
            
        except Exception as e:
            logger.error(f'下載變體圖片時發生錯誤: {str(e)}')
            return False
            
    def process_midjourney_message(self, message, item_data, item_type="hexagram"):
        """處理 Midjourney 消息並保存圖片（適用於卦象或人物卡）"""
        try:
            # 創建目錄
            dir_path = self.create_item_directory(item_data, item_type)
            
            # 獲取圖片 URL
            if message.attachments:
                image_url = message.attachments[0].url
                # 構建保存路徑
                file_name = f"{item_type}_{item_data.get('卦象編號', item_data.get('卡牌編號'))}.png"
                save_path = os.path.join(dir_path, file_name)
                
                # 下載並保存圖片
                if self.download_image(image_url, save_path):
                    return save_path
                    
            return None
            
        except Exception as e:
            logger.error(f'處理 Midjourney 消息時發生錯誤: {str(e)}')
            return None
            
    def save_upscaled_image(self, message, item_data, upscale_number, item_type="hexagram"):
        """保存放大後的圖片（適用於卦象或人物卡）"""
        try:
            # 創建目錄
            dir_path = self.create_item_directory(item_data, item_type)
            
            # 獲取圖片 URL
            if message.attachments:
                image_url = message.attachments[0].url
                # 構建保存路徑
                file_name = f"{item_type}_{item_data.get('卦象編號', item_data.get('卡牌編號'))}_upscaled_{upscale_number}.png"
                save_path = os.path.join(dir_path, file_name)
                
                # 下載並保存圖片
                if self.download_image(image_url, save_path):
                    return save_path
                    
            return None
            
        except Exception as e:
            logger.error(f'保存放大圖片時發生錯誤: {str(e)}')
            return None

def create_image_processor():
    """創建圖片處理器實例"""
    return ImageProcessor() 