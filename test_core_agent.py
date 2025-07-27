#!/usr/bin/env python3
"""
Core Agent Logic Test Script
Tests the complete coaching assistant pipeline from message input to response.
"""

import time
import logging
from datetime import datetime
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def test_intent_classification():
    """Test the intent classification system."""
    print("\n🧠 TEST 1: Intent Classification")
    print("=" * 50)
    
    try:
        from intent_classifier import IntentClassifier
        classifier = IntentClassifier()
        
        test_messages = [
            ("I feel overwhelmed and stressed", "emotional"),
            ("How should I organize my schedule?", "practical"),
            ("What's my purpose in life?", "reflective"),
            ("I'm stuck and can't get started", "motivational"),
            ("Had an argument with my friend", "social"),
            ("Should I take this job or not?", "decision"),
            ("I completed my project today!", "progress"),
            ("Hello, how are you?", "general")
        ]
        
        correct_predictions = 0
        total_tests = len(test_messages)
        
        for message, expected_intent in test_messages:
            result = classifier.classify_intent(message)
            actual_intent = result.intent.value
            is_correct = actual_intent == expected_intent
            
            status = "✅" if is_correct else "❌"
            print(f"{status} '{message}' -> {actual_intent} (expected: {expected_intent})")
            
            if is_correct:
                correct_predictions += 1
        
        accuracy = correct_predictions / total_tests
        print(f"\n📊 Intent Classification Accuracy: {accuracy:.1%} ({correct_predictions}/{total_tests})")
        
        return accuracy >= 0.75  # 75% accuracy threshold
        
    except Exception as e:
        print(f"❌ Intent classification test failed: {e}")
        return False

def test_llm_client():
    """Test the LLM client functionality."""
    print("\n🤖 TEST 2: LLM Client")
    print("=" * 50)
    
    try:
        from llm_client import LLMClient, CoachingContext
        from intent_classifier import MessageIntent
        
        client = LLMClient()
        
        # Test model connection
        model_info = client.get_model_info()
        print(f"📋 Model Status: {model_info.get('status', 'Unknown')}")
        
        if model_info.get('status') != 'Available':
            print("⚠️ Model not available - testing fallback responses only")
            return test_fallback_responses(client)
        
        # Test coaching response generation
        test_context = CoachingContext(
            user_message="I'm feeling stuck with my goals and don't know what to do next",
            sender="TestUser",
            intent=MessageIntent.MOTIVATIONAL,
            confidence=0.9,
            personal_profile={
                "communication_style": {
                    "tone": "supportive",
                    "approach": "practical"
                }
            },
            conversation_history=[],
            relevant_principles=["Progress over perfection", "Small steps lead to big changes"],
            timestamp=datetime.now()
        )
        
        print("🔄 Generating coaching response...")
        start_time = time.time()
        response = client.generate_response(test_context)
        response_time = time.time() - start_time
        
        if response:
            print(f"✅ Response generated in {response_time:.1f}s")
            print(f"📝 Response: {response[:100]}...")
            
            # Check response quality
            word_count = len(response.split())
            has_encouragement = any(word in response.lower() 
                                  for word in ['can', 'able', 'possible', 'step', 'start', 'try'])
            
            print(f"📊 Analysis:")
            print(f"   - Word count: {word_count}")
            print(f"   - Contains encouragement: {'✅' if has_encouragement else '❌'}")
            
            return word_count > 20 and has_encouragement
        else:
            print("❌ No response generated")
            return False
            
    except Exception as e:
        print(f"❌ LLM client test failed: {e}")
        return False

def test_fallback_responses(client):
    """Test fallback responses when LLM is unavailable."""
    print("🔄 Testing fallback responses...")
    
    try:
        from llm_client import CoachingContext
        from intent_classifier import MessageIntent
        
        intents_to_test = [
            MessageIntent.EMOTIONAL,
            MessageIntent.PRACTICAL,
            MessageIntent.MOTIVATIONAL
        ]
        
        for intent in intents_to_test:
            context = CoachingContext(
                user_message="Test message",
                sender="TestUser",
                intent=intent,
                confidence=0.8,
                personal_profile={},
                conversation_history=[],
                relevant_principles=[],
                timestamp=datetime.now()
            )
            
            fallback = client.generate_fallback_response(context)
            if fallback and len(fallback) > 20:
                print(f"✅ {intent.value} fallback: {fallback[:50]}...")
            else:
                print(f"❌ {intent.value} fallback failed")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ Fallback test failed: {e}")
        return False

