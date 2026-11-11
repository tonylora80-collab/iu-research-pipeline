import csv

input_file = "data/raw_samples.csv"
output_file = "data/clean_samples.csv"

valid_rows = []
rejected_count = 0

with open(input_file, mode="r") as infile:
    reader = csv.DictReader(infile)
    for row in reader:
        if not row["sequencing_score"] or row["status"] != "COMPLETE":
            print(f"[REJECTED] Sample {row['sample_id']} - Incomplete or failed QC")
            rejected_count += 1
            continue
        
        clean_row = {
            "sample_id": row["sample_id"],
            "gene_marker": row["gene_marker"],
            "sequencing_score": row["sequencing_score"],
            "status": row["status"]
        }
        valid_rows.append(clean_row)

with open(output_file, mode="w", newline="") as outfile:
    fieldnames = ["sample_id", "gene_marker", "sequencing_score", "status"]
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(valid_rows)

print(f"\nSummary: {len(valid_rows)} clean samples ready. {rejected_count} rejected.")
