import streamlit as st
import markdown
import os
import pandas as pd
import sqlite3
import plotly.express as px

# Define your password
correct_password = os.environ.get('HYDRANT_PASSWORD')
db_table = os.environ.get('HYDRANT_DB_TABLE')



# Streamlit page configuration
st.set_page_config(page_title='Hydrant Tracker', layout='centered')


def get_map_data():
    # Establish a connection to the database
    conn = sqlite3.connect('./streamlit/hydrant.db')

    # Write your SQL query
    query = "SELECT * FROM " + db_table

    # Convert the SQL query result to a DataFrame
    df = pd.read_sql_query(query, conn)

    # Close the connection
    conn.close()

    return df

def update_map_data(id, status, pressure):
    try:
        # Establish a connection to the database
        conn = sqlite3.connect('./streamlit/hydrant.db')
        cursor = conn.cursor()

        update_query = "UPDATE " + db_table+" SET status = ?, pressure = ? WHERE id = ?"
        # Write your SQL query
        cursor.execute(update_query, (status, pressure, id))
        conn.commit()


        query = "SELECT * FROM hydrant_status WHERE id = 14336"
        cursor.execute(query)
        row = cursor.fetchall()
        print(row)

    except sqlite3.Error as e:
        print("Database error:", e)
        row = ''

    finally:
        # Close the connection
        conn.close()
        return row

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
    cols = st.columns(6)
    with cols[0]:
        if st.button('Map'):
            st.session_state['page'] = 'Map'
    with cols[1]:
        if st.button('Issues'):
            st.session_state['page'] = 'Issues'


     # Set default page if not selected
    if 'page' not in st.session_state:
        st.session_state['page'] = 'Map'

    # Render page based on navigation selection
    if st.session_state['page'] == 'Map':

        st.subheader('Hydrant Map')
        df = get_map_data()
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



else:
    st.error('Password incorrect. Try again.')