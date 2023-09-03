import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from streamlit_extras.dataframe_explorer import dataframe_explorer
from streamlit_extras.no_default_selectbox import selectbox
from streamlit_extras.grid import grid
import traceback
from wordcloud import WordCloud

st.set_page_config(
    page_title="Dataframe Viewer",
    page_icon="📊",
    layout="wide"
)

def convert_df(df, index = False):
    return df.to_csv(index = index).encode('utf-8')

with st.sidebar:
    with st.expander(label = '**Upload files**', expanded = True):
        st.session_state.files = st.file_uploader("Upload files", type = ["csv"], accept_multiple_files = True, label_visibility = 'collapsed')
    if st.session_state.files:
        st.session_state.file_name = {}
        for i in range(0, len(st.session_state.files)):
            st.session_state.file_name[st.session_state.files[i].name] = i
            if 'csv' in st.session_state.files[i].name or 'CSV' in st.session_state.files[i].name:
                st.session_state.files[i] = pd.read_csv(st.session_state.files[i])
                st.session_state.files[i]['Row_Number_'] = np.arange(0, len(st.session_state.files[i]))
        st.session_state.select_df = selectbox("Select Dataframe", st.session_state.file_name.keys(), no_selection_label = None)
    else:
        st.session_state.select_df = None
        st.session_state.filtered_df = pd.DataFrame()

st.title("**Pandas DataFrame Viewer**", anchor = False)

main_tabs = st.tabs(['**DataFrame**', "**Statistics**", "**Grapher**", "**Reshaper**"])

with main_tabs[0]:
    st.write("")
    log = ''
    if st.session_state.select_df:
        with st.sidebar:
            with st.expander(label = '**Filters**'):
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
                # columns_to_show_df = st.data_editor(pd.DataFrame({"Column Name": st.session_state.filtered_df.columns.to_list(), "Show?": True, "Type": st.session_state.filtered_df.dtypes}), num_rows="fixed", hide_index = True, disabled = ["Columns"], height = 250, use_container_width = True)
            curr_filtered_df = st.session_state.filtered_df[columns_to_show_df[columns_to_show_df['Show?'] == True]['Column Name'].to_list()]
        st.data_editor(curr_filtered_df, use_container_width = True, num_rows="dynamic", hide_index = False)
        st.caption("**:red[Note:] To delete rows, press delete button in keyboard after selecting rows**")
        st.markdown(f"**DataFrame Shape: {curr_filtered_df.shape[0]} x {curr_filtered_df.shape[1]}**")
        st.download_button(label="**Download Modified DataFrame as CSV**", data = convert_df(curr_filtered_df), file_name=f"{st.session_state.select_df}", mime='text/csv')
        st.subheader("**Console Log**", anchor = False)
        st.markdown(f'{log}')

with main_tabs[1]:
    st.write("")
    if st.session_state.select_df:
        stats = curr_filtered_df.describe().copy().T
        stats['Unique'] = curr_filtered_df.apply(lambda x: len(x.unique()))
        st.dataframe(stats, use_container_width = True, hide_index = False)
        st.markdown(f"**DataFrame Shape: {curr_filtered_df.shape[0]} x {curr_filtered_df.shape[1]}**")
        st.download_button(label="**Download Statistics DataFrame as CSV**", data = convert_df(stats), file_name=f"stats_{st.session_state.select_df}", mime='text/csv')

