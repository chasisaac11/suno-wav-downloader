"""
Suno WAV Downloader - Automated bulk download script
Downloads all WAV files from a Suno workspace

Author: Your Name
Date: 2024
Requirements: Python 3.8+, Selenium, Chrome/Chromium browser
"""

import os
import time
import logging
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import json
from datetime import datetime

# Configure logging
logging.basicConfig(
      level=logging.INFO,
      format='%(asctime)s - %(levelname)s - %(message)s',
      handlers=[
                logging.FileHandler('suno_downloader.log'),
                logging.StreamHandler()
      ]
)
logger = logging.getLogger(__name__)


class SunoDownloader:
      """Automates downloading WAV files from Suno AI music platform"""

    def __init__(self, workspace_url, download_dir=None, headless=False):
              """
                      Initialize the Suno downloader

                                      Args:
                                                  workspace_url (str): Full URL to your Suno workspace
                                                              download_dir (str): Directory to save files (default: ~/Downloads)
                                                                          headless (bool): Run browser in headless mode (default: False)
                                                                                  """
              self.workspace_url = workspace_url
              self.download_dir = download_dir or os.path.expanduser("~/Downloads")
              self.headless = headless
              self.driver = None
              self.downloaded_files = []
              self.failed_downloads = []

        # Create download directory if it doesn't exist
              Path(self.download_dir).mkdir(parents=True, exist_ok=True)
              logger.info(f"Download directory set to: {self.download_dir}")

    def setup_driver(self):
              """Configure and initialize Chrome WebDriver"""
              try:
                            chrome_options = Options()

            # Set download directory
                  prefs = {
                                    "download.default_directory": self.download_dir,
                                    "download.prompt_for_download": False,
                                    "safebrowsing.enabled": False
                  }
            chrome_options.add_experimental_option("prefs", prefs)

            if self.headless:
                              chrome_options.add_argument("--headless")

            # Other useful options
            chrome_options.add_argument("--start-maximized")
            chrome_options.add_argument("--disable-notifications")
            chrome_options.add_argument("--disable-popup-blocking")

            self.driver = webdriver.Chrome(options=chrome_options)
            self.driver.set_page_load_timeout(30)
            logger.info("Chrome WebDriver initialized successfully")

except Exception as e:
            logger.error(f"Failed to initialize WebDriver: {e}")
            raise

    def navigate_to_workspace(self):
              """Navigate to the Suno workspace"""
        try:
                      logger.info(f"Navigating to workspace: {self.workspace_url}")
                      self.driver.get(self.workspace_url)
                      time.sleep(3)  # Wait for page to load
            logger.info("Successfully navigated to workspace")
            return True
except Exception as e:
            logger.error(f"Failed to navigate to workspace: {e}")
            return False

    def get_total_song_count(self):
              """Extract the total number of songs in the workspace"""
        try:
                      # Look for text like "30 songs"
                      song_count_text = self.driver.find_element(
                                        By.XPATH, 
                                        "//*[contains(text(), 'songs')]"
                      ).text
                      count = int(song_count_text.split()[0])
                      logger.info(f"Total songs in workspace: {count}")
                      return count
except Exception as e:
            logger.warning(f"Could not determine exact song count: {e}")
            return None

    def scroll_to_load_all_songs(self):
              """Scroll through the page to ensure all songs are loaded"""
        try:
                      logger.info("Scrolling to load all songs...")
                      last_height = self.driver.execute_script("return document.body.scrollHeight")
                      scroll_count = 0

            while True:
                              # Scroll down
                              self.driver.execute_script("window.scrollBy(0, 1000);")
                              time.sleep(1)
                              scroll_count += 1

                # Calculate new height
                              new_height = self.driver.execute_script("return document.body.scrollHeight")

                if new_height == last_height:
                                      logger.info(f"All songs loaded after {scroll_count} scrolls")
                                      break

                last_height = new_height

                # Safety limit
                if scroll_count > 50:
                                      logger.warning("Reached maximum scroll attempts")
                                      break

            return True
except Exception as e:
            logger.error(f"Error while scrolling: {e}")
            return False

    def get_song_menu_buttons(self):
              """Find all song menu buttons (three dots) on the page"""
        try:
                      # Find all three-dot menu buttons
                      menu_buttons = self.driver.find_elements(
                                        By.XPATH,
                                        "//button[contains(@aria-label, 'menu') or contains(@class, 'menu')]"
                      )
                      logger.info(f"Found {len(menu_buttons)} menu buttons")
                      return menu_buttons
except Exception as e:
            logger.error(f"Error finding menu buttons: {e}")
            return []

    def download_song_wav(self, menu_button, song_index):
              """
                      Download WAV file for a specific song

                                      Args:
                                                  menu_button: WebElement of the menu button
                                                              song_index: Index of the song (for logging)

                                                                              Returns:
                                                                                          bool: True if successful, False otherwise
                                                                                                  """
        try:
                      logger.info(f"Processing song {song_index}...")

            # Click the menu button
                      self.driver.execute_script("arguments[0].scrollIntoView(true);", menu_button)
            time.sleep(0.5)
            self.driver.execute_script("arguments[0].click();", menu_button)
            time.sleep(1)

            # Look for Download option
            try:
                              download_option = WebDriverWait(self.driver, 5).until(
                                                    EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'Download')]"))
                              )
                              self.driver.execute_script("arguments[0].click();", download_option)
                              time.sleep(0.5)
