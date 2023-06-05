import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from PIL import Image

chart_df = pd.read_csv("chart_data.csv")


pepsico_vend_codes = [28400, 30000, 71461]


# Create the layout of the Streamlit application
st.image('pepsico-logo.png')
st.title('PepsiCo Market Analysis')

tab1, tab2 = st.tabs(["📊 KPIs", "📈 Time Series Chart"])

with tab1:
    col1, col2 = st.columns(2)

    col1.metric(label="💰 2011 Revenue", value="$332,054,362")
    col1.metric(label="🤹‍♂️ Market Share", value="59.13%")
    col2.metric(label="🔢 2011 Units Sold", value="126,315,847 units")
    col2.metric(label="📦 VSoD", value="3,956,230 units (50.53%)")

    col5, col6 = st.columns(2)
    with col5:
        st.write("🌎 Top 3 Regions in NY in 2011")
        st.subheader("1. Los Angeles")
        st.subheader("2. New York")
        st.subheader("3. Chicago")

    with col6:
        st.write("👥 Top Customers in NY in 2011")
        st.subheader("1. Chain98")
        st.subheader("2. Chain112")
        st.subheader("3. Chain5")


    st.write("🥨 Market-wide Top Products in NY in 2011 with avg PR")
    st.subheader("1. 00-03-28400-03345 (0.542)")
    st.subheader("2. 00-01-28400-03875 (0.545)")
    st.subheader("3. 00-02-28400-06408 (0.466)")

with tab2:

    agree = st.checkbox('Only PepsiCo Products')

    if agree:
        filtered_chart_df = chart_df[chart_df["first(VEND)"].isin(pepsico_vend_codes)]
    else:
        filtered_chart_df = chart_df

    # Options for the filter dropdown
    filter_options = filtered_chart_df['UPC'].unique()

    # Add the filter dropdown component
    selected_filter = st.selectbox('Select Product:', filter_options)

    # Filter the data based on the selected filter value
    filtered_df = filtered_chart_df[filtered_chart_df['UPC'] == selected_filter]

    # Create three columns in Streamlit
    col1, col2, col3 = st.columns(3)

    # Display the values in the respective columns
    col1.markdown("**🏢 Parent Company**")
    if  (filtered_df['first(VEND)'].iloc[0]) in pepsico_vend_codes:
        col1.write("PEPSICO INC")
    else:
        col1.write(filtered_df['first(L3)'].iloc[0])


    col2.write("**🏷️ Brand**")
    col2.write(filtered_df['first(L5)'].iloc[0])

    col3.write("**💬 Description**")
    col3.write(filtered_df['first(L9)'].iloc[0])

    # Create the bar chart
    fig = go.Figure()
    fig.add_trace(go.Bar(x=filtered_df['WEEK'], y=filtered_df['sum(DOLLARS)'], name='Revenue'))
    fig.add_trace(go.Bar(x=filtered_df['WEEK'], y=filtered_df['sum(UNITS)'], name='Units Sold'))
    fig.add_trace(go.Bar(x=filtered_df['WEEK'], y=filtered_df['avg(PR)'], name='Average Time with Price Reduction'))
    fig.add_trace(go.Bar(x=filtered_df['WEEK'], y=filtered_df['avg(D)'], name='Average Marketing Support'))
    # fig.add_trace(go.Bar(x=filtered_df['WEEK'], y=filtered_df['Average_Marketing_Support'], name='Average Marketing Support'))

    fig.update_layout(barmode='group',title=f"🗽 Time Series Chart for {selected_filter} in New York", xaxis_title='Week', yaxis_title='Metrics', width=850)

    # Render the bar chart
    st.plotly_chart(fig)
