import numpy as np
from collections import defaultdict
import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from scipy import stats
import urllib
import urllib.parse

'''--------------------- Part One: Dataframe construction -----------------------'''
df0 = pd.read_csv(r"C:\Users\David\Documents\MacBook Backup\Python files\RGMP\summer 2019\my_dash_app\myenv\env_with_financial-1.csv",header=None)
df1 = df0.replace(np.NaN,'')
df = np.array(df1)

def get_dict_keys(x, df):
    return [[k.strip() for idx, k in enumerate(df[i]) if k != '' and idx <= x][-1] for i in range(4)]


def get_json():

    # create dict of company data
    nested_dict = lambda: defaultdict(nested_dict)
    data = nested_dict()

    for idx_row, row in enumerate(df):
        for idx_val, value in enumerate(row):
            if idx_row < 4 or idx_val < 2:
                continue

            # if data exists
            if value != '' and value != '--' and value != '-':

                tick = df[:, 0][idx_row]

                # find keys and add value
                keys_fin = get_dict_keys(idx_val, df)
                data[tick][keys_fin[0]][keys_fin[1]][keys_fin[2]][keys_fin[3]] = value

    return dict(data)

def key_at_depth(dct, dpt):
     if dpt > 0:
         return [key for k, subdct in dct.items() for key in key_at_depth(subdct, dpt-1)]
     else:
         return dct.keys()

def get_data_arr(data, key1, key2, key3, key4):
    tickers, data_points = [], []
    for t, _ in data.items():
        try:
            data_points.append(float(data[t][key1][key2][key3][key4]))
            tickers.append(t)
        except:
            pass

    return tickers, data_points


data = get_json()

def bubble_plot_data(data, topic, bucket, metric, size_parameter):
    bub_amt_change, bub_pct_change, bub_tickers, bub_industry, bub_size_parameter = [], [], [], [], []
    for t, _ in data.items():
        try:
            if bool(data[t][topic][bucket][metric][pct_change_q]) == True:
                bub_amt_change.append(data[t][topic][bucket][metric][value_change_q])
                bub_pct_change.append(data[t][topic][bucket][metric][pct_change_q])
                bub_industry.append(data[t][financials_topic_q][descriptive_bucket_q][industry_q][value_2017_q])
                bub_size_parameter.append(data[t][financials_topic_q][company_valuation_bucket_q][market_cap_q][value_2017_q])
                bub_tickers.append(t)
            else:
                continue
        except:
            pass
    return bub_tickers, bub_amt_change, bub_pct_change, bub_size_parameter, bub_industry

# get all keys at every depth
keys_fin = [list(set(key_at_depth(data, i))) for i in range(5)]
keys_fin = [sorted(set(x)) for x in keys_fin]

#creating bubble plot dropdown menu options
'''damages topic'''
damages_q = keys_fin[1][0]
dmgs_bckts_list = [damages_q]

damages_bucket_q = keys_fin[2][1]
env_fines_amt_q = keys_fin[3][9]
discharges_water_q = keys_fin[3][19]
amt_spills_q = keys_fin[3][2]
hazardous_waste_q = keys_fin[3][12]
dmgs_bckt_list = [env_fines_amt_q, discharges_water_q, amt_spills_q, hazardous_waste_q]

'''emissions topic'''
emissions_q = keys_fin[1][1]


total_emissions_bucket_q = keys_fin[2][8]
direct_co2_emissions_q = keys_fin[3][5]
ghg_emissions_q = keys_fin[3][22]
ods_emissions_q = keys_fin[3][15]
tot_emns_bckt_list = [direct_co2_emissions_q, ghg_emissions_q, ods_emissions_q]

emissions_per_sales_energy_q = keys_fin[2][3]
ghg_intensity_energy_q = keys_fin[3][11]
ghg_intensity_sales_q = keys_fin[3][10]
emns_sales_eng_list = [ghg_intensity_energy_q, ghg_intensity_sales_q]

emns_bckts_list = [total_emissions_bucket_q, emissions_per_sales_energy_q]

'''recycled resources topic'''
recycled_resources_q = keys_fin[1][3]



water_recycled_bucket_q = keys_fin[2][13]
pct_water_recycled_q = keys_fin[3][0]
tot_water_recycled_q = keys_fin[3][25]
wat_recy_bckt_list = [pct_water_recycled_q, tot_water_recycled_q]

