import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
import streamlit as st
from streamlit_extras.dataframe_explorer import dataframe_explorer
from streamlit_extras.no_default_selectbox import selectbox
from streamlit_extras.grid import grid
import streamlit_antd_components as sac
from streamlit_card import card
from streamlit_lottie import st_lottie
import traceback
from wordcloud import WordCloud
import pygwalker as pyg
import sketch
import os
import json
from datetime import datetime

os.environ['SKETCH_MAX_COLUMNS'] = '50'

st.set_page_config(
    page_title="Dataframe Viewer",
    page_icon="📊",
    layout="wide"
)

@st.cache_resource(show_spinner = 0, experimental_allow_widgets=True)
def sidebar_animation(date):
    st_lottie(load_lottiefile("lottie_files/Animation - 1694990107205.json"))

def convert_df(df, index = False):
    return df.to_csv(index = index).encode('utf-8')

def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)

with st.sidebar:
    sidebar_animation(datetime.now().date())
    page = sac.menu([
    sac.MenuItem('Home', icon='house'),
    sac.MenuItem('DataFrame', icon='speedometer2'),
    sac.MenuItem('Statistics', icon='plus-slash-minus'),
    sac.MenuItem('Grapher', icon='graph-up'),
    sac.MenuItem('Reshaper', icon='square-half'),
    sac.MenuItem('PygWalker', icon='plugin'),
    sac.MenuItem('Ask AI', icon='robot'),
    sac.MenuItem('My Projects', icon ='card-text')
    ], index=0, format_func='title', size='small', indent=15, open_index=None, open_all=True, return_index=True)

    with st.expander(label = '**Upload files**', expanded = False):
        st.session_state.files = st.file_uploader("Upload files", type = ["csv"], accept_multiple_files = True, label_visibility = 'collapsed')
        if st.session_state.files:
            st.session_state.file_name = {}
            for i in range(0, len(st.session_state.files)):
                st.session_state.file_name[st.session_state.files[i].name] = i
                if 'csv' in st.session_state.files[i].name or 'CSV' in st.session_state.files[i].name:
                    st.session_state.files[i] = pd.read_csv(st.session_state.files[i])
                    st.session_state.files[i]['Row_Number_'] = np.arange(0, len(st.session_state.files[i]))
            st.session_state.select_df = selectbox("**Select Dataframe**", st.session_state.file_name.keys(), no_selection_label = None)
        else:
            st.session_state.select_df = None
            st.session_state.filtered_df = pd.DataFrame()

@st.cache_resource(show_spinner = 0, experimental_allow_widgets=True)
def home(date):
    st.divider()
    col = st.columns([5, 1])
    with col[0].container():
        st.markdown('''##### Hi, I am Sumit 👋
                    
#### A Data Analyst Aspirant From India\n**I am passionate about Data Analysis, Data Visualization, Machine Learning, Frontend and Backend Developing, Data Structures and Algorithms.**''')

    with col[1].container():
        st_lottie(load_lottiefile("lottie_files/Animation - 1694988603751.json"))

    st.divider()

    col = st.columns([2, 1])
    with col[0].container():
        st.markdown('''##### :film_projector: About the Project\n**`v2.0 Beta` ~v1.5 Beta~  ~v1.0 Beta~**\n* **This website can be used for Data Analysis, Data Filtering, Data Modifying and Data Visualization purposes.**\n* **This Project is solely inspired by my experience with the [`PandasGUI`]((https://github.com/adamerose/PandasGUI)) Library.**\n* **Re-created most of the functions of PandasGUI library.**\n* **Libraries Used: [`Streamlit`](https://streamlit.io/), [`Streamlit_extras`](https://extras.streamlit.app/), [`Pandas`](https://pandas.pydata.org/), [`Numpy`](https://numpy.org/), [`Plotly`](https://plotly.com/), [`Wordcloud`](https://amueller.github.io/word_cloud/), [`PygWalker`](https://github.com/Kanaries/pygwalker), [`Sketch`](https://github.com/approximatelabs/sketch), [`Streamlit Lottie`](https://github.com/andfanilo/streamlit-lottie/tree/main), [`Streamlit-Antd-Components`](https://github.com/nicedouble/StreamlitAntdComponents). :red[(New)]**\n* **Implemented `PygWalker` for more efficient Data Analysis. :red[(New)]**\n* **Implemented `Sketch` Library for data analysis with the help of AI. :red[(New)]**\n* **Implemented `Lottie` Animations. :red[(New)]**\n* **`UI` Changes done. :red[(New)]**\n* **Stores data in browser's cache.**\n* **During the use of AI, your dataframe information will be feeded into language models for analysis. :red[(New)]**\n* **Open Source.**\n* **As this project is in beta stage, if you find any :red[errors] please send me a screenshot in the feedback form.**

**If this sounds interesting to you, consider starring in my GitHub Repo.**

**Share the website with your friends.**

**[`GitHub Repo Link >`](https://bit.ly/3QT0wkx)**
    ''')

    with col[1].container():
        st_lottie(load_lottiefile("lottie_files/Animation - 1694988937837.json"))
        st_lottie(load_lottiefile("lottie_files/Animation - 1694989926620.json"), height = 300)

    st.divider()

    col1 = st.columns([2, 1])

    with col1[0].container():
        st.markdown('''
    ##### 🔮 Future Work

    * **Adding Code Export for graphs and for changes in dataframe**
    * **Adding Query based filtering**
    * **More Error Handling**
    ''')
    with col1[1].container():
        st_lottie(load_lottiefile("lottie_files/Animation - 1694991370591.json"), height = 150)
    st.divider()
    col2 = st.columns([2, 1])
    with col2[0].container():
        st.markdown('''
        ##### 📞 Contact with me

        * **Connect with me on [`LinkedIn>`](https://bit.ly/3DyD6cP)**
        * **My Github Profile [`Github>`](https://github.com/sumit10300203)**
        * **Mail me on `sumit10300203@gmail.com`**
        * **Please leave us your Feedback on [`Feedback G-Form>`](https://forms.gle/vzVN6h7FtwCn45hw6)**
        ''')
    with col2[1].container():
        st_lottie(load_lottiefile("lottie_files/Animation - 1694990540946.json"), height = 150)

