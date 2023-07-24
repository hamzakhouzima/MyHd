import streamlit as st
import pandas as pd

df = pd.read_excel(
    io='departement_num_62-B2B.xlsx',
    engine='openpyxl'
)

st.dataframe(df)
st.sidebar.header('Filters')

# Convert 'date_creation' to datetime format
df['date_creation'] = pd.to_datetime(df['date_creation'])

# Year Filter
year_filter = st.sidebar.checkbox("Filter by Year")
selected_year = None
if year_filter:
    selected_year = st.sidebar.slider("Select a year", df['date_creation'].dt.year.min(), df['date_creation'].dt.year.max())

# Domaine Activite Filter
domaine_activite_filter = st.sidebar.checkbox("Filter by Domaine Activite")
domaine_activite = None
if domaine_activite_filter:
    domaine_activite = st.sidebar.multiselect(
        'Select an activity',
        options=df['domaine_activite'].unique(),
        default=df['domaine_activite'].unique()
    )

# Perform the query based on the selected activity and/or year (if any filters are applied)
if domaine_activite and selected_year:
    df_selection = df.query('domaine_activite == @domaine_activite & date_creation.dt.year == @selected_year')
elif domaine_activite:
    df_selection = df.query('domaine_activite == @domaine_activite')
elif selected_year:
    df_selection = df.query('date_creation.dt.year == @selected_year')
else:
    df_selection = df

# Display the filtered data
st.dataframe(df_selection)
