#!/usr/bin/env python3
"""
Test script to verify PhantomText package functionality before publishing.
"""

def test_imports():
    """Test that all main classes can be imported."""
    try:
        from phantomtext import ContentInjector, ContentObfuscator, FileScanner, FileSanitizer
        print("✅ All main classes import successfully")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_package_info():
    """Test package metadata."""
    try:
        import phantomtext
        print(f"✅ Package version: {phantomtext.__version__}")
        print(f"✅ Package author: {phantomtext.__author__}")
        return True
    except Exception as e:
        print(f"❌ Package info error: {e}")
        return False

def test_basic_functionality():
    """Test basic functionality of core classes."""
    try:
        from phantomtext.content_obfuscation import ContentObfuscator
        
        obfuscator = ContentObfuscator()
        # Test with a simple text obfuscation
        result = obfuscator.obfuscate("Hello World", "Hello", 
                                    obfuscation_technique="zeroWidthCharacter",
                                    file_format="html")
        if result:
            print("✅ Basic obfuscation functionality works")
            return True
        else:
            print("❌ Obfuscation returned empty result")
            return False
    except Exception as e:
        print(f"❌ Functionality test error: {e}")
        return False

def main():
    """Run all tests."""
    print("🧪 Testing PhantomText package...")
    print("-" * 50)
    
    tests = [
        test_imports,
        test_package_info,
        test_basic_functionality
    ]
    
    passed = 0
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("-" * 50)
    print(f"Results: {passed}/{len(tests)} tests passed")
    
    if passed == len(tests):
        print("🎉 All tests passed! Package is ready for publication.")
        return True
    else:
        print("⚠️  Some tests failed. Please fix issues before publishing.")
        return False

if __name__ == "__main__":
    main()
