import streamlit as st

# Mock Database
users = {"pharmacist1": "password123"}
medications = {
    "Atorvastatin": {"stock": 10},
    "Acetaminophen": {"stock": 5},
    "Lisinopril": {"stock": 0},
}
prescriptions = [
    {"id": 1, "patient": "John Doe", "medication": "Atorvastatin", "status": "Pending"},
    {"id": 2, "patient": "Jane Smith", "medication": "Lisinopril", "status": "Pending"},
]


# Login Function
def login(username, password):
    return username in users and users[username] == password


# Streamlit App
st.title("Pharmacy Management System")

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.subheader("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if login(username, password):
            st.session_state.logged_in = True
            st.success(f"Welcome, {username}!")
        else:
            st.error("Invalid credentials.")
else:
    st.sidebar.title("Menu")
    option = st.sidebar.radio("Select an option:", ["View Prescriptions", "Fill Prescription", "Logout"])

    if option == "View Prescriptions":
        st.subheader("Pending Prescriptions")
        for prescription in prescriptions:
            if prescription["status"] == "Pending":
                st.write(
                    f"ID: {prescription['id']}, Patient: {prescription['patient']}, Medication: {prescription['medication']}, Status: {prescription['status']}")

    elif option == "Fill Prescription":
        st.subheader("Fill a Prescription")
        prescription_id = st.number_input("Enter Prescription ID:", min_value=1)

        if st.button("Fill"):
            for prescription in prescriptions:
                if prescription["id"] == int(prescription_id) and prescription["status"] == "Pending":
                    medication = prescription["medication"]
                    if medications[medication]["stock"] > 0:
                        medications[medication]["stock"] -= 1
                        prescription["status"] = "Filled"
                        st.success(f"Prescription for {medication} has been filled.")
                    else:
                        st.error(f"{medication} is out of stock.")
                    break

    elif option == "Logout":
        st.session_state.logged_in = False

