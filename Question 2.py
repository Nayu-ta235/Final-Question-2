import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def main():
    st.title("📊 Student Marks Analysis System")
    st.write("Enter details for **THREE (3)** students")
    
    # Initialize session state to store student data
    if 'students' not in st.session_state:
        st.session_state.students = []
    if 'submitted_count' not in st.session_state:
        st.session_state.submitted_count = 0
    
    # Input widgets
    st.subheader("Student Information")
    student_name = st.text_input("Student Name")
    gender = st.radio("Gender", ["Male", "Female"])
    marks = st.number_input("Marks (0-100)", min_value=0, max_value=100, step=1)
    submit_button = st.button("Submit")
    
    # Exception handling for empty name
    if submit_button:
        try:
            if not student_name or student_name.strip() == "":
                raise ValueError("Student name cannot be empty!")
            
            if st.session_state.submitted_count < 3:
                st.session_state.students.append({
                    "name": student_name,
                    "gender": gender,
                    "marks": marks
                })
                st.session_state.submitted_count += 1
                st.success(f"✅ Student {student_name} added. ({st.session_state.submitted_count}/3 students)")
                st.rerun()
            else:
                st.warning("⚠️ You have already entered 3 students!")
                
        except ValueError as e:
            st.error(f"Error: {e}")
    
    # Process and display analysis only when 3 students are entered
    if st.session_state.submitted_count == 3:
        st.subheader("📈 Marks Analysis")
        
        # Extract marks into NumPy array
        marks_array = np.array([s["marks"] for s in st.session_state.students])
        
        mean_marks = np.mean(marks_array)
        max_marks = np.max(marks_array)
        
        st.write(f"**Mean Marks:** {mean_marks:.2f}")
        st.write(f"**Maximum Marks:** {max_marks}")
        
        # Create Pandas DataFrame
        data = []
        for s in st.session_state.students:
            result = "Pass" if s["marks"] >= 50 else "Fail"
            data.append({
                "Student Name": s["name"],
                "Gender": s["gender"],
                "Marks": s["marks"],
                "Result": result
            })
        
        df = pd.DataFrame(data)
        
        # Sort by marks in ascending order
        df_sorted = df.sort_values(by="Marks", ascending=True)
        
        st.subheader("📋 Student Records (Sorted by Marks - Ascending)")
        st.dataframe(df_sorted)
        
        # Display result summary
        st.subheader("📌 Result Classification")
        pass_count = len(df[df["Result"] == "Pass"])
        fail_count = len(df[df["Result"] == "Fail"])
        st.write(f"✅ Pass: {pass_count} student(s)")
        st.write(f"❌ Fail: {fail_count} student(s)")
        
        # Graph visualization
        st.subheader("📊 Marks Visualization")
        fig, ax = plt.subplots()
        bars = ax.bar(df["Student Name"], df["Marks"], color=['green' if m >= 50 else 'red' for m in df["Marks"]])
        ax.set_ylabel("Marks")
        ax.set_title("Student Marks")
        ax.set_ylim(0, 100)
        
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 2, f'{int(height)}', ha='center', va='bottom')
        
        st.pyplot(fig)
        
        # Reset button
        if st.button("Reset All Data"):
            st.session_state.students = []
            st.session_state.submitted_count = 0
            st.rerun()

if __name__ == "__main__":
    main()