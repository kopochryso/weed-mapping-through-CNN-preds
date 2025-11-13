🌱 Weed Mapping Through CNN Predictions
Generating Weed Distribution Maps Using YOLO Detections & UAV Metadata

This repository contains the code used to generate three different weed-mapping products from drone imagery and YOLO detection outputs.
The pipeline combines:

- YOLO prediction .txt label files

- UAV metadata (timestamp, GPS coordinates, altitude, etc.)

- Custom Python scripts

- QGIS for geographic visualization

- These tools were developed as part of my research work in Precision Agriculture.

⚠️ Disclaimer

GPS positions originate from non-RTK UAV sensors, meaning final maps are suitable for:

visualization,
scouting,
agronomic insights,
…but NOT for high-precision applications (e.g., patch-spraying) unless RTK-grade GPS data is provided.

📌 Project Structure
weed-mapping-through-CNN-preds/
│
├── src/
│   ├── part1_dominant_weed_map.py
│   ├── part2_relative_percentage_map.py
│   ├── part3_absolute_weed_counts.py  
│
├── data_example/
│   ├── metadata_example.csv
│   └── labels_example/
│
├── outputs_example/
│
├── requirements.txt
└── README.md

📍 The Three Types of Weed Maps
1️⃣ Dominant Weed Map

Shows which weed class is most dominant in each frame.
Example:
Frame contains 10 AMARE, 5 CHEAL, 3 CYPES → Dominant weed = AMARE

Use case:

Quickly visualize which weed species dominates each part of the field

2️⃣ Relative Percent (%) Weed Coverage

Shows the percentage of each weed class relative to total detections per frame.

Example:
Frame: 10 AMARE, 1 CHEAL
→ AMARE = 90%, CHEAL = 10%

Use case:

Comparing weed distributions across species

Field-level weed pressure analysis per species

3️⃣ Absolute Number of Weeds (Per Class)

Counts every weed detection per frame, independently of other classes.

Example:
Frame contains:

10 AMARE

5 CHEAL

2 CYPES

Then three maps are produced showing the absolute count for each class.

Use case:

Raw density information

Input for heatmaps or kernel density estimation in QGIS

Per-species scouting

🚀 Running the Scripts

All scripts live in:

src/


Example usage (absolute counts script):

python src/part3_absolute_weed_counts.py \
  --yolo path/to/labels \
  --metadata path/to/metadata.csv \
  --output outputs/absolute_counts \
  --save_per_frame \
  --save_per_weed


More detailed instructions will be added per script.

❤️ Thanks for checking out this repository!