import json

def calculate_normalized_start(subchunk, original_length):
    return subchunk['original_start_ms'] / original_length

def generate_sound_events(page):
    original_length = page['original_file']['length_ms']
    sound_events = []
    for i, subchunk in enumerate(page['subchunk_files']):
        subchunk['original_start_ms'] = sum(c['length_ms'] for c in page['subchunk_files'][:i])
        start = calculate_normalized_start(subchunk, original_length)
        sound_events.append({"start": start, "id": f"{i+1:02d}"})
        del subchunk['original_start_ms']
    return sound_events

def main():
    with open('mp3_files_info.json', 'r') as file:
        data = json.load(file)

    all_sound_events = [generate_sound_events(page) for page in data]

    with open('sound_events.json', 'w') as file:
        json.dump(all_sound_events, file, indent=2)

if __name__ == '__main__':
    main()
