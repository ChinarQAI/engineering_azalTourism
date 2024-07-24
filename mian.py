import streamlit as st
import requests

# Define the endpoint URL
endpoint_url = "http://127.0.0.1:8000//azal/itinerary_generator/"

# Step 1: Ask the user for the location
st.title("Azal Itinerary Generator")
st.subheader("Select a location to visit")
location = st.selectbox("Where to visit?", ["Izmir", "Bursa", "Istanbul"])

# Step 2: Ask the user for the number of days
st.subheader("Enter the number of days")
number_of_days = st.number_input("Number of days", min_value=1, step=1)

# Step 3: Chat interface to get a query from the user
st.subheader("Tell us something about you")
query = st.text_area("Describe what you would like to do")

if st.button("Generate Itinerary"):
    if location and number_of_days and query:
        # Modify the query with additional information
        modified_query = f"{query} I am visiting {location}, I am visiting for {number_of_days} days."

        # Prepare the payload for the API request
        payload = {
            "query": modified_query,
            "session_id": "unique_session_id"  # You can generate or fetch a unique session ID as needed
        }

        try:
            # Send the request to the endpoint
            response = requests.post(endpoint_url, json=payload)
            response_data = response.json()

            if response.status_code == 200:
                # Display the generated itinerary
                st.success("Itinerary Generated Successfully!")
                st.write(response_data)
            else:
                st.error(f"Error: {response_data.get('detail', 'An error occurred')}")

        except Exception as e:
            st.error(f"Error in sending request: {e}")
    else:
        st.error("Please fill all the fields.")

