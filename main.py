####NOTES
"""
before running this script, the gyro data should be labelled gyro.csv
the acceleration data should be labelled accel.csv
the video timestamps should be labelled vid_stamps.csv
the video mp4 should be labelled input.mp4

the script will generate cam0 folder and imu0.csv which can be dragged into kalibr workspace to create a rosbag
"""

#-----interpolates the timestamps of the gyroscopic data onto the acceleromter timestamps, and then merges into single file------

import numpy as np
from scipy.interpolate import CubicSpline

# Load CSV files (no headers, format: x,y,z,timestamp)
accel_data = np.loadtxt('accel.csv', delimiter=',')
gyro_data = np.loadtxt('gyro.csv', delimiter=',')

# Extract timestamps (4th column) and sensor values (first 3 columns)
accel_times = accel_data[:, 3]
accel_values = accel_data[:, 0:3]

gyro_times = gyro_data[:, 3]
gyro_values = gyro_data[:, 0:3]

# Ensure gyro timestamps are strictly increasing
sorted_indices = np.argsort(gyro_times)
gyro_times = gyro_times[sorted_indices]
gyro_values = gyro_values[sorted_indices]

# Create cubic spline interpolators for gyro x, y, z
spline_x = CubicSpline(gyro_times, gyro_values[:, 0])
spline_y = CubicSpline(gyro_times, gyro_values[:, 1])
spline_z = CubicSpline(gyro_times, gyro_values[:, 2])

# Interpolate gyro values to match accel timestamps
gyro_interp_x = spline_x(accel_times)
gyro_interp_y = spline_y(accel_times)
gyro_interp_z = spline_z(accel_times)

# Combine into output: [timestamp, gyro_x, gyro_y, gyro_z, accel_x, accel_y, accel_z]
imu_data = np.column_stack((
    accel_times,
    gyro_interp_x,
    gyro_interp_y,
    gyro_interp_z,
    accel_values
))

# Save to imu0.csv (no header)
np.savetxt('imu0.csv', imu_data, delimiter=',', fmt='%.9f')

#---------turning video into frames-----------
#make sure to create folder cam0 and rename the video mp4 to input.mp4

import subprocess

cmd = [
    "ffmpeg",
    "-i", "input.mp4",
    "-vsync", "0",
    "-frame_pts", "1",
    "cam0/%010d.png"
]

subprocess.run(cmd, check=True) #runs the command to seperate the mp4 into its frames and then inserts it into cam0 folder

#------------assigning valid timestamps to each frame------------


import os
import pandas as pd

# Load the list of timestamps from the CSV (no header)
vid_stamps = pd.read_csv('vid_stamps.csv', header=None)[0].tolist()

frames_dir = 'cam0'
# Get all PNG files, sorted to match the order of extraction
frame_files = sorted([f for f in os.listdir(frames_dir) if f.endswith('.png')])

# Check that the number of frames matches the number of timestamps
if len(frame_files) != len(vid_stamps):
    raise ValueError(f"Number of frames ({len(frame_files)}) does not match number of timestamps ({len(vid_stamps)})")

# Rename each frame to the corresponding timestamp
for fname, ts in zip(frame_files, vid_stamps):
    src = os.path.join(frames_dir, fname)
    dst = os.path.join(frames_dir, f"{ts}.png")
    os.rename(src, dst)

print(f"Renamed {len(frame_files)} frames to match vid_stamps.csv timestamps.")