energy_recycled_bucket_q = keys_fin[2][5]
renewables_pct_energy_q = keys_fin[3][23]
renewable_energy_use_q = keys_fin[3][17]
eng_recy_bckt_list = [renewables_pct_energy_q,renewable_energy_use_q]

waste_recycled_bucket_q = keys_fin[2][11]
waste_recycled_pct_total_q = keys_fin[3][28]
waste_recycled_q = keys_fin[3][27]
waste_recy_bckt_list = [waste_recycled_pct_total_q, waste_recycled_q]

recy_res_bckts_list = [water_recycled_bucket_q,energy_recycled_bucket_q,waste_recycled_bucket_q]

'''resource consumption topic'''
resource_consumption_q = keys_fin[1][4]



water_consumption_bucket_q = keys_fin[2][12]
water_use_q = keys_fin[3][26]
water_intensity_sales_q = keys_fin[3][29]
wat_cons_bckt_list = [water_use_q, water_intensity_sales_q]

energy_consumption_bucket_q = keys_fin[2][4]
energy_consumption_q = keys_fin[3][20]
energy_intensity_sales_q = keys_fin[3][8]
eng_cons_bckt_list = [energy_consumption_q, energy_intensity_sales_q]

waste_consumption_bucket_q = keys_fin[2][10]
tot_waste_q = keys_fin[3][24]
waste_generated_sales_q = keys_fin[3][30]
wast_cons_bckt_list = [tot_waste_q, waste_generated_sales_q]

rsc_cons_bckts_list = [water_consumption_bucket_q, energy_consumption_bucket_q, waste_consumption_bucket_q]

'''Financials topic'''
financials_topic_q = keys_fin[1][2]



gaap_bucket_q = keys_fin[2][6]
revenue_q = keys_fin[3][18]
eps_q = keys_fin[3][6]
gaap_bckt_list = [revenue_q, eps_q]

ratios_bucket_q = keys_fin[2][7]
pe_ratio_q = keys_fin[3][16]
debt_to_equity_q = keys_fin[3][4]
ratios_bckt_list = [pe_ratio_q, debt_to_equity_q]

volatility_bucket_q = keys_fin[2][9]
adjusted_beta_q = keys_fin[3][1]
vol_bckt_list = [adjusted_beta_q]

company_valuation_bucket_q = keys_fin[2][0]
market_cap_q = keys_fin[3][14]
ev_q = keys_fin[3][7]
comp_val_bckt_list = [market_cap_q, ev_q]

descriptive_bucket_q = keys_fin[2][2]
industry_q = keys_fin[3][13]
country_q = keys_fin[3][3]
desc_bckt_list = [industry_q, country_q]

finc_bckts_list = [gaap_bucket_q, ratios_bucket_q, volatility_bucket_q,\
                   company_valuation_bucket_q, descriptive_bucket_q ]
'''calculations'''
pct_change_q = keys_fin[4][0]
value_2017_q = keys_fin[4][1]
value_change_q = keys_fin[4][2]
prop_change_q = keys_fin[4][3]

topics_list = [damages_q, emissions_q, recycled_resources_q, resource_consumption_q]

buckets_list = [damages_bucket_q, total_emissions_bucket_q, emissions_per_sales_energy_q,\
                water_recycled_bucket_q, energy_recycled_bucket_q, waste_recycled_bucket_q,\
                water_consumption_bucket_q, energy_consumption_bucket_q, waste_consumption_bucket_q]

metrics_list = [env_fines_amt_q, discharges_water_q, amt_spills_q, hazardous_waste_q,\
                direct_co2_emissions_q, ghg_emissions_q, ods_emissions_q,\
                ghg_intensity_energy_q, ghg_intensity_sales_q, pct_water_recycled_q,\
                tot_water_recycled_q, renewables_pct_energy_q,renewable_energy_use_q,\
                waste_recycled_pct_total_q, waste_recycled_q,water_use_q,water_intensity_sales_q,\
                energy_consumption_q, energy_intensity_sales_q,tot_waste_q, waste_generated_sales_q]

size_parameters_list = [market_cap_q,revenue_q]

calculations_list = [pct_change_q, value_2017_q, value_change_q, prop_change_q]


