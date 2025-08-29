# YouTube Data Scraper using YouTube Data API v3

A Python script to collect YouTube video metadata (title, views, likes, comments, channel info, etc.) and automatically save it to Google Sheets. Perfect for research projects, content analysis, or building datasets.

## 📋 Table of Contents
- [Features](#-features)
- [Prerequisites](#-prerequisites)
- [Installation](#-installation)
- [Setup Guide](#-setup-guide)
  - [Step 1: Get YouTube Data API Key](#step-1-get-youtube-data-api-key-)
  - [Step 2: Set Up Google Sheets API Access](#step-2-set-up-google-sheets-api-access-)
  - [Step 3: Create and Configure Google Sheet](#step-3-create-and-configure-google-sheet-)
- [Usage](#-usage)
- [Data Structure](#-data-structure)
- [Common Issues & Solutions](#-common-issues--solutions)
- [Contributing](#-contributing)
- [License](#-license)

## 🚀 Features

- ✅ Extract video metadata from YouTube URLs
- ✅ Automatically save data to Google Sheets
- ✅ Prevent duplicate entries
- ✅ Batch processing for multiple videos
- ✅ Error handling and retry logic
- ✅ Preserve existing data when adding new videos
- ✅ Support for various YouTube URL formats

## 📦 Prerequisites

- Python 3.7 or higher
- Google account
- Google Cloud Platform account (free)

## 💻 Installation

1. **Clone this repository:**
   ```bash
   git clone https://github.com/yourusername/youtube-data-scraper.git
   cd youtube-data-scraper
   ```

2. **Install required packages:**
   ```bash
   pip install --upgrade google-api-python-client pandas gspread gspread-pandas oauth2client
   ```

   **If you encounter `'pip' is not recognized` error on Windows:**
   ```bash
   py -m pip install --upgrade google-api-python-client pandas gspread gspread-pandas oauth2client
   ```

## 🛠 Setup Guide

### Step 1: Get YouTube Data API Key 🔑

1. **Go to Google Cloud Console:** https://console.cloud.google.com/

2. **Create a New Project:**
   - Click "Select a project" → "New Project"
   - Give it a name (e.g., "YouTube Data Scraper")
   - Click "Create"

3. **Enable YouTube Data API v3:**
   - Go to "APIs & Services" → "Library"
   - Search for "YouTube Data API v3"
   - Click on it and press "ENABLE"

4. **Create API Key:**
   - Go to "APIs & Services" → "Credentials"
   - Click "+ CREATE CREDENTIALS" → "API key"
   - Copy the generated API key and save it securely

### Step 2: Set Up Google Sheets API Access 📄

1. **Enable Required APIs:**
   - In the same Google Cloud project, enable these APIs:
     - **Google Sheets API**: Go to Library → Search "Google Sheets API" → Enable
     - **Google Drive API**: Go to Library → Search "Google Drive API" → Enable

2. **Create Service Account:**
   - Go to "APIs & Services" → "Credentials"
   - Click "+ CREATE CREDENTIALS" → "Service account"
   - Enter name (e.g., "sheets-writer") → "CREATE AND CONTINUE" → "DONE"

3. **Generate JSON Key:**
   - Find your service account in the credentials list
   - Click on it → "KEYS" tab → "ADD KEY" → "Create new key"
   - Select "JSON" → "CREATE"
   - A JSON file will download automatically - **keep this file safe!**

### Step 3: Create and Configure Google Sheet 📊

1. **Create New Google Sheet:**
   - Go to https://sheets.google.com
   - Create a new blank spreadsheet
   - Rename it (e.g., "YouTube Video Data")

2. **Share with Service Account:**
   - Open the downloaded JSON file
   - Find the `"client_email"` field and copy the email address
   - In your Google Sheet, click "Share"
   - Paste the client email
   - Set permission to "Editor"
   - Uncheck "Notify people" → Click "Share"

## 📖 Usage

1. **Configure the script:**
   - Open `yt_data_collector.py`
   - Replace `YOUR_API_KEY_HERE` with your YouTube API key
   - Replace `YOUR_SHEET_NAME_HERE` with your Google Sheet name
   - Replace `YOUR_JSON_FILE_NAME.json` with your downloaded JSON filename
   - Add your YouTube video URLs to the `VIDEO_URLS` list

2. **Example configuration:**
   ```python
   # Configuration section
   YOUTUBE_API_KEY = "AIzaSyABC123xyz..."
   GOOGLE_SHEET_NAME = "YouTube Video Data"
   GOOGLE_CREDS_FILE = "my-project-credentials.json"
   
   VIDEO_URLS = [
       "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
       "https://www.youtube.com/watch?v=jNQXAC9IVRw",
       # Add more URLs here
   ]
   ```

3. **Run the script:**
   ```bash
   python yt_data_collector.py
   ```

4. **Check your Google Sheet** - data should appear automatically!

## 📊 Data Structure

The script collects the following data for each video:

| Column | Description |
|--------|-------------|
| Title | Video title |
| Published Date | Upload date (YYYY-MM-DD format) |
| Views | Total view count |
| Likes | Total like count |
| Comments | Total comment count |
| Channel Title | Name of the YouTube channel |
| Video URL | Full YouTube URL |

## 🔧 Common Issues & Solutions

### Issue 1: `'pip' is not recognized` (Windows)

**Problem:** Windows can't find pip command

**Solution:** Use Python launcher instead:
```bash
py -m pip install [package_name]
```

**Permanent Fix:** Add Python Scripts to PATH
1. Find Python installation: `py -0p`
2. Add `\Scripts` folder to Windows PATH environment variable
3. Restart terminal

### Issue 2: `Google Drive API has not been used` Error

**Problem:** Missing Google Drive API permission

**Solution:**
1. Go to Google Cloud Console
2. Navigate to "APIs & Services" → "Library"
3. Search for "Google Drive API" and enable it
4. Wait 2-5 minutes for changes to propagate
5. Run script again

### Issue 3: `Permission denied` or `Forbidden` Error

**Problem:** Service account doesn't have access to Google Sheet

**Solutions:**
1. **Check sharing:** Ensure you shared the sheet with the correct `client_email` from your JSON file
2. **Verify permissions:** Service account needs "Editor" access
3. **Correct sheet name:** Make sure `GOOGLE_SHEET_NAME` matches exactly

### Issue 4: `Invalid API Key` Error

**Problem:** YouTube API key is incorrect or restricted

**Solutions:**
1. **Verify API key:** Check if you copied the complete key
2. **Check restrictions:** In Google Cloud Console, ensure API key isn't restricted
3. **Enable YouTube API:** Make sure YouTube Data API v3 is enabled

### Issue 5: Script runs but no data appears

**Problem:** Usually related to file paths or credentials

**Solutions:**
1. **File location:** Ensure JSON credentials file is in the same folder as the script
2. **File name:** Check that `GOOGLE_CREDS_FILE` matches your actual JSON filename
3. **Sheet name:** Verify `GOOGLE_SHEET_NAME` is exactly the same as your Google Sheet name

### Issue 6: `ModuleNotFoundError`

**Problem:** Required packages not installed

**Solution:**
```bash
pip install --upgrade google-api-python-client pandas gspread gspread-pandas oauth2client
```

If pip doesn't work:
```bash
py -m pip install --upgrade google-api-python-client pandas gspread gspread-pandas oauth2client
```

### Issue 7: Quota Exceeded Error

**Problem:** YouTube API has daily quota limits

**Solutions:**
1. **Wait:** Quotas reset daily
2. **Batch processing:** Process videos in smaller batches
3. **Check quota:** Monitor usage in Google Cloud Console

## 🎯 Pro Tips

1. **Test with one video first** - Add just one URL to `VIDEO_URLS` for initial testing
2. **Keep credentials secure** - Never share your API key or JSON file publicly
3. **Monitor API usage** - YouTube API has daily quotas
4. **Regular backups** - Download your Google Sheet data periodically
5. **URL formats supported:** 
   - `https://www.youtube.com/watch?v=VIDEO_ID`
   - `https://youtu.be/VIDEO_ID`
   - `https://youtube.com/watch?v=VIDEO_ID`

## 📝 Example Output

After running the script successfully, your Google Sheet will look like this:

| Title | Published Date | Views | Likes | Comments | Channel Title | Video URL |
|-------|----------------|--------|--------|-----------|---------------|-----------|
| Sample Video Title | 2024-01-15 | 1500000 | 45000 | 2300 | Channel Name | https://www.youtube.com/watch?v=... |

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

This tool is for educational and research purposes. Please respect YouTube's Terms of Service and API usage policies. The authors are not responsible for any misuse of this tool.

---

**Need help?** Open an issue on GitHub or check the [Troubleshooting](#-common-issues--solutions) section above.

**Found this useful?** ⭐ Star this repository to help others find it!
