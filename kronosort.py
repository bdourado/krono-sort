import os
import re
import shutil
import zipfile
import io
from datetime import datetime
from pathlib import Path
from PIL import Image
from PIL.ExifTags import TAGS
import pillow_heif
from tqdm import tqdm

# Register HEIF support for Pillow
pillow_heif.register_heif_opener()

# Disable DecompressionBomb warning for large images
Image.MAX_IMAGE_PIXELS = None

# Configuration
SOURCE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.heic', '.mp4', '.mov'}
IGNORE_EXTENSIONS = {'.json', '.html', '.txt'}
DATE_REGEX_PATTERNS = [
    re.compile(r'(\d{4})(\d{2})(\d{2})'),  # YYYYMMDD
    re.compile(r'(\d{4})-(\d{2})-(\d{2})'),  # YYYY-MM-DD
]

def get_exif_date_from_bytes(file_bytes):
    """Extracts creation date from EXIF metadata in a bytes stream."""
    try:
        with Image.open(io.BytesIO(file_bytes)) as img:
            exif_data = img.getexif()
            if exif_data:
                for tag_id, value in exif_data.items():
                    tag = TAGS.get(tag_id, tag_id)
                    if tag == 'DateTimeOriginal' or tag == 'DateTime':
                        # Format is usually YYYY:MM:DD HH:MM:SS
                        return datetime.strptime(value[:10], '%Y:%m:%d')
    except Exception:
        pass
    return None

def get_regex_date(filename):
    """Extracts date from filename using regex."""
    for pattern in DATE_REGEX_PATTERNS:
        match = pattern.search(filename)
        if match:
            try:
                year, month, day = match.groups()
                return datetime(int(year), int(month), int(day))
            except ValueError:
                continue
    return None

def get_unique_path(target_path):
    """Ensures a unique filename by appending a suffix if it already exists."""
    if not target_path.exists():
        return target_path
    
    stem = target_path.stem
    suffix = target_path.suffix
    directory = target_path.parent
    counter = 1
    
    while True:
        new_path = directory / f"{stem}_{counter}{suffix}"
        if not new_path.exists():
            return new_path
        counter += 1

def process_zip(zip_path, dest_path):
    """Processes a single ZIP file."""
    try:
        with zipfile.ZipFile(zip_path, 'r', allowZip64=True) as zf:
            # Filter entries
            entries = [
                info for info in zf.infolist() 
                if not info.is_dir() and Path(info.filename).suffix.lower() in SOURCE_EXTENSIONS
            ]
            
            if not entries:
                return

            for info in tqdm(entries, desc=f"Processing {zip_path.name}", unit="file", leave=False):
                filename = Path(info.filename).name
                date = None
                
                # Try EXIF (only for images)
                if Path(info.filename).suffix.lower() in {'.jpg', '.jpeg', '.png', '.heic'}:
                    try:
                        with zf.open(info) as f:
                            date = get_exif_date_from_bytes(f.read())
                    except Exception:
                        pass
                
                # Try Regex
                if not date:
                    date = get_regex_date(filename)
                
                # Determine target folder
                if filename.startswith("FB_IMG_"):
                    target_folder = dest_path / "Facebook"
                elif filename.startswith("Screenshot_"):
                    target_folder = dest_path / "Screenshot"
                elif filename.startswith("Screenrecorder") or filename.startswith("Screen_Recording"):
                    target_folder = dest_path / "Screenrecorder"
                elif date:
                    target_folder = dest_path / str(date.year) / f"{date.month:02d}"
                else:
                    target_folder = dest_path / "Others"

                target_folder.mkdir(parents=True, exist_ok=True)
                target_file_path = get_unique_path(target_folder / filename)
                
                # Extract file
                try:
                    with zf.open(info) as source, open(target_file_path, "wb") as target:
                        shutil.copyfileobj(source, target)
                except Exception as e:
                    print(f"\nError extracting {filename} from {zip_path.name}: {e}")
    except zipfile.BadZipFile:
        print(f"Error: {zip_path.name} is a corrupted ZIP file.")
    except Exception as e:
        print(f"Error processing {zip_path.name}: {e}")

def organize_from_zips(source_input, dest_dir):
    """Main function to organize files from ZIPs."""
    source_path = Path(source_input)
    dest_path = Path(dest_dir)
    
    if not source_path.exists():
        print(f"Error: Source path {source_input} does not exist.")
        return

    zip_files = []
    if source_path.is_file():
        if source_path.suffix.lower() == '.zip':
            zip_files = [source_path]
        else:
            print("Error: Source file is not a ZIP file.")
            return
    elif source_path.is_dir():
        zip_files = sorted(list(source_path.glob('*.zip')))

    if not zip_files:
        print("No ZIP files found to process.")
        return

    print(f"Found {len(zip_files)} ZIP file(s) to process.")

    for zip_path in tqdm(zip_files, desc="Overall Progress", unit="zip"):
        process_zip(zip_path, dest_path)

if __name__ == "__main__":
    print("--- KronoSort: Zip-to-Folder Edition ---")
    src = input("Enter ZIP file or folder containing ZIPs: ").strip()
    dst = input("Enter destination directory path: ").strip()
    
    if src and dst:
        organize_from_zips(src, dst)
        print("\nOrganization complete!")
    else:
        print("Source and destination paths are required.")
