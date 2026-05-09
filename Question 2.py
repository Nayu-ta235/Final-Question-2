import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# a. Input Collection
student_data_list = []
print("Enter data for 3 students:")

try:
    for i in range(3):
        name = input(f"Student {i+1} Name: ")
        if not name.strip():
            raise ValueError("Name cannot be empty!")  # b. Exception Handling
        
        gender = input(f"Gender (M/F): ")
        marks = float(input(f"Marks: "))
        student_data_list.append({"Name": name, "Gender": gender, "Marks": marks})

    # d. Create DataFrame
    df = pd.DataFrame(student_data_list)

    # c. NumPy Analysis
    marks_array = df['Marks'].values
    print(f"\nMean Marks: {np.mean(marks_array):.2f}")
    print(f"Maximum Marks: {np.max(marks_array)}")

    # e. Data Processing
    df['Result'] = df['Marks'].apply(lambda x: "Pass" if x >= 50 else "Fail")

    print("\n--- Processed Data ---")
    print(df)  # Changed from display() to print() for compatibility

    print("\n--- Sorted by Marks ---")
    print(df.sort_values(by="Marks"))  # Changed from display() to print()

    # f. Visualizing (Graph)
    df.plot(kind='bar', x='Name', y='Marks', color='skyblue', title='Student Marks')
    plt.ylabel('Marks')
    plt.show()

except ValueError as e:
    print(f"Input Error: {e}")