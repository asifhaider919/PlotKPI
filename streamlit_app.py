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

        # Combine date and time into datetime column
        df['DateTime'] = pd.to_datetime(df[date_column] + ' ' + df[time_column], format='%Y-%m-%d %H:%M:%S')

        # Create a new DataFrame with Date, Time, Metric
        df_plot = df[[date_column, time_column, metric_column]].copy()
        df_plot['Time'] = pd.to_datetime(df_plot[time_column], format='%H:%M:%S').dt.time

        # Plotting
        if st.button("Plot Metric Series"):
            fig = px.line(df_plot, x='Time', y=metric_column, color=date_column,
                          title="Metric Series Plot", labels={'Time': 'Time', 'value': 'Metric'})
            st.plotly_chart(fig)

# Run the app
if __name__ == "__main__":
    main()
