# Publishing PhantomText to PyPI

This guide will help you publish the PhantomText package to PyPI.

## Before Publishing

1. **Update Personal Information**: Make sure to update the following in both `setup.py` and `pyproject.toml`:
   - `author_email`: Replace `luca.pajola@example.com` with your actual email
   - `url`: Replace `https://github.com/lucapajola/PhantomText` with your actual GitHub repository URL

2. **Create PyPI Account**: 
   - Sign up at [https://pypi.org/account/register/](https://pypi.org/account/register/)
   - Sign up at [https://test.pypi.org/account/register/](https://test.pypi.org/account/register/) for testing

3. **Generate API Tokens** (recommended over passwords):
   - Go to PyPI Account Settings > API tokens
   - Create a new token for your project

## Publishing Steps

### 1. Test Locally
```bash
# Install in development mode
pip install -e .

# Run the test script
python test_package.py
```

### 2. Build the Package
```bash
# Use the provided build script
./build_package.sh

# Or manually:
python -m build
```

### 3. Test Upload to Test PyPI (Recommended)
```bash
# Upload to Test PyPI first
python -m twine upload --repository testpypi dist/*

# Install from Test PyPI to verify
pip install --index-url https://test.pypi.org/simple/ phantomtext
```

### 4. Upload to Real PyPI
```bash
# Upload to real PyPI
python -m twine upload dist/*
```

### 5. Verify Installation
```bash
# Install from PyPI
pip install phantomtext

# Test the installation
python -c "import phantomtext; print(phantomtext.__version__)"
```

## Version Management

To release a new version:

1. Update the version in `setup.py` and `phantomtext/__init__.py`
2. Update the `CHANGELOG.md` if you have one
3. Create a git tag: `git tag v0.1.1`
4. Push the tag: `git push origin v0.1.1`
5. Rebuild and republish the package

## Important Notes

- Package name `phantomtext` must be unique on PyPI
- If the name is taken, you'll need to choose a different name
- Consider adding a `CHANGELOG.md` file to track versions
- Make sure all sensitive files are excluded via `.gitignore` and `MANIFEST.in`

## Troubleshooting

### Common Issues

1. **Package name already exists**: Choose a different name
2. **Authentication errors**: Use API tokens instead of passwords
3. **File permission errors**: Make sure all files are readable
4. **Missing dependencies**: Update `requirements.txt` and `setup.py`

### Checking Package Contents
```bash
# Extract and check the built package
tar -tzf dist/phantomtext-0.1.0.tar.gz | head -20
```

## After Publishing

1. Add installation instructions to your README
2. Create GitHub releases for version tracking
3. Consider setting up automated publishing via GitHub Actions
4. Monitor download statistics on PyPI
