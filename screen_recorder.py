import pyautogui
import cv2
import numpy as np
import os
import keyboard
from datetime import datetime
import win32gui
import win32con
import sys


if getattr(sys, 'frozen', False):  # Check if running as PyInstaller .exe
    hwnd = win32gui.GetForegroundWindow()
    win32gui.ShowWindow(hwnd, win32con.SW_HIDE)


OUTPUT_DIR = r"C:\Local  Screen Recording"
TOTAL_DURATION = 5000  # Total recording duration in seconds (1 hour 23 minutes)
SEGMENT_DURATION = 600  # Duration of each video segment in seconds (10 minutes)
FPS = 10  # Frames per second (reduced for file size)
SCREEN_SIZE = pyautogui.size()  # Get screen resolution (width, height)

try:
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
except Exception:
    exit(1)  # Silently exit on error


def create_new_video_writer():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = os.path.join(OUTPUT_DIR, f"screen_recording_{timestamp}.mp4")
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")  
    return cv2.VideoWriter(output_file, fourcc, FPS, (SCREEN_SIZE.width, SCREEN_SIZE.height)), output_file

pyautogui.FAILSAFE = False  # Disable failsafe to avoid interruptions
total_frames = int(TOTAL_DURATION * FPS)
segment_frames = int(SEGMENT_DURATION * FPS)
current_frame = 0

out, current_output_file = create_new_video_writer()

while current_frame < total_frames:
    
    if keyboard.is_pressed("ctrl+shift+q"):
        break
    
    
    if current_frame % segment_frames == 0 and current_frame != 0:
        out.release()  # Close current video
        out, current_output_file = create_new_video_writer()  # Start new video

    
    img = pyautogui.screenshot()
    
    frame = np.array(img)
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    
    out.write(frame)
    current_frame += 1


out.release()