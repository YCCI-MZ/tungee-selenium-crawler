# Tungee Enterprise Data Crawler

## Overview
This project is a Selenium-based web automation and crawling tool designed to extract structured enterprise information from a B2B CRM platform.

The tool automates authenticated workflows, navigates dynamically rendered tables, and collects company-level data for downstream analysis.

## Features
- Automated login and authenticated session handling
- Dynamic table pagination and row-level navigation
- Multi-window management for detail pages
- Structured data extraction and persistence

## Tech Stack
- Python
- Selenium
- Pandas
- ChromeDriver

## Project Structure
```text
tanqi-selenium-crawler/
├── main.py
├── README.md
├── requirements.txt
└── .gitignore
```

## Usage

1. Install dependencies
```text
pip install -r requirements.txt
```
2. Run the crawler
```text
python main.py
```