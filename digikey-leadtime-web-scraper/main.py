"""
Digikey Web Scraper - OPTIMIZED FULL VERSION ⚡
Author: defacto092
"""
from selenium.webdriver.common.keys import Keys
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from bs4 import BeautifulSoup
import time
import random
from datetime import datetime
from typing import Dict, List, Optional
import logging
import re



logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)



class DigikeyScraperError(Exception):
    """Custom exception for Digikey scraper errors"""
    pass



class DigikeyLeadTimeScraper:
    """Optimized web scraper with all features"""
    
    SEARCH_URL = "https://www.digikey.de/en/products/result?keywords={}"
    
    USER_AGENTS = [
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    ]
    
    def __init__(self, headless: bool = False, timeout: int = 15):
        """Initialize scraper"""
        self.headless = headless
        self.timeout = timeout
        self.driver = None
        self.wait = None
        self.cookies_accepted = False
        
    def setup_driver(self):
        """Initialize Chrome driver - NO STEALTH for Chrome 144+"""
        try:
            options = uc.ChromeOptions()
            
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.add_argument("--window-size=1920,1080")
            options.add_argument("--start-maximized")
            
            if self.headless:
                options.add_argument("--headless=new")
            
            user_agent = random.choice(self.USER_AGENTS)
            options.add_argument(f"user-agent={user_agent}")
            
            # ✅ UC 3.5.5 САМ обходить всі детекції!
            self.driver = uc.Chrome(options=options, version_main=None)
            self.driver.set_page_load_timeout(120)
            
            # NO STEALTH! UC 3.5.5 вже стелс!
            
            self.wait = WebDriverWait(self.driver, self.timeout)
            logger.info("✅ Driver initialized")
            
        except Exception as e:
            logger.error(f"❌ Driver init failed: {str(e)}")
            raise DigikeyScraperError(f"Driver initialization failed: {str(e)}")
    
    def accept_cookies(self):
        """Accept cookies and close privacy banners"""
        if self.cookies_accepted:
            return True
            
        try:
            logger.info("🍪 Looking for cookie banner...")
            
            # ✅ OPTIMIZED: Reduced from 2s to 0.5s
            time.sleep(0.5)
            
            # Multiple selectors for cookie accept buttons
            cookie_selectors = [
                "//button[contains(text(), 'Accept')]",
                "//button[contains(text(), 'Accept All')]",
                "//button[contains(text(), 'Akzeptieren')]",
                "//button[contains(@id, 'accept')]",
                "//button[contains(@id, 'cookie')]",
                "//button[contains(@class, 'accept')]",
                "//a[contains(text(), 'Accept')]",
                "//*[@id='onetrust-accept-btn-handler']",
                "//*[contains(@class, 'cookie-accept')]",
                "//button[contains(., 'I Accept')]"
            ]
            
            for selector in cookie_selectors:
                try:
                    # ✅ OPTIMIZED: Reduced timeout from 3s to 2s
                    button = WebDriverWait(self.driver, 2).until(
                        EC.element_to_be_clickable((By.XPATH, selector))
                    )
                    button.click()
                    self.cookies_accepted = True
                    logger.info("✅ Accepted cookies")
                    time.sleep(0.3)  # ✅ OPTIMIZED: Reduced from 1s
                    return True
                except:
                    continue
            
            logger.info("ℹ️ No cookie banner found")
            self.cookies_accepted = True
            return True
            
        except Exception as e:
            logger.debug(f"Cookie banner handling: {str(e)}")
            self.cookies_accepted = True
            return True
    
    def human_delay(self, min_sec: float = 0.5, max_sec: float = 1.5):
        """Optimized random delay"""
        time.sleep(random.uniform(min_sec, max_sec))
    
    def scroll_to(self, element):
        """Scroll to element"""
        try:
            self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)
            time.sleep(0.3)  # ✅ OPTIMIZED: Reduced from 0.5-1.5s
        except Exception as e:
            logger.debug(f"Scroll error: {str(e)}")
    
    def search_part(self, part_number: str) -> bool:
        """Search for part number"""
        try:
            logger.info(f"🔍 Searching: {part_number}")
            
            url = self.SEARCH_URL.format(part_number)
            logger.info(f"📍 URL: {url}")
            
            for attempt in range(3):
                try:
                    self.driver.get(url)
                    break
                except TimeoutException:
                    logger.warning(f"⚠️ Timeout attempt {attempt + 1}/3")
                    if attempt < 2:
                        time.sleep(2)  # ✅ OPTIMIZED: Reduced from 5s
                    else:
                        return False
                except Exception as e:
                    logger.error(f"⚠️ Navigate error attempt {attempt + 1}/3: {e}")
                    if attempt < 2:
                        time.sleep(2)
                    else:
                        return False
            
            time.sleep(1)  # ✅ OPTIMIZED: Reduced from 3-5s
            
            self.accept_cookies()
            
            time.sleep(0.5)  # ✅ OPTIMIZED: Reduced from 2-3s
            
            logger.info(f"📄 Page: {self.driver.title}")
            
            try:
                self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
                
                page_source = self.driver.page_source.lower()
                if "404" in self.driver.title or "not found" in page_source:
                    logger.error("❌ 404 page")
                    return False
                
                logger.info("✅ Page loaded")
                return True
                
            except TimeoutException:
                logger.warning("⚠️ Timeout")
                return False
                
        except Exception as e:
            logger.error(f"❌ Search error: {str(e)}")
            return False
    
    def navigate_to_product(self, part_number: str) -> bool:
        """Navigate to product page"""
        try:
            logger.info(f"🔎 Finding product: {part_number}")
            time.sleep(0.5)  # ✅ OPTIMIZED: Reduced from 2-3s
            
            page_source = self.driver.page_source.lower()
            current_url = self.driver.current_url
            
            if "/products/detail/" in current_url and part_number.lower() in page_source:
                logger.info("✅ Already on product detail page")
                return True
            
            logger.info("📋 On search results page, looking for product link...")
            
            try:
                self.driver.execute_script("window.scrollBy(0, 300);")
                time.sleep(0.5)  # ✅ OPTIMIZED: Reduced from 1-2s
                
                link_selectors = [
                    f"//a[contains(@href, '/products/detail/') and contains(., '{part_number}')]",
                    f"//td[contains(., '{part_number}')]//ancestor::tr//a[contains(@href, '/products/detail/')]",
                    "//table[@id='productTable']//a[contains(@href, '/products/detail/')]",
                    "//table//tr//td[1]//a[contains(@href, '/products/detail/')]"
                ]
                
                product_link = None
                for selector in link_selectors:
                    try:
                        elements = self.driver.find_elements(By.XPATH, selector)
                        logger.info(f"Found {len(elements)} elements with selector")
                        
                        for elem in elements:
                            try:
                                elem_text = elem.text.upper()
                                elem_href = elem.get_attribute('href')
                                
                                logger.info(f"Checking element: {elem_text[:30]}")
                                
                                if part_number.upper() in elem_text or '/products/detail/' in elem_href:
                                    product_link = elem
                                    logger.info(f"✅ Found matching link: {elem_text[:50]}")
                                    break
                            except:
                                continue
                                
                        if product_link:
                            break
                    except Exception as e:
                        logger.debug(f"Selector failed: {selector} - {e}")
                        continue
                
                if product_link:
                    self.scroll_to(product_link)
                    time.sleep(0.3)  # ✅ OPTIMIZED: Reduced from 1-2s
                    
                    logger.info(f"Clicking link: {product_link.get_attribute('href')}")
                    self.driver.execute_script("arguments[0].click();", product_link)
                    
                    time.sleep(2) 
                    logger.info("✅ Clicked product link")
                    
                    new_url = self.driver.current_url
                    if "/products/detail/" in new_url:
                        logger.info(f"✅ Successfully navigated to: {new_url}")
                        return True
                    else:
                        logger.warning(f"⚠️ Not on detail page: {new_url}")
                        return False
                else:
                    logger.error("❌ Product link not found in search results")
                    return False
                    
            except Exception as e:
                logger.error(f"❌ Navigation error: {e}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Navigation failed: {str(e)}")
            return False
    
    def check_stock(self) -> Dict[str, any]:
        """Check stock status"""
        try:
            logger.info("📦 Checking stock...")
            
            page_text = self.driver.page_source.lower()
            
            in_stock = False
            quantity = 0
            status_text = ""
            
            if "0 in stock" in page_text or "0 - in stock" in page_text:
                in_stock = False
                quantity = 0
                status_text = "Out of Stock (0)"
                logger.info("📉 OUT OF STOCK (0 units)")
                
            elif "out of stock" in page_text or "not available" in page_text:
                in_stock = False
                status_text = "Out of Stock"
                logger.info("📉 OUT OF STOCK")
                
            elif "in stock" in page_text:
                match = re.search(r'(\d+(?:,\d+)*)\s*(?:-\s*)?(?:in stock|available)', page_text, re.IGNORECASE)
                if match:
                    quantity = int(match.group(1).replace(',', ''))
                    
                    if quantity == 0:
                        in_stock = False
                        status_text = "Out of Stock (0)"
                        logger.info("📉 OUT OF STOCK (0 units found)")
                    else:
                        in_stock = True
                        status_text = f"{quantity} In Stock"
                        logger.info(f"✅ IN STOCK: {status_text}")
                else:
                    in_stock = False
                    status_text = "Out of Stock"
                    logger.info("📉 OUT OF STOCK (no quantity)")
            
            return {
                'in_stock': in_stock,
                'quantity': quantity,
                'status_text': status_text
            }
            
        except Exception as e:
            logger.error(f"❌ Stock check error: {str(e)}")
            return {'in_stock': False, 'quantity': 0, 'status_text': 'Unknown'}
    
    def click_lead_time(self) -> bool:
        """Click Check Lead Time button"""
        try:
            logger.info("🔎 Looking for Lead Time button...")
            
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight / 2);")
            time.sleep(0.5)  # ✅ OPTIMIZED: Reduced from 1-2s
            
            selectors = [
                "//*[contains(text(), 'Check Lead Time')]",
                "//*[contains(text(), 'Lead Time')]",
                "//button[contains(., 'Lead Time')]",
                "//a[contains(text(), 'Check Lead Time')]",
                "//a[contains(@class, 'lead-time')]"
            ]
            
            button = None
            for selector in selectors:
                try:
                    button = self.wait.until(EC.element_to_be_clickable((By.XPATH, selector)))
                    logger.info(f"✅ Found button")
                    break
                except TimeoutException:
                    continue
            
            if button is None:
                logger.warning("⚠️ Button not found, scrolling more...")
                for i in range(5):
                    self.driver.execute_script("window.scrollBy(0, 300);")
                    time.sleep(0.3)  # ✅ OPTIMIZED: Reduced from 0.5-1s
                
                for selector in selectors:
                    try:
                        button = self.driver.find_element(By.XPATH, selector)
                        break
                    except NoSuchElementException:
                        continue
                
                if button is None:
                    logger.warning("⚠️ Button still not found")
                    return False
            
            self.scroll_to(button)
            time.sleep(0.3)  # ✅ OPTIMIZED: Reduced from 1-2s
            
            try:
                button.click()
            except:
                self.driver.execute_script("arguments[0].click();", button)
            
            logger.info("✅ Clicked Lead Time button")
            
            time.sleep(1.5)  # ✅ OPTIMIZED: Reduced from 3-5s
            return True
    
        except Exception as e:
            logger.error(f"❌ Button click error: {str(e)}")
            return False
    
    def enter_quantity(self, quantity: int = 9999999) -> bool:
        """Enter quantity with full error handling"""
        try:
            logger.info(f"📝 Entering: {quantity:,}")
            
            logger.info("⏳ Waiting for modal to appear...")
            time.sleep(1)  # ✅ OPTIMIZED: Reduced from 7-10s to 1s
            
            selectors = [
                '//input[@data-testid="lt-input-qty"]',
                '//input[@inputmode="numeric"]',
                '//input[@id="quantity-input"]',
                '//input[contains(@class, "MuiInputBase-input")]',
            ]
            
            input_field = None
            for selector in selectors:
                try:
                    input_field = WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, selector))
                    )
                    logger.info(f"✅ Found input with: {selector}")
                    break
                except TimeoutException:
                    logger.debug(f"Selector failed: {selector}")
                    continue
            
            if input_field is None:
                logger.error("❌ Could not find input field")
                return False
            
            try:
                WebDriverWait(self.driver, 5).until(EC.visibility_of(input_field))
                logger.info("✅ Input is visible")
            except:
                logger.warning("⚠️ Input may not be visible")
            
            current = input_field.get_attribute('value')
            logger.info(f"Current value before input: '{current}'")
            
            logger.info("🔤 Using character-by-character typing...")
            
            try:
                input_field.click()
                time.sleep(0.3)  # ✅ OPTIMIZED: Reduced from 0.5-1s
                
                input_field.send_keys(Keys.CONTROL + 'a')
                time.sleep(0.1)  # ✅ OPTIMIZED: Reduced from 0.2-0.3s
                input_field.send_keys(Keys.BACKSPACE)
                time.sleep(0.3)  # ✅ OPTIMIZED: Reduced from 0.5-1s
                
                logger.info("✅ Cleared field")
                
                qty_str = str(quantity)
                logger.info(f"Typing: {qty_str}")
                
                for i, char in enumerate(qty_str):
                    input_field.send_keys(char)
                    time.sleep(0.06)  # ✅ OPTIMIZED: Reduced from 0.08
                    if (i + 1) % 3 == 0:
                        logger.info(f"Typed {i+1}/{len(qty_str)} characters...")
                
                logger.info(f"✅ Finished typing all {len(qty_str)} characters")
                
                time.sleep(0.5)  # ✅ OPTIMIZED: Reduced from 1-2s
                
                input_field.send_keys(Keys.TAB)
                logger.info("✅ Pressed TAB to validate")
                
                time.sleep(0.5)  # ✅ OPTIMIZED: Reduced from 1-2s
                
                final_value = input_field.get_attribute('value')
                logger.info(f"Final value in field: '{final_value}'")
                
                final_clean = final_value.replace(',', '').replace(' ', '')
                expected = str(quantity)
                
                if final_clean == expected or expected in final_clean:
                    logger.info(f"✅ Successfully entered: {final_value}")
                    return True
                else:
                    logger.error(f"❌ Value mismatch. Expected: {expected}, Got: {final_clean}")
                    
                    try:
                        screenshot_path = f"/tmp/qty_mismatch_{int(time.time())}.png"
                        self.driver.save_screenshot(screenshot_path)
                        logger.info(f"📸 Screenshot: {screenshot_path}")
                    except:
                        pass
                    
                    return False
                
            except Exception as e:
                logger.error(f"❌ Typing failed: {e}")
                
                try:
                    screenshot_path = f"/tmp/typing_error_{int(time.time())}.png"
                    self.driver.save_screenshot(screenshot_path)
                    logger.info(f"📸 Screenshot: {screenshot_path}")
                except:
                    pass
                
                return False
            
        except Exception as e:
            logger.error(f"❌ Input error: {str(e)}")
            import traceback
            logger.error(traceback.format_exc())
            return False
    
    def click_update_button(self) -> bool:
        """Click Update button in lead time modal"""
        try:
            logger.info("🔘 Looking for Update button...")
            
            update_selectors = [
                "//button[contains(text(), 'Update')]",
                "//button[text()='Update']",
                "//button[@type='button' and contains(., 'Update')]",
            ]
            
            button = None
            for selector in update_selectors:
                try:
                    button = WebDriverWait(self.driver, 5).until(
                        EC.element_to_be_clickable((By.XPATH, selector))
                    )
                    logger.info("✅ Found Update button")
                    break
                except TimeoutException:
                    continue
            
            if button is None:
                logger.warning("⚠️ Update button not found")
                return False
            
            self.scroll_to(button)
            time.sleep(0.3)  # ✅ OPTIMIZED: Reduced from 0.5-1s
            
            try:
                button.click()
            except:
                self.driver.execute_script("arguments[0].click();", button)
            
            logger.info("✅ Clicked Update button")
            
            time.sleep(2)  # ✅ OPTIMIZED: Reduced from 5-8s
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Update button error: {str(e)}")
            return False
    
    def extract_table(self) -> List[Dict[str, any]]:
        """Extract lead time table"""
        try:
            logger.info("📊 Extracting table...")
            
            try:
                self.wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, "table")))
            except TimeoutException:
                logger.warning("⚠️ No tables found")
                return []
            
            time.sleep(1)  # ✅ OPTIMIZED: Reduced from 2-3s
            
            lead_time_data = []
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            tables = soup.find_all('table')
            
            logger.info(f"Found {len(tables)} tables")
            
            for table_idx, table in enumerate(tables):
                try:
                    rows = table.find_all('tr')
                    
                    if len(rows) < 2:
                        continue
                    
                    logger.info(f"Processing table {table_idx} with {len(rows)} rows")
                    
                    for row_idx, row in enumerate(rows[1:]):
                        cells = row.find_all(['td', 'th'])
                        
                        if len(cells) >= 2:
                            try:
                                qty_text = cells[0].get_text().strip()
                                qty = int(re.sub(r'[^\d]', '', qty_text))
                                
                                date_text = cells[1].get_text().strip()
                                ship_date = self.parse_date(date_text)
                                
                                if qty > 0 and ship_date:
                                    lead_time_data.append({
                                        'qty': qty,
                                        'ship_date': ship_date,
                                        'raw_text': f"QTY: {qty}, Date: {date_text}"
                                    })
                                    logger.info(f"✅ Found: {qty:,} on {ship_date}")
                                    
                            except (ValueError, IndexError, AttributeError) as e:
                                logger.debug(f"Row parse error: {str(e)}")
                                continue
                    
                    if lead_time_data:
                        break
                        
                except Exception as e:
                    logger.debug(f"Table error: {str(e)}")
                    continue
            
            if not lead_time_data:
                logger.warning("⚠️ No data extracted")
            else:
                logger.info(f"✅ Extracted {len(lead_time_data)} entries")
            
            return lead_time_data
            
        except Exception as e:
            logger.error(f"❌ Extraction error: {str(e)}")
            return []
    
    def parse_date(self, date_str: str) -> Optional[str]:
        """Parse date"""
        if not date_str:
            return None
        
        date_str = date_str.strip()
        
        formats = [
            "%d.%m.%Y",
            "%m/%d/%Y",
            "%d/%m/%Y",
            "%Y-%m-%d",
            "%d-%m-%Y",
            "%B %d, %Y",
            "%d %B %Y",
        ]
        
        for fmt in formats:
            try:
                parsed = datetime.strptime(date_str, fmt)
                return parsed.strftime("%d.%m.%Y")
            except ValueError:
                continue
        
        return None
    
    def scrape_part(self, part_number: str) -> Dict[str, any]:
        """Main scraping workflow"""
        result = {
            'part_number': part_number,
            'success': False,
            'in_stock': False,
            'current_quantity': 0,
            'lead_times': [],
            'error': None,
            'timestamp': datetime.now().isoformat()
        }
        
        try:
            if not self.search_part(part_number):
                result['error'] = "Part not found"
                return result
            
            if not self.navigate_to_product(part_number):
                result['error'] = "Navigation failed"
                return result
            
            stock = self.check_stock()
            result['in_stock'] = stock['in_stock']
            result['current_quantity'] = stock['quantity']
            
            if stock['in_stock']:
                result['success'] = True
                logger.info(f"✅ {part_number}: In stock")
                return result
            
            if not self.click_lead_time():
                result['error'] = "Could not click lead time"
                return result
            
            if not self.enter_quantity():
                result['error'] = "Could not enter quantity"
                return result
            
            if not self.click_update_button():
                result['error'] = "Could not click Update button"
                return result
            
            lead_times = self.extract_table()
            result['lead_times'] = lead_times
            result['success'] = True if lead_times else False
            
            if lead_times:
                logger.info(f"✅ Successfully scraped {part_number}")
            else:
                result['error'] = "No lead time data"
            
            return result
            
        except Exception as e:
            logger.error(f"❌ Scrape error: {str(e)}")
            result['error'] = str(e)
            return result
    
    def close(self):
        """Close driver"""
        if self.driver:
            try:
                self.driver.quit()
                logger.info("✅ Driver closed")
            except:
                pass
    
    def print_results(self, result: Dict[str, any]):
        """Print results"""
        print("\n" + "="*70)
        print(f"PART NUMBER: {result['part_number']}")
        print("="*70)
        print(f"Status: {'✅ SUCCESS' if result['success'] else '❌ FAILED'}")
        print(f"Timestamp: {result['timestamp']}")
        print(f"In Stock: {'Yes' if result['in_stock'] else 'No'}")
        print(f"Current Quantity: {result['current_quantity']:,}")
        
        if result['error']:
            print(f"Error: {result['error']}")
        
        if result['lead_times']:
            print("\nLead Time Schedule:")
            print("-" * 70)
            print(f"{'QTY':<15} | {'Ship Date':<20}")
            print("-" * 70)
            for entry in result['lead_times']:
                print(f"{entry['qty']:<15,} | {entry['ship_date']:<20}")
        
        print("="*70 + "\n")



