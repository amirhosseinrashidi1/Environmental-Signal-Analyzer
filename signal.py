import tkinter as tk
from tkinter import messagebox
import sounddevice as sd
import numpy as np
from scipy.fft import fft
import matplotlib.pyplot as plt
import pandas as pd
import sqlite3
import subprocess
import platform

# ----------- Audio Capture -------------------
def capture_audio(duration=5, fs=44100):
    print("Recording audio...")
    audio_data = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='float64')
    sd.wait()
    print("Audio recording completed.")
    return np.squeeze(audio_data)

# ----------- Audio Analysis -------------------
def analyze_audio(signal, fs=44100):
    freq_data = fft(signal)
    freqs = np.fft.fftfreq(len(signal), 1 / fs)
    magnitude = np.abs(freq_data)
    return freqs[:len(freqs)//2], magnitude[:len(freqs)//2]

# ----------- Wi-Fi Scan -------------------
def scan_wifi():
    try:
        if platform.system() == "Linux":
            result = subprocess.check_output(["nmcli", "-t", "-f", "SSID,SIGNAL", "dev", "wifi"])
        elif platform.system() == "Windows":
            result = subprocess.check_output(["netsh", "wlan", "show", "networks", "mode=bssid"])
        else:
            raise EnvironmentError("Unsupported operating system.")
        return result.decode(errors="ignore")
    except Exception as e:
        raise RuntimeError(f"Wi-Fi scan error: {e}")

def parse_wifi_output(output):
    networks = []
    for line in output.splitlines():
        if "SSID" in line and ":" in line:
            ssid = line.split(":")[1].strip()
            signal_line = next((l for l in output.splitlines() if "Signal" in l or "SIGNAL" in l), None)
            signal = signal_line.split(":")[1].strip() if signal_line else "Unknown"
            networks.append((ssid, signal))
    return networks

# ----------- Plotting -------------------
def plot_signal(freqs, magnitude, title="Frequency Spectrum"):
    plt.figure(figsize=(10, 4))
    plt.plot(freqs, magnitude, color='blue')
    plt.title(title)
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Magnitude")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def plot_wifi(networks):
    if not networks:
        print("No networks found.")
        return
    ssids = [ssid for ssid, _ in networks]
    strengths = [int(sig) if sig.isdigit() else 0 for _, sig in networks]

    plt.figure(figsize=(10, 4))
    plt.bar(ssids, strengths, color='orange')
    plt.title("Wi-Fi Signal Strength")
    plt.xlabel("SSID")
    plt.ylabel("Signal (%)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# ----------- Excel Export -------------------
def save_to_excel(data_dict, filename):
    df = pd.DataFrame(data_dict)
    df.to_excel(filename, index=False)
    print(f"Data saved to {filename}.")

# ----------- Database Export -------------------
def save_to_db(table, data_dict):
    conn = sqlite3.connect("signals.db")
    df = pd.DataFrame(data_dict)
    df.to_sql(table, conn, if_exists="replace", index=False)
    conn.close()
    print(f"Data saved to table '{table}' in signals.db.")

# ----------- Audio Processing -------------------
def process_audio():
    try:
        signal = capture_audio()
        freqs, mag = analyze_audio(signal)
        plot_signal(freqs, mag, "Audio Signal Analysis")
        save_to_excel({'Frequency': freqs, 'Magnitude': mag}, "audio_signal.xlsx")
        save_to_db("audio_signals", {'Frequency': freqs, 'Magnitude': mag})
        messagebox.showinfo("Success", "Audio signal analyzed and saved.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# ----------- Wi-Fi Processing -------------------
def process_wifi():
    try:
        raw_output = scan_wifi()
        networks = parse_wifi_output(raw_output)
        if not networks:
            messagebox.showinfo("Info", "No Wi-Fi networks found.")
            return
        plot_wifi(networks)
        data = {'SSID': [n[0] for n in networks], 'Signal': [n[1] for n in networks]}
        save_to_excel(data, "wifi_data.xlsx")
        save_to_db("wifi_signals", data)
        messagebox.showinfo("Success", "Wi-Fi data saved successfully.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# ----------- GUI -------------------
def launch_gui():
    root = tk.Tk()
    root.title("Environmental Signal Analyzer")
    root.geometry("400x300")
    root.resizable(False, False)

    lbl = tk.Label(root, text="Select the type of signal to analyze:", font=("Arial", 11))
    lbl.pack(pady=20)

    btn_audio = tk.Button(root, text="🎙️ Analyze Audio Signal", command=process_audio, font=("Arial", 12), bg="#4CAF50", fg="white", padx=10, pady=5)
    btn_audio.pack(pady=10)

    btn_wifi = tk.Button(root, text="📡 Analyze Wi-Fi Signal", command=process_wifi, font=("Arial", 12), bg="#2196F3", fg="white", padx=10, pady=5)
    btn_wifi.pack(pady=10)

    root.mainloop()

# Launch the GUI
if __name__ == "__main__":
    launch_gui()
