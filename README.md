# 0day Scraper

## Description
The 0day Scraper is a Python application designed to scrape and process data from various sources. It includes a graphical user interface (GUI) for reading CSV files and other functionalities. Please note that this is still a work-in-progress and is still far from finished.
Future Features i plan to add:
🔹 0day Scraper
Scrapes Exploit-DB for the latest vulnerabilities.
Fetches zero-day exploit news from an online news API.
Summarizes exploit descriptions using AI-powered text summarization.

🔹 Threat Intelligence Integrations
Queries Shodan for additional threat insights.
Fetches VirusTotal API data (planned feature).

🔹 CSV Reader GUI
Loads scraped exploit data from CSV.
Provides an interactive dark-themed interface for easy navigation.
Displays pie chart visualizations for exploit trends.

🔹 Automation & Export
Saves scraped exploits and news into CSV files for further analysis.
Auto-executes the CSV Reader GUI after scraping.

## Requirements
- Python 3.11 or higher
- Required packages (see `requirements.txt` for a complete list)

## Prerequisites
1. Install Python from the official website: [python.org](https://www.python.org/downloads/).
2. Create a virtual environment to manage dependencies:
   ```bash
   python -m venv myenv
   source myenv/Scripts/activate  # On Windows
   # or
   source myenv/bin/activate  # On macOS/Linux

## **Installation**
1. Clone the repository:
   ```bash   
   git clone <your-repo-url>
   cd CNWC
   
2. Install the required packages:
   ```bash
   pip install -r requirements.txt

## **Usage**
Run the main script to start the application:
- python 0day_scraper.py

## **File Structure**
- 0day_scraper.py: Main script for the application.
- csv_reader_gui.py: GUI for reading CSV files.
- zero_day_news.csv: Sample data file.
- cyberpunk_background.jpg: Background image used in the GUI.
- exploitdb/: Directory containing additional resources or data.

## **License**
This project is licensed under the MIT License.