if page == 0:
    st.title("**📋 Pandas DataFrame Viewer**", anchor = False)
    st.caption("**Made for Coders with ❤️**")
    home(datetime.now().date())
elif page != 7:
    st.title("**📋 Pandas DataFrame Viewer**", anchor = False)
    st.caption("**Made for Coders with ❤️**")
    log = ''
    with st.expander(label = '**Filters**'):
        if st.session_state.select_df:
            try:
                st.session_state.filtered_df = st.session_state.files[st.session_state.file_name[st.session_state.select_df]]
                typess = ['int64', 'float64', 'str', 'bool', 'object', 'timestamp']
                columns_to_show_df = st.data_editor(pd.DataFrame({"Column Name": st.session_state.filtered_df.drop('Row_Number_', axis = 1).columns.to_list(), "Show?": True, "Convert Type": st.session_state.filtered_df.drop('Row_Number_', axis = 1).dtypes.astype(str)}), column_config = {"Convert Type": st.column_config.SelectboxColumn("Convert Type", options = typess, required=True, default = 5)}, num_rows="fixed", hide_index = True, disabled = ["Columns"], height = 250, use_container_width = True)
                for i in range(0, columns_to_show_df.shape[0]):
                    if columns_to_show_df["Convert Type"][i] == 'timestamp':
                        st.session_state.filtered_df[columns_to_show_df["Column Name"][i]] = pd.to_datetime(st.session_state.filtered_df[columns_to_show_df["Column Name"][i]])
                    else:
                        st.session_state.filtered_df[columns_to_show_df["Column Name"][i]] = st.session_state.filtered_df[columns_to_show_df["Column Name"][i]].astype(columns_to_show_df["Convert Type"][i])
                st.caption("**:red[Note:] Date / Time column will always be converted to Timestamp**")
                st.session_state.filtered_df = dataframe_explorer(st.session_state.filtered_df, case=False)
                st.session_state.filtered_df.drop('Row_Number_', axis = 1, inplace = True)
            except:
                log = traceback.format_exc()
            curr_filtered_df = st.session_state.filtered_df[columns_to_show_df[columns_to_show_df['Show?'] == True]['Column Name'].to_list()]

if page == 1:
    st.write("")
    if st.session_state.select_df:
        st.data_editor(curr_filtered_df, use_container_width = True, num_rows="dynamic", hide_index = False)
        st.caption("**:red[Note:] To delete rows, press delete button in keyboard after selecting rows**")
        st.markdown(f"**DataFrame Shape: {curr_filtered_df.shape[0]} x {curr_filtered_df.shape[1]}**")
        st.download_button(label="**Download Modified DataFrame as CSV**", data = convert_df(curr_filtered_df), file_name=f"{st.session_state.select_df}", mime='text/csv')
        st.subheader("**Console Log**", anchor = False)
        st.markdown(f'{log}')

elif page == 2:
    st.write("")
    if st.session_state.select_df:
        stats = curr_filtered_df.describe().copy().T
        stats['Unique'] = curr_filtered_df.apply(lambda x: len(x.unique()))
        st.dataframe(stats, use_container_width = True, hide_index = False)
        st.markdown(f"**DataFrame Shape: {curr_filtered_df.shape[0]} x {curr_filtered_df.shape[1]}**")
        st.download_button(label="**Download Statistics DataFrame as CSV**", data = convert_df(stats, index = True), file_name=f"stats_{st.session_state.select_df}", mime='text/csv')

