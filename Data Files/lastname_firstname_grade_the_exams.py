import re

import numpy as np
import pandas as pd

# Name of the file.
filename = input("Enter a filename: ")

# Create raw dataframe with one column.
try:
    df_raw = pd.read_csv(filename, sep=" ", header=None)
except:
    print("File cannot be found!")

print("**** ANALYZING ****")

# Create general dataframe from raw with 'Student Code' column separated with the rest.
df_general = df_raw[0].str.split(',', n=1, expand=True)
df_general.rename(columns={0: "Student Code", 1: "Answers"}, inplace=True)


# Convert Answers column to numpy array.
def to_array(answer_str):
    return np.array(answer_str.split(','))


df_general['Answers'] = df_general['Answers'].apply(to_array)


# Check valid Student Code from df_raw for display to console.
def check_code(code):
    if not re.findall("^N[0-9]{8}", code[0:9]):
        print(code)
        return code


# Check valid data from df_raw for display to console.
def check_data(raw_str):
    if len(raw_str.split(',')) != 26:
        print(raw_str)
        return raw_str


# Check valid Student Code from df_general for Valid column.
def find_invalid_code(student_code):
    if not re.findall("^N[0-9]{8}", student_code):
        return False
    else:
        return True


# Check valid Answers array from df_general for Valid column.
def find_invalid_answer(answer_arr):
    if answer_arr.size != 25:
        return False
    else:
        return True


# Create Valid column to distinguish valid rows.
df_general["Valid"] = df_general["Student Code"].apply(find_invalid_code) & df_general["Answers"].apply(
    find_invalid_answer)

# Count total valid rows.
valid_lines = df_general["Valid"].values.sum()

# Count total invalid rows.
invalid_lines = df_general["Student Code"].count() - valid_lines

# Display to console analysis result.
if invalid_lines == 0:
    print("No errors found!")
else:
    print("- Invalid line of data: does not contain exactly 26 values:")
    df_raw[0].apply(check_data)
    print("- Invalid line of data: N# is invalid")
    df_raw[0].apply(check_code)

# Display total report to console.
print("\n**** REPORT ****")
print(f"Total valid lines of data: {valid_lines}")
print(f"Total invalid lines of data: {invalid_lines}")


# Count correct answer when compare to answer_key in array.
def count_correct_answer(answer_arr):
    answer_key = np.array("B,A,D,D,C,B,D,A,C,C,D,B,A,B,A,C,B,D,A,C,A,A,B,D,D".split(','))
    correct_answers = answer_key == answer_arr
    return np.count_nonzero(correct_answers == True)


# Count blank (empty) answers in array.
def count_blank_answer(answer_arr):
    blank_answers = np.where(answer_arr == '')
    return np.count_nonzero(blank_answers)


# Create valid dataframe only for valid data.
df_valid = df_general.loc[(df_general["Valid"]), ["Student Code", "Answers"]]

# Create Correct Total column in df_valid.
df_valid["Correct Total"] = df_valid["Answers"].apply(count_correct_answer)

# Create Blank Total column in df_valid.
df_valid["Blank Total"] = df_valid["Answers"].apply(count_blank_answer)

# Create Incorrect Total column in df_valid.
df_valid["Incorrect Total"] = 25 - df_valid["Correct Total"] - df_valid["Blank Total"]

# Calculate grade for each Student.
df_valid["Grades"] = df_valid["Correct Total"] * 4 + df_valid["Incorrect Total"] * (-1)

print("\n*************************************************************************")
print(df_valid)
print("*************************************************************************\n")

# Report mean, the highest score, the lowest score, range of scores and median score in dataframe.
print(f"Mean (average) score: {round(df_valid['Grades'].mean(), 2)}")
print(f"The Highest score: {df_valid['Grades'].max()}")
print(f"The Lowest score: {df_valid['Grades'].min()}")
print(f"Range of scores: {df_valid['Grades'].max() - df_valid['Grades'].min()}")
print(f"Median score: {int(df_valid['Grades'].median())}")

# Create Report dataframe for export to txt file.
df_report = df_valid[['Student Code', 'Grades']]
df_report.to_csv(f'{filename.replace(".txt","")}_grades.txt', sep=',', header=None, index=None)