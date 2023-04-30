# import streamlit as st
# import pandas as pd
# import numpy as np
# import plost
# from PIL import Image


# # Page setting
# st.set_page_config(layout="wide")

# with open('style.css') as f:
#     st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# # Data
# # seattle_weather = pd.read_csv('https://raw.githubusercontent.com/tvst/plost/master/data/seattle-weather.csv', parse_dates=['date'])
# # stocks = pd.read_csv('https://raw.githubusercontent.com/dataprofessor/data/master/stocks_toy.csv')

# # Row A
# a1, a2, a3 = st.columns(3)
# a1.image(Image.open('streamlit-logo-secondary-colormark-darktext.png'))
# a2.metric("Wind", "999 mph", "8%")
# a3.metric("Humidity", "-86%", "4%")

# # Row B
# b1, b2, b3, b4 = st.columns(4)
# b1.metric("Temperature", "70 °F", "1.2 °F")
# b2.metric("Wind", "9 mph", "8%")
# b3.metric("Humidity", "86%", "4%")
# b4.metric("Humidity", "86%", "4%")

# # Row C
# c1, c2 = st.columns((7, 3))
# with c1:
#     st.markdown('### Heatmap')
#     plost.time_hist(
#         data=seattle_weather,
#         date='date',
#         x_unit='week',
#         y_unit='day',
#         color='temp_max',
#         aggregate='median',
#         legend=None)
# with c2:
#     st.markdown('### Bar chart')
#     plost.donut_chart(
#         data=stocks,
#         theta='q2',
#         color='company')

# st.write('Hello World')


from sqlalchemy.schema import *
from sqlalchemy.engine import create_engine
from sqlalchemy import *
from urllib.parse import quote
import textwrap
from yaml.loader import SafeLoader
import yaml
import numpy as np
import plotly.express as px
import streamlit as st
import pandas as pd
from streamlit_autorefresh import st_autorefresh
import streamlit_authenticator as stauth

from datetime import datetime

current_time = datetime.now()


st_autorefresh(interval=5000)
# st.title('Tutorial')
# st.write('My First App 12')
st.write(current_time)

# button1 = st.button("click me")

# if button1:
#     st.write('This is some text')

# like = st.checkbox("do you like this app")
# button2 = st.button("submit")
# if button2:
#     if like:
#         st.write("thanks")
#     else:
#         st.write('f u')

# streamlit_app.py


# animal = st.radio("best animal?", ("lion", "bear"))

# options = st.multiselect("best animal?", ('a', 'b'))


# button1 = st.sidebar.button("clean text")
# text = st.sidebar.text_area("Write text")


# def clean_text(text):
#     text = text.replace("m", "M")
#     return text


# if button1:
#     col1, col2 = st.columns(2)

#     col1.header('Original')
#     col1.write(text)

#     col2.header('Modified')
#     clean = st.write(clean_text(text))
#     col2.write(clean)


def line_():
    st.header("Line Chart")

    data = {"a": [23, 12, 78, 4, 54], "b": [0, 13, 88, 1, 3],
            "c": [45, 2, 546, 67, 56]}

    df = pd.DataFrame(data)
    df
    st.line_chart(data=df)


DB_NAME = st.secrets["DB_NAME"]
IP_PORT = st.secrets["IP_PORT"]

st.write(DB_NAME)
st.write(IP_PORT)

db_connection_str = (
    f"mysql+pymysql://{DB_NAME}:%s@{IP_PORT}/{DB_NAME}?charset=utf8mb4"
    % quote(f"{DB_NAME}"))
engine = create_engine(db_connection_str, echo=False)

sql = textwrap.dedent("""\
select region,sum(total_revenue) as total from 5000_sale_orders
group by 1
       """)

sql_output = []
with engine.connect() as con:
    rs = con.execute(sql)
    for row in rs:
        sql_output.append(dict(row))
df = pd.DataFrame(sql_output)


st.sidebar.header('Options')


region = st.sidebar.multiselect("select the region:",
                                options=df['region'].unique(),
                                default=df['region'].unique()
                                )


df_selection = df.query("region == @region")


df_selection['total'] = df_selection['total'].astype(
    float)
st.dataframe(df_selection[['region', 'total']])
st.bar_chart(data=df_selection,
             x='region', y='total'
             )


sql = textwrap.dedent("""\
select year(order_date) order_year,sum(total_revenue) as total from 5000_sale_orders
group by 1
       """)

sql_output = []
with engine.connect() as con:
    rs = con.execute(sql)
    for row in rs:
        sql_output.append(dict(row))
df = pd.DataFrame(sql_output)

st.line_chart(data=df,
              x='order_year', y='total'
              )

hide_streamlit_style = """
            <style>
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)


# with open('config.yaml') as file:
#     config = yaml.load(file, Loader=SafeLoader)

# authenticator = stauth.Authenticate(
#     config['credentials'],
#     config['cookie']['name'],
#     config['cookie']['key'],
#     config['cookie']['expiry_days'],
#     config['preauthorized']
# )


# name, authentication_status, username = authenticator.login('Login', 'main')


# if st.session_state["authentication_status"]:
#     authenticator.logout('Logout', 'main')
#     st.write(f'Welcome *{st.session_state["name"]}*')
#     st.title('Some content')
#     line_()
# elif st.session_state["authentication_status"] is False:
#     st.error('Username/password is incorrect')
# elif st.session_state["authentication_status"] is None:
#     st.warning('Please enter your username and password')
