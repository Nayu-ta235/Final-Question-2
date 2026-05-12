import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Initialize session state to store student data
if 'students' not in st.session_state:
    st.session_state.students = []
if 'submitted_count' not in st.session_state:
    st.session_state.submitted_count = 0

# Title
st.title("📊 Student Marks Analysis System")
st.markdown("---")

st.subheader("Student Registration Form")

# Input widgets
col1, col2 = st.columns(2)

with col1:
    student_name = st.text_input("Student Name", key="name_input")

with col2:
    gender = st.radio("Gender", ["Male", "Female"], key="gender_input")

marks = st.number_input("Marks (0-100)", min_value=0, max_value=100, step=1, key="marks_input")

submit_button = st.button("Submit", key="submit_btn")

if submit_button:
    try:
        # Validate student name is not empty
        if not student_name or student_name.strip() == "":
            raise ValueError("Student name cannot be empty!")
        
        # Validate marks range (already handled by number_input but added for safety)
        if marks < 0 or marks > 100:
            raise ValueError("Marks must be between 0 and 100!")
        
        # Store student data
        st.session_state.students.append({
            "name": student_name.strip(),
            "gender": gender,
            "marks": marks
        })
        st.session_state.submitted_count += 1
        
        st.success(f"✅ Student {student_name} registered successfully!")
        
        # Show remaining students to register
        remaining = 3 - st.session_state.submitted_count
        if remaining > 0:
            st.info(f"📌 Need to register {remaining} more student(s)")
        
    except ValueError as e:
        st.error(f"❌ Error: {e}")

st.markdown("---")

# Check if 3 students have been submitted
if st.session_state.submitted_count >= 3:
    st.subheader("📈 Analysis Results")
    
    marks_array = np.array([s["marks"] for s in st.session_state.students[:3]])
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Mean Marks", f"{np.mean(marks_array):.2f}")
    with col2:
        st.metric("Maximum Marks", f"{np.max(marks_array)}")
    
    data = []
    for student in st.session_state.students[:3]:
        # Determine pass/fail (2e)
        result = "Pass" if student["marks"] >= 50 else "Fail"
        data.append({
            "Student Name": student["name"],
            "Gender": student["gender"],
            "Marks": student["marks"],
            "Result": result
        })
    
    df = pd.DataFrame(data)
    
    st.subheader("📋 Student Data DataFrame")
    st.dataframe(df)
    
    st.subheader("📊 Sorted by Marks (Ascending)")
    df_sorted = df.sort_values(by="Marks", ascending=True)
    st.dataframe(df_sorted)
    
    st.subheader("📌 Result Summary")
    pass_count = len(df[df["Marks"] >= 50])
    fail_count = len(df[df["Marks"] < 50])
    
    col1, col2 = st.columns(2)
    with col1:
        st.info(f"✅ Pass: {pass_count} student(s)")
    with col2:
        st.warning(f"❌ Fail: {fail_count} student(s)")
    
    st.subheader("📊 Student Marks Visualization")
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Bar chart
    bars = ax.bar(df["Student Name"], df["Marks"], color=['green' if m >= 50 else 'red' for m in df["Marks"]])
    
    # Add value labels on bars
    for bar, marks in zip(bars, df["Marks"]):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 1,
                f'{marks}', ha='center', va='bottom', fontweight='bold')
    
    # Add horizontal line for pass mark
    ax.axhline(y=50, color='blue', linestyle='--', linewidth=2, label='Pass Mark (50)')
    
    # Customize chart
    ax.set_xlabel("Student Name", fontsize=12)
    ax.set_ylabel("Marks", fontsize=12)
    ax.set_title("Student Marks Analysis", fontsize=14, fontweight='bold')
    ax.set_ylim(0, 105)
    ax.legend()
    ax.grid(axis='y', alpha=0.3)
    
    st.pyplot(fig)
    
    # Add a reset button
    st.markdown("---")
    if st.button("🔄 Reset All Data"):
        st.session_state.students = []
        st.session_state.submitted_count = 0
        st.rerun()

else:
    st.info(f"📝 Please register all 3 students. Currently registered: {st.session_state.submitted_count}/3")