except TimeoutException:
                logger.warning(f"Download option not found for song {song_index}")
                return False

            # Look for WAV Audio option
            try:
                              wav_option = WebDriverWait(self.driver, 5).until(
                                                    EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'WAV Audio')]"))
                              )
                              self.driver.execute_script("arguments[0].click();", wav_option)
                              time.sleep(1)
except TimeoutException:
                logger.warning(f"WAV Audio option not found for song {song_index}")
                return False

            # Wait for download dialog and click "Download File"
            try:
                              download_button = WebDriverWait(self.driver, 10).until(
                                                    EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'Download File')]"))
                              )
                              time.sleep(2)  # Wait for file processing
                self.driver.execute_script("arguments[0].click();", download_button)
                time.sleep(2)  # Wait for download to start

                logger.info(f"Successfully initiated download for song {song_index}")
                self.downloaded_files.append(f"Song {song_index}")
                return True

except TimeoutException:
                logger.warning(f"Download File button not found for song {song_index}")
                return False

except Exception as e:
            logger.error(f"Error downloading song {song_index}: {e}")
            self.failed_downloads.append(f"Song {song_index}: {str(e)}")
            return False
finally:
            # Close any open menus by clicking elsewhere
              try:
                                self.driver.execute_script("document.body.click();")
                                time.sleep(0.5)
                            except:
                pass

                                  def run(self, max_songs=None, delay_between_downloads=2):
                                            """
                                                    Execute the complete download process

                                                                    Args:
                                                                                max_songs (int): Maximum number of songs to download (None = all)
                                                                                            delay_between_downloads (int): Delay in seconds between each download
                                                                                                    """
                                            try:
                                                          # Initialize
                                                          logger.info("=== Starting Suno WAV Downloader ===")
                                                          self.setup_driver()

            # Navigate to workspace
            if not self.navigate_to_workspace():
                              raise Exception("Failed to navigate to workspace")

            # Get song count
            total_songs = self.get_total_song_count()

            # Load all songs
            if not self.scroll_to_load_all_songs():
                              logger.warning("Could not load all songs, continuing anyway...")

            # Download songs
            menu_buttons = self.get_song_menu_buttons()
            max_downloads = max_songs if max_songs else len(menu_buttons)

            logger.info(f"Starting download of {min(max_downloads, len(menu_buttons))} songs...")

            for index, menu_button in enumerate(menu_buttons[:max_downloads], 1):
                              logger.info(f"--- Song {index}/{min(max_downloads, len(menu_buttons))} ---")

                # Re-fetch menu buttons to avoid stale element references
                              if index > 1:
                                                    menu_buttons = self.get_song_menu_buttons()
                                                    menu_button = menu_buttons[index - 1]

                self.download_song_wav(menu_button, index)

                # Add delay between downloads
                if index < min(max_downloads, len(menu_buttons)):
                                      logger.info(f"Waiting {delay_between_downloads} seconds before next download...")
                                      time.sleep(delay_between_downloads)

            # Summary
            logger.info("=== Download Complete ===")
            logger.info(f"Successfully downloaded: {len(self.downloaded_files)} files")
            if self.failed_downloads:
                              logger.warning(f"Failed downloads: {len(self.failed_downloads)}")
                              for failed in self.failed_downloads:
                                                    logger.warning(f"  - {failed}")

                          return {
                                            "success": True,
                                            "downloaded": len(self.downloaded_files),
                                            "failed": len(self.failed_downloads),
                                            "download_dir": self.download_dir
                          }

except Exception as e:
            logger.error(f"Fatal error during download process: {e}")
            return {
                              "success": False,
                              "error": str(e),
                              "downloaded": len(self.downloaded_files),
                              "failed": len(self.failed_downloads)
            }
finally:
            # Cleanup
              if self.driver:
                                logger.info("Closing WebDriver...")
                                self.driver.quit()


def main():
      """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(
              description="Download all WAV files from a Suno workspace"
    )
    parser.add_argument(
              "workspace_url",
              help="Full URL to your Suno workspace (e.g., https://suno.com/create?wid=...)"
    )
    parser.add_argument(
              "--download-dir",
              default=os.path.expanduser("~/Downloads"),
              help="Directory to save WAV files (default: ~/Downloads)"
    )
    parser.add_argument(
              "--max-songs",
              type=int,
              default=None,
              help="Maximum number of songs to download (default: all)"
    )
    parser.add_argument(
              "--delay",
              type=int,
              default=2,
              help="Delay in seconds between downloads (default: 2)"
    )
    parser.add_argument(
              "--headless",
              action="store_true",
              help="Run browser in headless mode"
    )

    args = parser.parse_args()

    # Create downloader and run
    downloader = SunoDownloader(
              workspace_url=args.workspace_url,
              download_dir=args.download_dir,
              headless=args.headless
    )

    result = downloader.run(
              max_songs=args.max_songs,
              delay_between_downloads=args.delay
    )

    # Print result
    print("\n" + "="*50)
    print("DOWNLOAD SUMMARY")
    print("="*50)
    print(f"Status: {'SUCCESS' if result['success'] else 'FAILED'}")
    print(f"Downloaded: {result['downloaded']} files")
    print(f"Failed: {result['failed']} files")
    if 'download_dir' in result:
              print(f"Location: {result['download_dir']}")
    if 'error' in result:
              print(f"Error: {result['error']}")
    print("="*50)


if __name__ == "__main__":
      main()
