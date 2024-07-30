import os
import json

slokas_directory = "slokas"
output_file = "slokas.json"
merged_data = []

# Iterate over the files in the directory
for filename in os.listdir(slokas_directory):
    if filename.endswith(".json"):
        file_path = os.path.join(slokas_directory, filename)
        with open(file_path, 'r', encoding='utf-8') as f:
            file_data = json.load(f)
            merged_data.append(file_data)

# Save the merged data to slokas.json
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(merged_data, f, indent=4, ensure_ascii=False)


print("Merged data saved to slokas.json.")
