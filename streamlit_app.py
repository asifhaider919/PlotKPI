import streamlit as st
import pandas as pd
import plotly.express as px

# Function to load data and prepare for visualization
def load_data(file):
    df = pd.read_excel(file)  # Adjust for your file type if not Excel
    
    # Assuming 'DATE', 'TIME', 'ITEM' are column names, adjust as needed
    df['DateTime'] = pd.to_datetime(df['DATE'] + ' ' + df['TIME'])  # Combine date and time
    
    return df

# Streamlit setup
st.set_page_config(layout="wide")

# Sidebar for file upload
st.sidebar.header("File Upload")
uploaded_file = st.sidebar.file_uploader("Choose an Excel file", type="xlsx")

# Main app logic
if uploaded_file:
    df = load_data(uploaded_file)
    
    # Pivot the data
    pivoted_df = df.pivot(index='DateTime', columns='ITEM', values='METRIC')  # Adjust columns as per your data
    
    # Prepare data for plotly express
    pivoted_df.reset_index(inplace=True)  # Reset index to use 'DateTime' as x-axis
    
    # Create chart using plotly express
    fig = px.line(pivoted_df, x='DateTime', y=pivoted_df.columns[1:], title='Metrics by Item over Time')
    
    # Customize the chart layout if needed
    fig.update_layout(
        xaxis_title='DateTime',
        yaxis_title='Metrics Value',
        width=1200,
        height=600,
        margin=dict(l=50, r=50, t=50, b=50),  # Adjust margins as needed
        paper_bgcolor='white',  # Set paper background color
        plot_bgcolor='white',   # Make plot area background white
        legend=dict(
            orientation='h',    # Horizontal legend
            yanchor='bottom',   # Anchor legend to bottom
            y=1.02,             # Adjust vertical position
            xanchor='right',    # Anchor legend to right
            x=1                 # Adjust horizontal position
        ),
        xaxis=dict(showgrid=True, gridcolor='lightgray', zeroline=False),  # Show gridlines and customize color
        yaxis=dict(showgrid=True, gridcolor='lightgray', zeroline=False)   # Show gridlines and customize color
    )
    
    # Display the chart
    st.plotly_chart(fig)

else:
    st.warning("Please upload an Excel file.")

