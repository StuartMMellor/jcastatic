import os
import json

def get_page_files(page_number):
    page_folder = f"Pagescopy/{page_number}/Audio/split_files"
    files = os.listdir(page_folder)
    # Exclude the original mp3 file
    original_file = f"Piano-{page_number:03d}-01.mp3"
    return [f"{page_folder}/{file}" for file in files if file != original_file]

def main():
    base_folder = "Pagescopy"
    page_folders = os.listdir(base_folder)

    page_files_list = []
    for page_folder in sorted(page_folders, key=lambda x: int(x)):
        if page_folder.isdigit():  # Check if it's a numbered page folder
            page_number = int(page_folder)
            page_files = get_page_files(page_number)
            page_info = {
                "page": {
                    str(page_number): page_files
                }
            }
            page_files_list.append(page_info)

    result = json.dumps(page_files_list, indent=4)
    print(result)

if __name__ == "__main__":
    main()
