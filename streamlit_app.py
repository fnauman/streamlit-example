import streamlit as st
import pandas as pd
import plost
import plotly.express as px

## Load data
df_schools = pd.read_csv('./data/schools_anon.csv')
df_students = pd.read_csv('./data/students_risk_anon.csv')
df_risk_per_school = df_students.groupby('School').agg({'Risk_factor': 'mean'}).reset_index()
# print(df_risk_per_school.head())

## Page setup
st.set_page_config(layout='wide', initial_sidebar_state='expanded')

## Set page title
st.markdown(
    """
    # School dashboard

    """,
    unsafe_allow_html=True
)

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    
# st.sidebar.header('School dashboard')


st.sidebar.subheader('Choose school property')
chosen_property = st.sidebar.selectbox('Select data', ('students per teacher', 'teachers with degree', 'teachers with permanent job'))

st.sidebar.subheader('School selection')
chosen_school = st.sidebar.selectbox('Select school', df_schools.school.unique(), index=0)
# plot_height = st.sidebar.slider('Specify plot height', 200, 500, 250)


# Row A
st.markdown('### Overall commune metrics')
col1, col2, col3 = st.columns(3)
col1.metric("Eligibility", "77%", "2%")
col2.metric("Attendance", "83%", "-4%")
col3.metric("Math", "82%", "-3%")

# Row B
c1, c2 = st.columns((7, 3))
with c1:
    st.markdown('### Students at risk in each school')
    st.plotly_chart(
        px.bar(
            df_risk_per_school, 
            x='School',
            y='Risk_factor', 
            color='Risk_factor',
            title='Risk Factor per School', 
        ), 
        use_container_width=True
    )
with c2:
    st.markdown('### School characteristics')
    
    st.plotly_chart(
        px.bar(
            df_schools[df_schools.school == chosen_school], 
            x='year',
            y=chosen_property, 
            color=chosen_property,
        )
    )

# Row C
st.markdown('### Eligibility over time')
# st.line_chart(df_schools, x='year', y='eligibility', height=plot_height)
st.plotly_chart(
    px.line(
        df_schools[df_schools.school == chosen_school],
        x='year',
        y='eligibility', 
    ), 
    use_container_width=True
)