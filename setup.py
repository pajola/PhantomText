from setuptools import setup, find_packages

setup(
    name='PhantomText',
    version='0.1.0',
    author='Your Name',
    author_email='your.email@example.com',
    description='A toolkit for content injection, obfuscation, scanning, and sanitization of various document formats.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/PhantomText',
    packages=find_packages(),
    install_requires=[
        # Add your project dependencies here
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)