lst = [env_fines_amt_q, discharges_water_q, amt_spills_q, hazardous_waste_q]
base_key1 = keys_fin[1][3]
base_key2 = keys_fin[2][5]
base_key3 = keys_fin[3][17]
base_key4 = keys_fin[4][0]
base_x,base_y = get_data_arr(data, base_key1, base_key2, base_key3, base_key4)


def initial_bubble_chart(data):
    bubble_tickers, energy_value_change, energy_pct_change, industry, market_cap = [], [], [], [], []
    for t, _ in data.items():
        try:
            if bool(data[t][resource_consumption_q][energy_consumption_bucket_q][energy_consumption_q][value_change_q]) == True:
                energy_value_change.append(data[t][resource_consumption_q][energy_consumption_bucket_q][energy_consumption_q][value_change_q])
                energy_pct_change.append(data[t][resource_consumption_q][energy_consumption_bucket_q][energy_consumption_q][pct_change_q])
                industry.append(data[t][financials_topic_q][descriptive_bucket_q][industry_q][value_2017_q])
                market_cap.append(data[t][financials_topic_q][company_valuation_bucket_q][market_cap_q][value_2017_q])
                bubble_tickers.append(t)
            else:
                continue
        except:
            pass
    x = list(zip(bubble_tickers, energy_value_change, energy_pct_change, market_cap, industry))
    y_test = pd.DataFrame(x)
    y_test.columns = ['Tickers', 'Energy Value Change', 'Energy percent change', 'market cap', 'industry']
    traces = []
    for industry_name in y_test['industry'].unique():
            df_by_industry = y_test[y_test['industry']==industry_name]
            traces.append(go.Scatter(
                x = df_by_industry['Energy Value Change'],
                y = df_by_industry['Energy percent change'],
                #makes this a scatter plot
                mode ='markers',
                opacity = 0.7,
                marker = dict(
                size = y_test['market cap'].astype(str).astype(float)/1000000000),
                #doesn't show proper ticker
                hovertext=bubble_tickers,
                name = industry_name,
                #template= {'template':'seaborn'}
            ))


    return {'data':traces,
            #remember that the graph dictionary takes two parameters:
            #1: 'data': traces
            #2: 'layout':go.Layout(), where the xaxis takes a dict
            'layout':go.Layout(
                title='Energy Consumption (MwH) 2012-2017 vs. 2017 Market Cap',
                xaxis={'title':'Energy Consumption Value Change'},
                yaxis={'title': 'Energy Consumption Percent Change'},
                hovermode = 'closest',
                template = 'plotly_white',


                )}



external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

