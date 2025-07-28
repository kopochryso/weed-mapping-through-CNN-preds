import os
import pandas as pd
from collections import Counter
 
# Paths
yolo_folder = r"C:\Users\...\cnn-annotations"  # Replace with actual folder path
metadata_file = r"C:\Users\...\metadata.csv”  # Replace with actual metadata file path
output_csv = "weed_coverage_with_coords.csv"
 
# Load metadata with GPS coordinates
metadata_df = pd.read_csv(metadata_file)
 
# Initialize dictionary to store counts
frame_counts = {}
 
# Loop through YOLO annotation files
for txt_file in os.listdir(yolo_folder):
	if txt_file.endswith(".txt"):
    	# Extract frame number from filename
    	try:
        	frame_num = int(txt_file.split("_")[-1].split(".txt")[0])  # Adjust if naming is different
    	except ValueError:
        	print(f"Skipping file: {txt_file} (Invalid frame number)")
        	continue
 
    	# Read YOLO annotations
    	with open(os.path.join(yolo_folder, txt_file), "r") as file:
        	lines = file.readlines()
   	
    	# Count occurrences of each class
    	class_counts = Counter([int(line.split()[0]) for line in lines])
    	total_weeds = sum(class_counts.values())
 
    	# Store as percentages
    	if total_weeds > 0:
        	frame_counts[frame_num] = {
            	class_id: (count / total_weeds) * 100 for class_id, count in class_counts.items()
       	 }
 
# Convert to DataFrame
weed_df = pd.DataFrame.from_dict(frame_counts, orient="index").reset_index()
weed_df.rename(columns={"index": "FrameNum"}, inplace=True)
 
# Merge with metadata
merged_df = pd.merge(weed_df, metadata_df, on="FrameNum", how="left")
 
# Save to CSV for QGIS
merged_df.to_csv(output_csv, index=False)
print(f"CSV saved: {output_csv}")

