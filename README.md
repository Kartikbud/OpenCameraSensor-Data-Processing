# OpenCameraSensor-Data-Processing

This file is supposed to be use to convert the raw IMU and Video data from the android app OpenCamera Sensor into a format which can be converted into rosbags in kalibr

First install the required libraries using `pip install -r requirements.txt`
Then rename the files:
- Video timestamps -> `vid_stamps.csv`
- Video mp4 -> `input.mp4`
- Acceleration csv -> `accel.csv`
- Gyro csv -> `gyro.csv`

Then make a new directory to extract the frames into: `mkdir cam0`

Now the script can be run: `python main.py`

After this is run there should be an imu0.csv file and cam0 directory that can be added into kalibr directory to then be converted into a rosbag

***Note:
Sometimes the imu0 file converts the timestamps into scientific numbers, this will break the bag converter script in kalibr.
To fix this, convert the timestamps to normal numbers and ensure there is no decimals.
