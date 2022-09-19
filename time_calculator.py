def extract_time(time_str):
    time_list = time_str.split(":")
    # Raise Exception if time list has a length different from 2
    if len(time_list) != 2:
        raise Exception("Error: Wrong Syntax.")
    hours_str = time_list[0].strip()
    minutes_str = time_list[1].strip()
    # Raise Exception if time has an invalid format
    if not (hours_str.isdigit() and minutes_str.isdigit()):
        raise Exception("Error: Invalid time.")
    hours = int(hours_str)
    minutes = int(minutes_str)
    time_in_minutes = hours*60+minutes
    return time_in_minutes


def extract_start_time(start_time_str):
    if "PM" in start_time_str and "AM" in start_time_str:
        raise Exception("Error: The start time should contain only AM or PM.")
    elif "PM" in start_time_str:
        start_time_str = start_time_str.replace("PM", "").strip()
        start_time_in_minutes = extract_time(start_time_str)+12*60
    elif "AM" in start_time_str:
        start_time_str = start_time_str.replace("AM", "").strip()
        start_time_in_minutes = extract_time(start_time_str)
    else:
        raise Exception("Error: The start time doesn't contain AM or PM.")
    return start_time_in_minutes


def sum_start_time_and_duration (start_time_in_minutes,duration_in_minutes):
    sum_in_minutes = start_time_in_minutes + duration_in_minutes
    days = int(sum_in_minutes / (24*60))
    hours = int((sum_in_minutes - days * (24*60)) / 60)
    minutes = sum_in_minutes - days * (24*60) - hours * 60
    end_time_list = [hours, minutes, days]
    return end_time_list


def generate_end_time_str(end_time_list):
    hours = end_time_list[0]
    hours_str = str(hours)
    minutes = end_time_list[1]
    minutes_str = str(minutes)
    if len(minutes_str) == 1:
        minutes_str = "0" + minutes_str
    if hours < 12:
        if hours_str == "0":
            hours_str = "12"
        end_time_str = hours_str + ":" + minutes_str + " AM"
    else:
        if hours_str != "12":
            end_time_str = str(int(hours_str)%12) + ":" + minutes_str + " PM"
        else:
            end_time_str = hours_str+ ":" + minutes_str + " PM"
    return end_time_str


def generate_duration_days_string(end_time_list):
    days = end_time_list[2]
    if days == 0:
        duration_days_str = None
    elif days == 1:
        duration_days_str = "(next day)"
    else:
        duration_days_str = "(" + str(days) + " days later)"
    return duration_days_str


def generate_week_day_string(end_time_list,starting_day):
    days = end_time_list[2]
    week_days = {"sunday": 0, "monday": 1, "tuesday": 2, "wednesday": 3, "thursday": 4, "friday": 5, "saturday": 6}
    if not starting_day.lower() in week_days:
        raise Exception("Error: Invalid starting day.")
    end_day_code = (week_days[starting_day.lower()]+days) % 7
    week_days_str_list = list(week_days.keys())
    week_days_code_list = list(week_days.values())
    position = week_days_code_list.index(end_day_code)
    end_day_str_lowercase = week_days_str_list[position]
    end_day_str = end_day_str_lowercase.capitalize()
    return end_day_str


def generate_strings(start_time_str, duration_str, starting_day):
    start_time_in_minutes = extract_start_time(start_time_str)
    duration_in_minutes = extract_time(duration_str)
    end_time_list = sum_start_time_and_duration(start_time_in_minutes, duration_in_minutes)
    end_time_str = generate_end_time_str(end_time_list)
    duration_days_str = generate_duration_days_string(end_time_list)
    if starting_day is not None:
        end_day_str = generate_week_day_string(end_time_list,starting_day)
    else:
        end_day_str = None
    strings = [end_time_str, end_day_str, duration_days_str]
    return strings


def add_time(*args):
    if len(args) == 2 and isinstance(args[0], str) and isinstance(args[1], str):
        start_time_str = args[0]
        duration_str = args[1]
        starting_day = None
        strings = generate_strings(start_time_str, duration_str, starting_day)
        end_time_str = strings[0]
        duration_days_str = strings[2]
        if duration_days_str is not None:
            print("# Returns: " + end_time_str + " " + duration_days_str)
        else:
            print("# Returns: " + end_time_str)

    elif len(args) == 3 and isinstance(args[0], str) and isinstance(args[1], str) and isinstance(args[2], str):
        start_time_str = args[0]
        duration_str = args[1]
        starting_day = args[2]
        strings = generate_strings(start_time_str, duration_str, starting_day)
        end_time_str = strings[0]
        end_day_str = strings[1]
        duration_days_str = strings[2]
        if duration_days_str is not None:
            print("# Returns: " + end_time_str + ", " + end_day_str + " " + duration_days_str)
        else:
            print("# Returns: " + end_time_str + ", " + end_day_str)
    else:
        raise Exception("Error: Wrong Parameters.")
