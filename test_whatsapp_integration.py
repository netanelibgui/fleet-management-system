#!/usr/bin/env python3
"""
WhatsApp Integration Test Script
Tests all major functionality of the WhatsApp driver.
"""

import time
import logging
import os
from datetime import datetime
from pathlib import Path

from whatsapp_driver import WhatsAppDriver, WhatsAppMessage

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def test_connection_and_login():
    """Test WhatsApp Web connection and login process."""
    print("\n🧪 TEST 1: Connection and Login")
    print("=" * 50)
    
    driver = WhatsAppDriver(headless=False)  # Use GUI for QR code scanning
    
    try:
        success = driver.connect_to_whatsapp()
        if success:
            print("✅ PASS: Successfully connected to WhatsApp Web")
            return driver
        else:
            print("❌ FAIL: Could not connect to WhatsApp Web")
            return None
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return None

def test_element_detection(driver: WhatsAppDriver):
    """Test element detection with fallback selectors."""
    print("\n🧪 TEST 2: Element Detection")
    print("=" * 50)
    
    test_results = []
    
    # Test key elements
    elements_to_test = [
        ("search_box", "Search Box"),
        ("message_input", "Message Input"),
        ("send_button", "Send Button"),
        ("messages", "Messages Container")
    ]
    
    for element_key, description in elements_to_test:
        try:
            element = driver.find_element_with_fallback(element_key, timeout=5)
            if element:
                print(f"✅ PASS: {description} found")
                test_results.append(True)
            else:
                print(f"❌ FAIL: {description} not found")
                test_results.append(False)
        except Exception as e:
            print(f"❌ ERROR: {description} - {e}")
            test_results.append(False)
    
    success_rate = sum(test_results) / len(test_results)
    print(f"\n📊 Element Detection Success Rate: {success_rate:.1%}")
    
    return success_rate > 0.75  # 75% success rate required

def test_search_functionality(driver: WhatsAppDriver):
    """Test contact search functionality."""
    print("\n🧪 TEST 3: Contact Search")
    print("=" * 50)
    
    # Test with a placeholder contact name
    test_contact = input("Enter a contact name to test search (or press Enter to skip): ").strip()
    
    if not test_contact:
        print("⏭️  SKIP: Contact search test skipped")            
        return True
    
    try:
        # Test search box interaction
        search_box = driver.find_element_with_fallback("search_box")
        if not search_box:
            print("❌ FAIL: Could not find search box")
            return False
        
        # Clear and type
        search_box.clear()
        search_box.send_keys(test_contact)
        time.sleep(2)
        
        print("✅ PASS: Search functionality works")
        
        # Clear search
        search_box.clear()
        time.sleep(1)
        
        return True
        
    except Exception as e:
        print(f"❌ ERROR: Search test failed - {e}")
        return False

def test_message_sending(driver: WhatsAppDriver):
    """Test message sending functionality."""
    print("\n🧪 TEST 4: Message Sending")
    print("=" * 50)
    
    test_contact = input("Enter a contact name to test messaging (or press Enter to skip): ").strip()
    
    if not test_contact:
        print("⏭️  SKIP: Message sending test skipped")
        return True
    
    test_message = "🤖 This is a test message from the Personal Coaching Assistant!\n\nIf you received this, the WhatsApp integration is working perfectly! ✨"
    
    try:
        # Send test message
        success = driver.send_message(test_contact, test_message)
        
        if success:
            print("✅ PASS: Message sent successfully")
            return True
        else:
            print("❌ FAIL: Message sending failed")
            return False
            
    except Exception as e:
        print(f"❌ ERROR: Message sending test failed - {e}")
        return False

def test_message_reading(driver: WhatsAppDriver):
    """Test message reading functionality."""
    print("\n🧪 TEST 5: Message Reading")
    print("=" * 50)
    
    try:
        # Test getting new messages
        messages = driver.get_new_messages()
        
        print(f"📨 Found {len(messages)} new messages")
        
        if messages:
            for i, msg in enumerate(messages[:3], 1):  # Show max 3 messages
                print(f"  {i}. From: {msg.sender}")
                print(f"     Text: {msg.text[:50]}...")
                print(f"     Time: {msg.timestamp}")
                print()
            
        print("✅ PASS: Message reading functionality works")
        return True
        
    except Exception as e:
        print(f"❌ ERROR: Message reading test failed - {e}")
        return False

