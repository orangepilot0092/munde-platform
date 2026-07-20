import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from dagster import materialize
from etl.sahyadri_etl.assets.document_processing import process_sample_government_report

if __name__ == "__main__":
    print("=== Starting Dagster Asset Materialization via Python API ===")
    try:
        # Execute the asset
        result = materialize([process_sample_government_report])

        if result.success:
            print("✅ Asset materialized successfully!")
        else:
            print("❌ Asset materialization failed.")
            # Print failure details
            for event in result.all_events:
                if event.is_failure:
                    print(f"Failure: {event.specific_message}")
    except Exception as e:
        print(f"❌ Execution crashed: {e}")
        import traceback

        traceback.print_exc()
