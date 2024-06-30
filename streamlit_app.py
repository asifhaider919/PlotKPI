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
    st.title("Excel Pivot Chart Replication")

    # Sidebar for file upload
    uploaded_file = st.file_uploader("Choose an Excel file", type="xlsx")

    if uploaded_file is not None:
        # Load data
        df = load_data(uploaded_file)

        # Attempt to create DateTime column
        try:
            df['DateTime'] = pd.to_datetime(df['DATE'] + ' ' + df['TIME'], format='%Y-%m-%d %H:%M:%S')
        except TypeError as e:
            st.write(f"Error details: {e}")
            st.write(df[['DATE', 'TIME']].head())
            return

        # Create a new DataFrame with Date, Time, Metric
        df_plot = df.melt(id_vars=['DATE', 'TIME', 'ITEM', 'DateTime'],
                          var_name='Metric', value_name='Value')

        # Plotting all metrics for each item
        if st.button("Plot All Metrics"):
            fig = px.line(df_plot, x='DateTime', y='Value', color='Metric',
                          facet_col='ITEM', facet_col_wrap=3,
                          labels={'DateTime': 'Date', 'Value': 'Metric Value'},
                          title="Excel Pivot Chart Replication")
            fig.update_yaxes(matches=None)  # Ensure y-axes are not shared across facets
            st.plotly_chart(fig)

# Run the app
if __name__ == "__main__":
    main()