def test_session_persistence(driver: WhatsAppDriver):
    """Test session persistence functionality."""
    print("\n🧪 TEST 6: Session Persistence")
    print("=" * 50)
    
    try:
        # Check login status
        is_logged_in = driver.is_logged_in()
        
        if is_logged_in:
            print("✅ PASS: Session persistence working - still logged in")
            return True
        else:
            print("❌ FAIL: Session lost or not persistent")
            return False
            
    except Exception as e:
        print(f"❌ ERROR: Session persistence test failed - {e}")
        return False

def test_error_handling(driver: WhatsAppDriver):
    """Test error handling and recovery."""
    print("\n🧪 TEST 7: Error Handling")
    print("=" * 50)
    
    try:
        # Test with non-existent contact
        result = driver.send_message("NonExistentContact12345", "Test message")
        
        if not result:
            print("✅ PASS: Properly handled non-existent contact")
        else:
            print("⚠️  WARNING: Message sent to non-existent contact (unexpected)")
        
        # Test connection refresh
        refresh_success = driver.refresh_connection()
        
        if refresh_success:
            print("✅ PASS: Connection refresh works")
        else:
            print("❌ FAIL: Connection refresh failed")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ ERROR: Error handling test failed - {e}")
        return False

def run_comprehensive_test():
    """Run all WhatsApp integration tests."""
    print("🚀 Personal Coaching Assistant - WhatsApp Integration Test Suite")
    print("=" * 70)
    print(f"📅 Test Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🖥️  Platform: Windows")
    print(f"🌐 Target: WhatsApp Web")
    print()
    
    # Track test results
    test_results = []
    driver = None
    
    try:
        # Test 1: Connection and Login
        driver = test_connection_and_login()
        test_results.append(("Connection & Login", driver is not None))
        
        if not driver:
            print("\n❌ CRITICAL: Cannot proceed without successful connection")
            return False
        
        # Test 2: Element Detection
        element_success = test_element_detection(driver)
        test_results.append(("Element Detection", element_success))
        
        # Test 3: Search Functionality
        search_success = test_search_functionality(driver)
        test_results.append(("Contact Search", search_success))
        
        # Test 4: Message Sending
        send_success = test_message_sending(driver)
        test_results.append(("Message Sending", send_success))
        
        # Test 5: Message Reading
        read_success = test_message_reading(driver)
        test_results.append(("Message Reading", read_success))
        
        # Test 6: Session Persistence
        session_success = test_session_persistence(driver)
        test_results.append(("Session Persistence", session_success))
        
        # Test 7: Error Handling
        error_success = test_error_handling(driver)
        test_results.append(("Error Handling", error_success))
        
    except KeyboardInterrupt:
        print("\n⏹️  Tests interrupted by user")
        return False
    
    finally:
        # Clean up
        if driver:
            driver.close()
            print("\n🧹 WebDriver session closed")
    
    # Generate test report
    print("\n" + "=" * 70)
    print("📋 WHATSAPP INTEGRATION TEST REPORT")
    print("=" * 70)
    
    passed_tests = 0
    total_tests = len(test_results)
    
    for test_name, success in test_results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"   {test_name:<20}: {status}")
        if success:
            passed_tests += 1
    
    success_rate = passed_tests / total_tests if total_tests > 0 else 0
    
    print(f"\n📊 OVERALL RESULTS:")
    print(f"   Tests Passed: {passed_tests}/{total_tests}")
    print(f"   Success Rate: {success_rate:.1%}")
    
    if success_rate >= 0.85:  # 85% success rate
        print(f"\n🎉 EXCELLENT! WhatsApp integration is ready for production!")
        print("🔜 Next steps:")
        print("   1. Integrate with LLM coaching responses")
        print("   2. Build message processing pipeline")
        print("   3. Add automatic response triggers")
    elif success_rate >= 0.70:  # 70% success rate
        print(f"\n✅ GOOD! WhatsApp integration is mostly working.")
        print("⚠️  Some issues may need attention before full deployment.")
    else:
        print(f"\n❌ NEEDS WORK! Several critical issues need to be resolved.")
        print("🔧 Review failed tests and update selectors/logic as needed.")
    
    return success_rate >= 0.70

if __name__ == "__main__":
    print("⚠️  IMPORTANT NOTES:")
    print("   • Make sure Chrome/Chromium is installed")
    print("   • WhatsApp Web will open in a browser window")
    print("   • You may need to scan QR code to log in")
    print("   • Have a test contact ready for messaging tests")
    print("   • Tests are non-destructive and won't spam contacts")
    print()
    
    input("Press Enter to continue with the tests...")
    
    success = run_comprehensive_test()
    
    print(f"\n🏁 Test suite completed: {'SUCCESS' if success else 'NEEDS ATTENTION'}")
    exit(0 if success else 1) 