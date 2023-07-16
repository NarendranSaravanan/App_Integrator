import streamlit as st
import smtplib
import imaplib

def send_email():
    st.subheader("Send Email")

    # Email input fields
    sender_email = st.text_input("Sender Email")
    sender_password = st.text_input("Sender Password", type="password")
    recipient_email = st.text_input("Recipient Email")
    subject = st.text_input("Subject")
    message = st.text_area("Message")
    send_button = st.button("Send Email")

    if send_button:
        if sender_email and sender_password and recipient_email and subject and message:
            try:
                # Establish an SMTP connection
                smtp_server = "smtp.gmail.com"
                smtp_port = 587
                with smtplib.SMTP(smtp_server, smtp_port) as server:
                    server.starttls()
                    server.login(sender_email, sender_password)

                    # Compose the email
                    email_message = f"Subject: {subject}\n\n{message}"

                    # Send the email
                    server.sendmail(sender_email, recipient_email, email_message)

                st.success("Email sent successfully!")
            except Exception as e:
                st.error(f"Error sending email: {e}")
        else:
            st.warning("Please fill in all the required fields.")

def receive_email():
    st.subheader("Receive Email")

    # Email input fields
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    receive_button = st.button("Receive Email")

    if receive_button:
        if email and password:
            try:
                # Establish an IMAP connection
                imap_server = "imap.gmail.com"
                imap_port = 993
                with imaplib.IMAP4_SSL(imap_server, imap_port) as server:
                    server.login(email, password)

                    # Select the mailbox (e.g., INBOX)
                    server.select()

                    # Search for unseen emails
                    _, email_uids = server.search(None, "UNSEEN")

                    if email_uids:
                        st.success("Received emails:")
                        for uid in email_uids[0].split():
                            _, email_data = server.fetch(uid, "(RFC822)")
                            raw_email = email_data[0][1].decode("utf-8")
                            st.code(raw_email, language="html")
                    else:
                        st.info("No new emails.")
            except Exception as e:
                st.error(f"Error receiving email: {e}")
        else:
            st.warning("Please enter your email credentials.")

def main():
    st.title("Email App")

    # Navigation options
    choice = st.sidebar.radio("Select an option", ("Send Email", "Receive Email"))

    if choice == "Send Email":
        send_email()
    elif choice == "Receive Email":
        receive_email()

if __name__ == "__main__":
    main()

