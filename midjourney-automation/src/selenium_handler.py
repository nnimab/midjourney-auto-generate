from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import logging
import time
import random
import json
import os
from config import (
    DISCORD_URL,
    DISCORD_EMAIL,
    DISCORD_PASSWORD,
    WAIT_TIME,
    CHANNEL_URL
)

# 設置日誌
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class SeleniumHandler:
    def __init__(self):
        self.driver = None
        self.setup_driver()
        
    def setup_driver(self):
        """設置 Chrome 驅動"""
        try:
            chrome_options = Options()
            
            # 基本的自動化隱藏設置
            chrome_options.add_argument('--disable-blink-features=AutomationControlled')
            chrome_options.add_argument('--disable-infobars')
            chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            
            # 禁用各種彈窗和通知
            chrome_options.add_argument('--disable-notifications')  # 禁用通知
            chrome_options.add_argument('--disable-popup-blocking')  # 禁用彈窗阻擋
            chrome_options.add_argument('--disable-save-password-bubble')  # 禁用密碼保存提示
            chrome_options.add_argument('--disable-password-generation')  # 禁用密碼生成
            chrome_options.add_argument('--disable-autofill')  # 禁用自動填充
            chrome_options.add_argument('--disable-autofill-keyboard-accessory-view[0]')
            chrome_options.add_argument('--disable-full-form-autofill-ios')
            
            # 禁用安全性相關彈窗
            chrome_options.add_argument('--disable-web-security')  # 禁用網頁安全檢查
            chrome_options.add_argument('--disable-features=TranslateUI')  # 禁用翻譯提示
            chrome_options.add_argument('--disable-ipc-flooding-protection')  # 禁用IPC洪水保護
            chrome_options.add_argument('--disable-renderer-backgrounding')  # 禁用渲染器背景化
            chrome_options.add_argument('--disable-backgrounding-occluded-windows')  # 禁用被遮擋窗口的背景化
            chrome_options.add_argument('--disable-client-side-phishing-detection')  # 禁用釣魚檢測
            chrome_options.add_argument('--disable-sync')  # 禁用同步
            chrome_options.add_argument('--disable-default-apps')  # 禁用默認應用
            
            # 禁用各種提示和建議
            chrome_options.add_argument('--no-first-run')  # 禁用首次運行提示
            chrome_options.add_argument('--no-default-browser-check')  # 禁用默認瀏覽器檢查
            chrome_options.add_argument('--disable-default-browser-check')  # 禁用默認瀏覽器檢查
            chrome_options.add_argument('--disable-extensions-http-throttling')  # 禁用擴展HTTP節流
            chrome_options.add_argument('--disable-extensions-file-access-check')  # 禁用擴展文件訪問檢查
            
            # 設置用戶偏好，進一步禁用彈窗
            prefs = {
                # 禁用密碼管理器
                'profile.password_manager_enabled': False,
                'profile.default_content_setting_values.notifications': 2,  # 禁用通知 (2 = 阻止)
                'profile.default_content_settings.popups': 0,  # 禁用彈窗
                'profile.managed_default_content_settings.images': 1,  # 允許圖片
                'profile.content_settings.plugin_whitelist.adobe-flash-player': 1,
                'profile.content_settings.exceptions.plugins.*,*.per_resource.adobe-flash-player': 1,
                'PluginsAllowedForUrls': 'https://discord.com',
                # 禁用自動填充
                'autofill.profile_enabled': False,
                'autofill.credit_card_enabled': False,
                'autofill.address_enabled': False,
                # 禁用翻譯
                'translate_enabled': False,
                # 禁用位置共享
                'profile.default_content_setting_values.geolocation': 2,
                # 禁用媒體流
                'profile.default_content_setting_values.media_stream': 2,
                # 禁用下載提示
                'profile.default_content_settings.multiple-automatic-downloads': 1,
                # 禁用安全瀏覽
                'safebrowsing.enabled': False,
                'safebrowsing.disable_download_protection': True,
                # 禁用各種提示
                'profile.default_content_setting_values.automatic_downloads': 1,
                'profile.password_manager_leak_detection': False,
                'profile.exit_type': 'Normal',
                'profile.exited_cleanly': True
            }
            chrome_options.add_experimental_option('prefs', prefs)
            
            # 啟用網絡請求監控
            chrome_options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})
            
            # 添加一些隨機的 user-agent
            user_agents = [
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
            ]
            chrome_options.add_argument(f'user-agent={random.choice(user_agents)}')
            
            # 使用內建的 ChromeDriver 管理器
            self.driver = webdriver.Chrome(options=chrome_options)
            
            # 修改 webdriver 特徵
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            # 進一步禁用密碼管理器和自動填充的JavaScript
            disable_features_script = """
                // 禁用密碼管理器
                Object.defineProperty(navigator, 'credentials', {
                    get: () => undefined
                });
                
                // 禁用自動填充
                document.addEventListener('DOMContentLoaded', function() {
                    const inputs = document.querySelectorAll('input');
                    inputs.forEach(input => {
                        input.setAttribute('autocomplete', 'off');
                        input.setAttribute('data-lpignore', 'true');
                    });
                });
                
                // 移除密碼保存提示
                window.addEventListener('beforeunload', function(e) {
                    delete e['returnValue'];
                });
            """
            self.driver.execute_script(disable_features_script)
            
            self.driver.implicitly_wait(WAIT_TIME)
            logger.info('Chrome 驅動已設置完成，已禁用所有彈窗和提示')
            
        except Exception as e:
            logger.error(f'設置 Chrome 驅動時發生錯誤: {str(e)}')
            raise
            
    def human_like_typing(self, element, text):
        """模擬人類輸入文字"""
        # 將文字分成小塊，每次輸入多個字符
        chunk_size = 5  # 每次輸入5個字符
        chunks = [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]
        
        for chunk in chunks:
            element.send_keys(chunk)
            time.sleep(random.uniform(0.001, 0.005))  # 極短的延遲
            
    def random_mouse_movement(self):
        """隨機移動滑鼠"""
        action = ActionChains(self.driver)
        x = random.randint(0, 500)
        y = random.randint(0, 500)
        action.move_by_offset(x, y).perform()
        action.reset_actions()
            
    def login_discord(self):
        """登入 Discord"""
        try:
            logger.info('開始登入 Discord...')
            self.driver.get(DISCORD_URL)
            
            # 隨機延遲
            time.sleep(random.uniform(2, 4))
            
            # 執行額外的彈窗禁用腳本
            additional_disable_script = """
                // 禁用所有可能的彈窗和提示
                window.alert = function() {};
                window.confirm = function() { return true; };
                window.prompt = function() { return null; };
                
                // 禁用密碼管理器相關功能
                if (navigator.credentials) {
                    navigator.credentials.create = function() { return Promise.reject(); };
                    navigator.credentials.get = function() { return Promise.reject(); };
                    navigator.credentials.store = function() { return Promise.reject(); };
                }
                
                // 移除所有可能的密碼保存相關事件監聽器
                document.addEventListener('submit', function(e) {
                    const form = e.target;
                    if (form && form.tagName === 'FORM') {
                        const inputs = form.querySelectorAll('input[type="password"]');
                        inputs.forEach(input => {
                            input.setAttribute('autocomplete', 'new-password');
                            input.setAttribute('data-lpignore', 'true');
                        });
                    }
                }, true);
                
                // 禁用瀏覽器的自動填充建議
                document.addEventListener('input', function(e) {
                    if (e.target.tagName === 'INPUT') {
                        e.target.setAttribute('autocomplete', 'off');
                        e.target.setAttribute('data-lpignore', 'true');
                    }
                }, true);
            """
            self.driver.execute_script(additional_disable_script)
            
            # 等待登入表單加載
            email_input = WebDriverWait(self.driver, WAIT_TIME).until(
                EC.presence_of_element_located((By.NAME, "email"))
            )
            password_input = self.driver.find_element(By.NAME, "password")
            
            # 設置輸入框屬性以禁用自動填充和密碼保存
            self.driver.execute_script("""
                arguments[0].setAttribute('autocomplete', 'new-email');
                arguments[0].setAttribute('data-lpignore', 'true');
                arguments[1].setAttribute('autocomplete', 'new-password');
                arguments[1].setAttribute('data-lpignore', 'true');
            """, email_input, password_input)
            
            # 隨機移動滑鼠
            self.random_mouse_movement()
            
            # 模擬人類輸入
            self.human_like_typing(email_input, DISCORD_EMAIL)
            time.sleep(random.uniform(0.5, 1.5))
            self.human_like_typing(password_input, DISCORD_PASSWORD)
            
            # 隨機延遲後提交
            time.sleep(random.uniform(0.8, 2))
            
            # 在提交前再次執行禁用腳本
            self.driver.execute_script("""
                // 在提交前禁用所有可能的彈窗
                window.onbeforeunload = null;
                document.onbeforeunload = null;
                
                // 移除所有事件監聽器
                const form = document.querySelector('form');
                if (form) {
                    form.addEventListener('submit', function(e) {
                        setTimeout(() => {
                            window.alert = function() {};
                            window.confirm = function() { return true; };
                        }, 100);
                    });
                }
            """)
            
            password_input.submit()
            
            # 等待頁面加載完成
            WebDriverWait(self.driver, WAIT_TIME).until(
                EC.url_changes(DISCORD_URL)
            )
            
            # 登入後再次執行禁用腳本
            time.sleep(2)  # 等待頁面穩定
            self.driver.execute_script(additional_disable_script)
            
            # 登入後的隨機延遲
            time.sleep(random.uniform(3, 5))
            
            logger.info('Discord 登入成功')
            return True
            
        except TimeoutException:
            logger.error('登入超時')
            return False
        except Exception as e:
            logger.error(f'登入時發生錯誤: {str(e)}')
            return False
            
    def navigate_to_channel(self):
        """導航到指定的 Discord 頻道"""
        try:
            logger.info('正在導航到目標頻道...')
            self.driver.get(CHANNEL_URL)
            
            # 添加隨機延遲
            time.sleep(random.uniform(5, 8))
            
            # 隨機滾動頁面
            self.driver.execute_script(f"window.scrollTo(0, {random.randint(100, 300)})")
            time.sleep(random.uniform(1, 2))
            
            return True
            
        except Exception as e:
            logger.error(f'導航到頻道時發生錯誤: {str(e)}')
            return False
            
    def send_message(self, message):
        """發送消息"""
        try:
            # 等待消息輸入框
            input_box = WebDriverWait(self.driver, WAIT_TIME).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "[role='textbox']"))
            )
            
            # 隨機移動滑鼠
            self.random_mouse_movement()
            
            # 模擬人類輸入
            self.human_like_typing(input_box, message)
            
            # 使用 Ctrl+Enter 發送消息
            action = ActionChains(self.driver)
            action.key_down(Keys.CONTROL).send_keys(Keys.RETURN).key_up(Keys.CONTROL).perform()
            
            # 發送後的短暫延遲
            time.sleep(random.uniform(0.5, 1))
            
            return True
            
        except Exception as e:
            logger.error(f'發送消息時發生錯誤: {str(e)}')
            return False
            
    def click_upscale_button(self, button_number):
        """點擊放大按鈕 (U1-U4)"""
        try:
            logger.info(f'等待 U{button_number} 按鈕出現...')
            wait = WebDriverWait(self.driver, WAIT_TIME)
            
            # 使用 XPath 定位按鈕
            button_xpath = f"//button[.//div[contains(@class, 'label') and text()='U{button_number}']]"
            
            # 等待按鈕可點擊
            button = wait.until(EC.element_to_be_clickable((By.XPATH, button_xpath)))
            
            # 確保按鈕在視圖中
            self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", button)
            time.sleep(1)
            
            # 使用 JavaScript 點擊按鈕
            click_script = """
            function simulateClick(element) {
                element.dispatchEvent(new MouseEvent('mousedown', {
                    bubbles: true,
                    cancelable: true,
                    view: window
                }));
                
                element.dispatchEvent(new MouseEvent('mouseup', {
                    bubbles: true,
                    cancelable: true,
                    view: window
                }));
                
                element.dispatchEvent(new MouseEvent('click', {
                    bubbles: true,
                    cancelable: true,
                    view: window
                }));
            }
            simulateClick(arguments[0]);
            """
            self.driver.execute_script(click_script, button)
            
            logger.info(f'已點擊 U{button_number} 按鈕')
            return True
            
        except TimeoutException:
            logger.error(f'等待 U{button_number} 按鈕超時')
            return False
        except Exception as e:
            logger.error(f'點擊 U{button_number} 按鈕時發生錯誤: {str(e)}')
            return False
            
    def close(self):
        """關閉瀏覽器"""
        if self.driver:
            self.driver.quit()
            logger.info('瀏覽器已關閉')
            
    def scroll_to_bottom(self):
        """滾動到頁面底部"""
        try:
            logger.info('滾動到頁面底部以獲取最新消息...')
            
            # 獲取頁面高度
            last_height = self.driver.execute_script("return document.body.scrollHeight")
            
            # 先嘗試滾動到中間
            self.driver.execute_script(f"window.scrollTo(0, {last_height/2});")
            time.sleep(0.5)
            
            # 然後滾動到底部
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)
            
            # 檢查是否需要多次滾動來加載更多內容
            for _ in range(3):
                # 再次獲取頁面高度
                new_height = self.driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    break
                    
                # 繼續滾動
                last_height = new_height
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(1)
                
            logger.info('已滾動到頁面底部')
            return True
            
        except Exception as e:
            logger.error(f'滾動頁面時發生錯誤: {str(e)}')
            return False
            
    def get_midjourney_image_urls(self, timeout=60):  # 增加默認超時時間
        """監控並獲取Midjourney圖片URL"""
        try:
            start_time = time.time()
            
            # 先確保滾動到頁面底部，獲取最新內容
            self.scroll_to_bottom()
            
            # 等待頁面加載完成
            time.sleep(2)
            
            # 獲取初始的attachments列表（每次調用此方法時重新獲取）
            initial_attachments = self._get_current_attachments()
            logger.info(f'初始附件數量: {len(initial_attachments)}')
            
            # 存儲初始的UUID集合，避免重複處理舊圖片
            initial_uuids = set()
            for url in initial_attachments:
                try:
                    if 'media.discordapp.net/attachments' in url:
                        image_name = url.split('/')[-1]
                        uuid = image_name.split('_')[0]
                        if len(uuid) == 36 and uuid.count('-') == 4:
                            initial_uuids.add(uuid)
                except:
                    pass
                    
            logger.info(f'初始UUID數量: {len(initial_uuids)}')
            
            # 等待新圖片出現
            wait_start = time.time()
            while time.time() - start_time < timeout:
                # 每5秒滾動一次頁面，確保能看到最新消息
                if time.time() - wait_start > 5:
                    self.scroll_to_bottom()
                    wait_start = time.time()
                
                # 獲取當前頁面上的所有圖片
                current_attachments = self._get_current_attachments()
                
                # 從當前附件中提取UUID
                current_uuids = set()
                for url in current_attachments:
                    try:
                        if 'media.discordapp.net/attachments' in url:
                            image_name = url.split('/')[-1]
                            uuid = image_name.split('_')[0]
                            if len(uuid) == 36 and uuid.count('-') == 4:
                                current_uuids.add(uuid)
                    except:
                        pass
                
                # 找出新增的UUID
                new_uuids = current_uuids - initial_uuids
                if new_uuids:
                    logger.info(f'發現新的UUID: {new_uuids}')
                    
                    # 使用第一個新UUID
                    new_uuid = list(new_uuids)[0]
                    
                    # 找到所有帶有這個UUID的圖片
                    grid_images = [img for img in current_attachments if new_uuid in img and '_grid_' in img]
                    logger.info(f'找到UUID: {new_uuid}, 預覽圖數量: {len(grid_images)}')
                    
                    # 確保找到足夠的預覽圖
                    retry_count = 0
                    while len(grid_images) < 4 and retry_count < 5:
                        logger.info(f'預覽圖不足4張 (當前: {len(grid_images)})，等待更多圖片加載...')
                        time.sleep(2)
                        self.scroll_to_bottom()
                        current_attachments = self._get_current_attachments()
                        grid_images = [img for img in current_attachments if new_uuid in img and '_grid_' in img]
                        retry_count += 1
                    
                    # 根據預覽圖順序構建原始圖片URL
                    if len(grid_images) >= 4:
                        # 按格子索引排序（例如 grid_0, grid_1, grid_2, grid_3）
                        grid_images.sort(key=lambda img: int(img.split('_grid_')[-1].split('.')[0]))
                        
                        image_urls = []
                        for grid_img in grid_images[:4]:
                            grid_index = grid_img.split('_grid_')[-1].split('.')[0]
                            image_urls.append(f"https://cdn.midjourney.com/{new_uuid}/0_{grid_index}.png")
                            
                        logger.info(f'構建的Midjourney圖片URLs: {image_urls}')
                        return image_urls
                    else:
                        # 如果無法從預覽圖確定順序，使用默認順序
                        image_urls = [
                            f"https://cdn.midjourney.com/{new_uuid}/0_{i}.png"
                            for i in range(4)
                        ]
                        logger.info(f'使用默認順序的Midjourney圖片URLs: {image_urls}')
                        return image_urls
                
                # 短暫等待後重新檢查
                time.sleep(1)
            
            logger.warning('等待圖片URL超時')
            return None
            
        except Exception as e:
            logger.error(f'獲取圖片URL時發生錯誤: {str(e)}')
            return None
            
    def _get_current_attachments(self):
        """獲取當前頁面上所有的attachments URL，保持它們在DOM中的順序"""
        try:
            # 使用更穩定的JavaScript獲取所有圖片URL，保持它們在DOM中的順序
            script = """
            function getAllImages() {
                let urls = [];
                let urlSet = new Set(); // 用於檢查URL是否已存在
                
                // 獲取所有圖片元素（保持DOM順序）
                let images = document.querySelectorAll('img');
                images.forEach(img => {
                    if (img.src && img.src.includes('media.discordapp.net/attachments')) {
                        if (!urlSet.has(img.src)) {
                            urls.push(img.src);
                            urlSet.add(img.src);
                        }
                    }
                });
                
                // 獲取所有背景圖片
                let elements = document.querySelectorAll('*');
                elements.forEach(el => {
                    let bg = window.getComputedStyle(el).backgroundImage;
                    if (bg && bg.includes('media.discordapp.net/attachments')) {
                        let url = bg.replace(/^url\\(['"](.+)['"]\)$/, '$1');
                        if (!urlSet.has(url)) {
                            urls.push(url);
                            urlSet.add(url);
                        }
                    }
                });
                
                return urls; // 返回陣列，保持順序
            }
            return getAllImages();
            """
            
            # 多次嘗試獲取URLs
            max_retries = 3
            for _ in range(max_retries):
                urls = self.driver.execute_script(script)
                if urls:
                    return urls  # 直接返回陣列，保持順序
                time.sleep(1)  # 短暫等待後重試
                
            return []
            
        except Exception as e:
            logger.error(f'獲取attachments時發生錯誤: {str(e)}')
            return []

def create_selenium_handler():
    """創建 Selenium 處理器實例"""
    return SeleniumHandler() 