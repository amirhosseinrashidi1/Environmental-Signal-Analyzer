# Environmental Signal Analyzer

## Overview
This is a Python-based graphical application for analyzing environmental signals. It supports two main types of signals: audio and Wi-Fi. The user-friendly GUI allows recording, analyzing, and visualizing these signals, and saving the results to both Excel files and a local SQLite database.

## Features

- **Audio Signal Analysis:**
  - Record audio for a fixed duration (default 5 seconds) at 44.1 kHz sample rate.
  - Perform frequency analysis using FFT (Fast Fourier Transform).
  - Visualize frequency spectrum in a plotted graph.
  - Export analysis data to Excel and SQLite database.

- **Wi-Fi Signal Scanning:**
  - Scan available Wi-Fi networks depending on the operating system (Linux or Windows).
  - Extract SSID and signal strength.
  - Display Wi-Fi signal strengths in a bar chart.
  - Save Wi-Fi scan results to Excel and SQLite database.

- **User-Friendly GUI** with buttons to select which signal to analyze.

## Requirements

Make sure you have the following Python packages installed:

```bash
pip install numpy scipy matplotlib pandas sounddevice
```

Tkinter is usually included with Python by default.

**Note:**  
- On Linux, the program relies on the `nmcli` command-line tool for Wi-Fi scanning.  
- On Windows, it uses the built-in `netsh` utility.

## Usage

Run the script via command line:

```bash
python your_script_name.py
```

A GUI window will appear, allowing you to choose between audio signal analysis or Wi-Fi scanning.

## How It Works

- **Audio recording:** captures sound from the microphone for a fixed time.
- **Audio analysis:** computes the FFT of the audio signal to extract frequency components.
- **Wi-Fi scanning:** uses system commands to get a list of nearby Wi-Fi networks and their signal strengths.
- **Visualization:** plots frequency spectra for audio and bar charts for Wi-Fi signals.
- **Data saving:** exports all results to both Excel files and an SQLite database (`signals.db`).

## Limitations & Notes

- Tested on Windows and Linux only.
- Requires microphone access for audio recording.
- Wi-Fi scanning commands may require appropriate permissions.
- Error messages are displayed via pop-up dialogs if anything goes wrong.


## Contribution

Feel free to open issues or contribute!
