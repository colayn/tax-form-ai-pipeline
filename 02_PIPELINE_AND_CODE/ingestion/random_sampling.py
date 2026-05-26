# =====================================================
# PURPOSE
# =====================================================
# This module performs reproducible random sampling
# of the original W-2 dataset.
#
# A representative subset of 50 PDF documents is
# selected using a fixed random seed to ensure
# deterministic sampling across environments.
#
# PIPELINE STAGE:
# Ingestion
#
# OUTPUT:
# sampling_input_docs/
# =====================================================

import os
import random
import shutil

# =====================================================
# CONFIGURATION
# =====================================================
source_dir = "input_docs"            # Folder with 250 PDFs
target_dir = "01_DATA_SOURCES/sampling_input_docs"   # Folder where the 50 will go
sample_size = 50
RANDOM_SEED = 42               # The "Magic Number" for reproducibility

# =====================================================
# SAMPLING LOGIC
# =====================================================

def perform_sampling():
    # 1. Create target directory if it doesn't exist
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
        print(f"Created directory: {target_dir}")

    # 2. Get list of all PDFs
    all_files = sorted([
        f for f in os.listdir(source_dir)
        if (
            f.endswith(".pdf")
            and "Zone.Identifier" not in f
        )
    ])
        # 3. Apply the Seed and Sample
    random.seed(RANDOM_SEED)

    selected_files = random.sample(
        all_files,
        sample_size
    )

    print(
        f"Successfully sampled {sample_size} files using seed {RANDOM_SEED}."
    )

    # =====================================================
    # SAVE SELECTED FILE LIST
    # =====================================================

    sample_log_path = os.path.join(
        target_dir,
        "selected_files.txt"
    )

    with open(sample_log_path, "w") as log_file:

        for filename in selected_files:

            log_file.write(f"{filename}\n")

    print(
        f"📝 Selected file list saved to: {sample_log_path}"
    )

    print(f"Successfully sampled {sample_size} files using seed {RANDOM_SEED}.")

    # 4. Copy files to the random folder
    for filename in selected_files:
        src_path = os.path.join(source_dir, filename)
        dst_path = os.path.join(target_dir, filename)
        shutil.copy(src_path, dst_path)

    print(f"✅ Subset ready in: {target_dir}")

if __name__ == "__main__":
    perform_sampling()