'''--------------------- Part Two: Dashboard Interface -----------------------'''
'''
            Pseudo for text popup below graph.
            if keys4 and data_points > 0:
                if
                {Selected ticker} increases {keys3} by ({data_points}*100)% per year on average.
            if keys4 and data_points < 0:
                {Selected ticker} decreases {keys3} by ({data_points}*100)% per year on average.
            '''
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = html.Div([

        html.Div([
            html.Div([
                dcc.Markdown(
                children='''
                Choose keys to pull data from JSON:
                '''
                ,style={'fontFamily':'helvetica',
                        'fontSize':18,
                        'marginLeft':80}
            )
            ]),
            dcc.Dropdown(
                options=[{'label': x, 'value': x} for x in keys_fin[1]],
                value=base_key1,
                id='key1',
                style={'marginTop': '1.5em',
                       'width':'80%',
                       'marginLeft':40}
            ),
            dcc.Dropdown(
                options= [{'label': x, 'value': x} for x in keys_fin[2]],
                #options = [{'label': str(keys_fin[2][10]), 'value': str(keys_fin[2][10])}],
                value= base_key2,
                id='key2',
                style={'marginTop': '1.5em',
                       'width':'80%',
                       'marginLeft':40}
            ),
            dcc.Dropdown(
                options=[{'label': x, 'value': x} for x in keys_fin[3]],
                value=base_key3,
                id='key3',
                style={'marginTop': '1.5em',
                       'marginRight':'1.5em',
                       'width':'80%',
                       'marginLeft':40}
            ),
            dcc.Dropdown(
                options=[{'label': x, 'value': x} for x in keys_fin[4]],
                value=base_key4,
                id='key4',
                style={'marginTop': '1.5em',
                       'width':'80%',
                       'marginLeft':40}
            )],className='row',
              style={'display':'inline-block','width':'50%'}),

            html.Div([dcc.Graph(id='output-graph',
                                figure={'data':[go.Bar(
                                    x=base_x,
                                    y=base_y

                                )],
                                'layout':go.Layout(
                                    title='My test bar chart'
                                )}

                        )],style={'marginTop': 1,
                               'marginLeft':0,
                               'display':'inline-block'},
                        className = 'row',
                    ),


        html.Div([
            html.Div([
                dcc.Markdown(
                id='txt_desc',
                style={'fontFamily':'helvetica',
                'fontSize':14,
                'display':'inline-block',
                'width':'100%',
                'marginTop':0,
                'marginLeft':15}
                )]),

            html.Div([
                html.Button(
                    'Remove Outliers', id='button',
                     n_clicks_timestamp=0),
                     ],className='six columns',
                     style={'marginLeft':50,
                     'marginRight':1,
                     'marginTop':10,
                     'marginBottom':100,
                     'width':'50%',
                     'display':'inline-block'}),
                html.A(
                'Download Data',
                id='download-link',
                download="rawdata.csv",
                href="",
                target="_blank",
                style={'marginLeft':50}
                    )
                ],
                  style={'display':'inline-block','width':'50%',
                         'border':{'width':'20px', 'color':'black'}}),

            html.Div([
                html.Div([
                        html.Div([dcc.Markdown(
                        children='''
                        This is a test Div:
                        '''
                        ,style={'fontFamily':'helvetica',
                                'fontSize':18,
                                'paddingBottom':0,
                                'display':'inline-block',}
                                )]),
                        html.Div([dcc.Graph(id='test-box',
                                      figure = {'data':[go.Box(
                                          #why can't I pass in base_y here?
                                          y=base_y,
                                          boxpoints='all',
                                          jitter=0.3,
                                          pointpos=0

                                      )],
                                      'layout':go.Layout(title='Test box plot',
                                                         xaxis = {'title':'testx'},
                                                         yaxis = {'title':'testy'},
                                                         hovermode = 'closest',
                                                         colorway = ['#890C58'],
                                                         height=400)

                                    }
                                )
                            ])
                        ],className='row',
                    ),
                    ],style={
                         'width':'50%',
                         'border':{'width':'2px', 'color':'black'}}
                         ,className='row'),
        html.Div([
                    html.Div([
                        dcc.Markdown(
                        children='''
                        Topic
                        '''
                        ,style={'fontFamily':'helvetica',
                                'fontSize':15,
                                'marginTop':20,
                                'marginLeft':40,
                                'display':'inline-block'}
                                ),
                        dcc.Dropdown(
                            options=[{'label': x, 'value': x} for x in topics_list],
                            value=topics_list[3],
                            id='topic',
                            style={'marginTop': 0,
                                   'marginRight':'1.5em',
                                   'width':'100%',
                                   'marginLeft':20,
                                   'display':'inline-block'}),
                        dcc.Markdown(
                        children='''
                        Bucket
                        '''
                        ,style={'fontFamily':'helvetica',
                                'fontSize':15,
                                'marginTop':20,
                                'marginLeft':40,
                                'display':'inline-block'}
                                ),
                        dcc.Dropdown(
                            options=[{'label': x, 'value': x} for x in rsc_cons_bckts_list],
                            value=rsc_cons_bckts_list[1],
                            id='bucket',
                            style={'marginTop': 0,
                                   'marginRight':'1.5em',
                                   'width':'100%',
                                   'marginLeft':20,
                                   'display':'inline-block'}),

                        dcc.Markdown(
                        children='''
                        Metric
                        '''
                        ,style={'fontFamily':'helvetica',
                                'fontSize':15,
                                'marginTop':20,
                                'marginLeft':40,
                                'display':'inline-block'}
                                ),
                        dcc.Dropdown(
                            options=[{'label': x, 'value': x} for x in eng_cons_bckt_list],
                            value=eng_cons_bckt_list[0],
                            id='metric',
                            style={'marginTop': 0,
                                   'marginRight':'1.5em',
                                   'width':'100%',
                                   'marginLeft':20,
                                   'display':'inline-block'}),
                        dcc.Markdown(
                        children='''
                        Size Parameter
                        '''
                        ,style={'fontFamily':'helvetica',
                                'fontSize':15,
                                'marginTop':20,
                                'marginLeft':40,
                                'display':'inline-block'}
                                ),
                        dcc.Dropdown(
                            options=[{'label': x, 'value': x} for x in size_parameters_list],
                            value=size_parameters_list[0],
                            id='size-parameter',
                            style={'marginTop': 0,
                                   'marginRight':'1.5em',
                                   'width':'100%',
                                   'marginLeft':20,
                                   'display':'inline-block'}),
                        ],className='three columns'
                    ),
                                html.Div([
                                    dcc.Graph(id='bubble-graph')
                                        #figure = go.Figure(initial_bubble_chart(data)))
                                        ],style={'display':'inline-block',
                                                'width':'80%',
                                                'border':{'width':'2px', 'color':'black'},
                                                'marginLeft':350,
                                                'marginTop':10},
                                                className = 'six columns'
                                                ),
                ],className='row'
            )
        ],style={'backgroundColor':'gray'},
    )

