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
messages = []  # For patient communication


# Login Function
def login(username, password):
    return username in users and users[username] == password


# Streamlit App
st.title("WELCOME TO PHARMANET")

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
    # Sidebar Menu
    st.sidebar.title("Menu")
    option = st.sidebar.radio(
        "Select an option:",
        ["Dashboard", "View Prescriptions", "Fill Prescription", "Inventory Management", "Patient Communication",
         "Logout"]
    )

    # Dashboard
    if option == "Dashboard":
        st.subheader("Dashboard")
        total_prescriptions = len(prescriptions)
        pending_prescriptions = len([p for p in prescriptions if p["status"] == "Pending"])
        filled_prescriptions = total_prescriptions - pending_prescriptions

        st.metric("Total Prescriptions", total_prescriptions)
        st.metric("Pending Prescriptions", pending_prescriptions)
        st.metric("Filled Prescriptions", filled_prescriptions)

    # View Prescriptions
    elif option == "View Prescriptions":
        st.subheader("Pending Prescriptions")
        for prescription in prescriptions:
            st.write(
                f"ID: {prescription['id']}, Patient: {prescription['patient']}, Medication: {prescription['medication']}, Status: {prescription['status']}"
            )

    # Fill Prescription
    elif option == "Fill Prescription":
        st.subheader("Fill a Prescription")
        prescription_id = st.number_input("Enter Prescription ID:", min_value=1, step=1)

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
            else:
                st.error(f"No pending prescription found with ID {int(prescription_id)}.")

    # Inventory Management
    elif option == "Inventory Management":
        st.subheader("Inventory Management")
        for medication, details in medications.items():
            st.write(f"{medication}: {details['stock']} units available")

        medication_name = st.text_input("Medication Name")
        restock_amount = st.number_input("Restock Amount", min_value=0, step=1)

        if st.button("Restock"):
            if medication_name in medications:
                medications[medication_name]["stock"] += restock_amount
                st.success(f"{restock_amount} units of {medication_name} added to inventory.")
            else:
                st.error(f"{medication_name} is not in the inventory.")

    # Patient Communication
    elif option == "Patient Communication":
        st.subheader("Patient Communication")

        # Send a message to a patient
        patient_name = st.text_input("Patient Name")
        message_content = st.text_area("Message Content")

        if st.button("Send Message"):
            messages.append({"patient": patient_name, "message": message_content})
            st.success(f"Message sent to {patient_name}!")

        # View all messages
        if messages:
            st.subheader("Message History")
            for msg in messages:
                st.write(f"To: {msg['patient']} - Message: {msg['message']}")

    # Logout
    elif option == "Logout":
        st.session_state.logged_in = False

