import streamlit as st
import pandas as pd
import plotly.express as px

# Function to load data and prepare for visualization
def load_data(file):
    df = pd.read_excel(file)  # Adjust for your file type if not Excel
    
    # Ensure columns 'DATE' and 'TIME' exist in the DataFrame
    if 'DATE' in df.columns and 'TIME' in df.columns:
        # Combine 'DATE' and 'TIME' into a single 'DateTime' column
        df['DateTime'] = pd.to_datetime(df['DATE'] + ' ' + df['TIME'], format='%Y-%m-%d %H:%M:%S')  # Adjust format as per your data
        
        # Drop 'DATE' and 'TIME' columns if needed
        df.drop(columns=['DATE', 'TIME'], inplace=True)
    else:
        st.error("Columns 'DATE' and/or 'TIME' not found in the uploaded file.")
        return None
    
    return df

# Streamlit setup
st.set_page_config(layout="wide")

# Sidebar for file upload
st.sidebar.header("File Upload")
uploaded_file = st.sidebar.file_uploader("Choose an Excel file", type="xlsx")

# Main app logic
if uploaded_file:
    df = load_data(uploaded_file)
    
    if df is not None:
        # Pivot the data to create the desired chart
        pivoted_df = df.pivot(index='DateTime', columns='ITEM', values='METRIC')  # Adjust column names as per your data
        
        # Reset index to have 'DateTime' as a column again
        pivoted_df.reset_index(inplace=True)
        
        # Melt the DataFrame to have 'ITEM' as a column (for legend)
        melted_df = pd.melt(pivoted_df, id_vars=['DateTime'], var_name='ITEM', value_name='METRIC')
        
        # Create chart using plotly express
        fig = px.line(melted_df, x='DateTime', y='METRIC', color='ITEM', title='Metrics by Item over Time')
        
        # Customize the chart layout if needed
        fig.update_layout(
            xaxis_title='DateTime',
            yaxis_title='Metric Value',
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