'''-------------------- Part three: Callbacks --------------------'''

'''
@app.callback(Output('key2', 'options'),
            [Input('key1', 'value')])
def update_date_dropdown(name):
    if name == 'Financials':
        return [{'label':'Financials Bucket','value': 'Financials Bucket'}]
    if name == 'Recycled Resources':
        return [{'label':'Recycled Resources Bucket','value': 'Recycled Resources Bucket'}]
    if name == 'Damages':
        return [{'label':'Damages Bucket','value': 'Damages Bucket'}]
    if name == 'Emissions':
        return [{'label':'Emissions Bucket','value': 'Emissions Bucket'}]
    if name == 'Resource Consumption':
        return [{'label':'Resource Consumption Bucket','value': 'Resource Consumption Bucket'}]
print(keys_fin[1][3])
'''

@app.callback(
    Output(component_id='bubble-graph', component_property='figure'),
    [Input(component_id='topic',
           component_property='value'),
     Input(component_id='bucket',
           component_property='value'),
     Input(component_id='metric',
           component_property='value'),
     Input(component_id='size-parameter',
           component_property='value')])
def update_bubble_plot(topic, bucket, metric, size_parameter):
    bub_tickers_g, amt_change_g, percent_change_g, size_parameter_g, bub_industry_g = bubble_plot_data(data, topic, bucket, metric, size_parameter)
    print("\n")
    print("bubble tickers\n")
    print(bub_tickers_g)
    print("bubble amount changes\n")
    print(amt_change_g)
    print("bubble percent changes\n")
    print(percent_change_g)
    print("bubble market caps\n")
    print(size_parameter_g)
    print("bubble industry\n")
    print(bub_industry_g)
    x = pd.DataFrame(pd.np.empty((0, 5)))
    bub_list = list(zip(bub_tickers_g, amt_change_g ,percent_change_g ,size_parameter_g ,bub_industry_g))
    print("bubble list\n")
    print(bub_list)
    bub_df = x.append(bub_list)
    bub_df.columns = ['Tickers', 'Value Change', 'percent change', 'market cap', 'industry']

    #if size_parameter == revenue_q:
        #y_test.columns = ['Tickers', 'Value Change', 'percent change', 'revenue', 'industry']

    traces = []
    for industry_name in bub_df['industry'].unique():
            df_by_industry = bub_df[bub_df['industry']==industry_name]
            traces.append(go.Scatter(
                x = df_by_industry['Value Change'],
                y = df_by_industry['percent change'],
                #makes this a scatter plot
                mode ='markers',
                opacity = 0.7,
                #marker = {'size':15},
                marker = dict(
                size = bub_df['market cap'].astype(str).astype(float)/1000000000),
                #doesn't show proper ticker
                hovertext=bub_tickers_g,
                name = industry_name,
                #template= {'template':'seaborn'}
            ))
    fig = go.Figure({'data':traces,
            #remember that the graph dictionary takes two parameters:
            #1: 'data': traces
            #2: 'layout':go.Layout(), where the xaxis takes a dict
            'layout':go.Layout(
                title='Energy Consumption (MwH) 2012-2017 vs. 2017 Market Cap',
                xaxis={'title':'Energy Consumption Value Change'},
                yaxis={'title': 'Energy Consumption Percent Change'},
                hovermode = 'closest',
                template = 'plotly_white',

                )
            }
        )
    return fig

@app.callback(
    Output('bucket', 'options'),
    [Input('topic','value')])
