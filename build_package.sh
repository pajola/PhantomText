#!/bin/bash

# PhantomText Package Build Script

echo "🔧 Building PhantomText package..."

# Clean previous builds
echo "🧹 Cleaning previous builds..."
rm -rf build/ dist/ *.egg-info/

# Install build dependencies
echo "📦 Installing build dependencies..."
pip install --upgrade setuptools wheel twine build

# Build the package
echo "🏗️  Building package..."
python -m build

# Check the package
echo "🔍 Checking package..."
python -m twine check dist/*

echo "✅ Build complete! Files created in dist/ directory:"
ls -la dist/

echo ""
echo "📤 To upload to PyPI:"
echo "   Test PyPI: python -m twine upload --repository testpypi dist/*"
echo "   Real PyPI: python -m twine upload dist/*"
echo ""
echo "🧪 To test installation locally:"
echo "   pip install dist/phantomtext-*.whl"
