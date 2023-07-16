from datetime import datetime
import streamlit.components.v1 as components
import streamlit as st
def calendar_template():
    return """
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/flatpickr/dist/flatpickr.min.css">
    <input id="datepicker" type="text" placeholder="Select a date">
    <script src="https://cdn.jsdelivr.net/npm/flatpickr"></script>
    <script>
    flatpickr("#datepicker", {
        dateFormat: "Y-m-d",
        onChange: function(selectedDates) {
            var selectedDate = selectedDates[0];
            var dateString = selectedDate.toISOString().split("T")[0];
            Shiny.setInputValue("selected_date", dateString);
        }
    });
    </script>
    """


st.title("Calendar App")

st.header("Select a Date")
components.html(calendar_template(), height=200)
selected_date = st.text_input("Selected Date", key="selected_date", value=datetime.now().date())
st.write("Selected date:", selected_date)