def update_bub_bucket_dropdown(bub_topic):
    if bub_topic == damages_q:
        bub_options=[{'label': damages_bucket_q, 'value': damages_bucket_q}]
    if bub_topic == emissions_q:
        bub_options=[{'label': x, 'value': x} for x in emns_bckts_list]
    if bub_topic == recycled_resources_q:
        bub_options=[{'label': x, 'value': x} for x in recy_res_bckts_list]
    if bub_topic == resource_consumption_q:
        bub_options=[{'label': x, 'value': x} for x in rsc_cons_bckts_list]

    return bub_options

@app.callback(
    Output('metric', 'options'),
    [Input('bucket','value')])
def update_bub_metric_dropdown(bub_bucket):
    #global bub_metric_options
    if bub_bucket == damages_bucket_q:
        bub_metric_options=[{'label': x, 'value': x} for x in dmgs_bckt_list]

    if bub_bucket == total_emissions_bucket_q:
        bub_metric_options=[{'label': x, 'value': x} for x in tot_emns_bckt_list]
    if bub_bucket == emissions_per_sales_energy_q:
        bub_metric_options=[{'label': x, 'value': x} for x in emns_sales_eng_list]

    if bub_bucket == water_recycled_bucket_q:
        bub_metric_options=[{'label': x, 'value': x} for x in wat_recy_bckt_list]
    if bub_bucket == energy_recycled_bucket_q:
        bub_metric_options=[{'label': x, 'value': x} for x in eng_recy_bckt_list]
    if bub_bucket == waste_recycled_bucket_q:
        bub_metric_options=[{'label': x, 'value': x} for x in waste_recy_bckt_list]

    if bub_bucket == water_consumption_bucket_q:
        bub_metric_options=[{'label': x, 'value': x} for x in wat_cons_bckt_list]
    if bub_bucket == energy_consumption_bucket_q:
        bub_metric_options=[{'label': x, 'value': x} for x in eng_cons_bckt_list]
    if bub_bucket == waste_consumption_bucket_q:
        bub_metric_options=[{'label': x, 'value': x} for x in wast_cons_bckt_list]
    else:
        pass

    return bub_metric_options

@app.callback(Output('txt_desc','children'),
              [Input('output-graph','hoverData'),
               Input('key3','value'),
               Input('key4','value')])
def callback_stats(hover_Data,key3,key4):
    if hover_Data is None:
        return 'Hover over data to get a description'
    else:
        x = hover_Data['points'][0]['x']
        y = hover_Data['points'][0]['y']
        if key4 == '% Change [5y]':
            if y < 0:
                stats = '''
                    {} Equity decreases {}
                    by {:.2f} % per year on average.

                    '''.format(x, key3, y*100)
            if y > 0:
                stats = '''
                    {} Equity increases {}
                    by {:.2f} % per year on average.

                    '''.format(x, key3, y*100)

        if key4 == 'Proportional Change':
            if y < 0:
                stats = '''
                    {} Equity decreases {} in proportion to
                    its total use by {:.2f} % per year on average.

                    '''.format(x, key3, y*100)
            if y > 0:
                stats = '''
                    {} Equity increases {} in proportion to
                    its total use by {:.2f} % per year on average.

                    '''.format(x, key3, y*100)

        if key4 == '2017 Value':
            if y < 0:
                stats = '''
                    {} Equity had a {}
                    of {:.2f} in 2017.

                    '''.format(x, key3, y)
            if y > 0:
                stats = '''
                    {} Equity had a {}
                    of {:.2f} in 2017.

                    '''.format(x, key3, y)

        if key4 == 'Average annual change [5y]':
            if y < 0:
                stats = '''
                    {} Equity decreases
                    by {:.2f} tons per year on average.

                    '''.format(x, y)
            if y > 0:
                stats = '''
                    {} Equity increases
                    by {:.2f} tons per year on average.

                    '''.format(x, y)

    return stats



