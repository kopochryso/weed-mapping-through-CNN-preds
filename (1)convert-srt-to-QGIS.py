import re
import pandas as pd
srt_file = r/"Users/…/file.srt"  # Replace path to your SRT file
frames = []
 with open (srt_file, "r") as file:
	data = file.read()
# Updated regex to match your SRT format
pattern = r"FrameCnt: (\d+).*?(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{3}).*?\[iso: \d+\] \[shutter: [\d/.]+] \[fnum: [\d.]+] \[ev: \d+\] \[color_md: \w+\] \[focal_len: [\d.]+] \[latitude: ([\d\.\-]+)] \[longitude: ([\d\.\-]+)] \[rel_alt: ([\d\.\-]+)"
matches = re.finditer(pattern, data, re.DOTALL)
# Extract matched data and store it in a list
for match in matches:
	frame_num = int(match.group(1))
	timestamp = match.group(2)
	latitude = float(match.group(3))
	longitude = float(match.group(4))
	rel_altitude = float(match.group(5))
	frames.append([frame_num, timestamp, latitude, longitude, rel_altitude])
 # Convert to a DataFrame and save to CSV
df = pd.DataFrame(frames, columns=["FrameNum", "Timestamp", "Latitude", "Longitude", "Rel_Altitude"])
df.to_csv("frame_metadata.csv", index=False)
print("CSV file created: frame_metadata.csv")
