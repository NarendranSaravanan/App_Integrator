import streamlit as st
import mysql.connector

# Dictionary to store events
event_notes = {}

# Connect to the MySQL database
cnx = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234",
    database="combine",
    auth_plugin='mysql_native_password'
)
cursor = cnx.cursor()

# Create a 'users' table to store user information
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(50) NOT NULL,
        password VARCHAR(100) NOT NULL
    )
""")
# Create a 'projects' table to store project information
cursor.execute("""
    CREATE TABLE IF NOT EXISTS projects (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT,
        project_title VARCHAR(100) NOT NULL,
        months INT,
        description TEXT,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
""")

# Create an 'internships' table to store internship information
cursor.execute("""
    CREATE TABLE IF NOT EXISTS internships (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT,
        company_name VARCHAR(100) NOT NULL,
        months INT,
        description TEXT,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
""")

# Create a 'certifications' table to store certification information
cursor.execute("""
    CREATE TABLE IF NOT EXISTS certifications (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT,
        certification_name VARCHAR(100) NOT NULL,
        description TEXT,
        domain VARCHAR(100),
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
""")

# Create a 'work_experience' table to store work experience information
cursor.execute("""
    CREATE TABLE IF NOT EXISTS work_experience (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT,
        company_name VARCHAR(100) NOT NULL,
        domain VARCHAR(100),
        description TEXT,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
""")
cnx.commit()


def login():
    st.subheader("Login")

    # Username and password input fields
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    # Login button
    if st.button("Login"):
        # Check username and password in the database
        cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        result = cursor.fetchone()

        if result:
            st.success("Logged in successfully!")
            user_id = result[0]
            options(user_id)
            return (True, user_id)
            
        else:
            st.error("Invalid username or password!")
            return(False, user_id)


def options(user_id):
    st.subheader("Options")

    # Navigation options
    choice = st.radio("Select an option", ("Work", "General", "Search"))

    if choice == "Work":
        work_profile(user_id)
    elif choice == "General":
            general_functionality(user_id)
      # Pass user_id to the search_users function

def register():
    st.subheader("Register")

    # Username and password input fields
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    # Register button
    if st.button("Register"):
        # Insert the new user into the 'users' table
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
        cnx.commit()

        st.success("Registration successful!")


def work_profile(user_id):
    st.title("Work Profile")

    # Display options for viewing and adding data
    st.header("Options")
    if st.button("View Projects"):
        display_projects(user_id)
    if st.button("View Internships"):
        display_internships(user_id)
    if st.button("View Certifications"):
        display_certifications(user_id)
    if st.button("View Work Experience"):
        display_work_experience(user_id)
    add_project_section(user_id)
    add_internship_section(user_id)
    add_certification_section(user_id)
    add_work_experience_section(user_id)
    send_email_button = st.button("Send Email")  # Button to send email in the work section

    if send_email_button:
        st.session_state.is_sending_email = True  # Set flag to indicate email is being sent
        options(user_id)  # Redirect to options to handle sending email

def display_projects(user_id):
    st.header("Projects")

    # Fetch and display existing projects from the database
    cursor.execute("SELECT * FROM projects WHERE user_id = %s", (user_id,))
    projects = cursor.fetchall()

    for project in projects:
        st.write("Project Title:", project[2])  # Adjust the column index based on your table structure
        st.write("Months:", project[3])
        st.write("Description:", project[4])
        st.write("---")


def display_internships(user_id):
    st.header("Internships")

    # Fetch and display existing internships from the database
    cursor.execute("SELECT * FROM internships WHERE user_id = %s", (user_id,))
    internships = cursor.fetchall()

    for internship in internships:
        st.write("Company Name:", internship[2])  # Adjust the column index based on your table structure
        st.write("Months:", internship[3])
        st.write("Description:", internship[4])
        st.write("---")


def display_certifications(user_id):
    st.header("Certifications")

    # Fetch and display existing certifications from the database
    cursor.execute("SELECT * FROM certifications WHERE user_id = %s", (user_id,))
    certifications = cursor.fetchall()

    for certification in certifications:
        st.write("Certification Name:", certification[2])  # Adjust the column index based on your table structure
        st.write("Description:", certification[3])
        st.write("Domain:", certification[4])
        st.write("---")


def display_work_experience(user_id):
    st.header("Work Experience")

    # Fetch and display existing work experience from the database
    cursor.execute("SELECT * FROM work_experience WHERE user_id = %s", (user_id,))
    work_experience = cursor.fetchall()

    for experience in work_experience:
        st.write("Company Name:", experience[2])  # Adjust the column index based on your table structure
        st.write("Domain:", experience[3])
        st.write("Description:", experience[4])
        st.write("---")


def add_project_section(user_id):
    st.header("Add New Project")
    cnx = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234",
    database="combine",
    auth_plugin='mysql_native_password'
)
    cursor = cnx.cursor()
    # Allow the user to enter project details and add to the database
    with st.form("add_project_form"):
        project_title = st.text_input("Project Title")
        months = st.number_input("Number of Months", min_value=1)
        description = st.text_area("Description")
        submit_button = st.form_submit_button("Add Project")

        if submit_button:
            if project_title:
                    # Insert the new project into the 'projects' table
                    cursor.execute(
                        "INSERT INTO projects (user_id, project_title, months, description) VALUES (%s, %s, %s, %s)",
                        (user_id, project_title, months, description))
                    cnx.commit()
                    st.success("Project added successfully!")
        else:
            st.warning("Please enter a project title.")


def add_internship_section(user_id):
    st.header("Add New Internship")

    # Allow the user to enter internship details and add to the database
    with st.form("add_internship_form"):
        company_name = st.text_input("Company Name")
        months = st.number_input("Number of Months", min_value=1)
        description = st.text_area("Description")
        submit_button = st.form_submit_button("Add Internship")

    if submit_button:
        if company_name:
            # Insert the new internship into the 'internships' table
            cursor.execute(
                "INSERT INTO internships (user_id, company_name, months, description) VALUES (%s, %s, %s, %s)",
                (user_id, company_name, months, description))
            cnx.commit()
            st.success("Internship added successfully!")
        else:
            st.warning("Please enter a company name.")


def add_certification_section(user_id):
    st.header("Add New Certification")

    # Allow the user to enter certification details and add to the database
    with st.form("add_certification_form"):
        certification_name = st.text_input("Certification Name")
        description = st.text_area("Description")
        domain = st.text_input("Domain")
        submit_button = st.form_submit_button("Add Certification")

    if submit_button:
        if certification_name:
            # Insert the new certification into the 'certifications' table
            cursor.execute(
                "INSERT INTO certifications (user_id, certification_name, description, domain) VALUES (%s, %s, %s, %s)",
                (user_id, certification_name, description, domain))
            cnx.commit()
            st.success("Certification added successfully!")
        else:
            st.warning("Please enter a certification name.")


def add_work_experience_section(user_id):
    st.header("Add New Work Experience")

    # Allow the user to enter work experience details and add to the database
    with st.form("add_work_experience_form"):
        company_name = st.text_input("Company Name")
        domain = st.text_input("Domain")
        description = st.text_area("Description")
        submit_button = st.form_submit_button("Add Work Experience")

    if submit_button:
        if company_name:
            # Insert the new work experience into the 'work_experience' table
            cursor.execute(
                "INSERT INTO work_experience (user_id, company_name, domain, description) VALUES (%s, %s, %s, %s)",
                (user_id, company_name, domain, description))
            cnx.commit()
            st.success("Work Experience added successfully!")
        else:
            st.warning("Please enter a company name.")


def search_users():
    st.subheader("Search Users")

    # Search options
    search_by = st.selectbox("Search by", ("Username", "Projects", "Internships"))
    search_query = st.text_input("Search query")
    search_button = st.button("Search")

    if search_button:
        if search_query:
            # Perform the search based on the chosen search_by option
            if search_by == "Username":
                cursor.execute("SELECT * FROM users WHERE username LIKE %s", (f"%{search_query}%",))
                results = cursor.fetchall()

                if results:
                    st.success("Search results:")
                    for result in results:
                        st.write("Username:", result[1])
                else:
                    st.warning("No matching users found.")
            elif search_by == "Projects":
                cursor.execute("SELECT users.username, projects.project_title FROM users INNER JOIN projects ON users.id = projects.user_id WHERE projects.project_title LIKE %s", (f"%{search_query}%",))
                results = cursor.fetchall()

                if results:
                    st.success("Search results:")
                    for result in results:
                        st.write("Username:", result[0])
                        st.write("Project Title:", result[1])
                else:
                    st.warning("No matching users found.")
            elif search_by == "Internships":
                cursor.execute("SELECT users.username, internships.company_name FROM users INNER JOIN internships ON users.id = internships.user_id WHERE internships.company_name LIKE %s", (f"%{search_query}%",))
                results = cursor.fetchall()

                if results:
                    st.success("Search results:")
                    for result in results:
                        st.write("Username:", result[0])
                        st.write("Company Name:", result[1])
                else:
                    st.warning("No matching users found.")
        else:
            st.warning("Please enter a search query.")


def general_functionality(user_id):
    st.subheader("General Functionality")


def main():
    st.title("SocialSync: Unified Social and Communication Hub")
    st.header("Welcome to the SocialSync!")

    # Navigation options
    st.sidebar.header("SocialSync!")
    choice = st.sidebar.radio("Select an option", ("Login", "Register", "Search"))
    result = None
    user_id = 1
    if choice == "Login":
         result= login()
         
    elif choice == "Register":
        register()
    elif choice == "Search":
        search_users()

    if result == True:
        options(user_id)
    

if __name__ == "__main__":
    main()
