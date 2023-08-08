import os
import shutil
import json
from mutagen.mp3 import MP3

def chop_mp3(file_path, max_part_size_mb=5):
    try:
        file_size_mb = os.path.getsize(file_path) / (1024 * 1024)

        # Calculate the number of parts to split the file into
        num_parts = int(file_size_mb / max_part_size_mb) + 1

        # Create a directory to store the split files
        output_directory = os.path.dirname(file_path) + "/split_files/"
        os.makedirs(output_directory, exist_ok=True)

        # Split the file into parts
        with open(file_path, "rb") as source_file:
            for i in range(num_parts):
                part_file_path = f"{output_directory}{os.path.basename(file_path)}_{i}.mp3"
                part_size = int(max_part_size_mb * 1024 * 1024)
                with open(part_file_path, "wb") as part_file:
                    part_file.write(source_file.read(part_size))

    except Exception as e:
        print(f"Error while processing {file_path}: {str(e)}")

def get_file_length_ms(file_path):
    try:
        audio = MP3(file_path)
        length_ms = int(audio.info.length * 1000)
        return length_ms
    except Exception as e:
        print(f"Error while getting audio length for {file_path}: {str(e)}")
        return None

def process_directory(directory_path, json_file_path):
    if not os.path.exists(directory_path):
        print(f"Directory '{directory_path}' does not exist.")
        return

    print(f"Processing files in directory: {directory_path}")

    data = []
    for root, _, files in os.walk(directory_path):
        for file in files:
            if file.lower().endswith(".mp3"):
                file_path = os.path.join(root, file)
                print(f"Processing file: {file_path}")
                chop_mp3(file_path)
                length_ms = get_file_length_ms(file_path)
                if length_ms is not None:
                    data.append({
                        "file": os.path.basename(file_path),
                        "size_mb": os.path.getsize(file_path) / (1024 * 1024),
                        "length_ms": length_ms
                    })

    with open(json_file_path, "w") as json_file:
        json.dump(data, json_file, indent=4)

if __name__ == "__main__":
    directory_to_search = "C:/Users/stuar/Documents/Software/JS/john-cage-final-audio-app/static/res/audio/Piano/Pagescopy"  # Replace this with the directory to search
    json_file_path = "split_files_info.json"

    process_directory(directory_to_search, json_file_path)

    print("MP3 chopping and JSON creation completed.")
