import pandas as pd
from datetime import datetime

from datetime import datetime

def parse_start_time(time_range):
    """
    Extracts and parses the start time from a 12-hour formatted time range.
    Example: "02:00 PM - 03:00 PM" returns a time object for 2:00 PM.
    If parsing fails, returns a default time of 00:00.
    """
    try:
        # Split on the delimiter " - " and take the first part.
        start_time_str = time_range.split(" - ")[0]
        return datetime.strptime(start_time_str, "%I:%M %p").time()
    except Exception:
        return datetime.strptime("00:00 AM", "%I:%M %p").time()


def convert_time_range(time_str):
    """
    Converts a time range from 24-hour format to 12-hour format.
    Example: "14:00 - 15:00" becomes "02:00 PM - 03:00 PM"
    If the format isn't recognized, returns the original string.
    """
    try:
        # Split the time range on " - "
        parts = time_str.split(" - ")
        if len(parts) != 2:
            return time_str
        # Convert each part from 24-hour to a datetime object using the expected format
        start_time = datetime.strptime(parts[0].strip(), "%H:%M")
        end_time = datetime.strptime(parts[1].strip(), "%H:%M")
        # Format the times into 12-hour format with AM/PM
        start_formatted = start_time.strftime("%I:%M %p")
        end_formatted = end_time.strftime("%I:%M %p")
        return f"{start_formatted} - {end_formatted}"
    except Exception as e:
        # In case of an error, return the original string
        return time_str

def clean_datesheet(file_path):
    """
    Reads the Excel file and extracts exam details including day, date, time, course code, and course name.
    Assumes the following structure:
      - Row 0: Metadata (e.g. "Spring 2025 Semester")
      - Row 1: Column headers (e.g. "Day", "Date", "Course Code 1", "Course Name 1", ...)
      - Row 2: Time row; each course column pair (code, name) shares the same time from this row.
      - Row 3+: Data rows.
    The date is converted to a string (YYYY-MM-DD) and missing values are replaced with empty strings.
    The time is converted from a 24-hour range (e.g., "14:00 - 15:00") to a 12-hour range (e.g., "02:00 PM - 03:00 PM").
    """
    df = pd.read_excel(file_path, header=None, sheet_name="Complete")
    # Use the third row (index 2) for time values
    time_row = df.iloc[2]
    data = df.iloc[3:].reset_index(drop=True)
    courses = []
    ncols = data.shape[1]
    
    for _, row in data.iterrows():
        day = row[0] if pd.notna(row[0]) else ""
        try:
            date_dt = pd.to_datetime(row[1], errors="coerce")
            if pd.isna(date_dt):
                continue
            date_str = date_dt.strftime("%Y-%m-%d")
        except Exception:
            continue

        # Iterate over course columns in pairs (course code, course name)
        for j in range(2, ncols, 2):
            course_code = row[j] if pd.notna(row[j]) else ""
            if course_code != "":
                course_name = row[j+1] if j+1 < ncols and pd.notna(row[j+1]) else ""
                time_slot = ""
                if j+1 < ncols and pd.notna(time_row[j+1]):
                    # Assume the time is given as a string like "14:00 - 15:00"
                    raw_time = str(time_row[j+1]).strip()
                    time_slot = convert_time_range(raw_time)
                courses.append({
                    "day": str(day).strip(),
                    "date": date_str,
                    "time": time_slot,
                    "course_code": str(course_code).strip(),
                    "course_name": str(course_name).strip()
                })
    return courses