def main():
    """Main execution with summary - OPTIMIZED"""
    
    test_parts = [
        "AD5412AREZ",
        "ADXL355BEZ",
        "CLA4603-085LF"
    ]
    
    print("\n" + "="*70)
    print("🚀 Digikey Lead Time Scraper - OPTIMIZED ⚡")
    print("="*70)
    start_time = time.time()
    print(f"📅 Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"📦 Processing {len(test_parts)} parts")
    print("="*70 + "\n")
    
    scraper = None
    results = []
    
    try:
        scraper = DigikeyLeadTimeScraper(headless=False)
        scraper.setup_driver()  # ✅ SETUP ONCE
        
        for idx, part_number in enumerate(test_parts):
            result = scraper.scrape_part(part_number)
            results.append(result)
            scraper.print_results(result)
            
            if idx < len(test_parts) - 1:
                logger.info("⏳ Waiting...")
                time.sleep(0.5)  # ✅ OPTIMIZED: Reduced from 1s
    except KeyboardInterrupt:
        logger.warning("⚠️ Interrupted")
    except Exception as e:
        logger.error(f"❌ Fatal: {str(e)}")
    finally:
        if scraper:
            scraper.close()
    
    # ✅ SUMMARY TABLE
    elapsed = time.time() - start_time
    successful = sum(1 for r in results if r['success'])
    failed = len(results) - successful
    
    print("\n" + "="*70)
    print("📊 EXECUTION SUMMARY")
    print("="*70)
    print(f"✅ Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"⏱️  Total time: {elapsed:.1f}s ({elapsed/60:.1f} minutes)")
    if len(test_parts) > 0:
        print(f"📈 Average per part: {elapsed/len(test_parts):.1f}s")
    print(f"✅ Successful: {successful}/{len(test_parts)}")
    print(f"❌ Failed: {failed}/{len(test_parts)}")
    if elapsed > 0:
        print(f"🚀 Speed improvement: ~{253/elapsed:.1f}x faster!")
    print("="*70 + "\n")
    
    # ✅ RESULTS TABLE
    print("📋 DETAILED RESULTS TABLE")
    print("="*70)
    print(f"{'Part Number':<20} | {'Status':<10} | {'Stock':<8} | {'Lead Times':<12}")
    print("-"*70)
    
    for result in results:
        status = "✅ SUCCESS" if result['success'] else "❌ FAILED"
        stock = f"{result['current_quantity']:,}" if result['current_quantity'] > 0 else "Out"
        lead_count = len(result['lead_times']) if result['lead_times'] else 0
        
        print(f"{result['part_number']:<20} | {status:<10} | {stock:<8} | {lead_count} entries")
    
    print("="*70 + "\n")
    
    # ✅ LEAD TIMES SUMMARY - ALL ENTRIES
    print("📦 LEAD TIME SUMMARY")
    print("="*70)
    
    for result in results:
        if result['lead_times']:
            print(f"\n{result['part_number']}:")
            print(f"  Total entries: {len(result['lead_times'])}")
            print(f"  {'#':<3} | {'QTY':<15} | {'Ship Date':<12}")
            print(f"  {'-'*3}-+-{'-'*15}-+-{'-'*12}")
            
            for idx, entry in enumerate(result['lead_times'], start=1):
                print(f"  {idx:<3} | {entry['qty']:<15,} | {entry['ship_date']:<12}")
        else:
            print(f"\n{result['part_number']}: No lead time data")
    
    print("\n" + "="*70 + "\n")


if __name__ == "__main__":
    main()