elif page == 3:
    st.write("")
    grapher_tabs = sac.segmented(
    items=[
        sac.SegmentedItem(label='Scatter'),
        sac.SegmentedItem(label='Line'),
        sac.SegmentedItem(label='Bar'),
        sac.SegmentedItem(label='Histogram'),
        sac.SegmentedItem(label='Box'),
        sac.SegmentedItem(label='Violin'),
        sac.SegmentedItem(label='Scatter 3D'),
        sac.SegmentedItem(label='Heatmap'),
        sac.SegmentedItem(label='Contour'),
        sac.SegmentedItem(label='Pie'),
        sac.SegmentedItem(label='Splom'),
        sac.SegmentedItem(label='Candlestick'),
        sac.SegmentedItem(label='Word Cloud'),
    ], label=None, position='top', index=0, format_func='title', radius='md', size='md', align='center', direction='horizontal', grow=True, disabled=False, readonly=False, return_index=True)
    
    if st.session_state.select_df:
        colorscales = {'Plotly3': px.colors.sequential.Plotly3, 'Viridis': px.colors.sequential.Viridis, 'Cividis': px.colors.sequential.Cividis, 'Inferno': px.colors.sequential.Inferno, 'Magma': px.colors.sequential.Magma, 'Plasma': px.colors.sequential.Plasma, 'Turbo': px.colors.sequential.Turbo, 'Blackbody': px.colors.sequential.Blackbody, 'Bluered': px.colors.sequential.Bluered, 'Electric': px.colors.sequential.Electric, 'Jet': px.colors.sequential.Jet, 'Rainbow': px.colors.sequential.Rainbow, 'Blues': px.colors.sequential.Blues, 'BuGn': px.colors.sequential.BuGn, 'BuPu': px.colors.sequential.BuPu, 'GnBu': px.colors.sequential.GnBu, 'Greens': px.colors.sequential.Greens, 'Greys': px.colors.sequential.Greys, 'OrRd': px.colors.sequential.OrRd, 'Oranges': px.colors.sequential.Oranges, 'PuBu': px.colors.sequential.PuBu, 'PuBuGn': px.colors.sequential.PuBuGn, 'PuRd': px.colors.sequential.PuRd, 'Purples': px.colors.sequential.Purples, 'RdBu': px.colors.sequential.RdBu, 'RdPu': px.colors.sequential.RdPu, 'Reds': px.colors.sequential.Reds, 'YlOrBr': px.colors.sequential.YlOrBr, 'YlOrRd': px.colors.sequential.YlOrRd, 'turbid': px.colors.sequential.turbid, 'thermal': px.colors.sequential.thermal, 'haline': px.colors.sequential.haline, 'solar': px.colors.sequential.solar, 'ice': px.colors.sequential.ice, 'gray': px.colors.sequential.gray, 'deep': px.colors.sequential.deep, 'dense': px.colors.sequential.dense, 'algae': px.colors.sequential.algae, 'matter': px.colors.sequential.matter, 'speed': px.colors.sequential.speed, 'amp': px.colors.sequential.amp, 'tempo': px.colors.sequential.tempo, 'Burg': px.colors.sequential.Burg, 'Burgyl': px.colors.sequential.Burgyl, 'Redor': px.colors.sequential.Redor, 'Oryel': px.colors.sequential.Oryel, 'Peach': px.colors.sequential.Peach, 'Pinkyl': px.colors.sequential.Pinkyl, 'Mint': px.colors.sequential.Mint, 'Blugrn': px.colors.sequential.Blugrn, 'Darkmint': px.colors.sequential.Darkmint, 'Emrld': px.colors.sequential.Emrld, 'Aggrnyl': px.colors.sequential.Aggrnyl, 'Bluyl': px.colors.sequential.Bluyl, 'Teal': px.colors.sequential.Teal, 'Tealgrn': px.colors.sequential.Tealgrn, 'Purp': px.colors.sequential.Purp, 'Purpor': px.colors.sequential.Purpor, 'Sunset': px.colors.sequential.Sunset, 'Magenta': px.colors.sequential.Magenta, 'Sunsetdark': px.colors.sequential.Sunsetdark, 'Agsunset': px.colors.sequential.Agsunset, 'Brwnyl': px.colors.sequential.Brwnyl}
        if grapher_tabs == 0:
            grid_grapher = grid([1, 2], vertical_align="bottom")
            with grid_grapher.expander(label = 'Features', expanded = True):
                y = selectbox('**Select y value**', curr_filtered_df.columns.to_list(), key = 'grid_grapher_1_1', no_selection_label = None)
                x = selectbox('**Select x value**', curr_filtered_df.columns.to_list(), key = 'grid_grapher_1_2', no_selection_label = None)
                color = selectbox('**Select color value**', curr_filtered_df.columns.to_list(), key = 'grid_grapher_1_3', no_selection_label = None)
                facet_row = selectbox('**Select facet row value**', curr_filtered_df.columns.to_list(), key = 'grid_grapher_1_4', no_selection_label = None)
                facet_col = selectbox('**Select facet col value**', curr_filtered_df.columns.to_list(), key = 'grid_grapher_1_5', no_selection_label = None)
                symbol = selectbox('**Select symbol value**', curr_filtered_df.columns.to_list(), key = 'grid_grapher_1_6', no_selection_label = None)
                size = selectbox('**Select size value**', curr_filtered_df.columns.to_list(), key = 'grid_grapher_1_7', no_selection_label = None)
                trendline = selectbox('**Select trendline**', ['ols', 'lowess'], key = 'grid_grapher_1_8', no_selection_label = None)
                marginal_x = selectbox('**Select marginal x**', ['histogram', 'rug', 'box', 'violin'], key = 'grid_grapher_1_9', no_selection_label = None)
                marginal_y = selectbox('**Select marginal y**', ['histogram', 'rug', 'box', 'violin'], key = 'grid_grapher_1_10', no_selection_label = None)
                plot_color = st.selectbox("**Select Plot Color Map**", colorscales.keys(), index = 0, key = 'grid_grapher_1_11')
            with grid_grapher.expander("", expanded = True):
                try:
                    if y:
                        fig = px.scatter(data_frame = curr_filtered_df, x = x, y = y, color = color, symbol = symbol, size = size, trendline = trendline, marginal_x = marginal_x, marginal_y = marginal_y, facet_row = facet_row, facet_col = facet_col, height = 750, render_mode='auto', color_continuous_scale = colorscales[plot_color])
                        fig.update_layout(coloraxis = fig.layout.coloraxis)
                        st.plotly_chart(fig, use_container_width = True)
                    else:
                        st.plotly_chart(px.scatter(height = 750, render_mode='auto'), use_container_width = True)
                    log = ''
                except Exception as e:
                    st.plotly_chart(px.scatter(height = 750, render_mode='auto'), use_container_width = True)
                    log = traceback.format_exc()
            st.subheader("**Console Log**", anchor = False)
            st.markdown(f'{log}')

        elif grapher_tabs == 1:
            grid_grapher = grid([1, 2], vertical_align="bottom")
            with grid_grapher.expander(label = 'Features', expanded = True):
                y = st.multiselect('**Select y values**', curr_filtered_df.columns.to_list(), key = 'grid_grapher_2_1', default = None)
                x = selectbox('**Select x value**', curr_filtered_df.columns.to_list(), key = 'grid_grapher_2_2',no_selection_label = None)
                color = selectbox('**Select color value**', curr_filtered_df.columns.to_list(), key = 'grid_grapher_2_3',no_selection_label = None)
                facet_row = selectbox('**Select facet row value**', curr_filtered_df.columns.to_list(), key = 'grid_grapher_2_4',no_selection_label = None)
                facet_col = selectbox('**Select facet col value**', curr_filtered_df.columns.to_list(), key = 'grid_grapher_2_5',no_selection_label = None)
                aggregation = selectbox('**Select aggregation**', ['mean', 'median', 'min', 'max', 'sum'], key = 'grid_grapher_2_6',no_selection_label = None)
                plot_color = st.selectbox("**Select Plot Color Map**", colorscales.keys(), index = 0, key = 'grid_grapher_2_7')
            with grid_grapher.expander("", expanded = True):
                try:
                    line_plot_df = curr_filtered_df.copy()
                    key_cols_line = [val for val in [x, color, facet_row, facet_col] if val is not None]
                    if key_cols_line != []:
                        if aggregation is not None:
                            line_plot_df = curr_filtered_df.groupby(key_cols_line).agg(aggregation).reset_index()
                        else:
                            line_plot_df = curr_filtered_df.sort_values(key_cols_line)
                    if y:
                        fig = px.line(data_frame = line_plot_df, x = x, y = y, color = color, facet_row = facet_row, facet_col = facet_col, render_mode='auto', height = 750, color_discrete_sequence = colorscales[plot_color])
                        fig.update_traces(connectgaps=True)
                        st.plotly_chart(fig, use_container_width = True)
                    else:
                        st.plotly_chart(px.line(height = 750, render_mode='auto'), use_container_width = True)
                except Exception as e:
                    st.plotly_chart(px.line(height = 750, render_mode='auto'), use_container_width = True)
                    log = traceback.format_exc()
            st.subheader("**Console Log**", anchor = False)
            st.markdown(f'{log}')

        elif grapher_tabs == 2:
            grid_grapher = grid([1, 2], vertical_align="bottom")
            with grid_grapher.expander(label = 'Features', expanded = True):
                y = st.multiselect('**Select y values**', curr_filtered_df.columns.to_list(), key = 'grid_grapher_3_1', default = None)
                x = selectbox('**Select x value**', curr_filtered_df.columns.to_list(), key = 'grid_grapher_3_2',no_selection_label = None)
                color = selectbox('**Select color value**', curr_filtered_df.columns.to_list(), key = 'grid_grapher_3_3',no_selection_label = None)
                facet_row = selectbox('**Select facet row value**', curr_filtered_df.columns.to_list(), key = 'grid_grapher_3_4',no_selection_label = None)
                facet_col = selectbox('**Select facet col value**', curr_filtered_df.columns.to_list(), key = 'grid_grapher_3_5',no_selection_label = None)
                aggregation = selectbox('**Select aggregation**', ['mean', 'median', 'min', 'max', 'sum'], key = 'grid_grapher_3_6',no_selection_label = None)
                plot_color = st.selectbox("**Select Plot Color Map**", colorscales.keys(), index = 0, key = 'grid_grapher_3_7')
                sort = selectbox('**Select sort type**', ['asc', 'desc'], key = 'grid_grapher_3_8',no_selection_label = None)
            with grid_grapher.expander("", expanded = True):
                try:
                    bar_plot_df = curr_filtered_df.copy()
                    key_cols_bar = [val for val in [x, color, facet_row, facet_col] if val is not None]
                    if key_cols_bar != []:
                        if aggregation is not None:
                            bar_plot_df = curr_filtered_df.groupby(key_cols_bar).agg(aggregation).reset_index()
                        else:
                            bar_plot_df = curr_filtered_df.sort_values(key_cols_bar)
                    if sort is not None:
                        if sort == 'asc':
                            bar_plot_df = bar_plot_df.sort_values(y, ascending=True)
                        else:
                            bar_plot_df = bar_plot_df.sort_values(y, ascending=False)
                    if y:
                        fig = px.bar(data_frame = bar_plot_df, x = x, y = y, color = color, facet_row = facet_row, facet_col = facet_col, height = 750, color_continuous_scale = colorscales[plot_color])
                        st.plotly_chart(fig, use_container_width = True)
                    else:
                        st.plotly_chart(px.bar(height = 750), use_container_width = True)
                except Exception as e:
                    st.plotly_chart(px.bar(height = 750), use_container_width = True)
                    log = traceback.format_exc()
            st.subheader("**Console Log**", anchor = False)
            st.markdown(f'{log}')

        elif grapher_tabs == 3:
            grid_grapher = grid([1, 2], vertical_align="bottom")
            with grid_grapher.expander(label = 'Features', expanded = True):
                x = st.multiselect('**Select x values**', curr_filtered_df.columns.to_list(), key = 'grid_grapher_4_1', default = None)
                color = selectbox('**Select color values**', curr_filtered_df.columns.to_list(), key = 'grid_grapher_4_2',no_selection_label = None)
                facet_row = selectbox('**Select facet row values**', curr_filtered_df.columns.to_list(), key = 'grid_grapher_4_3',no_selection_label = None)
                facet_col = selectbox('**Select facet col values**', curr_filtered_df.columns.to_list(), key = 'grid_grapher_4_4',no_selection_label = None)
                marginal = selectbox('**Select marginal**', ['rug', 'box', 'violin'], key = 'grid_grapher_4_5', no_selection_label = None)
                plot_color = st.selectbox("**Select Plot Color Map**", colorscales.keys(), index = 0, key = 'grid_grapher_4_6')
                cumulative = st.checkbox('Cumulative ?', key = 'grid_grapher_4_7')
            with grid_grapher.expander("", expanded = True):
                try:
                    if x:
                        fig = px.histogram(data_frame = curr_filtered_df, x = x, color = color, facet_row = facet_row, facet_col = facet_col, marginal = marginal, cumulative = cumulative, height = 750, color_discrete_sequence = colorscales[plot_color])
                        st.plotly_chart(fig, use_container_width = True)
                    else:
                        st.plotly_chart(px.bar(height = 750), use_container_width = True)
                except Exception as e:
                    st.plotly_chart(px.bar(height = 750), use_container_width = True)
                    log = traceback.format_exc()
            st.subheader("**Console Log**", anchor = False)
            st.markdown(f'{log}')

        elif grapher_tabs == 4:
            grid_grapher = grid([1, 2], vertical_align="bottom")
            with grid_grapher.expander(label = 'Features', expanded = True):
                y = st.multiselect('**Select y values**', curr_filtered_df.columns.to_list(), key = 'grid_grapher_5_1', default = None)
                x = selectbox('**Select x value**', curr_filtered_df.columns.to_list(), key = 'grid_grapher_5_2',no_selection_label = None)
                color = selectbox('**Select color value**', curr_filtered_df.columns.to_list(), key = 'grid_grapher_5_3',no_selection_label = None)
                facet_row = selectbox('**Select facet row value**', curr_filtered_df.columns.to_list(), key = 'grid_grapher_5_4',no_selection_label = None)
                facet_col = selectbox('**Select facet col value**', curr_filtered_df.columns.to_list(), key = 'grid_grapher_5_5',no_selection_label = None)
                plot_color = st.selectbox("**Select Plot Color Map**", colorscales.keys(), index = 0, key = 'grid_grapher_5_6')
            with grid_grapher.expander("", expanded = True):
                try:
                    if y:
                        fig = px.box(data_frame = curr_filtered_df, x = x, y = y, color = color, facet_row = facet_row, facet_col = facet_col, height = 750, color_discrete_sequence = colorscales[plot_color])
                        st.plotly_chart(fig, use_container_width = True)
                    else:
                        st.plotly_chart(px.box(height = 750), use_container_width = True)
                except Exception as e:
                    st.plotly_chart(px.box(height = 750), use_container_width = True)
                    log = traceback.format_exc()
            st.subheader("**Console Log**", anchor = False)
            st.markdown(f'{log}')

        elif grapher_tabs == 5:
            grid_grapher = grid([1, 2], vertical_align="bottom")
            with grid_grapher.expander(label = 'Features', expanded = True):
                y = st.multiselect('**Select y values**', curr_filtered_df.columns.to_list(), key = 'grid_grapher_6_1', default = None)
                x = selectbox('**Select x value**', curr_filtered_df.columns.to_list(), key = 'grid_grapher_6_2',no_selection_label = None)
                color = selectbox('**Select color value**', curr_filtered_df.columns.to_list(), key = 'grid_grapher_6_3',no_selection_label = None)
                facet_row = selectbox('**Select facet row value**', curr_filtered_df.columns.to_list(), key = 'grid_grapher_6_4',no_selection_label = None)
                facet_col = selectbox('**Select facet col value**', curr_filtered_df.columns.to_list(), key = 'grid_grapher_6_5',no_selection_label = None)
                plot_color = st.selectbox("**Select Plot Color Map**", colorscales.keys(), index = 0, key = 'grid_grapher_6_6')
            with grid_grapher.expander("", expanded = True):
                try:
                    if y:
                        fig = px.violin(data_frame = curr_filtered_df, x = x, y = y, color = color, facet_row = facet_row, facet_col = facet_col, height = 750, color_discrete_sequence = colorscales[plot_color])
                        st.plotly_chart(fig, use_container_width = True)
                    else:
                        st.plotly_chart(px.violin(height = 750), use_container_width = True)
                except Exception as e:
                    st.plotly_chart(px.violin(height = 750), use_container_width = True)
                    log = traceback.format_exc()
            st.subheader("**Console Log**", anchor = False)
            st.markdown(f'{log}')

        elif grapher_tabs == 6:
            grid_grapher = grid([1, 2], vertical_align="bottom")
            with grid_grapher.expander(label = 'Features', expanded = True):
                y = selectbox('**Select y value**', curr_filtered_df.columns.to_list(), key = 'grid_grapher_7_1', no_selection_label = None)
                x = selectbox('**Select x value**', curr_filtered_df.columns.to_list(), key = 'grid_grapher_7_2',no_selection_label = None)
                z = selectbox('**Select z value**', curr_filtered_df.columns.to_list(), key = 'grid_grapher_7_3',no_selection_label = None)
                color = selectbox('**Select color value**', curr_filtered_df.columns.to_list(), key = 'grid_grapher_7_4',no_selection_label = None)
                plot_color = st.selectbox("**Select Plot Color Map**", colorscales.keys(), index = 0, key = 'grid_grapher_7_5')
            with grid_grapher.expander("", expanded = True):
                try:
                    if y:
                        fig = px.scatter_3d(data_frame = curr_filtered_df, x = x, y = y, z = z, color = color, height = 750, color_discrete_sequence = colorscales[plot_color])
                        st.plotly_chart(fig, use_container_width = True)
                    else:
                        st.plotly_chart(px.bar(height = 750), use_container_width = True)
                except Exception as e:
                    st.plotly_chart(px.bar(height = 750), use_container_width = True)
                    log = traceback.format_exc()
            st.subheader("**Console Log**", anchor = False)
            st.markdown(f'{log}')

        elif grapher_tabs == 7:
            grid_grapher = grid([1, 2], vertical_align="bottom")
            with grid_grapher.expander(label = 'Features', expanded = True):
                y = selectbox('**Select y value**', curr_filtered_df.columns.to_list(), key = 'grid_grapher_8_1', no_selection_label = None)
                x = selectbox('**Select x value**', curr_filtered_df.columns.to_list(), key = 'grid_grapher_8_2',no_selection_label = None)
                z = selectbox('**Select z value**', curr_filtered_df.columns.to_list(), key = 'grid_grapher_8_3',no_selection_label = None)
                facet_row = selectbox('**Select facet row value**', curr_filtered_df.columns.to_list(), key = 'grid_grapher_8_4',no_selection_label = None)
                facet_col = selectbox('**Select facet col value**', curr_filtered_df.columns.to_list(), key = 'grid_grapher_8_5',no_selection_label = None)
                plot_color = st.selectbox("**Select Plot Color Map**", colorscales.keys(), index = 0, key = 'grid_grapher_8_6')
            with grid_grapher.expander("", expanded = True):
                try:
                    if y:
                        fig = px.density_heatmap(data_frame = curr_filtered_df, x = x, y = y, z = z, facet_row = facet_row, facet_col = facet_col, height = 750, color_continuous_scale = colorscales[plot_color])
                        st.plotly_chart(fig, use_container_width = True)
                    else:
                        st.plotly_chart(px.density_heatmap(height = 750), use_container_width = True)
                except Exception as e:
                    st.plotly_chart(px.density_heatmap(height = 750), use_container_width = True)
                    log = traceback.format_exc()
            st.subheader("**Console Log**", anchor = False)
            st.markdown(f'{log}')

        elif grapher_tabs == 8:
            grid_grapher = grid([1, 2], vertical_align="bottom")
            with grid_grapher.expander(label = 'Features', expanded = True):
                y = selectbox('**Select y value**', curr_filtered_df.columns.to_list(), key = 'grid_grapher_9_1', no_selection_label = None)
                x = selectbox('**Select x value**', curr_filtered_df.columns.to_list(), key = 'grid_grapher_9_2',no_selection_label = None)
                z = selectbox('**Select z value**', curr_filtered_df.columns.to_list(), key = 'grid_grapher_9_3',no_selection_label = None)
                facet_row = selectbox('**Select facet row value**', curr_filtered_df.columns.to_list(), key = 'grid_grapher_9_4',no_selection_label = None)
                facet_col = selectbox('**Select facet col value**', curr_filtered_df.columns.to_list(), key = 'grid_grapher_9_5',no_selection_label = None)
                plot_color = st.selectbox("**Select Plot Color Map**", colorscales.keys(), index = 0, key = 'grid_grapher_9_6')
            with grid_grapher.expander("", expanded = True):
                try:
                    if y:
                        fig = px.density_contour(data_frame = curr_filtered_df, x = x, y = y, color = z, facet_row = facet_row, facet_col = facet_col, height = 750)
                        fig.update_traces(contours_coloring = 'fill', contours_showlabels = True, colorscale = plot_color)
                        st.plotly_chart(fig, use_container_width = True)
                    else:
                        st.plotly_chart(px.density_contour(height = 750), use_container_width = True)
                except Exception as e:
                    st.plotly_chart(px.density_contour(height = 750), use_container_width = True)
                    log = traceback.format_exc()
            st.subheader("**Console Log**", anchor = False)
            st.markdown(f'{log}')

        elif grapher_tabs == 9:
            grid_grapher = grid([1, 2], vertical_align="bottom")
            with grid_grapher.expander(label = 'Features', expanded = True):
                name = selectbox('**Select name value**', curr_filtered_df.columns.to_list(), key = 'grid_grapher_10_1', no_selection_label = None)
                value = selectbox("**Select value's value**", curr_filtered_df.columns.to_list(), key = 'grid_grapher_10_2',no_selection_label = None)
                color = selectbox('**Select color value**', curr_filtered_df.columns.to_list(), key = 'grid_grapher_10_3',no_selection_label = None)
                facet_row = selectbox('**Select facet row value**', curr_filtered_df.columns.to_list(), key = 'grid_grapher_10_4',no_selection_label = None)
                facet_col = selectbox('**Select facet col value**', curr_filtered_df.columns.to_list(), key = 'grid_grapher_10_5',no_selection_label = None)
                plot_color = st.selectbox("**Select Plot Color Map**", colorscales.keys(), index = 0, key = 'grid_grapher_10_6')
            with grid_grapher.expander("", expanded = True):
                try:
                    if name:
                        # if facet_row is not None or facet_col is not None:
                        #     raise NotImplementedError
                        fig = px.pie(data_frame = curr_filtered_df, names = name, values = value, color = color, facet_row = facet_row, facet_col = facet_col, height = 750, color_discrete_sequence = colorscales[plot_color])
                        st.plotly_chart(fig, use_container_width = True)
                    else:
                        st.plotly_chart(px.pie(height = 750), use_container_width = True)
                except Exception as e:
                    st.plotly_chart(px.pie(height = 750), use_container_width = True)
                    log = traceback.format_exc()
            st.subheader("**Console Log**", anchor = False)
            st.markdown(f'{log}')

        elif grapher_tabs == 10:
            grid_grapher = grid([1, 2], vertical_align="bottom")
            with grid_grapher.expander(label = 'Features', expanded = True):
                dimensions = st.multiselect('**Select dimensions value**', curr_filtered_df.columns.to_list(), key = 'grid_grapher_11_1', default = None)
                color = selectbox('**Select color value (Column should be included as one of the dimension value)**', curr_filtered_df.columns.to_list(), key = 'grid_grapher_11_2',no_selection_label = None)
                diag = st.selectbox("**Select Diagonal Plot**", ['scatter', 'histogram', 'box'], index = 1, key = 'grid_grapher_11_3')
                plot_color = st.selectbox("**Select Plot Color Map**", ['Greys', 'YlGnBu', 'Greens', 'YlOrRd', 'Bluered', 'RdBu', 'Reds', 'Blues', 'Picnic', 'Rainbow', 'Portland', 'Jet', 'Hot', 'Blackbody', 'Earth', 'Electric', 'Viridis', 'Cividis'], index = 0, key = 'grid_grapher_11_4')
            
            with grid_grapher.expander("", expanded = True):
                try:
                    if dimensions:
                        # fig = px.scatter_matrix(data_frame = curr_filtered_df, dimensions = dimensions, color = color, height = 750, color_continuous_scale = colorscales[plot_color])
                        fig = ff.create_scatterplotmatrix(curr_filtered_df[dimensions], diag = diag, title = "", index = color, colormap = plot_color, height = 750)
                        st.plotly_chart(fig, use_container_width = True)
                    else:
                        st.plotly_chart(px.bar(height = 750), use_container_width = True)
                except Exception as e:
                    st.plotly_chart(px.bar(height = 750), use_container_width = True)
                    log = traceback.format_exc()
            st.subheader("**Console Log**", anchor = False)
            st.markdown(f'{log}')

        elif grapher_tabs == 11:
            grid_grapher = grid([1, 2], vertical_align="bottom")
            with grid_grapher.expander(label = 'Features', expanded = True):
                x = selectbox('**Select x value**', curr_filtered_df.columns.to_list(), key = 'grid_grapher_12_1', no_selection_label = None)
                open = selectbox('**Select open value**', curr_filtered_df.columns.to_list(), key = 'grid_grapher_12_2',no_selection_label = None)
                high = selectbox('**Select high value**', curr_filtered_df.columns.to_list(), key = 'grid_grapher_12_3',no_selection_label = None)
                low = selectbox('**Select low value**', curr_filtered_df.columns.to_list(), key = 'grid_grapher_12_4',no_selection_label = None)
                close = selectbox('**Select close value**', curr_filtered_df.columns.to_list(), key = 'grid_grapher_12_5',no_selection_label = None)
            with grid_grapher.expander("", expanded = True):
                try:
                    if x and open and high and low and close:
                        fig = go.Figure(data=[go.Candlestick(x = curr_filtered_df[x], open = curr_filtered_df[open], high = curr_filtered_df[high], low = curr_filtered_df[low], close = curr_filtered_df[close])])
                        fig.update_layout(height=750)
                        st.plotly_chart(fig, use_container_width = True)
                    else:
                        st.plotly_chart(px.density_contour(height = 750), use_container_width = True)
                except Exception as e:
                    st.plotly_chart(px.density_contour(height = 750), use_container_width = True)
                    log = traceback.format_exc()
            st.subheader("**Console Log**", anchor = False)
            st.markdown(f'{log}')

        elif grapher_tabs == 12:
            grid_grapher = grid([1, 2], vertical_align="bottom")
            with grid_grapher.expander(label = 'Features', expanded = True):
                words = st.multiselect('**Select words value**', curr_filtered_df.columns.to_list(), key = 'grid_grapher_13_1', default = None)
                plot_color = st.selectbox("**Select Plot Color Map**", colorscales.keys(), index = 0, key = 'grid_grapher_13_2')
            with grid_grapher.expander("", expanded = True):
                try:
                    if words:
                        if type(words) == str:
                            words = [words]
                        text = ' '.join(pd.concat([curr_filtered_df[x].dropna().astype(str) for x in words]))
                        wc = WordCloud(scale=2, collocations=False).generate(text)
                        st.plotly_chart(px.imshow(wc, color_continuous_scale = colorscales[plot_color]), height = 750, use_container_width = True)
                    else:
                        st.plotly_chart(px.bar(height = 750), use_container_width = True)
                except Exception as e:
                    st.plotly_chart(px.bar(height = 750), use_container_width = True)
                    log = traceback.format_exc()
            st.subheader("**Console Log**", anchor = False)
            st.markdown(f'{log}')

