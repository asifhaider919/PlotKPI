import streamlit as st
import pandas as pd
import plotly.express as px

# Set wide layout
st.set_page_config(layout="wide")

# Function to read Excel file
def read_excel_file(uploaded_file):
    df = pd.read_excel(uploaded_file, engine='openpyxl')  # Adjust engine as needed
    return df

# Sidebar for file upload
st.sidebar.header("File Upload")
uploaded_file = st.sidebar.file_uploader("Choose an Excel file", type="xlsx")

# Default chart height
default_chart_height = 400

if uploaded_file is not None:
    # Load the Excel file
    df = read_excel_file(uploaded_file)

    # Display the loaded dataframe
    st.subheader("Uploaded Data")
    st.write(df)

    # Ensure the required columns are present
    if 'DATE' in df.columns and 'TIME' in df.columns and 'ITEM' in df.columns:
        # Combine DATE and TIME into a new DateTime column
        df['DateTime'] = pd.to_datetime(df['DATE'].astype(str) + ' ' + df['TIME'].astype(str))

        # Unique items and metrics
        items = df['ITEM'].unique().tolist()
        metrics = df.columns[3:].tolist()  # Assuming metrics start from the 4th column

        # Sidebar for selecting items and metrics
        selected_item = st.sidebar.selectbox("Select Item", items)
        selected_metric = st.sidebar.selectbox("Select Metric", metrics)

        # Filter data based on selected item
        filtered_df = df[df['ITEM'] == selected_item]

        # Create the plot
        fig = px.line(filtered_df, x='TIME', y='DATE', hover_data=['DateTime', 'ITEM', selected_metric],
                      line_group='ITEM', labels={'DATE': 'Date', 'TIME': 'Time'}, color_discrete_sequence=px.colors.qualitative.Alphabet)

        # Customize layout
        fig.update_layout(
            title=f"{selected_item} - {selected_metric}",
            xaxis_title='Time',
            yaxis_title='Date',
            height=default_chart_height,
            hovermode="x unified",
            margin=dict(l=50, r=50, t=50, b=50),
            legend=dict(
                title=None,
                orientation="h",
                yanchor="bottom",
                y=-0.25,
                xanchor="right",
                x=1
            )
        )

        # Display the plot
        st.plotly_chart(fig)

    else:
        st.warning("Required columns 'DATE', 'TIME', and 'ITEM' not found in the uploaded file.")

else:
    st.info("Please upload an Excel file.")
