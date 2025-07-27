#!/usr/bin/env python3
"""
Test script to verify Personal Coaching Assistant foundation setup.
"""

import json
import sys
from pathlib import Path
import pandas as pd

def test_project_structure():
    """Test that all required files and directories exist."""
    print("🔍 Testing project structure...")
    
    required_files = [
        "main_loop.py",
        "whatsapp_driver.py", 
        "profile.json",
        "reminders.xlsx",
        "requirements.txt",
        "README.md"
    ]
    
    required_dirs = [
        "embeddings",
        "logs", 
        "temp",
        "personal-coaching-env"
    ]
    
    missing_files = []
    missing_dirs = []
    
    for file in required_files:
        if not Path(file).exists():
            missing_files.append(file)
        else:
            print(f"  ✓ {file}")
    
    for dir_name in required_dirs:
        if not Path(dir_name).exists():
            missing_dirs.append(dir_name)
        else:
            print(f"  ✓ {dir_name}/")
    
    if missing_files or missing_dirs:
        print(f"  ❌ Missing files: {missing_files}")
        print(f"  ❌ Missing directories: {missing_dirs}")
        return False
    
    print("  ✅ All required files and directories present")
    return True

def test_profile_json():
    """Test that profile.json is valid and loadable."""
    print("\n🔍 Testing profile.json...")
    
    try:
        with open("profile.json", 'r', encoding='utf-8') as f:
            profile = json.load(f)
        
        # Check for required sections
        required_sections = [
            "metadata",
            "personality", 
            "coaching_principles",
            "response_templates",
            "behavioral_patterns",
            "personal_context",
            "conversation_rules",
            "time_based_behavior",
            "micro_actions_library"
        ]
        
        missing_sections = []
        for section in required_sections:
            if section not in profile:
                missing_sections.append(section)
            else:
                print(f"  ✓ {section}")
        
        if missing_sections:
            print(f"  ❌ Missing sections: {missing_sections}")
            return False
        
        print("  ✅ profile.json is valid and complete")
        return True
        
    except json.JSONDecodeError as e:
        print(f"  ❌ Invalid JSON format: {e}")
        return False
    except Exception as e:
        print(f"  ❌ Error loading profile.json: {e}")
        return False

def test_reminders_excel():
    """Test that reminders.xlsx is readable."""
    print("\n🔍 Testing reminders.xlsx...")
    
    try:
        df = pd.read_excel("reminders.xlsx")
        
        required_columns = [
            "Task",
            "Scheduled_Time", 
            "Message",
            "Status",
            "Created_Date",
            "User"
        ]
        
        missing_columns = []
        for col in required_columns:
            if col not in df.columns:
                missing_columns.append(col)
            else:
                print(f"  ✓ {col}")
        
        if missing_columns:
            print(f"  ❌ Missing columns: {missing_columns}")
            return False
        
        print(f"  ✅ reminders.xlsx is valid ({len(df)} rows)")
        return True
        
    except Exception as e:
        print(f"  ❌ Error reading reminders.xlsx: {e}")
        return False

def test_imports():
    """Test that core imports work."""
    print("\n🔍 Testing core imports...")
    
    imports_to_test = [
        ("pandas", "pd"),
        ("json", None),
        ("pathlib", "Path"),
        ("datetime", "datetime")
    ]
    
    failed_imports = []
    
    for module_name, alias in imports_to_test:
        try:
            if alias:
                exec(f"import {module_name} as {alias}")
            else:
                exec(f"import {module_name}")
            print(f"  ✓ {module_name}")
        except ImportError:
            failed_imports.append(module_name)
            print(f"  ❌ {module_name}")
    
    if failed_imports:
        print(f"  ❌ Failed imports: {failed_imports}")
        return False
    
    print("  ✅ All core imports successful")
    return True

def test_main_files():
    """Test that main Python files are syntactically valid."""
    print("\n🔍 Testing Python file syntax...")
    
    python_files = ["main_loop.py", "whatsapp_driver.py"]
    
    for file_name in python_files:
        try:
            with open(file_name, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Try to compile the file
            compile(content, file_name, 'exec')
            print(f"  ✓ {file_name} syntax valid")
            
        except SyntaxError as e:
            print(f"  ❌ {file_name} syntax error: {e}")
            return False
        except Exception as e:
            print(f"  ❌ {file_name} error: {e}")
            return False
    
    print("  ✅ All Python files have valid syntax")
    return True

def main():
    """Run all foundation tests."""
    print("🚀 Personal Coaching Assistant - Foundation Setup Test")
    print("=" * 60)
    
    tests = [
        test_project_structure,
        test_profile_json,
        test_reminders_excel,
        test_imports,
        test_main_files
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        else:
            print(f"\n⚠️  Test failed: {test.__name__}")
    
    print("\n" + "=" * 60)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 Foundation setup is complete and working!")
        print("\n🔮 Next steps:")
        print("  1. Install Ollama and download a model")
        print("  2. Set up WhatsApp Web integration") 
        print("  3. Build the RAG knowledge base")
        print("  4. Implement core agent logic")
        return 0
    else:
        print("❌ Some tests failed. Please fix the issues above.")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 