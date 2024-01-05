import streamlit as st
import markdown
import os
import pandas as pd
import sqlite3
import plotly.express as px
import psycopg2
from sqlalchemy import URL
from sqlalchemy import create_engine
import logging

# Define your password
correct_password = os.environ.get('HYDRANT_PASSWORD')

db_host = os.getenv('HYDRANT_HOST')
db_name = os.getenv('HYDRANT_DB')
db_user = os.getenv('HYDRANT_USER')
db_password = os.getenv('HYDRANT_PASS')
db_port = os.getenv('HYDRANT_PORT')
db_table = os.environ.get('HYDRANT_DB_TABLE')


# Streamlit page configuration
st.set_page_config(page_title='Hydrant Tracker', layout='centered')


def get_map_data(table):
    # Establish a connection to the database
    url_object = URL.create(
    "postgresql",
    username=os.getenv('HYDRANT_USER'),
    password=os.getenv('HYDRANT_PASS'),
    host=os.getenv('HYDRANT_HOST'),
    database=os.getenv('HYDRANT_DB'),
)
    # Create a SQLAlchemy engine
    engine = create_engine(url_object)

    with engine.connect() as conn, conn.begin():  
        df = pd.read_sql_table(table, conn)  
        return df

def update_map_data(id, status, pressure):
    try:
        # Establish a connection to the database
        conn = psycopg2.connect(
            dbname=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port,
        )
        cursor = conn.cursor()

        # Correct the placeholder syntax
        update_query = "UPDATE " + db_table + " SET status = %s, pressure = %s WHERE id = %s"

        # Execute the query
        cursor.execute(update_query, (status, pressure, id))
        conn.commit()

        # Check if any row is affected
        if cursor.rowcount == 0:
            print("No rows updated")
            return False

        return True

    except psycopg2.Error as e:
        print(f"An error occurred: {e}")
        conn.rollback()
        return False

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def make_map(df):
    color_scale = {'not ok': 'red', 'ok': 'green', 'needs testing': 'yellow'} 

    fig = px.scatter_mapbox(df, 
                            lat="latitude", 
                            lon="longitude", 
                            hover_name="status", 
                            hover_data=["status", "pressure", "id"],
                            color='status',
                            color_discrete_map=color_scale,  # Specify color scale
                            zoom=8, 
                            height=350,
                            width=800)

    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r":10,"t":10,"l":10,"b":10})

    # Update legend
    fig.update_traces(marker=dict(size=10))  # Adjust marker size as needed
    fig.update_layout(legend_title_text='status')
    return fig



# Streamlit app
st.title('Hydrant Tracker')

# Ask for the password
password = st.text_input("Enter the password", type='password')

# Check the password
if password == correct_password:
    st.success('Password Correct!')

    # Generate the navbar with buttons
    cols = st.columns(3)
    with cols[0]:
        if st.button('Map'):
            st.session_state['page'] = 'Map'
    with cols[1]:
        if st.button('Issues'):
            st.session_state['page'] = 'Issues'
    with cols[2]:
        if st.button('Wicker Park'):
            st.session_state['page'] = 'Wicker Park'


     # Set default page if not selected
    if 'page' not in st.session_state:
        st.session_state['page'] = 'Map'

    # Render page based on navigation selection
    if st.session_state['page'] == 'Map':

        st.subheader('Hydrant Map')
        df = get_map_data(db_table)
        fig = make_map(df)
        st.plotly_chart(fig)


        # Input form
        with st.form('Data Input Form'):
            id = st.number_input('id', step=1)
            status = st.text_input('status')
            pressure = st.number_input('pressure', format="%.1f")
            submitted = st.form_submit_button('Update Hydrant')

            if submitted:
                row = update_map_data(id, status, pressure)
                st.rerun()
    
    # Render page based on navigation selection
    if st.session_state['page'] == 'Issues':
        st.subheader('Hydrants with Issues')


        # Render page based on navigation selection
    if st.session_state['page'] == 'Wicker Park':
        st.subheader('Hydrants with Issues')

        st.subheader('Hydrant Map')
        df = get_map_data('wicker_park_hydrants')
        fig = make_map(df)
        st.plotly_chart(fig)


        # Input form
        with st.form('Data Input Form'):
            id = st.number_input('id', step=1)
            status = st.text_input('status')
            pressure = st.number_input('pressure', format="%.1f")
            submitted = st.form_submit_button('Update Hydrant')

            if submitted:
                row = update_map_data(id, status, pressure)
                st.rerun()



else:
    st.error('Password incorrect. Try again.')