@app.callback(
    Output(component_id='output-graph', component_property='figure'),
    [Input(component_id='key1',
           component_property='value'),
     Input(component_id='key2',
           component_property='value'),
     Input(component_id='key3',
           component_property='value'),
     Input(component_id='key4',
           component_property='value'),
     Input('button','n_clicks')]
)
def update_value(key1, key2, key3, key4, button):
    x, y = get_data_arr(data, key1, key2, key3, key4)
    y_values_float = np.array(y).astype(float)
    new_tickers, new_data_flt, new_data_str = [],[], []
    data_list = list(zip(x, y_values_float))
    data_dict = dict(data_list)
    def detect_outliers(data_dict):
        values = list(data_dict.values())
        threshold = 2
        mean = np.mean(values)
        std = np.std(values)

        for i,_ in data_dict.items():
            z_score = (_ - mean)/std
            if np.abs(z_score) < threshold:
                new_tickers.append(i)
                new_data_flt.append(_)

        for i in new_data_flt:
            new_data_str.append(i.astype(str))

            #return new_tickers,new_data_str
        return new_tickers,new_data_str

    num = np.arange(1,100)
    nums = []
    for i in num:
        nums.append(int(i))

    if button == 1 or button == 3 or button == 5 or button == 7 or button == 9 or button == 11:
    #if button == (nums[button]) and (nums[button] % 2 == 1):
        detect_outliers(data_dict)
        figure={
        'data': [go.Bar(
            x=new_tickers,
            y=new_data_str,
            type='bar',
            name=key4,
            marker_color='#890C58'
            )
            ],
            'layout': go.Layout(
                title = key3 + " " + key4,
            )
        }

    else:
    #if button == (nums[button]) and (nums[button] % 2 == 1):
        figure={
        'data': [go.Bar(
            x=x,
            y=y,
            type='bar',
            name=key4,
            marker_color='#890C58'
            )
        ],
        'layout': go.Layout(
            title = key3 + " " + key4,

            )
        }
    return figure


@app.callback(
    Output(component_id='test-box', component_property='figure'),
    [Input(component_id='key1',
           component_property='value'),
     Input(component_id='key2',
           component_property='value'),
     Input(component_id='key3',
           component_property='value'),
     Input(component_id='key4',
           component_property='value'),
     Input('button','n_clicks')])
def update_box_value(key1, key2, key3, key4, button):
    x, y = get_data_arr(data, key1, key2, key3, key4)
    y_values_float = np.array(y).astype(float)
    new_tickers, new_data_flt, new_data_str = [],[], []
    data_list = list(zip(x, y_values_float))
    data_dict = dict(data_list)
    def detect_outliers(data_dict):
        values = list(data_dict.values())
        threshold = 2
        mean = np.mean(values)
        std = np.std(values)

        for i,_ in data_dict.items():
            z_score = (_ - mean)/std
            if np.abs(z_score) < threshold:
                new_tickers.append(i)
                new_data_flt.append(_)

        for i in new_data_flt:
            new_data_str.append(i.astype(str))

            #return new_tickers,new_data_str
        return new_tickers,new_data_str

    if button == 1 or button == 3 or button == 5 or button == 7 or button == 9 or button == 11:
    #if button == (nums[button]) and (nums[button] % 2 == 1):
        detect_outliers(data_dict)
        figure = {'data':[go.Box(
            #why can't I pass in base_y here?
            y=new_data_str,
            boxmean = 'sd',
            boxpoints='all',
            jitter=0.3,
            pointpos=0

        )],
        'layout':go.Layout(title='Test box plot',
                           xaxis = {'title':'testx'},
                           yaxis = {'title':'testy'},
                           hovermode = 'closest',
                           colorway = ['#890C58'],
                           height=400)
                }

    else:
    #if button == (nums[button]) and (nums[button] % 2 == 1):
        figure = {'data':[go.Box(
            #why can't I pass in base_y here?
            y=y,
            boxmean = 'sd',
            boxpoints='all',
            jitter=0.3,
            pointpos=0

        )],
        'layout':go.Layout(title='Test box plot',
                           xaxis = {'title':'testx'},
                           yaxis = {'title':'testy'},
                           hovermode = 'closest',
                           colorway = ['#890C58'],
                           height=400)
                }
    return figure

@app.callback(
    Output('download-link', 'href'),
    [Input('key1','value'),
     Input('key2','value'),
     Input('key3','value'),
     Input('key4','value')])
def update_download_link(key1,key2,key3,key4):
    tickers, data_points = get_data_arr(data, key1, key2, key3, key4)
    data_floats = np.array(data_points).astype(float)
    data_list = list(zip(tickers, data_floats))
    data_dict = dict(data_list)
    to_export = pd.DataFrame(data_list, columns=['Tickers', key3 + '' + key4])

    csv_string = to_export.to_csv(index=False, encoding='utf-8')
    csv_string = "data:text/csv;charset=utf-8," + urllib.parse.quote(csv_string)
    return csv_string

app.run_server(debug=True, port=5000)