elif page == 4:
    st.write("")
    reshaper_tabs = sac.segmented(
    items=[
        sac.SegmentedItem(label='Pivot'),
        sac.SegmentedItem(label='Melt'),
        sac.SegmentedItem(label='Merge'),
        sac.SegmentedItem(label='Concat'),
        sac.SegmentedItem(label='Join')
    ], label=None, position='top', index=0, format_func='title', radius='md', size='md', align='center', direction='horizontal', grow=True, disabled=False, readonly=False, return_index=True)
    if st.session_state.select_df:  
        if reshaper_tabs == 0:
            grid_grapher = grid([1, 2], vertical_align="bottom")
            with grid_grapher.expander(label = 'Features', expanded = True):
                index = st.multiselect('**Select index value**', curr_filtered_df.columns.to_list(), key = 'grid_reshaper_1_1', default = None)
                column = st.multiselect('**Select column value**', curr_filtered_df.columns.to_list(), key = 'grid_reshaper_1_2',default = None)
                value = st.multiselect("**Select value's value**", curr_filtered_df.columns.to_list(), key = 'grid_reshaper_1_3',default = None)
                aggfunc = st.selectbox('**Select aggfunc**', ['count','mean', 'median','mode','min','max','sum'], key = 'grid_reshaper_1_4', index = 1)
            with grid_grapher.expander("", expanded = True):
                try:
                    if index or column:
                        tmp = curr_filtered_df.pivot_table(index = index, columns = column, values = value, aggfunc = aggfunc).copy()
                        st.dataframe(tmp, height = 750, use_container_width = True)
                        st.markdown(f"**DataFrame Shape: {tmp.shape[0]} x {tmp.shape[1]}**")
                        st.download_button(label="**Download Modified DataFrame as CSV**", data = convert_df(tmp), file_name=f"Pivot_{st.session_state.select_df}", mime='text/csv')
                    else:
                        st.dataframe(pd.DataFrame(), use_container_width = True)
                except Exception as e:
                    st.dataframe(pd.DataFrame(), use_container_width = True)
                    log = traceback.format_exc()
            st.subheader("**Console Log**", anchor = False)
            st.markdown(f'{log}')

        elif reshaper_tabs == 1:
            grid_grapher = grid([1, 2], vertical_align="bottom")
            with grid_grapher.expander(label = 'Features', expanded = True):
                id_vars = st.multiselect('**Select id_vars value**', curr_filtered_df.columns.to_list(), key = 'grid_reshaper_2_1', default = None)
                value_vars = st.multiselect('**Select value_vars value**', curr_filtered_df.columns.to_list(), key = 'grid_reshaper_2_2', default = None)
            with grid_grapher.expander("", expanded = True):
                try:
                    if id_vars or value_vars:
                        tmp = curr_filtered_df.melt(id_vars = id_vars, value_vars = value_vars)
                        st.dataframe(tmp, height = 750, use_container_width = True)
                        st.markdown(f"**DataFrame Shape: {tmp.shape[0]} x {tmp.shape[1]}**")
                        st.download_button(label="**Download Modified DataFrame as CSV**", data = convert_df(tmp), file_name=f"Melt_{st.session_state.select_df}", mime='text/csv')
                    else:
                        st.dataframe(pd.DataFrame(), use_container_width = True)
                except Exception as e:
                    st.dataframe(pd.DataFrame(), use_container_width = True)
                    log = traceback.format_exc()
            st.subheader("**Console Log**", anchor = False)
            st.markdown(f'{log}')

        elif reshaper_tabs == 2:
            grid_grapher = grid([1, 2], vertical_align="bottom")
            other_dataframe = pd.DataFrame()
            with grid_grapher.expander(label = 'Features', expanded = True):
                other = selectbox("Select other Dataframe", list(filter(lambda x: x != st.session_state.select_df, st.session_state.file_name.keys())), key = 'grid_reshaper_3_1', no_selection_label = None)
                if other:
                    other_dataframe = st.session_state.files[st.session_state.file_name[other]].drop('Row_Number_', axis = 1)
                how = st.selectbox('**Select how**', ['inner', 'left', 'right', 'outer'], key = 'grid_reshaper_3_2', index = 0)
                left_on = st.multiselect('**Select left on values**', curr_filtered_df.columns.to_list(), key = 'grid_reshaper_3_3',default = None)
                right_on = st.multiselect('**Select right on values (Other DataFrame)**', other_dataframe.columns.to_list(), key = 'grid_reshaper_3_4',default = None)
                validate = selectbox('**Select validate**', ['one_to_one', 'one_to_many', 'many_to_one', 'many_to_many'], key = 'grid_reshaper_3_5',no_selection_label = None)
            with grid_grapher.expander("", expanded = True):
                try:
                    if not(other_dataframe.empty) and left_on and right_on:
                        tmp = curr_filtered_df.merge(right = other_dataframe, how = how, left_on = left_on, right_on = right_on, validate = validate)
                        st.dataframe(tmp, height = 750, use_container_width = True)
                        st.markdown(f"**DataFrame Shape: {tmp.shape[0]} x {tmp.shape[1]}**")
                        st.download_button(label="**Download Modified DataFrame as CSV**", data = convert_df(tmp), file_name=f"Merged_{st.session_state.select_df}", mime='text/csv')
                    else:
                        st.dataframe(pd.DataFrame(), use_container_width = True)
                except Exception as e:
                    st.dataframe(pd.DataFrame(), use_container_width = True)
                    log = traceback.format_exc()
            st.subheader("**Console Log**", anchor = False)
            st.markdown(f'{log}')

        elif reshaper_tabs == 3:
            grid_grapher = grid([1, 2], vertical_align="bottom")
            other_dataframe = []
            with grid_grapher.expander(label = 'Features', expanded = True):
                other = st.multiselect("**Select other Dataframe**", list(filter(lambda x: x != st.session_state.select_df, st.session_state.file_name.keys())), key = 'grid_reshaper_4_1', default = None)
                if other:
                    other_dataframe = [st.session_state.files[st.session_state.file_name[df]].drop('Row_Number_', axis = 1) for df in other]
                axis = st.selectbox('**Select axis**', ['0 (rows)', '1 (columns)'], key = 'grid_reshaper_4_2')
                ignore_index = st.checkbox('Ignore Index ?', key = 'grid_reshaper_4_3')
            with grid_grapher.expander("", expanded = True):
                try:
                    if other_dataframe:
                        tmp = pd.concat([curr_filtered_df] + other_dataframe, axis = int(axis[0]), ignore_index = ignore_index)
                        st.dataframe(tmp, height = 750, use_container_width = True)
                        st.markdown(f"**DataFrame Shape: {tmp.shape[0]} x {tmp.shape[1]}**")
                        st.download_button(label="**Download Modified DataFrame as CSV**", data = convert_df(tmp), file_name=f"Concat_{st.session_state.select_df}", mime='text/csv')
                    else:
                        st.dataframe(pd.DataFrame(), use_container_width = True)
                except Exception as e:
                    st.dataframe(pd.DataFrame(), use_container_width = True)
                    log = traceback.format_exc()
            st.subheader("**Console Log**", anchor = False)
            st.markdown(f'{log}')

        elif reshaper_tabs == 4:
            grid_grapher = grid([1, 2], vertical_align="bottom")
            other_dataframe = pd.DataFrame()
            with grid_grapher.expander(label = 'Features', expanded = True):
                other = selectbox("Select other Dataframe", list(filter(lambda x: x != st.session_state.select_df, st.session_state.file_name.keys())), key = 'grid_reshaper_5_1', no_selection_label = None)
                if other:
                    other_dataframe = st.session_state.files[st.session_state.file_name[other]].drop('Row_Number_', axis = 1)
                how = st.selectbox('**Select how**', ['inner', 'left', 'right', 'outer'], key = 'grid_reshaper_5_2', index = 0)
                on = selectbox('**Select on values**', curr_filtered_df.columns.to_list(), key = 'grid_reshaper_5_3', no_selection_label = None)
                lsuffix = st.text_input("**Suffix to use from left frame's overlapping columns**", placeholder = "Enter lsuffix", key = 'grid_reshaper_5_4')
                rsuffix = st.text_input("**Suffix to use from right frame's overlapping columns**", placeholder = "Enter rsuffix", key = 'grid_reshaper_5_5')
                sort = st.checkbox('Sort ?', key = 'grid_reshaper_5_6')

            with grid_grapher.expander("", expanded = True):
                try:
                    if not(other_dataframe.empty):
                        tmp = curr_filtered_df.join(other_dataframe, how = how, on = on, lsuffix = lsuffix, rsuffix = rsuffix, sort = sort)
                        st.dataframe(tmp, height = 750, use_container_width = True)
                        st.markdown(f"**DataFrame Shape: {tmp.shape[0]} x {tmp.shape[1]}**")
                        st.download_button(label="**Download Modified DataFrame as CSV**", data = convert_df(tmp), file_name=f"Join_{st.session_state.select_df}", mime='text/csv')
                    else:
                        st.dataframe(pd.DataFrame(), use_container_width = True)
                except Exception as e:
                    st.dataframe(pd.DataFrame(), use_container_width = True)
                    log = traceback.format_exc()
            st.subheader("**Console Log**", anchor = False)
            st.markdown(f'{log}')

