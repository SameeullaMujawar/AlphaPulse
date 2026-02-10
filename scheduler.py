import schedule
import time
import subprocess

def run_pipeline():
    print("Running AlphaPulse pipeline...")

    subprocess.run([
        "python",
        "Week-1/DATA_ACQUISITION_CLEANING.py"
    ])

    subprocess.run([
        "python",
        "Week-2/Quantitative_Analysis.py"
    ])

    print("Pipeline completed successfully.")

# Schedule job
schedule.every().day.at("17:48").do(run_pipeline)

print("Scheduler started...")

while True:
    schedule.run_pending()
    time.sleep(60)
