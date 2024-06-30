import streamlit as st
import pandas as pd
import plotly.express as px

# Function to load data
@st.cache
def load_data(file):
    df = pd.read_excel(file)
    return df

# Main function to run the app
def main():
    st.title("Metric Series Plot")

    # Sidebar for file upload
    uploaded_file = st.file_uploader("Choose an Excel file", type="xlsx")

    if uploaded_file is not None:
        # Load data
        df = load_data(uploaded_file)

        # Sidebar to select columns
        date_column = st.sidebar.selectbox("Select Date Column", df.columns)
        time_column = st.sidebar.selectbox("Select Time Column", df.columns)
        metric_column = st.sidebar.selectbox("Select Metric Column", df.columns)

        # Plotting
        if st.button("Plot Metric Series"):
            fig = px.line(df_plot, x='Time', y=metric_column, color=date_column,
                          title="Metric Series Plot", labels={'Time': 'Time', 'value': 'Metric'})
            st.plotly_chart(fig)

# Run the app
if __name__ == "__main__":
    main()
