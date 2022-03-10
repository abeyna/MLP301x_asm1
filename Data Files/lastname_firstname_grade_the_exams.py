import numpy as np
import pandas as pd

filename = input("Enter a filename: ")
try:
    with open(filename, "r") as file1:
        answer_list = [line.split() for line in file1]
    print(f"Successfully opened {filename}")
except:
    print("File cannot be found!")

np_answer = np.array(answer_list)