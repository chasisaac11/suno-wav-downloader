# Suno WAV Downloader

Automated bulk downloader for WAV files from [Suno AI](https://suno.com) music workspaces. Download multiple songs at once with Python automation or follow manual browser steps.

## Features

- 🚀 **Automated Downloading**: Uses Selenium to automate the entire download process
- - 📦 **Bulk Operations**: Download all songs from a workspace automatically
  - - ⚙️ **Configurable**: Command-line options for delays, max songs, custom directories
    - - 📝 **Logging**: Detailed logging of all operations and errors
      - - 🛡️ **Error Handling**: Robust error handling and recovery
        - - ⏱️ **300x Faster**: Automation is ~300x faster than manual clicking
         
          - ## Quick Start
         
          - ### Prerequisites
          - - Python 3.8+
            - - Chrome/Chromium browser
              - - ChromeDriver (matching your Chrome version)
               
                - ### Installation
               
                - ```bash
                  # Clone the repository
                  git clone https://github.com/yourusername/suno-wav-downloader.git
                  cd suno-wav-downloader

                  # Install dependencies
                  pip install -r requirements.txt

                  # Download ChromeDriver
                  # https://chromedriver.chromium.org/
                  ```

                  ### Usage

                  ```bash
                  # Basic usage
                  python suno_downloader.py "https://suno.com/create?wid=YOUR-WORKSPACE-ID"

                  # Download only first 10 songs
                  python suno_downloader.py "YOUR_URL" --max-songs 10

                  # Custom download directory
                  python suno_downloader.py "YOUR_URL" --download-dir ~/Music/Suno

                  # Headless mode (no browser window)
                  python suno_downloader.py "YOUR_URL" --headless

                  # Adjust delay between downloads
                  python suno_downloader.py "YOUR_URL" --delay 5
                  ```

                  ## Manual Download Process

                  If you prefer to download manually:

                  1. Go to your Suno workspace
                  2. 2. For each song, click the three-dot menu (⋯)
                     3. 3. Click "Download" → "WAV Audio"
                        4. 4. Click "Download File" button
                           5. 5. Repeat for all songs
                              6. 6. On duplicates, click "Keep Both" to save with "-2" suffix
                                
                                 7. ## File Structure
                                
                                 8. ```
                                    suno-wav-downloader/
                                    ├── suno_downloader.py   # Main automation script
                                    ├── requirements.txt     # Python dependencies
                                    ├── LICENSE             # MIT License
                                    ├── .gitignore          # Git ignore rules
                                    └── README.md           # This file
                                    ```

                                    ## Command-Line Options

                                    | Option | Description | Default |
                                    |--------|-------------|---------|
                                    | `workspace_url` | Full Suno workspace URL | Required |
                                    | `--download-dir` | Directory to save WAV files | ~/Downloads |
                                    | `--max-songs` | Maximum songs to download | All |
                                    | `--delay` | Seconds between downloads | 2 |
                                    | `--headless` | Run without browser window | False |

                                    ## Troubleshooting

                                    **ChromeDriver not found**
                                    - Download from https://chromedriver.chromium.org/
                                    - - Ensure version matches your Chrome installation
                                      - - Add to PATH or place in same directory as script
                                       
                                        - **Module 'selenium' not found**
                                        - ```bash
                                          pip install --upgrade selenium
                                          ```

                                          **Downloads failing**
                                          - Check internet connection
                                          - - Increase delay: `--delay 5` or `--delay 10`
                                            - - Ensure Suno.com is accessible
                                              - - Check available disk space
                                               
                                                - ## How It Works
                                               
                                                - 1. Opens Chrome browser (or headless)
                                                  2. 2. Navigates to your workspace
                                                     3. 3. Scrolls through page to load all songs
                                                        4. 4. For each song, it:
                                                           5.    - Clicks the menu button
                                                                 -    - Selects "Download" → "WAV Audio"
                                                                      -    - Clicks "Download File"
                                                                           -    - Waits before next download
                                                                            
                                                                                - 5. Downloads go to your Downloads folder
                                                                                  6. 6. Duplicates get "-2" suffix (Mac standard)
                                                                                     7. 7. Logs all results to `suno_downloader.log`
                                                                                       
                                                                                        8. ## Performance
                                                                                       
                                                                                        9. - **30 songs**: ~2 minutes (vs 5-10 minutes manually)
                                                                                           - - **100 songs**: ~5-7 minutes (vs 20-30 minutes manually)
                                                                                             - - **300+ songs**: ~15-20 minutes (vs 100+ minutes manually)
                                                                                              
                                                                                               - ## License
                                                                                              
                                                                                               - This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.
                                                                                              
                                                                                               - ## Disclaimer
                                                                                              
                                                                                               - This tool is for personal use only. It automates the download process but respects Suno's Terms of Service. Only download files you have created or have permission to download.
                                                                                              
                                                                                               - ## Support
                                                                                              
                                                                                               - For issues, suggestions, or contributions, please open an issue on GitHub.
                                                                                              
                                                                                               - ---

                                                                                               **Made with ❤️ for Suno AI music creators**
