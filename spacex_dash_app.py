# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown',
                                             options=[
                                                {'label': 'All Sites', 'value': 'ALL'},
                                                {'label': 'CCAFS LC-40', 'value': 'ccafs_lc'},
                                                {'label': 'CCAFS SLC-40', 'value': 'ccafs_slc'},
                                                {'label': 'KSC LC-39A', 'value': 'ksc_lc'},
                                                {'label': 'VAFB SLC-4E', 'value': 'vafb_scl'},
                                             ],
                                             value='ALL',
                                             placeholder='Please Select a Launch Site',
                                             searchable=True,
                                ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                                min=0,
                                                max=10000,
                                                step=1000,
                                                value=[min_payload, max_payload],
                                ),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'), 
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(option):
    temp_df = spacex_df
    if option == 'ALL':
        pie_fig = px.pie(temp_df, values='class', names='Launch Site', title='Success rates for all launch sites')
        return pie_fig
    elif option == 'ccafs_lc':
        temp_df = spacex_df[spacex_df['Launch Site'] == 'CCAFS LC-40']
        temp_df = temp_df[temp_df.columns[1:]]
        success_count = temp_df[temp_df['class'] == 1]['class'].count()
        fail_count = temp_df[temp_df['class'] == 0]['class'].count()
        pie_fig = px.pie(values=[success_count, fail_count], names=['Success', 'Failure'],title='Success Rate for CCAFS LC-40')
        return pie_fig
    elif option == 'ccafs_slc':
        temp_df = spacex_df[spacex_df['Launch Site'] == 'CCAFS SLC-40']
        temp_df = temp_df[temp_df.columns[1:]]
        success_count = temp_df[temp_df['class'] == 1]['class'].count()
        fail_count = temp_df[temp_df['class'] == 0]['class'].count()
        pie_fig = px.pie(values=[success_count, fail_count], names=['Success', 'Failure'], title='Success Rate ')
        return pie_fig
    elif option == 'ksc_lc':
        temp_df = spacex_df[spacex_df['Launch Site'] == 'KSC LC-39A']
        temp_df = temp_df[temp_df.columns[1:]]
        success_count = temp_df[temp_df['class'] == 1]['class'].count()
        fail_count = temp_df[temp_df['class'] == 0]['class'].count()
        pie_fig = px.pie(values=[success_count, fail_count], names=['Success', 'Failure'], title='Success Rates')
        return pie_fig
    elif option == 'vafb_scl':
        temp_df = spacex_df[spacex_df['Launch Site'] == 'VAFB SLC-4E']
        temp_df = temp_df[temp_df.columns[1:]]
        success_count = temp_df[temp_df['class'] == 1]['class'].count()
        fail_count = temp_df[temp_df['class'] == 0]['class'].count()
        pie_fig = px.pie(values=[success_count, fail_count], names=['Success', 'Failure'], title='Success Rates')
        return pie_fig


# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output

@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
             [Input(component_id='site-dropdown', component_property='value'),
              Input(component_id='payload-slider', component_property='value')]
              )
def get_success_chart(option, slider_val):
    temp_df = spacex_df
    if option == 'ALL':
        temp_df = temp_df[(temp_df['Payload Mass (kg)'] >= slider_val[0]) & (temp_df['Payload Mass (kg)'] <= slider_val[1])]
        scatter_fig = px.scatter(data_frame = temp_df, y='class', x='Payload Mass (kg)', color='Booster Version Category')
        return scatter_fig
    elif option == 'ccafs_lc':
        temp_df = spacex_df[spacex_df['Launch Site'] == 'CCAFS LC-40']
        temp_df = temp_df[temp_df.columns[1:]]
        temp_df = temp_df[(temp_df['Payload Mass (kg)'] >= slider_val[0]) & (temp_df['Payload Mass (kg)'] <= slider_val[1])]
        scatter_fig = px.scatter(data_frame = temp_df, y='class', x='Payload Mass (kg)', color='Booster Version Category')
        return scatter_fig
    elif option == 'ccafs_slc':
        temp_df = spacex_df[spacex_df['Launch Site'] == 'CCAFS SLC-40']
        temp_df = temp_df[temp_df.columns[1:]]
        temp_df = temp_df[(temp_df['Payload Mass (kg)'] >= slider_val[0]) & (temp_df['Payload Mass (kg)'] <= slider_val[1])]
        scatter_fig = px.scatter(data_frame = temp_df, y='class',x='Payload Mass (kg)', color='Booster Version Category')
        return scatter_fig
    elif option == 'ksc_lc':
        temp_df = spacex_df[spacex_df['Launch Site'] == 'KSC LC-39A']
        temp_df = temp_df[temp_df.columns[1:]]
        temp_df = temp_df[(temp_df['Payload Mass (kg)'] >= slider_val[0]) & (temp_df['Payload Mass (kg)'] <= slider_val[1])]
        scatter_fig = px.scatter(data_frame = temp_df, y='class',x='Payload Mass (kg)', color='Booster Version Category')
        return scatter_fig
    elif option == 'vafb_scl':
        temp_df = spacex_df[spacex_df['Launch Site'] == 'VAFB SLC-4E']
        temp_df = temp_df[temp_df.columns[1:]]
        temp_df = temp_df[(temp_df['Payload Mass (kg)'] >= slider_val[0]) & (temp_df['Payload Mass (kg)'] <= slider_val[1])]
        scatter_fig = px.scatter(data_frame = temp_df, values='y',x='Payload Mass (kg)', color='Booster Version Category')
        return scatter_fig

# Run the app
if __name__ == '__main__':
    app.run_server(port=5500)