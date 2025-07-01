# lost-but-i-found

This project identifies songs in video or audio files using [Shazam](https://github.com/sergree/shazamio). The script extracts audio with FFmpeg, sends it to Shazam for recognition and writes the matches to a text file. File dialogs are provided via Tkinter so you can choose the input and where to save the results.

## Requirements

- Python 3
- The `ffmpeg` command line tool must be installed and available in your `PATH`.
- Python packages:
  - `ffmpeg-python`
  - `shazamio`
  - `tkinter` (included with most Python installs)

Install the required Python packages with:

```
pip install -r requirements.txt
```

## Usage

Run the main script and follow the dialogs to select the video folder and the output file:

```bash
python shazam.py
```

For extra logs during processing, pass `--verbose`:

```bash
python shazam.py --verbose
```
