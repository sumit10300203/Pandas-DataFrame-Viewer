import pandas as pd
import numpy as np
import streamlit as st
from streamlit_extras.dataframe_explorer import dataframe_explorer
from streamlit_extras.no_default_selectbox import selectbox
from streamlit_extras.grid import grid
import traceback


st.set_page_config(
    page_title="Dataframe Viewer",
    page_icon="📊",
    layout="wide"
)

col = st.columns([5, 1])
with col[0].container():
    st.markdown('''##### Hi, I am Sumit 👋
### A Data Analyst Aspirant From India
**I am passionate about Data Analysis, Data Visualization, Machine Learning, Frontend and Backend Developing, Data Structures and Algorithms.**
''')

with col[1].container():
    st.image("images/ug kid img.png", width = 100, clamp = True)

st.divider()

col = st.columns([2, 1])
with col[0].container():
    st.markdown('''##### :film_projector: About the Project

**v1.0 Beta**

* **This website can be used for Data Analysis, Data Filtering, Data Modifying and Data Visualization purposes.**
* **This Project is solely inspired by my experience with the [PandasGUI]((https://github.com/adamerose/PandasGUI)) Library.**
* **Re-created most of the functions of PandasGUI library.**
* **Libraries Used: [Streamlit](https://streamlit.io/), [Streamlit_extras](https://extras.streamlit.app/), [Pandas](https://pandas.pydata.org/), [Numpy](https://numpy.org/), [Plotly](https://plotly.com/), [Wordcloud](https://amueller.github.io/word_cloud/).**
* **Stores data in browser's cache.**
* **Open Source.**
* **As this project is in beta stage, if you find any :red[errors] please send me a screenshot in the feedback form.**

**If this sounds interesting to you, consider starring in my GitHub Repo.**

**Share the website with your friends.**
                
**[GitHub Repo Link >](https://bit.ly/3QT0wkx)**
''')

with col[1].container():
    st.image("images/4002785.png", width = 400, clamp = True)

st.divider()

with st.container():
    st.markdown('''
##### 🔮 Future Work

* **Adding Code Export for graphs and for changes in dataframe**
* **More Error Handling**


##### 📞 Contact with me

* **Connect with me on [LinkedIn >](https://bit.ly/3DyD6cP)**            
* **Mail me on sumit10300203@gmail.com**
* **Please leave us your Feedback on [Feedback G-Form>](https://forms.gle/vzVN6h7FtwCn45hw6)**
''')
