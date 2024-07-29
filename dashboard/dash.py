import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns
from astropy.coordinates import SkyCoord, Angle
import astropy.units as u
import sqlite3
from datetime import datetime, timedelta

# Page configuration
st.set_page_config(
    page_title="SDEC",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="expanded")

alt.themes.enable("dark")

# Function to load data from a SQLite table
def load_data(table_name):
    conn = sqlite3.connect('/home/vignesh-nadar/vikky/My Work/finalProject/data_release.db')
    query = f"SELECT * FROM {table_name}"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# Function to load dataset based on selection

#def load_data(dr):
#    data_path = f'/home/vignesh-nadar/vikky/Projects & Skills/My Work/Project 2/Stellar Predictor/data/{dr}.csv'  # Update with your directory path
#    try:
#        data = pd.read_csv(data_path)
#        data.drop(['objid', 'run', 'rerun', 'camcol', 'field', 'specobjid'], axis=1, inplace=True)
#        return data
#    except FileNotFoundError:
#        st.error(f"Data for {dr} is not available. Please add the {dr}.csv file to the specified path.")
#        return None

# Title and description
st.title("""This application performs an intermediate level exploratory data analysis (EDA) on the SDSS dataset.
You can explore different visualizations based on photometric data.""")

# Sidebar for user input
st.sidebar.header('Select Data Release')
selected_dr = st.sidebar.selectbox('Select the required DR:', ['dr18', 'dr17', 'dr16', 'dr15'])

# Sidebar for color theme

color_theme = ['plotly']

# Load the selected dataset
data = load_data(selected_dr)


def generate_summary_table(df):
    summary = pd.DataFrame({
        'Column': df.columns,
        'Data Type': df.dtypes.values
    })
    return summary

# Generate summary table
summary_df = generate_summary_table(data)

st.sidebar.header('About')
with st.sidebar:
    # Display summary table
    st.sidebar.header('Dataset Shape')
    st.sidebar.write(f'Rows: {data.shape[0]}')
    st.sidebar.write(f'Columns: {data.shape[1]}')


# Filter data based on class
galaxy = data[data['class'] == 'GALAXY']
star = data[data['class'] == 'STAR']
qso = data[data['class'] == 'QSO']

# Convert coordinates
ra1 = Angle(galaxy['ra'], u.degree)
dec1 = Angle(galaxy['dec'], u.degree)
coords1 = SkyCoord(ra=ra1, dec=dec1, frame='icrs')

ra2 = Angle(star['ra'], u.degree)
dec2 = Angle(star['dec'], u.degree)
coords2 = SkyCoord(ra=ra2, dec=dec2, frame='icrs')

ra3 = Angle(qso['ra'], u.degree)
dec3 = Angle(qso['dec'], u.degree)
coords3 = SkyCoord(ra=ra3, dec=dec3, frame='icrs')


st.header('Sky Map of Galaxies, Stars, and Quasars')
fig, ax = plt.subplots(figsize=(6, 8), subplot_kw={'projection': 'mollweide'}, facecolor='none')
ax.scatter(coords1.ra.wrap_at(180*u.degree).radian, coords1.dec.radian, s=1, c='r', alpha=0.6, label='Galaxy')
ax.scatter(coords2.ra.wrap_at(180*u.degree).radian, coords2.dec.radian, s=1, c='b', alpha=0.6, label='Star')
ax.scatter(coords3.ra.wrap_at(180*u.degree).radian, coords3.dec.radian, s=1, c='g', alpha=0.6, label='Quasar')
ax.tick_params(axis='x', colors='black')  # Set x-axis tick color
ax.tick_params(axis='y', colors='white')  # Set y-axis tick color
ax.legend(loc="upper right", scatterpoints=1, fontsize=6)
ax.grid(True)
st.pyplot(fig)

_MJD_BASE_TIME_ = datetime.strptime('17/11/1858 00:00', '%d/%m/%Y %H:%M')

def convertMJD(x=0):
    return _MJD_BASE_TIME_ + timedelta(days=x)

# Filter data according to classes
timeline_stars  = data.loc[data['class']=='STAR'  , 'mjd']
timeline_galaxy = data.loc[data['class']=='GALAXY', 'mjd']
timeline_qso    = data.loc[data['class']=='QSO'   , 'mjd']

# Layout with three columns
col1, col2, col3 = st.columns(3)

with col1:
    st.header('Class Distribution')
    class_counts = data['class'].value_counts().reset_index()
    class_counts.columns = ['class', 'count']
    fig3 = px.pie(class_counts, values='count', names='class', hole=0.4)
    st.plotly_chart(fig3)

    fig = px.imshow(data[data['class']=='STAR'][['u', 'g', 'r', 'i', 'z']].corr(), 
                labels=dict(x='Bands', y='Bands', color='Correlation'),
                title='Star', color_continuous_scale='reds')
    st.plotly_chart(fig)



with col2:
    st.header('Dec Distribution by Class')
    fig = px.box(data, x='class', y='dec', color='class')
    fig.update_layout(
    width=2000,
    height=500
    )
    st.plotly_chart(fig)

    fig2 = px.imshow(data[data['class']=='GALAXY'][['u', 'g', 'r', 'i', 'z']].corr(), 
                 labels=dict(x='Bands', y='Bands', color='Correlation'),
                 title='Galaxy', color_continuous_scale='reds')
    
    st.plotly_chart(fig2)


with col3:
    st.header('Distribution of Modified Julian Date (MJD) by Class')

    # Create figure and axes
    fig, ax = plt.subplots(figsize=(16, 10))

    # Plot kernel density estimate for each class
    sns.kdeplot(timeline_stars, label='STAR', ax=ax)
    sns.kdeplot(timeline_galaxy, label='GALAXY', ax=ax)
    sns.kdeplot(timeline_qso, label='QSO', ax=ax)

    # Set plot labels and title
    plt.xlabel('Modified Julian Date (MJD)')
    plt.ylabel('Density')

    # Show legend
    plt.legend()

    # Display the plot in Streamlit
    st.pyplot(fig)

    fig3 = px.imshow(data[data['class']=='QSO'][['u', 'g', 'r', 'i', 'z']].corr(), 
                 labels=dict(x='Bands', y='Bands', color='Correlation'),
                 title='QSO', color_continuous_scale='reds')
    
    st.plotly_chart(fig3)




# Additional visualizations can be added similarly