with main_tabs[2]:
    st.write("")
    grapher_tabs = st.tabs(["**Scatter**", "**Line**", "**Bar**", "**Histogram**", "**Box**", "**Violin**", "**Scatter 3D**", "**Heatmap**", "**Contour**", "**Pie**", "**Splom**", "**Candlestick**", "**Word Cloud**"])
    if st.session_state.select_df:
        with grapher_tabs[0]:
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
            with grid_grapher.container():
                try:
                    if y:
                        fig = px.scatter(data_frame = curr_filtered_df, x = x, y = y, color = color, symbol = symbol, size = size, trendline = trendline, marginal_x = marginal_x, marginal_y = marginal_y, facet_row = facet_row, facet_col = facet_col, height = 750, render_mode='auto', color_continuous_scale = px.colors.sequential.Plasma)
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
                    
        with grapher_tabs[1]:
            grid_grapher = grid([1, 2], vertical_align="bottom")
            with grid_grapher.expander(label = 'Features', expanded = True):
                y = st.multiselect('**Select y values**', curr_filtered_df.columns.to_list(), key = 'grid_grapher_2_1', default = None)
                x = selectbox('**Select x value**', curr_filtered_df.columns.to_list(), key = 'grid_grapher_2_2',no_selection_label = None)
                color = selectbox('**Select color value**', curr_filtered_df.columns.to_list(), key = 'grid_grapher_2_3',no_selection_label = None)
                facet_row = selectbox('**Select facet row value**', curr_filtered_df.columns.to_list(), key = 'grid_grapher_2_4',no_selection_label = None)
                facet_col = selectbox('**Select facet col value**', curr_filtered_df.columns.to_list(), key = 'grid_grapher_2_5',no_selection_label = None)
                aggregation = selectbox('**Select aggregation**', ['mean', 'median', 'min', 'max', 'sum'], key = 'grid_grapher_2_6',no_selection_label = None)
            with grid_grapher.container():
                try:
                    line_plot_df = curr_filtered_df.copy()
                    key_cols_line = [val for val in [x, color, facet_row, facet_col] if val is not None]
                    if key_cols_line != []:
                        if aggregation is not None:
                            line_plot_df = curr_filtered_df.groupby(key_cols_line).agg(aggregation).reset_index()
                        else:
                            line_plot_df = curr_filtered_df.sort_values(key_cols_line)
                    if y:
                        fig = px.line(data_frame = line_plot_df, x = x, y = y, color = color, facet_row = facet_row, facet_col = facet_col, render_mode='auto', height = 750, color_discrete_sequence = px.colors.sequential.Plasma)
                        fig.update_traces(connectgaps=True)
                        st.plotly_chart(fig, use_container_width = True)
                    else:
                        st.plotly_chart(px.line(height = 750, render_mode='auto'), use_container_width = True)
                except Exception as e:
                    st.plotly_chart(px.line(height = 750, render_mode='auto'), use_container_width = True)
                    log = traceback.format_exc()
            st.subheader("**Console Log**", anchor = False)
            st.markdown(f'{log}')

        with grapher_tabs[2]:
            grid_grapher = grid([1, 2], vertical_align="bottom")
            with grid_grapher.expander(label = 'Features', expanded = True):
                y = st.multiselect('**Select y values**', curr_filtered_df.columns.to_list(), key = 'grid_grapher_3_1', default = None)
                x = selectbox('**Select x value**', curr_filtered_df.columns.to_list(), key = 'grid_grapher_3_2',no_selection_label = None)
                color = selectbox('**Select color value**', curr_filtered_df.columns.to_list(), key = 'grid_grapher_3_3',no_selection_label = None)
                facet_row = selectbox('**Select facet row value**', curr_filtered_df.columns.to_list(), key = 'grid_grapher_3_4',no_selection_label = None)
                facet_col = selectbox('**Select facet col value**', curr_filtered_df.columns.to_list(), key = 'grid_grapher_3_5',no_selection_label = None)
                aggregation = selectbox('**Select aggregation**', ['mean', 'median', 'min', 'max', 'sum'], key = 'grid_grapher_3_6',no_selection_label = None)
                sort = selectbox('**Select sort type**', ['asc', 'desc'], key = 'grid_grapher_3_7',no_selection_label = None)
            with grid_grapher.container():
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
                        fig = px.bar(data_frame = bar_plot_df, x = x, y = y, color = color, facet_row = facet_row, facet_col = facet_col, height = 750, color_continuous_scale = px.colors.sequential.Plasma)
                        st.plotly_chart(fig, use_container_width = True)
                    else:
                        st.plotly_chart(px.bar(height = 750), use_container_width = True)
                except Exception as e:
                    st.plotly_chart(px.bar(height = 750), use_container_width = True)
                    log = traceback.format_exc()
            st.subheader("**Console Log**", anchor = False)
            st.markdown(f'{log}')

        with grapher_tabs[3]:
            grid_grapher = grid([1, 2], vertical_align="bottom")
            with grid_grapher.expander(label = 'Features', expanded = True):
                x = st.multiselect('**Select x values**', curr_filtered_df.columns.to_list(), key = 'grid_grapher_4_1', default = None)
                color = selectbox('**Select color values**', curr_filtered_df.columns.to_list(), key = 'grid_grapher_4_2',no_selection_label = None)
                facet_row = selectbox('**Select facet row values**', curr_filtered_df.columns.to_list(), key = 'grid_grapher_4_3',no_selection_label = None)
                facet_col = selectbox('**Select facet col values**', curr_filtered_df.columns.to_list(), key = 'grid_grapher_4_4',no_selection_label = None)
                marginal = selectbox('**Select marginal**', ['rug', 'box', 'violin'], key = 'grid_grapher_4_5', no_selection_label = None)
                cumulative = st.checkbox('Cumulative ?', key = 'grid_grapher_4_6')
            with grid_grapher.container():
                try:
                    if x:
                        fig = px.histogram(data_frame = curr_filtered_df, x = x, color = color, facet_row = facet_row, facet_col = facet_col, marginal = marginal, cumulative = cumulative, height = 750, color_discrete_sequence = px.colors.sequential.Plasma)
                        st.plotly_chart(fig, use_container_width = True)
                    else:
                        st.plotly_chart(px.bar(height = 750), use_container_width = True)
                except Exception as e:
                    st.plotly_chart(px.bar(height = 750), use_container_width = True)
                    log = traceback.format_exc()
            st.subheader("**Console Log**", anchor = False)
            st.markdown(f'{log}')

        with grapher_tabs[4]:
            grid_grapher = grid([1, 2], vertical_align="bottom")
            with grid_grapher.expander(label = 'Features', expanded = True):
                y = st.multiselect('**Select y values**', curr_filtered_df.columns.to_list(), key = 'grid_grapher_5_1', default = None)
                x = selectbox('**Select x value**', curr_filtered_df.columns.to_list(), key = 'grid_grapher_5_2',no_selection_label = None)
                color = selectbox('**Select color value**', curr_filtered_df.columns.to_list(), key = 'grid_grapher_5_3',no_selection_label = None)
                facet_row = selectbox('**Select facet row value**', curr_filtered_df.columns.to_list(), key = 'grid_grapher_5_4',no_selection_label = None)
                facet_col = selectbox('**Select facet col value**', curr_filtered_df.columns.to_list(), key = 'grid_grapher_5_5',no_selection_label = None)
            with grid_grapher.container():
                try:
                    if y:
                        fig = px.box(data_frame = curr_filtered_df, x = x, y = y, color = color, facet_row = facet_row, facet_col = facet_col, height = 750, color_discrete_sequence = px.colors.sequential.Plasma)
                        st.plotly_chart(fig, use_container_width = True)
                    else:
                        st.plotly_chart(px.box(height = 750), use_container_width = True)
                except Exception as e:
                    st.plotly_chart(px.box(height = 750), use_container_width = True)
                    log = traceback.format_exc()
            st.subheader("**Console Log**", anchor = False)
            st.markdown(f'{log}')

        with grapher_tabs[5]:
            grid_grapher = grid([1, 2], vertical_align="bottom")
            with grid_grapher.expander(label = 'Features', expanded = True):
                y = st.multiselect('**Select y values**', curr_filtered_df.columns.to_list(), key = 'grid_grapher_6_1', default = None)
                x = selectbox('**Select x value**', curr_filtered_df.columns.to_list(), key = 'grid_grapher_6_2',no_selection_label = None)
                color = selectbox('**Select color value**', curr_filtered_df.columns.to_list(), key = 'grid_grapher_6_3',no_selection_label = None)
                facet_row = selectbox('**Select facet row value**', curr_filtered_df.columns.to_list(), key = 'grid_grapher_6_4',no_selection_label = None)
                facet_col = selectbox('**Select facet col value**', curr_filtered_df.columns.to_list(), key = 'grid_grapher_6_5',no_selection_label = None)
            with grid_grapher.container():
                try:
                    if y:
                        fig = px.violin(data_frame = curr_filtered_df, x = x, y = y, color = color, facet_row = facet_row, facet_col = facet_col, height = 750, color_discrete_sequence = px.colors.sequential.Plasma)
                        st.plotly_chart(fig, use_container_width = True)
                    else:
                        st.plotly_chart(px.violin(height = 750), use_container_width = True)
                except Exception as e:
                    st.plotly_chart(px.violin(height = 750), use_container_width = True)
                    log = traceback.format_exc()
            st.subheader("**Console Log**", anchor = False)
            st.markdown(f'{log}')

        with grapher_tabs[6]:
            grid_grapher = grid([1, 2], vertical_align="bottom")
            with grid_grapher.expander(label = 'Features', expanded = True):
                y = selectbox('**Select y value**', curr_filtered_df.columns.to_list(), key = 'grid_grapher_7_1', no_selection_label = None)
                x = selectbox('**Select x value**', curr_filtered_df.columns.to_list(), key = 'grid_grapher_7_2',no_selection_label = None)
                z = selectbox('**Select z value**', curr_filtered_df.columns.to_list(), key = 'grid_grapher_7_3',no_selection_label = None)
                color = selectbox('**Select color value**', curr_filtered_df.columns.to_list(), key = 'grid_grapher_7_4',no_selection_label = None)
            with grid_grapher.container():
                try:
                    if y:
                        fig = px.scatter_3d(data_frame = curr_filtered_df, x = x, y = y, z = z, color = color, height = 750, color_discrete_sequence = px.colors.sequential.Plasma)
                        st.plotly_chart(fig, use_container_width = True)
                    else:
                        st.plotly_chart(px.bar(height = 750), use_container_width = True)
                except Exception as e:
                    st.plotly_chart(px.bar(height = 750), use_container_width = True)
                    log = traceback.format_exc()
            st.subheader("**Console Log**", anchor = False)
            st.markdown(f'{log}')

        with grapher_tabs[7]:
            grid_grapher = grid([1, 2], vertical_align="bottom")
            with grid_grapher.expander(label = 'Features', expanded = True):
                y = selectbox('**Select y value**', curr_filtered_df.columns.to_list(), key = 'grid_grapher_8_1', no_selection_label = None)
                x = selectbox('**Select x value**', curr_filtered_df.columns.to_list(), key = 'grid_grapher_8_2',no_selection_label = None)
                z = selectbox('**Select z value**', curr_filtered_df.columns.to_list(), key = 'grid_grapher_8_3',no_selection_label = None)
                facet_row = selectbox('**Select facet row value**', curr_filtered_df.columns.to_list(), key = 'grid_grapher_8_4',no_selection_label = None)
                facet_col = selectbox('**Select facet col value**', curr_filtered_df.columns.to_list(), key = 'grid_grapher_8_5',no_selection_label = None)
            with grid_grapher.container():
                try:
                    if y:
                        fig = px.density_heatmap(data_frame = curr_filtered_df, x = x, y = y, z = z, facet_row = facet_row, facet_col = facet_col, height = 750, color_continuous_scale = px.colors.sequential.Plasma)
                        st.plotly_chart(fig, use_container_width = True)
                    else:
                        st.plotly_chart(px.density_heatmap(height = 750), use_container_width = True)
                except Exception as e:
                    st.plotly_chart(px.density_heatmap(height = 750), use_container_width = True)
                    log = traceback.format_exc()
            st.subheader("**Console Log**", anchor = False)
            st.markdown(f'{log}')

        with grapher_tabs[8]:
            grid_grapher = grid([1, 2], vertical_align="bottom")
            with grid_grapher.expander(label = 'Features', expanded = True):
                y = selectbox('**Select y value**', curr_filtered_df.columns.to_list(), key = 'grid_grapher_9_1', no_selection_label = None)
                x = selectbox('**Select x value**', curr_filtered_df.columns.to_list(), key = 'grid_grapher_9_2',no_selection_label = None)
                z = selectbox('**Select z value**', curr_filtered_df.columns.to_list(), key = 'grid_grapher_9_3',no_selection_label = None)
                facet_row = selectbox('**Select facet row value**', curr_filtered_df.columns.to_list(), key = 'grid_grapher_9_4',no_selection_label = None)
                facet_col = selectbox('**Select facet col value**', curr_filtered_df.columns.to_list(), key = 'grid_grapher_9_5',no_selection_label = None)
            with grid_grapher.container():
                try:
                    if y:
                        fig = px.density_contour(data_frame = curr_filtered_df, x = x, y = y, color = z, facet_row = facet_row, facet_col = facet_col, height = 750)
                        fig.update_traces(contours_coloring = 'fill', contours_showlabels = True, colorscale = 'Plasma')
                        st.plotly_chart(fig, use_container_width = True)
                    else:
                        st.plotly_chart(px.density_contour(height = 750), use_container_width = True)
                except Exception as e:
                    st.plotly_chart(px.density_contour(height = 750), use_container_width = True)
                    log = traceback.format_exc()
            st.subheader("**Console Log**", anchor = False)
            st.markdown(f'{log}')

        with grapher_tabs[9]:
            grid_grapher = grid([1, 2], vertical_align="bottom")
            with grid_grapher.expander(label = 'Features', expanded = True):
                name = selectbox('**Select name value**', curr_filtered_df.columns.to_list(), key = 'grid_grapher_10_1', no_selection_label = None)
                value = selectbox("**Select value's value**", curr_filtered_df.columns.to_list(), key = 'grid_grapher_10_2',no_selection_label = None)
                color = selectbox('**Select color value**', curr_filtered_df.columns.to_list(), key = 'grid_grapher_10_3',no_selection_label = None)
                facet_row = selectbox('**Select facet row value**', curr_filtered_df.columns.to_list(), key = 'grid_grapher_10_4',no_selection_label = None)
                facet_col = selectbox('**Select facet col value**', curr_filtered_df.columns.to_list(), key = 'grid_grapher_10_5',no_selection_label = None)
            with grid_grapher.container():
                try:
                    if name:
                        # if facet_row is not None or facet_col is not None:
                        #     raise NotImplementedError
                        fig = px.pie(data_frame = curr_filtered_df, names = name, values = value, color = color, facet_row = facet_row, facet_col = facet_col, height = 750, color_discrete_sequence = px.colors.sequential.Plasma)
                        st.plotly_chart(fig, use_container_width = True)
                    else:
                        st.plotly_chart(px.pie(height = 750), use_container_width = True)
                except Exception as e:
                    st.plotly_chart(px.pie(height = 750), use_container_width = True)
                    log = traceback.format_exc()
            st.subheader("**Console Log**", anchor = False)
            st.markdown(f'{log}')

        with grapher_tabs[10]:
            grid_grapher = grid([1, 2], vertical_align="bottom")
            with grid_grapher.expander(label = 'Features', expanded = True):
                dimensions = st.multiselect('**Select dimensions value**', curr_filtered_df.columns.to_list(), key = 'grid_grapher_11_1', default = None)
                color = selectbox('**Select color value**', curr_filtered_df.columns.to_list(), key = 'grid_grapher_11_2',no_selection_label = None)
            with grid_grapher.container():
                try:
                    if dimensions or color:
                        fig = px.scatter_matrix(data_frame = curr_filtered_df, dimensions = dimensions, color = color, height = 750, color_continuous_scale = px.colors.sequential.Plasma)
                        st.plotly_chart(fig, use_container_width = True)
                    else:
                        st.plotly_chart(px.bar(height = 750), use_container_width = True)
                except Exception as e:
                    st.plotly_chart(px.bar(height = 750), use_container_width = True)
                    log = traceback.format_exc()
            st.subheader("**Console Log**", anchor = False)
            st.markdown(f'{log}')

        with grapher_tabs[11]:
            grid_grapher = grid([1, 2], vertical_align="bottom")
            with grid_grapher.expander(label = 'Features', expanded = True):
                x = selectbox('**Select x value**', curr_filtered_df.columns.to_list(), key = 'grid_grapher_12_1', no_selection_label = None)
                open = selectbox('**Select open value**', curr_filtered_df.columns.to_list(), key = 'grid_grapher_12_2',no_selection_label = None)
                high = selectbox('**Select high value**', curr_filtered_df.columns.to_list(), key = 'grid_grapher_12_3',no_selection_label = None)
                low = selectbox('**Select low value**', curr_filtered_df.columns.to_list(), key = 'grid_grapher_12_4',no_selection_label = None)
                close = selectbox('**Select close value**', curr_filtered_df.columns.to_list(), key = 'grid_grapher_12_5',no_selection_label = None)
            with grid_grapher.container():
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

        with grapher_tabs[12]:
            grid_grapher = grid([1, 2], vertical_align="bottom")
            with grid_grapher.expander(label = 'Features', expanded = True):
                words = st.multiselect('**Select words value**', curr_filtered_df.columns.to_list(), key = 'grid_grapher_13_1', default = None)
            with grid_grapher.container():
                try:
                    if words:
                        if type(words) == str:
                            words = [words]
                        text = ' '.join(pd.concat([curr_filtered_df[x].dropna().astype(str) for x in words]))
                        wc = WordCloud(scale=2, collocations=False).generate(text)
                        st.plotly_chart(px.imshow(wc, color_continuous_scale = px.colors.sequential.Plasma), height = 750, use_container_width = True)
                    else:
                        st.plotly_chart(px.bar(height = 750), use_container_width = True)
                except Exception as e:
                    st.plotly_chart(px.bar(height = 750), use_container_width = True)
                    log = traceback.format_exc()
            st.subheader("**Console Log**", anchor = False)
            st.markdown(f'{log}')

