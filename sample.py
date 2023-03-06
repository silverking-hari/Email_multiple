import openpyxl
import pyodbc
import random
import pandas as pd
import os
import json
from datetime import date
from mail import current_dir, calling_mail, smtp_logout, server

'''pattern for checking the email header'''

email_pattern = r'email|email_address|email-id|.*mail*'
dob_pattern = r'\b\d{2}/\d{2}/\d{4}\b|date of birth|Year of birth|dob|birthdate|\w*birth\w*|d.o.b'
doj_pattern = r'.*join|doj'
name_pattern = r'.*name'

# file directory for data extraction
filepath = current_dir / 'data_source'
file_list = os.listdir(filepath)
with open(current_dir / 'master_copies' / 'copied_file.txt', 'r+') as copied_file:
    data = copied_file.read()


def input_files(files):
    master_copy = pd.read_csv(current_dir / 'master_copies' / 'master_copy.csv')
    if files.endswith(".csv"):
        df = pd.read_csv(os.path.join(filepath, files))
        master_copy = pd.concat([master_copy, df], ignore_index=True).drop_duplicates()

    elif files.endswith(".xlsx") or files.endswith(".xls"):
        df = pd.read_excel(os.path.join(filepath, files))
        master_copy = pd.concat([master_copy, df], ignore_index=True).drop_duplicates()

    elif files.endswith(".json"):
        with open(os.path.join(filepath, files), 'r') as json_file:
            data = json.load(json_file)
        df = pd.json_normalize(data)
        master_copy = pd.concat([master_copy, df], ignore_index=True).drop_duplicates()

    master_copy.to_csv(current_dir / 'master_copies' / 'master_copy.csv', index=False)


def find_column(df, pattern):
    matching_columns = df.columns[df.columns.str.contains(pattern, case=False)]
    if len(matching_columns) > 0:
        return matching_columns.tolist()[0]
    else:
        return None


def call_letter_event():
    pass


def motivational_event():
    tem = "Templates \\ motivational"
    time = date.today().strftime("%A")
    if time.lower() == 'monday':
        sub = f"Motivation of this week - {date.today()}"


def public_holiday():
    pass


def anniversary_event():
    tem = "Templates \\ anniversary"
    doj_column = find_column(df, doj_pattern)
    if doj_column is None:
        print('No date of joining column found')
    else:
        df[doj_column] = pd.to_datetime(df[doj_column])

    time_completion = pd.to_datetime('today') - df[doj_column]
    years = time_completion.dt.days // 365
    # subj = random.choice[
    #   "Thank you for {} years of support", "Looking back on {} years of growth", "{} Years of Serving Our Community",
    #    "Crazy how time flies: It’s been {} years since our launch!",
    #    "Thanks for being part of our journey during this {} year",].format(years)

    one_year_employees = df[years >= 1]

    print(one_year_employees[email_column].unique())
    print(one_year_employees[name_column])
    '''
    for e, n in zip(one_year_employees[email_column].unique(), one_year_employees[name_column]):
        calling_mail(e, n, subj, tem)
    smtp_logout(True)
    '''


def birthday_event():
    tem = "Templates\\birthday"
    random_file = random.choice((os.listdir(current_dir / 'Templates' / 'birthday')))
    sub = ("HAPPY BIRTHDAY!", "❤ Happy Birthday from us!", "It's Almost Your Birthday , Let’s Celebrate?,",
           "Have the Best. Birthday. Ever.", "Let’s celebrate your birthday!",
           "We Heard It’s Your Birthday!", "Your Birthday Just Got Even More Empowering.",
           "happy happy happy birthday")
    subj = random.choice(sub)

    # Algorithm for find the column header
    dob_column = find_column(df, dob_pattern)
    if dob_column is None:
        print('No date of birth column found')
    else:
        df[dob_column] = pd.to_datetime(df[dob_column])  # convert 'date' column to datetime type

    # Get the current month and day
    now = date.today()
    current_month, current_day = now.month, now.day

    # Filter the dataframe to rows where the month and day of 'dob_header' matches the current month and day
    dob_matches = df[(df[dob_column].dt.month == current_month) & (df[dob_column].dt.day == current_day)]

    # Print the matching rows
    if len(dob_matches) > 0:
        for e, n in zip(dob_matches[email_column].unique(), dob_matches[name_column]):
            calling_mail(e, n, subj, tem, random_file)
        smtp_logout(server)


    '''
    for emp in df[email_column].unique():
        if emp in dob_matches[email_column].unique():
            continue
        calling_mail(emp, n=None, )'''

if file_list is not None:
    for unread_files in file_list:
        # Check if the file has already been copied
        if unread_files not in data:
            df = input_files(unread_files)
            with open(current_dir / 'master_copies' / 'copied_file.txt', 'a+') as copied_file:
                copied_file.write(unread_files + ',')
                copied_file.close()
    df = pd.read_csv(current_dir / 'master_copies' / 'master_copy.csv')
else:
    print("there's no file in the included directory so extracting data from database")
    # connecting the database
    server = 'SSLTP11497\SQLEXPRESS'
    database = 'master'

    # connection object
    cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER=' + server + ';DATABASE=' + database)
    cursor = cnxn.cursor()

    df = pd.read_sql("select * from ")

name_column = find_column(df, name_pattern)
if name_column is None:
    print('No name column found')
else:
    print('Name column:', name_column)

email_column = find_column(df, email_pattern)
if email_column is None:
    print('No email column found')
else:
    print('Email column:', email_column)

if __name__ == "__main__":
    birthday_event()
    # anniversary_event()
    # motivational_event()