elif page == 5:
    if st.session_state.select_df:
        st.markdown("**Are you sure of proceeding to PygWalker interface?**")
        try:
            if st.button("Continue", key = 'PygWalker'):
                pyg.walk(curr_filtered_df, env = 'Streamlit', dark = 'media')
        except Exception as e:
            st.dataframe(pd.DataFrame(), use_container_width = True)
            log = traceback.format_exc()
        st.subheader("**Console Log**", anchor = False)
        st.markdown(f'{log}')


elif page == 6:
    if st.session_state.select_df:
        preference_ai = st.radio("**Select your Preference**", options = ["**Ask about the selected Dataframe**", "**Ask how to perform actions on selected Dataframe**"], horizontal = True)
        prompt = st.text_area("Enter Promt", placeholder = "Enter your promt", label_visibility="collapsed")
        proceed_ai = st.button("Continue", key = 'ask_ai')
        with st.expander("**AI says**", expanded = True):
            st.divider()
            try:
                if preference_ai == "**Ask about the selected Dataframe**" and prompt and proceed_ai:
                    st.markdown(curr_filtered_df.sketch.ask(prompt, call_display=False))
                elif preference_ai == "**Ask how to perform actions on selected Dataframe**" and prompt and proceed_ai:
                    st.markdown(curr_filtered_df.sketch.howto(prompt, call_display=False))
            except Exception as e:
                st.dataframe(pd.DataFrame(), use_container_width = True)
                log = traceback.format_exc()
        st.subheader("**Console Log**", anchor = False)
        st.markdown(f'{log}')
