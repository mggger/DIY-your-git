import subprocess
from datetime import datetime, timedelta

# 字符映射字典
chars = {
    'A': [1, 2, 3, 4, 5, 6, 7, 10, 14, 17, 22, 23, 24, 25, 26, 27],
    'B': [0, 1, 2, 3, 4, 5, 6, 7, 10, 13, 14, 17, 20, 22, 23, 25, 26],
    'C': [1, 2, 3, 4, 5, 7, 13, 14, 20, 21, 27],
    'D': [0, 1, 2, 3, 4, 5, 6, 7, 13, 14, 20, 22, 23, 24, 25, 26],
    'E': [0, 1, 2, 3, 4, 5, 6, 7, 10, 13, 14, 17, 20, 21, 24, 27],
    'F': [0, 1, 2, 3, 4, 5, 6, 7, 10, 14, 17, 21, 24],
    'G': [1, 2, 3, 4, 5, 7, 13, 14, 17, 20, 21, 24, 25, 26, 27],
    'H': [0, 1, 2, 3, 4, 5, 6, 10, 17, 21, 22, 23, 24, 25, 26, 27],
    'I': [0, 6, 7, 8, 9, 10, 11, 12, 13, 14, 20],
    'J': [5, 7, 13, 14, 20, 21, 22, 23, 24, 25, 26],
    'K': [0, 1, 2, 3, 4, 5, 6, 10, 16, 18, 21, 22, 26, 27],
    'L': [0, 1, 2, 3, 4, 5, 6, 13, 20, 27],
    'M': [0, 1, 2, 3, 4, 5, 6, 8, 16, 22, 28, 29, 30, 31, 32, 33, 34],
    'N': [0, 1, 2, 3, 4, 5, 6, 8, 9, 10, 17, 18, 19, 21, 22, 23, 24, 25, 26, 27],
    'O': [1, 2, 3, 4, 5, 7, 13, 14, 20, 22, 23, 24, 25, 26],
    'P': [0, 1, 2, 3, 4, 5, 6, 7, 10, 14, 17, 22, 23],
    'Q': [1, 2, 3, 4, 5, 7, 13, 14, 19, 20, 22, 23, 24, 25, 26, 27],
    'R': [0, 1, 2, 3, 4, 5, 6, 7, 10, 14, 17, 22, 23, 25, 26, 27],
    'S': [1, 2, 6, 7, 10, 13, 14, 17, 20, 21, 25, 26],
    'T': [0, 7, 14, 15, 16, 17, 18, 19, 20, 21, 28],
    'U': [0, 1, 2, 3, 4, 5, 6, 13, 20, 21, 22, 23, 24, 25, 26, 27],
    'V': [0, 1, 2, 3, 4, 5, 13, 20, 21, 22, 23, 24, 25, 26],
    'W': [0, 1, 2, 3, 4, 5, 6, 12, 18, 26, 28, 29, 30, 31, 32, 33, 34],
    'X': [0, 1, 2, 4, 5, 6, 10, 17, 21, 22, 23, 25, 26, 27],
    'Y': [0, 1, 2, 10, 17, 18, 19, 20, 21, 22, 23],
    'Z': [0, 4, 5, 6, 7, 10, 11, 13, 14, 16, 17, 20, 21, 22, 23, 27],
}


def first_sunday(year):
    """获取指定年份的第一个星期日"""
    first_day = datetime(year, 1, 1)
    day_of_week = first_day.weekday()
    days_until_sunday = (6 - day_of_week) % 7  # Python中周一是0，周日是6
    return first_day + timedelta(days=days_until_sunday)


def string_to_ascii_art(s):
    """将字符串转换为ASCII艺术图"""
    sunday = 0
    days = [" "] * 365

    for char in s:
        char = char.upper()
        if char == " ":
            sunday += 7 * 2
            continue

        if char not in chars:
            continue

        char_pattern = chars[char]
        width = max(char_pattern) // 7 + 1

        for day in char_pattern:
            if sunday + day < len(days):
                days[sunday + day] = "#"

        sunday += (width + 1) * 7

    # 将天数转换为周视图
    weeks = [[" " for _ in range(53)] for _ in range(7)]
    for i, day in enumerate(days):
        if day == "#":
            week = i // 7
            weekday = i % 7
            if week < 53:
                weeks[weekday][week] = day

    return "\n".join("".join(week) for week in weeks)


def string_to_dates(year, s):
    """将字符串转换为日期列表"""
    sunday = first_sunday(year)
    dates = []

    for char in s:
        char = char.upper()
        if char == " ":
            sunday += timedelta(days=7 * 2)
            continue

        if char not in chars:
            continue

        char_pattern = chars[char]
        width = max(char_pattern) // 7 + 1

        for day in char_pattern:
            date = sunday + timedelta(days=day)
            dates.append(date)

        sunday += timedelta(days=(width + 1) * 7)

    return dates


def main():

    dates = string_to_dates(2025, "QUIET")
    print(dates)

    # Git提交
    for date in dates:
        date_string = date.strftime("%c")
        command = f'git commit --date="{date_string}" -m "{date.strftime("%a %b %d %Y")}" --allow-empty'
        subprocess.run(command, shell=True)


if __name__ == "__main__":
    main()