import os
import json
from mutagen.mp3 import MP3

def get_file_length_ms(file_path):
    try:
        audio = MP3(file_path)
        length_ms = int(audio.info.length * 1000)
        return length_ms
    except Exception as e:
        print(f"Error while getting audio length for {file_path}: {str(e)}")
        return None

def natural_sort_key(s):
    import re
    return [int(text) if text.isdigit() else text.lower()
            for text in re.split(r'(\d+)', s)]

def process_directory(directory_path, json_file_path):
    if not os.path.exists(directory_path):
        print(f"Directory '{directory_path}' does not exist.")
        return

    print(f"Processing files in directory: {directory_path}")

    data = []
    page_folders = os.listdir(directory_path)
    page_folders.sort(key=natural_sort_key)  # Sort the folders numerically
    for page_folder in page_folders:
        page_data = {
            "page_number": int(page_folder),  # Convert page_folder to integer
            "original_file": None,
            "subchunk_files": []
        }

        page_folder_path = os.path.join(directory_path, page_folder, "Audio")
        for file in os.listdir(page_folder_path):
            if file.lower().endswith(".mp3"):
                file_path = os.path.join(page_folder_path, file)
                length_ms = get_file_length_ms(file_path)
                if length_ms is not None:
                    if "Piano-" in file:
                        page_data["original_file"] = {
                            "file_name": file,
                            "size_mb": os.path.getsize(file_path) / (1024 * 1024),
                            "length_ms": length_ms
                        }
                    else:
                        file_info = {
                            "file_name": file,
                            "size_mb": os.path.getsize(file_path) / (1024 * 1024),
                            "length_ms": length_ms
                        }
                        page_data["subchunk_files"].append(file_info)

        # Process sub-chunk files in the "split_audio" folder
        split_audio_path = os.path.join(directory_path, page_folder, "Audio", "split_files")
        for file in os.listdir(split_audio_path):
            if file.lower().endswith(".mp3"):
                file_path = os.path.join(split_audio_path, file)
                length_ms = get_file_length_ms(file_path)
                if length_ms is not None:
                    file_info = {
                        "file_name": file,
                        "size_mb": os.path.getsize(file_path) / (1024 * 1024),
                        "length_ms": length_ms
                    }
                    page_data["subchunk_files"].append(file_info)

        data.append(page_data)

    with open(json_file_path, "w") as json_file:
        json.dump(data, json_file, indent=4)

if __name__ == "__main__":
    directory_to_search = "./Pagescopy"  # Replace this with the directory to search
    json_file_path = "mp3_files_info.json"

    process_directory(directory_to_search, json_file_path)

    print("MP3 file information extraction completed.")
