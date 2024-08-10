import pandas as pd
import streamlit as st
import numpy as np

from sqlalchemy import create_engine
import pymysql

# Function to retrieve data from the database
def dataBasefunction(query):
    engine = create_engine("mysql+pymysql://root:Bike3211@localhost/streamlit_p")
    with engine.connect() as connect:
        df = pd.read_sql(query,connect)
    return df

# Initial query to get unique transport names
data_query = "select * from redbus_p"
gf = dataBasefunction(data_query)
transport_info = gf["Transports_Name"].unique()

# Selectbox for bus names
selected_bus_name = st.selectbox("Select Bus Name", transport_info)

# Query to filter based on the selected bus name and the "From" and "To" locations

from_route = []
to_route = []

if selected_bus_name:
    query = f"select * from redbus_p where Transports_Name = '{selected_bus_name}'"
    gf = dataBasefunction(query)
    route_title = gf["Route_Titles"].unique()
    asdf = list(route_title)
    
    for asd in asdf:
        from_singleroute = asd.split("to")[0]
        from_route.append(from_singleroute)
        to_singleroute = asd.split("to")[1]
        to_route.append(to_singleroute)
    
    print(type(from_route))
    from_route_unique = list(set(from_route))

    from_location = st.selectbox("From",from_route_unique)
  
    from_location_correction = from_location + '%'
    
    if from_location:
        query = f"select * from redbus_p where Transports_Name='{selected_bus_name}' and Route_Titles like '{from_location_correction}%'"
        gf = dataBasefunction(query)
    
    to_route_unique = list(set(to_route))
    to_location = st.selectbox("To",to_route_unique)
    to_location_correction = '%' + to_location
    if to_location:
        query = f"select * from redbus_p where Transports_Name='{selected_bus_name}' and Route_Titles like '{from_location_correction}%to%{to_location_correction}'"
        gf = dataBasefunction(query)

    st.dataframe(pd.DataFrame(gf))