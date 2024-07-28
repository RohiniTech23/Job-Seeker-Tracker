import streamlit as st
from supabase import create_client, Client

# Access Supabase configuration from secrets
url = st.secrets["supabase"]["url"]
key = st.secrets["supabase"]["key"]
supabase: Client = create_client(url, key)

# Function to insert a new job post
def insert_job_post(location, link, description=""):
    data = {
        "location": location,
        "link": link,
        "description": description
    }
    try:
        response = supabase.table("job_posts").insert(data).execute()
        st.success("Job post added successfully!")
        st.write("Response:", response)
    except Exception as e:
        st.error(f"An error occurred: {e}")

# Function to get job posts by location
def get_job_posts(location):
    try:
        response = supabase.table("job_posts").select("*").eq("location", location).execute()
        return response.data
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return []

# Streamlit UI
st.title("Job Seeker Tracker")

menu = ["Add Job Post", "View Job Posts"]
choice = st.sidebar.selectbox("Menu", menu)

locations = ["Bangalore","Mysore","Hyderabad","Chennai", "Pune", "Noida"]

if choice == "Add Job Post":
    st.subheader("Add Job Post")
    location = st.selectbox("Select Location", locations)
    link = st.text_input("Job Post Link")
    description = st.text_area("Description (optional)")

    if st.button("Add"):
        if link:
            insert_job_post(location, link, description)
        else:
            st.error("Job post link is required.")

elif choice == "View Job Posts":
    st.subheader("View Job Posts")
    location = st.selectbox("Select Location to View", locations)
    if st.button("View"):
        posts = get_job_posts(location)
        if posts:
            for post in posts:
                st.write(f"**Link**: {post['link']}")
                if post['description']:
                    st.write(f"**Description**: {post['description']}")
                st.write("---")
        else:
            st.write("No job posts found for this location.")
