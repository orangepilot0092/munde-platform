import os
import time
from huggingface_hub import HfApi, snapshot_download

# Target directory on the 2TB D: drive
DOWNLOAD_DIR = "/mnt/d/sahyadri-data/datasets/indic"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

api = HfApi()
token = os.environ.get("HF_TOKEN")

print("🔍 Fetching metadata for Hindi (hi) and Marathi (mr) datasets...")
# Fetch separately. Sorting by "downloads" defaults to descending.
hi_datasets = list(api.list_datasets(filter="language:hi", sort="downloads", limit=300, token=token))
mr_datasets = list(api.list_datasets(filter="language:mr", sort="downloads", limit=300, token=token))

# Combine and remove duplicates based on dataset ID
unique_datasets = {ds.id: ds for ds in hi_datasets + mr_datasets}.values()
datasets = list(unique_datasets)

print(f"✅ Found {len(datasets)} unique datasets. Starting download process...\n")

success_count = 0
fail_count = 0

for i, ds in enumerate(datasets):
    ds_id = ds.id
    
    # OPTIONAL: Skip the massive general-purpose C4 dataset to prioritize specific Indic datasets
    if "allenai/c4" in ds_id:
        print(f"[{i+1}/{len(datasets)}] ⏩ Skipping {ds_id} (Too large/general for initial Atlas)")
        continue

    safe_name = ds_id.replace("/", "__")
    target_path = os.path.join(DOWNLOAD_DIR, safe_name)

    # Skip if already downloaded and not empty
    if os.path.exists(target_path) and any(os.scandir(target_path)):
        print(f"[{i+1}/{len(datasets)}] ⏩ Skipping {ds_id} (Already exists)")
        continue

    print(f"[{i+1}/{len(datasets)}] 📥 Downloading {ds_id} ({ds.downloads} downloads)...")

    try:
        snapshot_download(
            repo_id=ds_id,
            repo_type="dataset",
            local_dir=target_path,
            resume_download=True,
            max_workers=4,
            token=token # <--- Added token here
        )
        print(f"✅ Success: {ds_id}")
        success_count += 1
    except Exception as e:
        print(f"❌ Failed: {ds_id} - {str(e)[:100]}")
        fail_count += 1
        
    # Sleep for 2 seconds to be polite to the API
    time.sleep(2)

print(f"\n🏆 Download Complete!")
print(f"✅ Successful: {success_count}")
print(f"❌ Failed: {fail_count}")
print(f"📂 Data stored in: {DOWNLOAD_DIR}")
