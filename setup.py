from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

with open('requirements.txt', 'r', encoding='utf-8') as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith('#')]

setup(
    name='phantomtext',
    version='0.1.0',
    author='Luca Pajola',
    author_email='luca.pajola@example.com',  # Update with your actual email
    description='A toolkit for content injection, obfuscation, scanning, and sanitization of various document formats.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/lucapajola/PhantomText',  # Update with your actual GitHub URL
    packages=find_packages(),
    install_requires=requirements + [
        'numpy>=1.19.0',
        'tqdm>=4.60.0',
    ],
    include_package_data=True,
    package_data={
        'phantomtext': ['fonts/*.ttf', 'fonts/*.pkl'],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Topic :: Security',
        'Topic :: Text Processing',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
    keywords='text obfuscation steganography content injection document security',
)