elif page == 7:
    st.title('My Projects', anchor = False)
    card_grid = grid(3, vertical_align="center")
    with card_grid.container():
        card(
        title="Pandas Dataframe Viewer",
        text="A website for quick data analysis and visualization of your dataset with AI",
        image="https://user-images.githubusercontent.com/66067910/266804437-e9572603-7982-4b19-9732-18a079d48f5b.png",
        url="https://github.com/sumit10300203/Pandas-DataFrame-Viewer", 
        on_click = lambda: None)
    with card_grid.container():
        card(
        title="GeeksForGeeks Profile Analytics",
        text="A website to view GFG user's profile analytics for making their coding journey in a more organized way",
        image="https://media.geeksforgeeks.org/wp-content/uploads/20220413171711/gfgblack.png",
        url="https://gfg-profile-analytics.streamlit.app/", 
        on_click = lambda: None)
    with card_grid.container():
        card(
        title="Thermal Power Plant Consumption Analysis in India",
        text="A PowerBI app to show analysis of power consumption in India (2017-2020) using Prophet Model",
        image="https://user-images.githubusercontent.com/66067910/259968786-4d4bf15a-8eef-4da3-8975-af3da9d22b1c.JPG",
        url="https://bit.ly/3OyRl64", 
        on_click = lambda: None)
