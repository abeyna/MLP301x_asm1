import re

import numpy as np
import pandas as pd

filename = input("Enter a filename: ")

try:
    df_raw = pd.read_csv(filename, sep=" ", header=None)
except:
    print("File cannot be found!")

print("**** ANALYZING ****")
print("\n*************************************************************************")

df_exam = df_raw[0].str.split(',', n=1, expand=True)
df_exam.rename(columns={0: "Student Code", 1: "Answers"}, inplace=True)


def to_array(answer_str):
    return np.array(answer_str.split(','))


df_exam['Answers'] = df_exam['Answers'].apply(to_array)


def check_code(code):
    if not re.findall("^N[0-9]{8}", code[0:9]):
        print("- Invalid line of data: N# is invalid")
        print(code)
        return code


def check_data(raw_str):
    if len(raw_str.split(',')) != 26:
        print("- Invalid line of data: does not contain exactly 26 values:")
        print(raw_str)
        return raw_str


def find_invalid_code(student_code):
    if not re.findall("^N[0-9]{8}", student_code):
        return False
    else:
        return True


def find_invalid_answer(answer_arr):
    if answer_arr.size != 25:
        return False
    else:
        return True


df_exam["Valid"] = df_exam["Student Code"].apply(find_invalid_code) & df_exam["Answers"].apply(find_invalid_answer)

valid_lines = df_exam["Valid"].values.sum()
invalid_lines = df_exam["Student Code"].count() - valid_lines

print(df_exam)
print("*************************************************************************\n")

if invalid_lines == 0:
    print("No errors found!")

df_raw[0].apply(check_data)
df_raw[0].apply(check_code)

print("\n**** REPORT ****")
print(f"Total valid lines of data: {valid_lines}")
print(f"Total invalid lines of data: {invalid_lines}")