with main_tabs[3]:
    st.write("")
    reshaper_tabs = st.tabs(["**Pivot**", "**Melt**", "**Merge**", "**Concat**", "**Join**"])
    if st.session_state.select_df:  
        with reshaper_tabs[0]:
            grid_grapher = grid([1, 2], vertical_align="bottom")
            with grid_grapher.expander(label = 'Features', expanded = True):
                index = st.multiselect('**Select index value**', curr_filtered_df.columns.to_list(), key = 'grid_reshaper_1_1', default = None)
                column = st.multiselect('**Select column value**', curr_filtered_df.columns.to_list(), key = 'grid_reshaper_1_2',default = None)
                value = st.multiselect("**Select value's value**", curr_filtered_df.columns.to_list(), key = 'grid_reshaper_1_3',default = None)
                aggfunc = st.selectbox('**Select aggfunc**', ['count','mean', 'median','mode','min','max','sum'], key = 'grid_reshaper_1_4', index = 1)
            with grid_grapher.container():
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

        with reshaper_tabs[1]:
            grid_grapher = grid([1, 2], vertical_align="bottom")
            with grid_grapher.expander(label = 'Features', expanded = True):
                id_vars = st.multiselect('**Select id_vars value**', curr_filtered_df.columns.to_list(), key = 'grid_reshaper_2_1', default = None)
                value_vars = st.multiselect('**Select value_vars value**', curr_filtered_df.columns.to_list(), key = 'grid_reshaper_2_2', default = None)
            with grid_grapher.container():
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

        with reshaper_tabs[2]:
            grid_grapher = grid([1, 2], vertical_align="bottom")
            other_dataframe = pd.DataFrame()
            with grid_grapher.expander(label = 'Features', expanded = True):
                other = selectbox("Select other Dataframe", list(filter(lambda x: x != st.session_state.select_df, st.session_state.file_name.keys())), key = 'grid_reshaper_3_1', no_selection_label = None)
                if other:
                    other_dataframe = st.session_state.files[st.session_state.file_name[other]]
                how = st.selectbox('**Select how**', ['inner', 'left', 'right', 'outer'], key = 'grid_reshaper_3_2', index = 0)
                left_on = st.multiselect('**Select left on values**', curr_filtered_df.columns.to_list(), key = 'grid_reshaper_3_3',default = None)
                right_on = st.multiselect('**Select right on values (Other DataFrame)**', other_dataframe.columns.to_list(), key = 'grid_reshaper_3_4',default = None)
                validate = selectbox('**Select validate**', ['one_to_one', 'one_to_many', 'many_to_one', 'many_to_many'], key = 'grid_reshaper_3_5',no_selection_label = None)
            with grid_grapher.container():
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

        with reshaper_tabs[3]:
            grid_grapher = grid([1, 2], vertical_align="bottom")
            other_dataframe = pd.DataFrame()
            with grid_grapher.expander(label = 'Features', expanded = True):
                other = selectbox("Select other Dataframe", list(filter(lambda x: x != st.session_state.select_df, st.session_state.file_name.keys())), key = 'grid_reshaper_4_1', no_selection_label = None)
                if other:
                    other_dataframe = st.session_state.files[st.session_state.file_name[other]]
                axis = st.selectbox('**Select axis**', ['0 (rows)', '1 (columns)'], key = 'grid_reshaper_4_2')
            with grid_grapher.container():
                try:
                    if not(other_dataframe.empty):
                        tmp = pd.concat([curr_filtered_df, other_dataframe], axis = int(axis[0]))
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
        
        with reshaper_tabs[4]:
            grid_grapher = grid([1, 2], vertical_align="bottom")
            other_dataframe = pd.DataFrame()
            with grid_grapher.expander(label = 'Features', expanded = True):
                other = selectbox("Select other Dataframe", list(filter(lambda x: x != st.session_state.select_df, st.session_state.file_name.keys())), key = 'grid_reshaper_5_1', no_selection_label = None)
                if other:
                    other_dataframe = st.session_state.files[st.session_state.file_name[other]]
                how = st.selectbox('**Select how**', ['inner', 'left', 'right', 'outer'], key = 'grid_reshaper_5_2', index = 0)
                on = selectbox('**Select on values**', curr_filtered_df.columns.to_list(), key = 'grid_reshaper_5_3', no_selection_label = None)
                lsuffix = st.text_input("**Suffix to use from left frame's overlapping columns**", placeholder = "Enter lsuffix", key = 'grid_reshaper_5_4')
                rsuffix = st.text_input("**Suffix to use from right frame's overlapping columns**", placeholder = "Enter rsuffix", key = 'grid_reshaper_5_5')
                sort = st.checkbox('Sort ?', key = 'grid_reshaper_5_6')

            with grid_grapher.container():
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
