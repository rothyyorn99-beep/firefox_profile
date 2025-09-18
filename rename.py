
import os

folder_path = r"D:\video\video"  # Change to your folder path
prefix_to_remove = "masstiktok_craftart70__"

for filename in os.listdir(folder_path):
    old_path = os.path.join(folder_path, filename)

    if os.path.isfile(old_path) and filename.startswith(prefix_to_remove):
        # Remove prefix
        new_filename = filename[len(prefix_to_remove):]
        new_path = os.path.join(folder_path, new_filename)

        os.rename(old_path, new_path)
        print(f"Renamed: {filename} -> {new_filename}")
