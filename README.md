# ⏳ KronoSort

**KronoSort** is a powerful, cross-platform Python automation tool designed to organize messy media exports (like Google Takeout) into a clean, chronological folder structure.

## 🚀 Features

- **Multi-Platform**: Works pipe-clean on Windows and Linux using `pathlib`.
- **Smart Date Detection**:
  - **1st Priority**: EXIF Metadata (`DateTimeOriginal`).
  - **2nd Priority**: Special Folder Routing:
    - `FB_IMG_` -> `Facebook/`
    - `Screenshot_` -> `Screenshot/`
    - `Screenrecorder` / `Screen_Recording` -> `Screenrecorder/`
  - **3rd Priority**: Filename Regex (Detects `YYYYMMDD` or `YYYY-MM-DD`).
  - **Fallback**: Moves unidentified files to an `Others` folder.
- **Robust File Management**:
  - **Collision Prevention**: Automatically renames files with numeric suffixes if a duplicate filename exists in the destination.
  - **Format Support**: Processes `.jpg`, `.jpeg`, `.png`, `.heic`, `.mp4`, `.mov`.
  - **HEIC Support**: Integrated `pi-heif` for modern iPhone photo formats.
- **Direct ZIP Reading**: Processes files directly without the need for prior manual extraction.
- **User Friendly**: Real-time progress tracking with `tqdm`.

## 🛠️ Installation

As modern Linux versions (Debian/Ubuntu) protect the system's Python environment, we recommend using a virtual environment (**venv**):

1. **Clone or download** the files to your machine.
2. **Create the virtual environment**:
   ```bash
   python3 -m venv venv
   ```
3. **Activate the environment**:
   - **Linux/macOS**:
     ```bash
     source venv/bin/activate
     ```
   - **Windows**:
     ```bash
     .\venv\Scripts\activate
     ```
4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## 📖 Usage

Run the script and follow the instructions:

```bash
python kronosort.py
```

- **Source Path**: Can be a single `.zip` file or a folder containing multiple Google Takeout `.zip` files.
- **Destination Path**: Where you want the `Year/Month/` folders to be created.

The script will read the files directly from the ZIPs!

## 📂 Example Output

```text
Destination/
├── 2023/
│   ├── 01/
│   │   └── photo_01.jpg
│   └── 12/
│       └── video_holiday.mp4
├── Facebook/
│   └── FB_IMG_12345.jpg
├── Screenshot/
│   └── Screenshot_2023.png
├── Screenrecorder/
│   └── Screenrecorder-2023.mp4
├── 2024/
│   └── 05/
│       └── image_1.png
└── Others/
    └── unknown_file.heic
```

## ⚖️ License
MIT License - Feel free to use and modify!

---
Developed with ❤️ to facilitate the organization of digital memories.
