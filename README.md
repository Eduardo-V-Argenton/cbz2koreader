# cbz2koreader

A command-line tool to send CBZ files to a KOReader device over SSH/SFTP and create KOReader metadata from `ComicInfo.xml` or command-line options.

> **Note:** This project was developed and tested on Linux. The Python source code should also work on Windows, but Windows support has not been extensively tested.

The device must have an SSH server running, and the destination folder must already exist. SSH authentication uses your local keys or SSH agent; use `--key` to select a private key.

## Run from source

From the project folder:

### Linux

```bash
python -m venv venv
source venv/bin/activate
python -m pip install -r requirements.txt
python main.py --help
```

### Windows

```powershell
py -m venv venv
.\venv\Scripts\Activate.ps1
py -m pip install -r requirements.txt
py main.py --help
```

## Usage

Replace `DEVICE_HOST` with your device’s IP address or hostname.

Send one file, multiple files, or a folder:

```bash
python main.py comic.cbz --host DEVICE_HOST
python main.py first.cbz second.cbz --host DEVICE_HOST
python main.py ./comics --host DEVICE_HOST
```

Files and folders can be combined. Folders are processed in alphabetical order without searching subfolders.

Set metadata while keeping the local CBZ unchanged:

```bash
python main.py comic.cbz --host DEVICE_HOST \
  --series "My Series" \
  --authors "Author One, Author Two" \
  --titles "Volume One" \
  --tags "Adventure, Fantasy" \
  --not_local_update
```

By default, missing `ComicInfo.xml` metadata is created locally, and supplied metadata changes are saved to the local CBZ before upload. Use `--not_local_update` to skip local changes.

| Option                        | Description                                                                  |
| ----------------------------- | ---------------------------------------------------------------------------- |
| `--host`                      | Device IP address or hostname (required)                                     |
| `--port`                      | SSH port (default: `2222`)                                                   |
| `--user`                      | SSH username (default: `root`)                                               |
| `--dest`                      | Remote folder (default: `/mnt/us/documents`)                                 |
| `--key`                       | Path to a private SSH key                                                    |
| `--series`                    | Series name for all selected files                                           |
| `--authors`                   | Comma-separated authors                                                      |
| `--tags`                      | Comma-separated tags                                                         |
| `--titles`                    | Comma-separated titles, one per file in processing order                     |
| `--series_indexes`            | Comma-separated series indexes, one per file                                 |
| `--not_use_comic_info_number` | Ignore the existing ComicInfo number when choosing the KOReader series index |
| `--update_local_series_index` | Write the series index to the local ComicInfo number                         |
| `--not_local_update`          | Keep local CBZ files unchanged                                               |

Existing ComicInfo numbers take precedence by default. To override them for KOReader, combine `--series_indexes` with `--not_use_comic_info_number`.

## Build a standalone executable

PyInstaller executables are platform-specific. A binary built on Linux will run on Linux, while a Windows `.exe` must be built on Windows.

Build and test separately for each target operating system and architecture.

### Linux

```bash
python -m PyInstaller --onefile --name cbz2koreader main.py
./dist/cbz2koreader --help
```

After downloading the Linux executable:

```bash
chmod +x cbz2koreader
./cbz2koreader comic.cbz --host DEVICE_HOST
```

### Windows

Run PyInstaller on Windows:

```powershell
py -m PyInstaller --onefile --name cbz2koreader main.py
.\dist\cbz2koreader.exe --help
```

Users of the standalone executable do not need Python installed.

The generated binaries can be attached separately to a GitHub Release, for example:

```text
cbz2koreader-linux-x86_64
cbz2koreader-windows-x86_64.exe
```
