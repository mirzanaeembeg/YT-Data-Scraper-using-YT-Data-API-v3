import pandas as pd
import re
from googleapiclient.discovery import build
from gspread_pandas import Spread, conf

# --- CONFIGURATION ---
# Replace with your YouTube Data API Key
YOUTUBE_API_KEY = "YOUR_YOUTUBE_API_KEY"

# Replace with the name of your Google Sheet
GOOGLE_SHEET_NAME = "Bangla Kids YouTube Data"

# Name of the JSON file you downloaded from Google Cloud
# Make sure this file is in the same directory as your script
GOOGLE_CREDS_FILE = "your_credentials_file_name.json"

# --- INPUT: PASTE YOUR VIDEO URLs HERE ---
# Add the YouTube video links you want to collect data for in this list.
VIDEO_URLS = [
    "https://www.youtube.com/watch?v=example_video_id_1",#pest yt video link inside every double quote
    "https://youtu.be/example_video_id_2",
    "https://www.youtube.com/watch?v=another_example_id"
    # Add more URLs here
    
]

# --- DO NOT EDIT BELOW THIS LINE ---

def extract_video_id(url):
    """
    Extracts the YouTube video ID from a URL using regex.
    Handles different URL formats (youtube.com, youtu.be).
    """
    patterns = [
        r'(?:v=|\/)([0-9A-Za-z_-]{11}).*',
        r'youtu\.be\/([0-9A-Za-z_-]{11})'
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None

def get_youtube_data_from_urls(api_key, urls):
    """
    Fetches details for a specific list of YouTube video URLs.
    """
    youtube = build("youtube", "v3", developerKey=api_key)
    all_video_data = []
    
    video_ids = [extract_video_id(url) for url in urls]
    video_ids = [vid_id for vid_id in video_ids if vid_id] # Remove any None values

    if not video_ids:
        print("No valid YouTube video IDs could be extracted from the URLs.")
        return pd.DataFrame()

    print(f"Found {len(video_ids)} valid video IDs. Fetching details...")

    # Process video IDs in batches of 50 (the API limit) for efficiency
    for i in range(0, len(video_ids), 50):
        batch_ids = video_ids[i:i+50]
        try:
            video_request = youtube.videos().list(
                part="snippet,statistics",
                id=",".join(batch_ids)
            )
            video_response = video_request.execute()

            for item in video_response.get("items", []):
                stats = item.get("statistics", {})
                video_data = {
                    "Title": item["snippet"]["title"],
                    "Published Date": item["snippet"]["publishedAt"].split("T")[0],
                    "Views": int(stats.get("viewCount", 0)),
                    "Likes": int(stats.get("likeCount", 0)),
                    "Comments": int(stats.get("commentCount", 0)),
                    "Channel Title": item["snippet"]["channelTitle"],
                    "Video URL": f"https://www.youtube.com/watch?v={item['id']}",
                }
                all_video_data.append(video_data)
        except Exception as e:
            print(f"An error occurred while fetching a batch: {e}")
            continue
            
    print(f"Data collection complete. Fetched details for {len(all_video_data)} videos.")
    return pd.DataFrame(all_video_data)

def append_to_google_sheet(df, sheet_name, creds_file):
    """
    Appends a Pandas DataFrame to a Google Sheet without overwriting existing data.
    """
    if df.empty:
        print("DataFrame is empty. Nothing to save to Google Sheets.")
        return
        
    print(f"Connecting to Google Sheets to append data to '{sheet_name}'...")
    try:
        config = conf.get_config(conf_dir=".", file_name=creds_file)
        spread = Spread(sheet_name, config=config)
        
        # Get the first worksheet
        worksheet = spread.sheets[0]
        
        # Get existing data to check if sheet is empty and find the next empty row
        existing_records = worksheet.get_all_records()
        
        if len(existing_records) == 0:
            # Sheet is empty, add headers and data starting from A1
            print("Sheet is empty. Adding headers and data...")
            spread.df_to_sheet(df, index=False, headers=True, sheet=worksheet, start='A1', replace=True)
        else:
            # Sheet has data, append new data without headers
            print(f"Sheet has {len(existing_records)} existing records. Appending new data...")
            next_row = len(existing_records) + 2  # +2 because we have headers in row 1
            start_cell = f'A{next_row}'
            
            # Append data without headers
            spread.df_to_sheet(df, index=False, headers=False, sheet=worksheet, start=start_cell, replace=False)
        
        print("Data successfully appended to Google Sheets! ✅")
    except Exception as e:
        print(f"Could not save to Google Sheets. Error: {e}")
        print("Please ensure you have shared your Google Sheet with the client_email in your JSON file.")


def check_for_duplicates(df, sheet_name, creds_file):
    """
    Check for duplicate video URLs to avoid adding the same video multiple times.
    Returns a DataFrame with only new videos.
    """
    try:
        config = conf.get_config(conf_dir=".", file_name=creds_file)
        spread = Spread(sheet_name, config=config)
        worksheet = spread.sheets[0]
        
        existing_records = worksheet.get_all_records()
        
        if len(existing_records) == 0:
            print("No existing data found. All videos will be added.")
            return df
        
        # Convert existing records to DataFrame
        existing_df = pd.DataFrame(existing_records)
        
        # Check if 'Video URL' column exists in existing data
        if 'Video URL' in existing_df.columns:
            existing_urls = set(existing_df['Video URL'].tolist())
            
            # Filter out videos that already exist
            new_videos = df[~df['Video URL'].isin(existing_urls)]
            
            duplicate_count = len(df) - len(new_videos)
            if duplicate_count > 0:
                print(f"Found {duplicate_count} duplicate video(s). Skipping them.")
            
            print(f"Adding {len(new_videos)} new video(s).")
            return new_videos
        else:
            print("No 'Video URL' column found in existing data. Adding all videos.")
            return df
            
    except Exception as e:
        print(f"Error checking for duplicates: {e}")
        print("Proceeding to add all videos...")
        return df


if __name__ == "__main__":
    # Fetch data from the list of URLs
    video_df = get_youtube_data_from_urls(YOUTUBE_API_KEY, VIDEO_URLS)
    
    # Check for duplicates and filter them out
    if not video_df.empty:
        filtered_df = check_for_duplicates(video_df, GOOGLE_SHEET_NAME, GOOGLE_CREDS_FILE)
        
        # Append the filtered data to Google Sheets
        if not filtered_df.empty:
            append_to_google_sheet(filtered_df, GOOGLE_SHEET_NAME, GOOGLE_CREDS_FILE)
        else:
            print("No new videos to add. All videos already exist in the sheet.")
    else:

        print("No video data was collected.")
