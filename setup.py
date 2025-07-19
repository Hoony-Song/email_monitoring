from setuptools import setup, find_packages

setup(
    name="email-monitor",
    version="2.0.0",
    description="모듈화된 이메일 모니터링 프로그램",
    author="Your Name",
    author_email="your.email@example.com",
    packages=find_packages(),
    install_requires=[
        "pillow>=9.0.0",
        "opencv-python>=4.5.0",
        "pytesseract>=0.3.10",
        "pyautogui>=0.9.50",
        "requests>=2.25.0",
        "numpy>=1.21.0",
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "email-monitor=main:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)