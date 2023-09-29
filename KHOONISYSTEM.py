import streamlit as st
import pandas as pd

# Function to read blood bank data from a text file or initialize with sample data
def read_blood_bank_data(filename):
    blood_bank_data = {}
    try:
        with open(filename, "r") as file:
            for line in file:
                blood_group, quantity = line.strip().split("|")
                blood_bank_data[blood_group.strip()] = int(quantity.strip())
    except FileNotFoundError:
        # Initialize with sample data if the file doesn't exist
        blood_bank_data = {
            'A+': 10,
            'A-': 5,
            'B+': 7,
            'B-': 3,
            'O+': 15,
            'O-': 8,
            'AB+': 4,
            'AB-': 2,
        }
        write_blood_bank_data(filename, blood_bank_data)
    return blood_bank_data

# Function to write blood bank data to a text file
def write_blood_bank_data(filename, blood_bank_data):
    with open(filename, "w") as file:
        for blood_group, quantity in blood_bank_data.items():
            file.write(f"{blood_group} | {quantity}\n")

# Function to donate blood
def donate_blood():
    st.subheader("Donate Blood")
    blood_group = st.selectbox("Select your blood group:", list(blood_bank_data.keys()))
    donation_quantity = st.number_input("Enter the quantity (in unit) to donate:", min_value=0)
    
    if st.button("Donate"):
        if donation_quantity <= 0:
            st.error("Donation quantity must be greater than 0.")
        else:
            blood_bank_data[blood_group] += donation_quantity
            st.success(f"You have donated {donation_quantity} unit of {blood_group} blood.")
            write_blood_bank_data(filename, blood_bank_data)

# Function to take blood
def take_blood():
    st.subheader("Take Blood")
    blood_group = st.selectbox("Select the blood group you need:", list(blood_bank_data.keys()))
    required_quantity = st.number_input("Enter the quantity (unit) required:", min_value=0)
    
    if st.button("Take"):
        if required_quantity <= 0:
            st.error("Required quantity must be greater than 0.")
        elif required_quantity <= blood_bank_data[blood_group]:
            blood_bank_data[blood_group] -= required_quantity
            st.success(f"You have taken {required_quantity} ml of {blood_group} blood.")
            write_blood_bank_data(filename, blood_bank_data)
        else:
            st.error("Insufficient blood quantity available in this blood group.")

# Function to display available blood quantities
def display_available_blood():
    st.subheader("Available Blood Quantities")
    data = {'Blood Group': list(blood_bank_data.keys()), 'Available Quantity (units)': list(blood_bank_data.values())}
    df = pd.DataFrame(data)
    st.dataframe(df, height=300)

# Main Streamlit App
st.title("Blood Bank Management System")

# Read blood bank data from a text file or initialize with sample data
filename = "blood_bank_data.txt"
blood_bank_data = read_blood_bank_data(filename)

# Sidebar menu
menu_choice = st.sidebar.selectbox("Menu", ["Donate Blood", "Take Blood", "Available Blood"])
if menu_choice == "Donate Blood":
    donate_blood()
elif menu_choice == "Take Blood":
    take_blood()
elif menu_choice == "Available Blood":
    display_available_blood()
