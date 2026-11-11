import csv
import hashlib
from datetime import datetime, timezone

input_file = "data/raw_samples.csv"
output_file = "data/clean_samples.csv"
audit_file = "data/audit.log"

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

# Generate SHA-256 digital fingerprint of the clean file
with open(output_file, "rb") as f:
    file_hash = hashlib.sha256(f.read()).hexdigest()

# Write compliance audit log entry
timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
log_entry = f"[{timestamp}] Processed {input_file} | Valid: {len(valid_rows)} | Rejected: {rejected_count} | SHA256: {file_hash}\n"

with open(audit_file, mode="a") as log:
    log.write(log_entry)

print(f"\nSummary: {len(valid_rows)} clean samples ready. {rejected_count} rejected.")
print(f"Audit Log Recorded: {log_entry.strip()}")
