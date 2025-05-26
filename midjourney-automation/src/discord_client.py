import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import random
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

# 設置日誌
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class DiscordHandler:
    def __init__(self, selenium_handler):
        self.selenium = selenium_handler
        self.driver = selenium_handler.driver
        
    def send_imagine_command(self, prompt):
        """發送 /imagine 指令"""
        try:
            # 構建命令（添加 aspect ratio 參數）
            prompt_with_ar = f"{prompt} --ar 2:3"
            
            # 點擊輸入框以確保焦點
            input_box = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "[role='textbox']"))
            )
            input_box.click()
            time.sleep(0.5)
            
            # 先輸入斜線命令
            self.selenium.human_like_typing(input_box, "/imagine")
            time.sleep(0.5)
            
            # 等待並選擇 imagine 命令
            imagine_option = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//div[contains(text(), '/imagine')]"))
            )
            imagine_option.click()
            time.sleep(0.5)
            
            # 輸入 prompt（包含 aspect ratio）
            self.selenium.human_like_typing(input_box, f" prompt: {prompt_with_ar}")
            
            # 使用 Ctrl+Enter 發送
            action = ActionChains(self.driver)
            action.key_down(Keys.CONTROL).send_keys(Keys.RETURN).key_up(Keys.CONTROL).perform()
            
            logger.info(f'已發送 prompt: {prompt_with_ar}')
            time.sleep(1)
            return True
                
        except Exception as e:
            logger.error(f'發送指令時發生錯誤: {str(e)}')
            return False
            
    def wait_for_image(self, timeout=60):
        """等待圖片生成完成"""
        try:
            # 等待 Midjourney 的回應
            start_time = time.time()
            last_progress = None
            wait = WebDriverWait(self.driver, timeout)
            
            while time.time() - start_time < timeout:
                # 尋找最新的消息
                messages = self.driver.find_elements(By.CSS_SELECTOR, "[class*='message-']")
                
                for message in reversed(messages):
                    try:
                        # 檢查是否是 Midjourney Bot 的消息
                        author = message.find_element(By.CSS_SELECTOR, "[class*='username-']")
                        if "Midjourney Bot" not in author.text:
                            continue
                            
                        # 檢查是否是進行中的消息
                        progress_elements = message.find_elements(By.CSS_SELECTOR, "[class*='progress-']")
                        if progress_elements:
                            current_progress = progress_elements[0].text
                            if current_progress != last_progress:
                                logger.info(f"圖片生成進度: {current_progress}")
                                last_progress = current_progress
                            continue
                            
                        # 使用 JavaScript 檢查圖片是否完全載入
                        check_image_script = """
                        let imgs = arguments[0].querySelectorAll('img[src*="cdn.discordapp.com"]');
                        for (let img of imgs) {
                            if (img.complete && img.naturalWidth > 0) {
                                return {
                                    loaded: true,
                                    src: img.src
                                };
                            }
                        }
                        return { loaded: false };
                        """
                        image_status = self.driver.execute_script(check_image_script, message)
                        
                        if image_status.get('loaded'):
                            logger.info(f"找到已載入的圖片: {image_status.get('src')}")
                            
                            # 檢查 U1-U4 按鈕
                            try:
                                # 等待任一 U 按鈕出現
                                u_button_xpath = "//button[.//div[contains(@class, 'label') and (text()='U1' or text()='U2' or text()='U3' or text()='U4')]]"
                                wait.until(EC.presence_of_element_located((By.XPATH, u_button_xpath)))
                                
                                # 確認所有按鈕都已載入
                                buttons_script = """
                                let result = [];
                                let buttons = arguments[0].querySelectorAll('button');
                                for (let btn of buttons) {
                                    let label = btn.querySelector('div[class*="label"]');
                                    if (label && /U[1-4]/.test(label.textContent)) {
                                        result.push(label.textContent);
                                    }
                                }
                                return result;
                                """
                                button_labels = self.driver.execute_script(buttons_script, message)
                                
                                if len(button_labels) >= 4:  # 確保所有 U1-U4 按鈕都存在
                                    logger.info(f"找到所有放大按鈕: {button_labels}")
                                    return message
                                    
                            except Exception as e:
                                logger.error(f"檢查按鈕時發生錯誤: {str(e)}")
                                continue
                            
                    except Exception as e:
                        logger.error(f"處理消息時發生錯誤: {str(e)}")
                        continue
                
                # 短暫延遲
                time.sleep(2)
            
            logger.error('等待圖片生成超時')
            return None
            
        except Exception as e:
            logger.error(f'等待圖片時發生錯誤: {str(e)}')
            return None

def create_discord_handler(selenium_handler):
    """創建 Discord 處理器實例"""
    return DiscordHandler(selenium_handler) 