import streamlit as st
import sqlite3
import pandas as pd

# --------------------------
# Database connection
# --------------------------
conn = sqlite3.connect("employees.db", check_same_thread=False)
cursor = conn.cursor()

# --------------------------
# Create table
# --------------------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS employees(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT,
    phone TEXT,
    department TEXT,
    position TEXT,
    salary REAL
)
""")
conn.commit()

# --------------------------
# Page config
# --------------------------
st.set_page_config(page_title="Employee Management System", layout="centered")
st.title("Employee Management System")

menu = ["add employee", "view employee", "update employee", "delete employee"]
choice = st.sidebar.selectbox("Menu", menu)

# --------------------------
# Add employee
# --------------------------
if choice == "add employee":
    st.subheader("+ Add New Employee")
    name = st.text_input("Name")
    email = st.text_input("Email")
    phone = st.text_input("Phone")
    department = st.selectbox("Department", ["HR", "Finance", "IT", "Sales", "Marketing"])
    position = st.text_input("Position")
    salary = st.number_input("Salary", min_value=0.0)

    if st.button("Save Employee"):
        cursor.execute("INSERT INTO employees(name,email,phone,department,position,salary) VALUES(?,?,?,?,?,?)",
                       (name, email, phone, department, position, salary))
        conn.commit()
        st.success(f"Employee {name} added successfully!")

# --------------------------
# View employees
# --------------------------
elif choice == "view employee":
    st.subheader("📋 View Employees")
    cursor.execute("SELECT * FROM employees")
    data = cursor.fetchall()
    df = pd.DataFrame(data, columns=["ID", "Name", "Email", "Phone", "Department", "Position", "Salary"])
    st.dataframe(df)

# --------------------------
# Update employee
# --------------------------
elif choice == "update employee":
    st.subheader("✏️ Update Employee")
    cursor.execute("SELECT * FROM employees")
    data = cursor.fetchall()
    df = pd.DataFrame(data, columns=["ID", "Name", "Email", "Phone", "Department", "Position", "Salary"])
    st.dataframe(df)

    employee_id = st.number_input("Enter Employee ID to Update", min_value=1)
    new_name = st.text_input("New Name")
    new_email = st.text_input("New Email")
    new_phone = st.text_input("New Phone")
    new_department = st.selectbox("New Department", ["HR", "Finance", "IT", "Sales", "Marketing"])
    new_position = st.text_input("New Position")
    new_salary = st.number_input("New Salary", min_value=0.0)

    if st.button("Update Employee"):
        cursor.execute("""UPDATE employees 
                          SET name=?, email=?, phone=?, department=?, position=?, salary=? 
                          WHERE id=?""",
                       (new_name, new_email, new_phone, new_department, new_position, new_salary, employee_id))
        conn.commit()
        st.success(f"Employee ID {employee_id} updated successfully!")

# --------------------------
# Delete employee
# --------------------------
elif choice == "delete employee":
    st.subheader("🗑️ Delete Employee")
    cursor.execute("SELECT * FROM employees")
    data = cursor.fetchall()
    df = pd.DataFrame(data, columns=["ID", "Name", "Email", "Phone", "Department", "Position", "Salary"])
    st.dataframe(df)

    employee_id = st.number_input("Enter Employee ID to Delete", min_value=1)
    if st.button("Delete Employee"):
        cursor.execute("DELETE FROM employees WHERE id=?", (employee_id,))
        conn.commit()
        st.warning(f"Employee ID {employee_id} deleted successfully!")
