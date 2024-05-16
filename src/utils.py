'''Utils module'''
from datetime import datetime, timedelta
from colorama import Fore, Style

def parse_input(user_input):
    '''Parsing user input'''
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

def format_cmd(text: str) -> str:
    '''Formating command name'''
    return Fore.CYAN + text + Style.RESET_ALL

def format_param(text: str) -> str:
    '''Formating parameter name'''
    return Fore.YELLOW + text + Style.RESET_ALL

def format_greeting(text: str) -> str:
    '''Formating greeting'''
    return Fore.GREEN + text + Style.RESET_ALL

def generate_input_invite() -> str:
    '''Generate input invite'''
    return Fore.GREEN + "\nEnter a command >>> " + Style.RESET_ALL

def get_greeting_tuple(birthday: str)  -> tuple:
    '''Calculate the user greeting date

    Args:
        birthday (str): the date in format YYYY.MM.DD.

    Returns:
        tuple in format (next_birthday_str, is_greet_this_week, greeting_date_str).
    '''
    today = datetime.today().date()
    today_year, today_month, today_day = today.timetuple()[0:3]
    birthday = datetime.strptime(birthday, "%d.%m.%Y").date()
    birthday_month, birthday_day = birthday.timetuple()[1:3]
    next_birthday_year =  today_year + 1 if (today_month,today_day)  > (birthday_month,birthday_day) else today_year
    next_birthday =  datetime(next_birthday_year, birthday_month, birthday_day).date()
    next_monday = next_birthday + timedelta(days = 7 - next_birthday.weekday())
    is_greet_this_week = next_birthday - today <= timedelta(days=6)
    greeting_date = next_monday if next_birthday.isoweekday() in (6,7) else next_birthday
    next_birthday_str = datetime.strftime(next_birthday,"%d.%m.%Y")
    greeting_date_str = datetime.strftime(greeting_date,"%d.%m.%Y")
    return (next_birthday_str, is_greet_this_week, greeting_date_str)
