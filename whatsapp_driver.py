#!/usr/bin/env python3
"""
WhatsApp Driver - Handles WhatsApp Web automation
Sends and receives WhatsApp messages via Selenium WebDriver.
Updated with 2024/2025 modern selectors and anti-detection techniques.
"""

import time
import logging
import json
import os
from datetime import datetime
from typing import List, Optional, Dict, Any
from dataclasses import dataclass
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
from webdriver_manager.chrome import ChromeDriverManager

@dataclass
class WhatsAppMessage:
    """Represents a WhatsApp message."""
    sender: str
    text: str
    timestamp: datetime
    message_id: str = ""
    is_group: bool = False
    group_name: str = ""

class WhatsAppDriver:
    """
    Handles WhatsApp Web automation using Selenium.
    Modern implementation with 2024/2025 selectors and anti-detection techniques.
    """
    
    def __init__(self, headless: bool = False, session_path: str = "whatsapp_session"):
        """
        Initialize WhatsApp driver.
        
        Args:
            headless: Run browser in headless mode
            session_path: Path to store browser session data
        """
        self.headless = headless
        self.session_path = Path(session_path)
        self.session_path.mkdir(exist_ok=True)
        
        self.driver = None
        self.wait = None
        self.logged_in = False
        self.last_message_check = datetime.now()
        
        self.logger = logging.getLogger(__name__)
        
        # Modern selectors with fallbacks (2024/2025)
        self.selectors = {
            # QR Code and Login
            "qr_code": [
                '[data-testid="qr-code"]',
                'canvas[aria-label*="qr"]',
                'canvas[aria-label*="Scan"]'
            ],
            "login_area": [
                '[data-testid="landing-wrapper"]',
                '.landing-window'
            ],
            
            # Search and Chat Navigation
            "search_box": [
                '[data-testid="chat-list-search"]',
                'div[contenteditable="true"][data-tab="3"]',
                'div[role="textbox"][placeholder*="Search"]'
            ],
            "chat_list": [
                '[data-testid="chat-list"]',
                '[data-testid="conversation-list"]',
                '.app-wrapper-web ._3uMse'
            ],
            
            # Message Composition
            "message_input": [
                '[data-testid="conversation-compose-box-input"]',
                'div[contenteditable="true"][data-tab="10"]',
                'div[role="textbox"][contenteditable="true"]',
                'div[title*="Type a message"]'
            ],
            "send_button": [
                '[data-testid="compose-btn-send"]',
                'button[data-tab="11"]',
                'span[data-testid="send"]',
                'button[aria-label*="Send"]'
            ],
            
            # Message Display
            "messages": [
                '[data-testid="message-list"]',
                '[data-testid="conversation-panel-messages"]',
                'div[role="application"]'
            ],
            "message_text": [
                '[data-testid="selectable-text"]',
                'span.selectable-text',
                '.message-text'
            ],
            
            # Contact and Chat
            "contact_title": [
                '[data-testid="conversation-info-header-chat-title"]',
                'span[title][dir="auto"]',
                '.chat-title'
            ],
            "new_message_indicator": [
                '[data-testid="unread-indicator"]',
                '.unread-count',
                '._38M1B'
            ]
        }
    
    def setup_driver(self) -> bool:
        """
        Set up Chrome WebDriver with modern anti-detection options.
        
        Returns:
            True if setup successful, False otherwise
        """
        try:
            chrome_options = Options()
            
            # Session persistence (avoids repeated QR scanning)
            chrome_options.add_argument(f"--user-data-dir={self.session_path}")
            chrome_options.add_argument("--profile-directory=coaching_bot_profile")
            
            # Anti-detection measures (2024/2025)
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            chrome_options.add_argument("--disable-extensions")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--no-first-run")
            chrome_options.add_argument("--no-default-browser-check")
            chrome_options.add_argument("--disable-default-apps")
            
            # User agent to appear more human
            chrome_options.add_argument(
                "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
            )
            
            # Disable automation indicators
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            
            # Headless mode if requested
            if self.headless:
                chrome_options.add_argument("--headless=new")  # Use new headless mode
                chrome_options.add_argument("--disable-gpu")
            
            # Window size for consistent behavior
            chrome_options.add_argument("--window-size=1920,1080")
            
            # Install and setup ChromeDriver automatically
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            
            # Additional anti-detection measures
            self.driver.execute_script(
                "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
            )
            self.driver.execute_cdp_cmd('Network.setUserAgentOverride', {
                "userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                            '(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
            })
            
            # Set up WebDriverWait
            self.wait = WebDriverWait(self.driver, 20)
            
            self.logger.info("✓ WebDriver setup completed with modern anti-detection measures")
            return True
            
        except Exception as e:
            self.logger.error(f"Error setting up WebDriver: {e}")
            return False
    
    def find_element_with_fallback(self, selector_key: str, timeout: int = 10):
        """
        Find element using fallback selectors.
        
        Args:
            selector_key: Key from self.selectors
            timeout: Maximum time to wait
            
        Returns:
            WebElement or None if not found
        """
        selectors = self.selectors.get(selector_key, [])
        if isinstance(selectors, str):
            selectors = [selectors]
            
        for selector in selectors:
            try:
                element = WebDriverWait(self.driver, timeout).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                )
                self.logger.debug(f"Found element with selector: {selector}")
                return element
            except TimeoutException:
                continue
                
        self.logger.warning(f"Could not find element for key: {selector_key}")
        return None

    def connect_to_whatsapp(self) -> bool:
        """
        Connect to WhatsApp Web and handle authentication.
        
        Returns:
            True if connected successfully, False otherwise
        """
        try:
            if not self.setup_driver():
                return False
            
            self.logger.info("Connecting to WhatsApp Web...")
            self.driver.get("https://web.whatsapp.com")
            
            # Add some human-like delay
            time.sleep(2)
            
            # Check if already logged in by looking for search box
            search_box = self.find_element_with_fallback("search_box", timeout=5)
            
            if search_box:
                self.logged_in = True
                self.logger.info("✓ Already logged in to WhatsApp Web")
                return True
            
            # Need to scan QR code
            self.logger.info("Waiting for QR code login...")
            qr_code = self.find_element_with_fallback("qr_code", timeout=10)
            
            if qr_code:
                self.logger.info("📱 QR Code detected! Please scan with your WhatsApp mobile app")
                self.logger.info("   1. Open WhatsApp on your phone")
                self.logger.info("   2. Go to Settings > Linked Devices")
                self.logger.info("   3. Tap 'Link a Device'")
                self.logger.info("   4. Scan the QR code displayed in the browser")
                
                # Wait for successful login (search box appears)
                search_box = self.find_element_with_fallback("search_box", timeout=60)
                
                if search_box:
                    self.logged_in = True
                    self.logger.info("✓ Successfully logged in to WhatsApp Web")
                    time.sleep(3)  # Allow interface to fully load
                    return True
                else:
                    self.logger.error("Login timeout - QR code may have expired")
                    return False
            else:
                self.logger.error("Could not find QR code or login interface")
                return False
            
        except Exception as e:
            self.logger.error(f"Error connecting to WhatsApp Web: {e}")
            return False
    
    def search_and_open_chat(self, contact: str) -> bool:
        """
        Search for a contact and open their chat.
        
        Args:
            contact: Contact name or phone number
            
        Returns:
            True if chat opened successfully, False otherwise
        """
        try:
            # Find and clear search box
            search_box = self.find_element_with_fallback("search_box")
            if not search_box:
                self.logger.error("Could not find search box")
                return False
            
            # Clear any existing search
            search_box.click()
            search_box.clear()
            time.sleep(0.5)
            
            # Type contact name
            search_box.send_keys(contact)
            time.sleep(2)  # Allow search results to load
            
            # Look for the contact in search results
            # Try multiple methods to find the contact
            contact_selectors = [
                f'span[title="{contact}"]',
                f'span[title*="{contact}"]',
                f'div[title="{contact}"]',
                f'//span[contains(text(), "{contact}")]'
            ]
            
            contact_element = None
            for selector in contact_selectors:
                try:
                    if selector.startswith('//'):
                        contact_element = self.driver.find_element(By.XPATH, selector)
                    else:
                        contact_element = self.driver.find_element(By.CSS_SELECTOR, selector)
                    break
                except NoSuchElementException:
                    continue
            
            if contact_element:
                contact_element.click()
                time.sleep(1)
                self.logger.info(f"✓ Opened chat with {contact}")
                return True
            else:
                self.logger.error(f"Contact '{contact}' not found in search results")
                return False
                
        except Exception as e:
            self.logger.error(f"Error searching for contact {contact}: {e}")
            return False

    def send_message(self, contact: str, message: str) -> bool:
        """
        Send a message to a specific contact.
        
        Args:
            contact: Contact name or phone number
            message: Message text to send
            
        Returns:
            True if message sent successfully, False otherwise
        """
        try:
            if not self.logged_in:
                self.logger.error("Not logged in to WhatsApp Web")
                return False
            
            # Search and open chat
            if not self.search_and_open_chat(contact):
                return False
            
            # Find message input
            message_input = self.find_element_with_fallback("message_input")
            if not message_input:
                self.logger.error("Could not find message input box")
                return False
            
            # Type message
            message_input.click()
            message_input.clear()
            
            # Handle multi-line messages
            lines = message.split('\n')
            for i, line in enumerate(lines):
                message_input.send_keys(line)
                if i < len(lines) - 1:  # Not the last line
                    message_input.send_keys(Keys.SHIFT + Keys.ENTER)
            
            time.sleep(0.5)  # Small delay before sending
            
            # Send message
            send_button = self.find_element_with_fallback("send_button")
            if send_button:
                send_button.click()
                time.sleep(1)
                self.logger.info(f"✓ Message sent to {contact}: {message[:50]}...")
                return True
            else:
                # Fallback: Press Enter to send
                message_input.send_keys(Keys.ENTER)
                time.sleep(1)
                self.logger.info(f"✓ Message sent to {contact} (fallback method): {message[:50]}...")
                return True
            
        except Exception as e:
            self.logger.error(f"Error sending message to {contact}: {e}")
            return False
    
    def get_latest_message_from_chat(self) -> Optional[WhatsAppMessage]:
        """
        Get the latest message from the currently open chat.
        
        Returns:
            WhatsAppMessage object or None if no message found
        """
        try:
            # Find all messages in the current chat
            message_container = self.find_element_with_fallback("messages")
            if not message_container:
                self.logger.error("Could not find message container")
                return None
            
            # Get all message elements - look for the last one
            message_elements = self.driver.find_elements(By.CSS_SELECTOR, 
                '[data-testid="msg-container"], .message-in, .message-out')
            
            if not message_elements:
                self.logger.warning("No messages found in chat")
                return None
            
            # Get the last message
            last_message_element = message_elements[-1]
            
            # Determine if message is from me or from contact
            is_from_me = 'message-out' in last_message_element.get_attribute('class') or \
                        'msg-container--from-me' in last_message_element.get_attribute('class')
            
            # Extract message text
            text_selectors = [
                '[data-testid="selectable-text"]',
                '.selectable-text',
                '.copyable-text'
            ]
            
            message_text = ""
            for selector in text_selectors:
                try:
                    text_element = last_message_element.find_element(By.CSS_SELECTOR, selector)
                    message_text = text_element.text.strip()
                    if message_text:
                        break
                except NoSuchElementException:
                    continue
            
            # Extract timestamp (simplified - current time for now)
            timestamp = datetime.now()
            
            # Try to get contact name from chat header
            contact_name = "Unknown"
            try:
                header_element = self.find_element_with_fallback("contact_title")
                if header_element:
                    contact_name = header_element.text.strip()
            except:
                pass
            
            message = WhatsAppMessage(
                text=message_text,
                sender=contact_name if not is_from_me else "Me",
                timestamp=timestamp,
                is_from_me=is_from_me
            )
            
            self.logger.debug(f"Retrieved message: {message_text[:50]}...")
            return message
            
        except Exception as e:
            self.logger.error(f"Error getting latest message: {e}")
            return None

    def get_new_messages(self) -> List[WhatsAppMessage]:
        """
        Retrieve new messages by checking chats with unread indicators.
        
        Returns:
            List of new WhatsAppMessage objects
        """
        new_messages = []
        
        try:
            if not self.logged_in:
                self.logger.error("Not logged in to WhatsApp Web")
                return new_messages
            
            # Find chats with unread message indicators
            unread_indicators = []
            for selector in self.selectors["new_message_indicator"]:
                try:
                    indicators = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    unread_indicators.extend(indicators)
                    if indicators:
                        break
                except:
                    continue
            
            if not unread_indicators:
                self.logger.debug("No unread messages found")
                return new_messages
            
            self.logger.info(f"Found {len(unread_indicators)} chats with unread messages")
            
            # Process each chat with unread messages
            for indicator in unread_indicators[:5]:  # Limit to 5 chats to avoid overwhelming
                try:
                    # Click on the chat (find parent chat element)
                    chat_element = indicator.find_element(By.XPATH, './ancestor::div[contains(@class, "chat") or @data-testid]')
                    chat_element.click()
                    time.sleep(1)
                    
                    # Get the latest message from this chat
                    latest_message = self.get_latest_message_from_chat()
                    if latest_message and not latest_message.is_from_me:
                        # Only add messages that are not from me and are newer than last check
                        if latest_message.timestamp > self.last_message_check:
                            new_messages.append(latest_message)
                    
                except Exception as e:
                    self.logger.warning(f"Error processing unread chat: {e}")
                    continue
            
            # Update last check time
            self.last_message_check = datetime.now()
            
            if new_messages:
                self.logger.info(f"Retrieved {len(new_messages)} new messages")
            
        except Exception as e:
            self.logger.error(f"Error retrieving new messages: {e}")
        
        return new_messages
    
    def get_contact_list(self) -> List[str]:
        """
        Get list of available contacts.
        
        Returns:
            List of contact names
        """
        try:
            # TODO: Implement contact list retrieval
            # contacts = []
            # chat_elements = self.driver.find_elements(By.CSS_SELECTOR, "[data-testid='cell-frame-title']")
            # for element in chat_elements:
            #     contacts.append(element.text)
            # return contacts
            
            return ["Contact 1", "Contact 2"]  # Placeholder
            
        except Exception as e:
            self.logger.error(f"Error getting contact list: {e}")
            return []
    
    def is_contact_online(self, contact: str) -> bool:
        """
        Check if a contact is currently online.
        
        Args:
            contact: Contact name to check
            
        Returns:
            True if contact is online, False otherwise
        """
        try:
            # TODO: Implement online status check
            # This would involve checking the contact's status in their chat
            return False  # Placeholder
            
        except Exception as e:
            self.logger.error(f"Error checking online status for {contact}: {e}")
            return False
    
    def send_image(self, contact: str, image_path: str, caption: str = "") -> bool:
        """
        Send an image to a specific contact.
        
        Args:
            contact: Contact name or phone number
            image_path: Path to the image file
            caption: Optional caption for the image
            
        Returns:
            True if image sent successfully, False otherwise
        """
        try:
            if not self.logged_in:
                self.logger.error("Not logged in to WhatsApp Web")
                return False
            
            if not os.path.exists(image_path):
                self.logger.error(f"Image file not found: {image_path}")
                return False
            
            # Search and open chat
            if not self.search_and_open_chat(contact):
                return False
            
            # Find attachment button (paperclip)
            attachment_selectors = [
                '[data-testid="attach-button"]',
                '[data-testid="clip"]',
                'span[data-icon="attach-menu"]',
                'span[data-icon="clip"]'
            ]
            
            attachment_button = None
            for selector in attachment_selectors:
                try:
                    attachment_button = self.driver.find_element(By.CSS_SELECTOR, selector)
                    break
                except NoSuchElementException:
                    continue
            
            if not attachment_button:
                self.logger.error("Could not find attachment button")
                return False
            
            attachment_button.click()
            time.sleep(1)
            
            # Find file input for images
            file_input_selectors = [
                'input[accept*="image"]',
                'input[type="file"]'
            ]
            
            file_input = None
            for selector in file_input_selectors:
                try:
                    file_input = self.driver.find_element(By.CSS_SELECTOR, selector)
                    break
                except NoSuchElementException:
                    continue
            
            if not file_input:
                self.logger.error("Could not find file input")
                return False
            
            # Upload the image
            file_input.send_keys(os.path.abspath(image_path))
            time.sleep(2)  # Wait for image to upload
            
            # Add caption if provided
            if caption:
                caption_selectors = [
                    '[data-testid="media-caption-input-container"] div[contenteditable="true"]',
                    'div[data-tab="10"][contenteditable="true"]'
                ]
                
                for selector in caption_selectors:
                    try:
                        caption_input = self.driver.find_element(By.CSS_SELECTOR, selector)
                        caption_input.send_keys(caption)
                        break
                    except NoSuchElementException:
                        continue
            
            # Find and click send button
            send_selectors = [
                '[data-testid="send-button"]',
                'span[data-icon="send"]',
                'button[data-tab="11"]'
            ]
            
            for selector in send_selectors:
                try:
                    send_button = self.driver.find_element(By.CSS_SELECTOR, selector)
                    send_button.click()
                    time.sleep(2)
                    self.logger.info(f"✓ Image sent to {contact}: {image_path}")
                    return True
                except NoSuchElementException:
                    continue
            
            self.logger.error("Could not find send button for image")
            return False
            
        except Exception as e:
            self.logger.error(f"Error sending image to {contact}: {e}")
            return False

    def is_logged_in(self) -> bool:
        """
        Check if still logged in to WhatsApp Web.
        
        Returns:
            True if logged in, False otherwise
        """
        try:
            if not self.driver:
                return False
                
            # Check for presence of search box (indicates logged in)
            search_box = self.find_element_with_fallback("search_box", timeout=3)
            logged_in = search_box is not None
            
            if not logged_in and self.logged_in:
                self.logger.warning("WhatsApp Web session expired")
                self.logged_in = False
            
            return logged_in
            
        except Exception as e:
            self.logger.error(f"Error checking login status: {e}")
            return False

    def refresh_connection(self) -> bool:
        """
        Refresh the WhatsApp Web connection.
        
        Returns:
            True if refreshed successfully, False otherwise
        """
        try:
            self.logger.info("Refreshing WhatsApp Web connection...")
            self.driver.refresh()
            time.sleep(3)
            
            # Check if we're still logged in
            if self.is_logged_in():
                self.logger.info("✓ Connection refreshed successfully")
                return True
            else:
                self.logger.warning("Need to re-authenticate after refresh")
                return self.connect_to_whatsapp()
                
        except Exception as e:
            self.logger.error(f"Error refreshing connection: {e}")
            return False

    def close(self):
        """Close the WebDriver and clean up resources."""
        try:
            if self.driver:
                self.driver.quit()
                self.logger.info("✓ WhatsApp driver closed")
        except Exception as e:
            self.logger.error(f"Error closing driver: {e}")
    
    def __enter__(self):
        """Context manager entry."""
        self.connect_to_whatsapp()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()

# Example usage and testing
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    # Test the WhatsApp driver (placeholder)
    driver = WhatsAppDriver()
    
    if driver.connect_to_whatsapp():
        print("WhatsApp driver initialized successfully!")
        
        # Test sending a message (placeholder)
        # driver.send_message("Test Contact", "Hello from the coaching assistant!")
        
        # Test getting messages (placeholder)
        # messages = driver.get_new_messages()
        # print(f"Retrieved {len(messages)} new messages")
    
    driver.close() 