def test_main_loop_integration():
    """Test the main loop integration."""
    print("\n🔄 TEST 3: Main Loop Integration")
    print("=" * 50)
    
    try:
        from main_loop import PersonalCoachingAssistant
        
        # Initialize coaching assistant
        print("🚀 Initializing Personal Coaching Assistant...")
        assistant = PersonalCoachingAssistant()
        
        # Test component initialization
        if not assistant.initialize_components():
            print("❌ Component initialization failed")
            return False
        
        print("✅ Components initialized successfully")
        
        # Test message processing
        test_messages = [
            "I'm feeling really overwhelmed with work",
            "How can I better organize my daily tasks?",
            "I completed my morning routine today!"
        ]
        
        successful_responses = 0
        
        for i, message in enumerate(test_messages, 1):
            print(f"\n📨 Test Message {i}: '{message}'")
            
            try:
                response = assistant.process_message(message, "TestUser")
                
                if response and len(response) > 10:
                    print(f"✅ Response: {response[:80]}...")
                    successful_responses += 1
                else:
                    print("❌ No valid response generated")
                    
            except Exception as e:
                print(f"❌ Error processing message: {e}")
        
        success_rate = successful_responses / len(test_messages)
        print(f"\n📊 Message Processing Success Rate: {success_rate:.1%}")
        
        # Test conversation history
        history_length = len(getattr(assistant, 'conversation_history', []))
        print(f"💭 Conversation History: {history_length} entries")
        
        return success_rate >= 0.67  # 2/3 success rate
        
    except Exception as e:
        print(f"❌ Main loop integration test failed: {e}")
        return False

def test_profile_integration():
    """Test profile integration with coaching responses."""
    print("\n👤 TEST 4: Profile Integration")
    print("=" * 50)
    
    try:
        # Check if profile.json exists
        profile_path = Path("profile.json")
        if not profile_path.exists():
            print("⚠️ profile.json not found - skipping profile integration test")
            return True
        
        # Load profile
        import json
        with open(profile_path, 'r', encoding='utf-8') as f:
            profile = json.load(f)
        
        print(f"📋 Profile loaded with {len(profile)} sections")
        
        # Check key sections
        required_sections = ['communication_style', 'coaching_principles', 'personal_context']
        found_sections = [section for section in required_sections if section in profile]
        
        print(f"✅ Found sections: {found_sections}")
        
        # Test with main loop
        from main_loop import PersonalCoachingAssistant
        assistant = PersonalCoachingAssistant()
        
        if assistant.initialize_components():
            # Check if profile was loaded
            loaded_profile = getattr(assistant, 'profile', {})
            if loaded_profile:
                print("✅ Profile successfully integrated into assistant")
                return True
            else:
                print("❌ Profile not integrated into assistant")
                return False
        else:
            print("❌ Assistant initialization failed")
            return False
            
    except Exception as e:
        print(f"❌ Profile integration test failed: {e}")
        return False

