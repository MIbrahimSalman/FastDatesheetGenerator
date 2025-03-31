import pandas as pd

def clean_datesheet(file_path):
    """
    Reads the Excel file and extracts exam details including day, date, time, course code, and course name.
    Assumes the following structure:
      - Row 0: Metadata (e.g. "Spring 2025 Semester")
      - Row 1: Column headers (e.g. "Day", "Date", "Course Code 1", "Course Name 1", ...)
      - Row 2: Time row; each course column pair (code, name) shares the same time from this row.
      - Row 3+: Data rows.
    The date is converted to a string (YYYY-MM-DD) and missing values are replaced with empty strings.
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
                # For each pair, the time is taken from the time_row (using the same column index as the course name)
                if j+1 < ncols and pd.notna(time_row[j+1]):
                    time_slot = str(time_row[j+1]).strip()
                courses.append({
                    "day": str(day).strip(),
                    "date": date_str,
                    "time": time_slot,
                    "course_code": str(course_code).strip(),
                    "course_name": str(course_name).strip()
                })
    return courses