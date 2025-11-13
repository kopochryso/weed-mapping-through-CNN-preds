import os
import pandas as pd
from collections import defaultdict
import argparse


# --------------------------------------------------------
# 1. ARGUMENT PARSER
# --------------------------------------------------------
def parse_args():
    parser = argparse.ArgumentParser(description="Weed Mapping – Absolute Weed Counts for QGIS")

    parser.add_argument("--yolo", type=str, required=True,
                        help="Folder containing YOLO .txt annotation files")
    parser.add_argument("--metadata", type=str, required=True,
                        help="CSV with FrameNum, Latitude, Longitude, Timestamp, etc.")
    parser.add_argument("--output", type=str, required=True,
                        help="Output folder for CSV results")

    parser.add_argument("--save_per_weed", action="store_true",
                        help="Save separate CSV per weed class")
    parser.add_argument("--save_per_frame", action="store_true",
                        help="Save per-frame weed counts")

    return parser.parse_args()


# --------------------------------------------------------
# 2. CLASS MAPPING
# --------------------------------------------------------
class_id_to_name = {
    0: "AMARE",
    1: "CHEAL",
    2: "CYPES",
    3: "POROL"
}


# --------------------------------------------------------
# 3. MAIN PIPELINE
# --------------------------------------------------------
def main():

    args = parse_args()

    yolo_folder = args.yolo
    metadata_file = args.metadata
    output_folder = args.output
    os.makedirs(output_folder, exist_ok=True)

    # Output files
    per_frame_output = os.path.join(output_folder, "per_frame_counts.csv")
    aggregated_output = os.path.join(output_folder, "aggregated_qgis_ready.csv")

    # Storage dictionaries
    per_weed_data = defaultdict(list)
    frame_counts = defaultdict(lambda: defaultdict(int))

    # --------------------------------------------------------
    # STEP 1: Parse YOLO annotation files
    # --------------------------------------------------------
    print("\n🔍 Reading YOLO annotation files...")

    for file in os.listdir(yolo_folder):
        if not file.endswith(".txt"):
            continue

        try:
            frame_num = int(file.split("_")[-1].split(".txt")[0])
        except:
            print(f"⚠️ Skipped file (cannot parse frame number): {file}")
            continue

        with open(os.path.join(yolo_folder, file), "r") as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) < 5:
                    continue

                class_id = int(parts[0])
                if class_id not in class_id_to_name:
                    continue

                weed_name = class_id_to_name[class_id]

                # Save individual annotation (optional)
                per_weed_data[weed_name].append({
                    "FrameNum": frame_num,
                    "ClassID": class_id,
                    "X_center": float(parts[1]),
                    "Y_center": float(parts[2]),
                    "Width": float(parts[3]),
                    "Height": float(parts[4])
                })

                # Count per frame
                frame_counts[frame_num][weed_name] += 1

    # --------------------------------------------------------
    # STEP 2: Save per-weed annotation files (optional)
    # --------------------------------------------------------
    if args.save_per_weed:
        print("📁 Saving per-weed CSV files...")
        for weed_name, records in per_weed_data.items():
            df = pd.DataFrame(records)
            df.to_csv(os.path.join(output_folder, f"{weed_name}.csv"), index=False)

    # --------------------------------------------------------
    # STEP 3: Convert counts to DataFrame
    # --------------------------------------------------------
    rows = []
    for frame_num, counts in frame_counts.items():
        row = {"FrameNum": frame_num}
        for weed_name in class_id_to_name.values():
            row[f"{weed_name}_Count"] = counts.get(weed_name, 0)
        rows.append(row)

    counts_df = pd.DataFrame(rows)
    counts_df["FrameNum"] = counts_df["FrameNum"].astype(int)

    # --------------------------------------------------------
    # STEP 4: Merge with metadata (FrameNum, Lat, Lon, Timestamp...)
    # --------------------------------------------------------
    print("📌 Merging with metadata...")

    metadata_df = pd.read_csv(metadata_file)
    merged_df = pd.merge(counts_df, metadata_df, on="FrameNum", how="left")

    if args.save_per_frame:
        merged_df.to_csv(per_frame_output, index=False)
        print(f"✅ Saved per-frame weed counts: {per_frame_output}")

    # --------------------------------------------------------
    # STEP 5: Aggregate by (Latitude, Longitude) for QGIS
    # --------------------------------------------------------
    print("🌍 Aggregating by geolocation for QGIS...")

    agg_dict = {f"{name}_Count": "sum" for name in class_id_to_name.values()}

    # Additional numeric fields to aggregate
    agg_dict.update({
        "Rel_Altitude": "mean" if "Rel_Altitude" in merged_df.columns else "first",
        "FrameNum": "count",
        "Timestamp": "first"
    })

    aggregated = merged_df.groupby(["Latitude", "Longitude"], as_index=False).agg(agg_dict)

    aggregated.to_csv(aggregated_output, index=False)
    print(f"🎉 Final QGIS-ready file saved to: {aggregated_output}")


# --------------------------------------------------------
# RUN
# --------------------------------------------------------
if __name__ == "__main__":
    main()
