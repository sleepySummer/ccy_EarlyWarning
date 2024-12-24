import os
import time
import schedule
import shutil
from datetime import date
import config


# Define the paths
source_folder=  config.source_folder
destin_folder= config.destin_folder
file_name = config.target_file_name


def check_and_process_file():
    source_file_path = os.path.join(source_folder, file_name)
    new_file_date = str(date.today()).replace("-", "")
    destination_file_path = os.path.join(destin_folder, new_file_date)
   
    # Check if the file exists
    if os.path.exists(source_file_path):
        print(f"{file_name} found. Processing...")
        os.system('python auto_guess.py')

        # del the file to the destination folder
        os.remove(source_file_path)
        print(f"{file_name} has been delete, checked cleaned version in {destin_folder}.")
    else:
        print(f"{file_name} not found. Rechecking in 10 seconds...")
        time.sleep(10)


def schedule_period(start_time, end_time):
    current_time = time.strftime("%H:%M")
    while start_time <= current_time < end_time:
        check_and_process_file()
        time.sleep(10)  # Wait 10 seconds before the next check
        current_time = time.strftime("%H:%M")
    print(f"Finished checking for the period from {start_time} to {end_time}.")



# Schedule for two periods: 10:30am - 11:00am and 2:45pm - 3:15pm
schedule.every().monday.at("10:45").do(schedule_period, start_time="10:45", end_time="11:15")
schedule.every().monday.at("14:45").do(schedule_period, start_time="14:45", end_time="15:15")
schedule.every().tuesday.at("10:45").do(schedule_period, start_time="10:45", end_time="11:15")
schedule.every().tuesday.at("14:45").do(schedule_period, start_time="14:45", end_time="15:15")
schedule.every().wednesday.at("10:45").do(schedule_period, start_time="10:45", end_time="11:15")
schedule.every().wednesday.at("14:45").do(schedule_period, start_time="14:45", end_time="15:15")
schedule.every().thursday.at("10:45").do(schedule_period, start_time="10:45", end_time="11:15")
schedule.every().thursday.at("14:45").do(schedule_period, start_time="14:45", end_time="15:15")
schedule.every().friday.at("10:45").do(schedule_period, start_time="10:45", end_time="11:15")
schedule.every().friday.at("14:45").do(schedule_period, start_time="14:45", end_time="15:15")

print("Scheduler started. Waiting for the scheduled time...")


while True:
    schedule.run_pending()
    time.sleep(10)