def test_error_handling():
    """Test error handling and graceful degradation."""
    print("\n🛡️ TEST 5: Error Handling")
    print("=" * 50)
    
    try:
        from main_loop import PersonalCoachingAssistant
        assistant = PersonalCoachingAssistant()
        
        # Test with invalid/edge case inputs
        edge_cases = [
            "",  # Empty message
            "a" * 1000,  # Very long message
            "🎉🎈🎊" * 10,  # Only emojis
            None,  # None input (will cause error but should be handled)
        ]
        
        handled_cases = 0
        
        for i, test_input in enumerate(edge_cases[:-1], 1):  # Skip None test for now
            try:
                response = assistant.process_message(test_input, "TestUser")
                if response:
                    print(f"✅ Edge case {i} handled gracefully")
                    handled_cases += 1
                else:
                    print(f"⚠️ Edge case {i} returned no response")
                    handled_cases += 0.5  # Partial credit
            except Exception as e:
                print(f"❌ Edge case {i} caused error: {e}")
        
        # Test fallback when LLM is unavailable
        try:
            from llm_client import LLMClient, CoachingContext
            from intent_classifier import MessageIntent
            
            # Create a client with invalid URL to test fallback
            client = LLMClient(ollama_url="http://invalid:9999")
            
            context = CoachingContext(
                user_message="Test message",
                sender="TestUser",
                intent=MessageIntent.GENERAL,
                confidence=0.8,
                personal_profile={},
                conversation_history=[],
                relevant_principles=[],
                timestamp=datetime.now()
            )
            
            fallback = client.generate_fallback_response(context)
            if fallback:
                print("✅ Fallback response works when LLM unavailable")
                handled_cases += 1
            else:
                print("❌ Fallback response failed")
                
        except Exception as e:
            print(f"⚠️ Fallback test error: {e}")
        
        success_rate = handled_cases / 4  # 4 total tests
        print(f"\n📊 Error Handling Success Rate: {success_rate:.1%}")
        
        return success_rate >= 0.75
        
    except Exception as e:
        print(f"❌ Error handling test failed: {e}")
        return False

def run_comprehensive_test():
    """Run all core agent tests."""
    print("🚀 Personal Coaching Assistant - Core Agent Logic Test Suite")
    print("=" * 70)
    print(f"📅 Test Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🎯 Testing: Intent Classification, LLM Client, Main Loop, Profile Integration")
    print()
    
    # Track test results
    test_results = []
    
    try:
        # Test 1: Intent Classification
        intent_success = test_intent_classification()
        test_results.append(("Intent Classification", intent_success))
        
        # Test 2: LLM Client
        llm_success = test_llm_client()
        test_results.append(("LLM Client", llm_success))
        
        # Test 3: Main Loop Integration
        main_loop_success = test_main_loop_integration()
        test_results.append(("Main Loop Integration", main_loop_success))
        
        # Test 4: Profile Integration
        profile_success = test_profile_integration()
        test_results.append(("Profile Integration", profile_success))
        
        # Test 5: Error Handling
        error_handling_success = test_error_handling()
        test_results.append(("Error Handling", error_handling_success))
        
    except KeyboardInterrupt:
        print("\n⏹️ Tests interrupted by user")
        return False
    
    # Generate test report
    print("\n" + "=" * 70)
    print("📋 CORE AGENT LOGIC TEST REPORT")
    print("=" * 70)
    
    passed_tests = 0
    total_tests = len(test_results)
    
    for test_name, success in test_results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"   {test_name:<25}: {status}")
        if success:
            passed_tests += 1
    
    success_rate = passed_tests / total_tests if total_tests > 0 else 0
    
    print(f"\n📊 OVERALL RESULTS:")
    print(f"   Tests Passed: {passed_tests}/{total_tests}")
    print(f"   Success Rate: {success_rate:.1%}")
    
    if success_rate >= 0.80:  # 80% success rate
        print(f"\n🎉 EXCELLENT! Core agent logic is ready for integration!")
        print("🔜 Next steps:")
        print("   1. Connect with WhatsApp messaging")
        print("   2. Add RAG knowledge base")
        print("   3. Implement task/reminder system")
    elif success_rate >= 0.60:  # 60% success rate
        print(f"\n✅ GOOD! Core agent logic is mostly working.")
        print("⚠️ Some components may need attention before full deployment.")
    else:
        print(f"\n❌ NEEDS WORK! Several critical issues need to be resolved.")
        print("🔧 Review failed tests and fix core logic issues.")
    
    return success_rate >= 0.60

if __name__ == "__main__":
    print("⚠️ IMPORTANT NOTES:")
    print("   • Make sure Ollama is running with Mistral model")
    print("   • Ensure all dependencies are installed")
    print("   • profile.json should exist for full testing")
    print("   • This tests the core agent logic without WhatsApp")
    print()
    
    input("Press Enter to start core agent tests...")
    
    success = run_comprehensive_test()
    
    print(f"\n🏁 Core agent test suite completed: {'SUCCESS' if success else 'NEEDS ATTENTION'}")
    exit(0 if success else 1) 