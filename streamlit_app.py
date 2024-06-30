import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# Set wide layout
st.set_page_config(layout="wide")

# Sidebar for file upload
st.sidebar.header("File Upload")
uploaded_file = st.sidebar.file_uploader("Choose an Excel file", type="xlsx")

# Default chart height
default_chart_height = 400

if uploaded_file is not None:
    # Load the Excel file
    df = pd.read_excel(uploaded_file)

    # Convert the DateTime column to pandas datetime type
    df['DateTime'] = pd.to_datetime(df['DateTime'])

    # Sidebar for controlling chart dimensions
    st.sidebar.header("Chart Settings")
    chart_width = st.sidebar.slider("Chart Width", min_value=500, max_value=1500, value=800)
    chart_height = st.sidebar.slider("Chart Height", min_value=200, max_value=800, value=default_chart_height)

    # Determine date range from DataFrame
    if 'DateTime' in df.columns:
        date_range = (df['DateTime'].min(), df['DateTime'].max())

        # DateTime slider in the sidebar
        start_date, end_date = st.sidebar.slider(
            "Select Date Range",
            min_value=datetime.date(date_range[0]),
            max_value=datetime.date(date_range[1]),
            value=(datetime.date(date_range[0]), datetime.date(date_range[1]))
        )

        # Convert start_date and end_date to datetime64[ns]
        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)

        # Ensure the 'items' column exists
        if 'items' in df.columns:
            # Multiselect dropdown for selecting metrics
            available_metrics = df.columns[2:].tolist()  # Assuming metrics start from column 3
            selected_metrics = st.sidebar.multiselect("Select Metrics", available_metrics, default=available_metrics)

            if len(selected_metrics) > 0:
                # Create two columns for displaying charts side by side
                col1, col2 = st.columns(2)

                # Iterate through each selected metric
                for metric in selected_metrics:
                    # Filter data based on selected date range and metric
                    filtered_df = df[(df['DateTime'] >= start_date) & (df['DateTime'] <= end_date)]

                    # Create an interactive plot using Plotly for each metric
                    fig = px.line(filtered_df, x='DateTime', y=metric, color='items', labels={'items': 'Item'}, height=chart_height)
                    fig.update_layout(
                        title=f"{metric} over Time",
                        xaxis_title='',
                        yaxis_title='',
                        width=chart_width,
                        margin=dict(l=0, r=20, t=50, b=0),  # Adjust margins as needed
                        paper_bgcolor='rgb(240, 240, 240)',  # Set paper background color
                        plot_bgcolor='rgba(0,0,0,0)',   # Make plot area transparent
                        legend=dict(
                            orientation='h',  # Horizontal orientation
                            yanchor='bottom',  # Anchor legend to the bottom of the plot area
                            y=1.02,  # Adjust vertical position
                            xanchor='right',  # Anchor legend to the right of the plot area
                            x=1  # Adjust horizontal position
                        ),
                        xaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.1)', zeroline=False),  # Show gridlines and customize color
                        yaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.1)', zeroline=False)  # Show gridlines and customize color
                    )

                    # Add vertical line to the plot
                    fig.add_vline(x=filtered_df['DateTime'].iloc[len(filtered_df)//2], line_width=2, line_dash="dash", line_color="red")

                    # Alternate placing charts in col1 and col2
                    if len(selected_metrics) % 2 == 1 or len(selected_metrics) == 1:
                        col1.plotly_chart(fig)
                    else:
                        col2.plotly_chart(fig)

            else:
                st.warning("Please select at least one metric to display.")

        else:
            st.error("'items' column not found in the uploaded file. Please check the column names.")

    else:
        st.warning("No DateTime column found in the uploaded file.")

