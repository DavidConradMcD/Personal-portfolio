import numpy as np
from collections import defaultdict
import pandas as pd
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
from plotly.subplots import make_subplots
from plotly import tools
#from scipy import stats
from collections import Counter
import glob
import os
from dash import dash_table
from portfoliowebsite import server
import pathlib
from flask import render_template_string
# Python program to show time by process_time()
#from time import process_time
#from jitcache import Cache


#cache = Cache()

# Start the stopwatch / counter
#t1_start = process_time()





##############################################################################################
                        #### Part One: Data Cleaning ####
##############################################################################################



                #### Tab One: Skills/Certifications Assessment ####

def jobs_app_layout(jobs_app):
    path = r"C:\Users\David\Documents\Ideas\Personal website\portfoliowebsite\job_postings_dash_app\job scrapes"
    col_names = ['Job Title','Company','Location','Link','Description']
    all_files = sorted(glob.glob(path + "/*.csv"))
    pd.options.display.float_format = '{:,.02f}'.format

    df_list = []
    desc_list = []
    file_order = 0
    file_order_list = []

    for filename in all_files:
        df1 = pd.read_csv(filename, names=col_names, header=None, sep=',').iloc[1:]
        file_order_list.append(file_order)
        df1['File order'] = file_order
        df_list.append(df1)
        file_order += 1

    df = pd.concat(df_list, axis=0, ignore_index=True)
    df = df[df['Description'].isna()==False]
    df = df.reset_index().drop(columns=['index'])

    file_order_list = df['File order']
    descriptions = df['Description']
    desc_list = list(descriptions)

    ### contains the string name for each skill
    skill_names = ['Python', 'SQL',' R ','Java', ' C ', 'C++', 'C#',\
                  'Hadoop', 'Spark', 'Tableau', 'Power BI', 'Sas', 'Excel', 'VBA', 'Macros', 'PowerPoint',\
                  'Microsoft Word', 'D3.js', 'Matlab', 'Jasper', 'Cognos', 'ggplot2', 'Dash',\
                  'Jupyter','Matplotlib','Nltk','Scikit-learn','TensorFlow','Weka','Google Analytics',\
                  'JavaScript','PHP','Ruby','Swift','Bloomberg','Reuters','SPSS','TypeScript','Perl']

    certifications = ['CSC','CFA','CPA','MBA','CFP','IFC','PFSA','FP I','FP II','AFP',\
                      'BCO','PLM','BMF','PTM','BDPM','WME','LIC',\
                      'IATP','IMT','AIS','NEC','CRM','ADMS','DFC','DFOL',\
                      'FLC','OLC','OPSC','CCSE','TTC','ETS','BMAP','ETFM']
    ### creating a dictionary that holds lists with variable names pertaining to each value in the above skill_names list ###
    skill_lists = {skill_names[i]: [] for i in range(len(skill_names))}
    certif_lists = {certifications[i]: [] for i in range(len(certifications))}
    for i in range(len(descriptions)):
        for j in range(len(skill_names)):
            if desc_list[i].__contains__(skill_names[j]) or \
            desc_list[i].__contains__(skill_names[j].upper()) or \
            desc_list[i].__contains__(skill_names[j].lower()) or \
            desc_list[i].__contains__(' ' + skill_names[j] + ' '):
                skill_lists[skill_names[j]].append(1)
            else:
                skill_lists[skill_names[j]].append(0)

    for i in range(len(descriptions)):
        for j in range(len(certifications)):
            if desc_list[i].__contains__(certifications[j]) or \
            desc_list[i].__contains__(' ' + certifications[j] + ' '):
                certif_lists[certifications[j]].append(1)
            else:
                certif_lists[certifications[j]].append(0)

    skill_df = pd.DataFrame(skill_lists)
    skill_df['File order'] = file_order_list
    certif_df = pd.DataFrame(certif_lists)
    certif_df['File order'] = file_order_list

    skill_counts = {skill_names[i]: [] for i in range(len(skill_names))}
    certif_counts = {certifications[i]: [] for i in range(len(certifications))}

    for i in range(len(skill_counts)):
        for j in range(len(all_files)):
            skill_counts[skill_names[i]].append((skill_df[(skill_df[skill_names[i]] == 1) & (skill_df['File order'] == j)].count())[0])

    for i in range(len(certif_counts)):
        for j in range(len(all_files)):
            certif_counts[certifications[i]].append((certif_df[(certif_df[certifications[i]] == 1) & (certif_df['File order'] == j)].count())[0])


    graph_sort_options = ['Base Chart','Highest Percentage Change','Highest Average Value']
    graph_type_options = ['Line Chart', 'Bar Chart']
    skill_or_certificaiton = ['Skills','Certifications']


    skill_pct_chg_list = []
    skill_avg_val_list = []
    for i in skill_df.columns[:-1]:
        try:
            skill_pct_chg_list.append([i,(sum((skill_df[i] == 1) & (skill_df['File order'] == 13)) - sum((skill_df[i] == 1) & (skill_df['File order'] == 0)))/(sum((skill_df[i] == 1) & (skill_df['File order'] == 0)))])
            skill_avg_val_list.append(sum(skill_counts[i])/len(all_files))
        except ZeroDivisionError as Error:
            pass
    skill_roc_df = pd.DataFrame(skill_pct_chg_list, columns=['Skill','Skill % Change'])
    skill_roc_df['Skill Avg Val'] = skill_avg_val_list
    skill_roc_df['% Change Skill'] = skill_roc_df['Skill % Change']*100
    skill_roc_df['% Skill Val'] = skill_roc_df['Skill Avg Val']/len(skill_roc_df['Skill'])
    skill_pct_chg_df = skill_roc_df.sort_values(by=['% Change Skill'],ascending=False)[:5]
    skill_val_chg_df = skill_roc_df.sort_values(by=['Skill Avg Val'],ascending=False)[:5]
    skill_roc_df = skill_roc_df.drop(columns=['Skill % Change'])

    certif_pct_chg_list = []
    certif_avg_val_list = []
    for i in certif_df.columns[:-1]:
        try:
            certif_pct_chg_list.append([i,(sum((certif_df[i] == 1) & (certif_df['File order'] == 13)) - sum((certif_df[i] == 1) & (certif_df['File order'] == 0)))/(sum((certif_df[i] == 1) & (certif_df['File order'] == 0)))])
            certif_avg_val_list.append(sum(certif_counts[i])/len(all_files))
        except ZeroDivisionError as Error:
            pass
    certif_roc_df = pd.DataFrame(certif_pct_chg_list, columns=['Certification','Certification % Change'])
    certif_roc_df['Certification Avg Val'] = certif_avg_val_list
    certif_roc_df['% Change Certification'] = certif_roc_df['Certification % Change']*100
    certif_roc_df['% Certification Val'] = certif_roc_df['Certification Avg Val']/len(certif_roc_df['Certification'])
    certif_pct_chg_df = certif_roc_df.sort_values(by=['% Change Certification'],ascending=False)[:5]
    certif_val_chg_df = certif_roc_df.sort_values(by=['Certification Avg Val'],ascending=False)[:5]
    certif_roc_df = certif_roc_df.drop(columns=['Certification % Change'])


    rate_chg_df = pd.concat([skill_roc_df,certif_roc_df],axis=1)
    rate_chg_df.columns = ['Name','Avg. Value','% Change', 'Proportion of total', 'Name C',\
          'Avg. Value C', '% Change C', 'Proportion of total C']
    rate_chg_df.round({'Avg. Value': 2, '% Change': 2, 'Proportion of total':2,
                       'Avg. Value C': 2, '% Change C': 2, 'Proportion of total C':2,})





    name_list = []
    for i,j in enumerate(rate_chg_df.columns):
        if i < 4:
            name_list.append({"name": j, "id": j})
        else:
            name_list.append({"name": j, "id": j})

    color_list = ['rgb(31, 119, 180)',
                 'rgb(255, 127, 14)',
                 'rgb(44, 160, 44)',
                 'rgb(214, 39, 40)',
                 'rgb(148, 103, 189)',
                 'rgb(140, 86, 75)',
                 'rgb(227, 119, 194)',
                 'rgb(127, 127, 127)',
                 'rgb(188, 189, 34)',
                 'rgb(23, 190, 207)']


    # Initialize base values
    base_skill_values = skill_names[0:3]
    base_df = df.merge(skill_df,left_index=True, right_index=True).drop(columns=['Link','File order_x','File order_y'])
    for i in range(len(base_skill_values)):
        base_df = base_df[base_df[base_skill_values[i]]==1]
    # Removes all columns that aren't specified in the skills checklist
    base_df =  base_df[list(base_df.columns[0:4])].reset_index().drop(columns='index')
    print(base_df.head(1))
    print('\n')

    def create_initial_graph(base_skill_values):
        traces = []

        for i in range(len(base_skill_values)):
            traces.append(go.Scatter(x = date_range,
                               y = skill_counts[base_skill_values[i]],
                               line=go.scatter.Line(
                                shape="spline",
                                smoothing = 1.0),
                               name = base_skill_values[i]))

        data = traces
        layout = go.Layout(
                      title='Skills mentioned in job postings (August to December)',hovermode='closest',
                      showlegend = True,
                      legend= {'itemsizing': 'constant'},
                      xaxis_title="Weekly scrape of Indeed job postings",
                      yaxis_title="# of mentions",
                      height = 400,
                      font=dict(
                        family="Courier New, monospace",
                        size=11,
                        color="#7f7f7f"),
                      margin=go.layout.Margin(
                          l=3,
                          r=3,
                          b=60,
                          t=50,
                          pad=1
                          ),
                      )

        fig = go.Figure(data=data,layout=layout)


        return fig


    base_skill_bar_vals = skill_names[:]
    def initial_bar_chart(base_skill_bar_vals):
        bar_width = 0.5

        traces = []
        for j in range(len(base_skill_bar_vals)):
            traces.append(go.Bar(
               x = [list(skill_counts.keys())[j]],
               y = [np.mean(skill_counts[base_skill_bar_vals[j]])],
               width=[bar_width],
               name = list(skill_counts.keys())[j],
               marker_color= color_list[1],
               ))

        data = traces

        layout = go.Layout(
          title='Skills Average Value',
          hovermode='closest',
          showlegend=False, legend= {'itemsizing': 'constant'},
          height = 225,
          font=dict(
            family="Courier New, monospace",
            size=11,
            color="#7f7f7f"),
          xaxis = {'automargin': True, 'title': 'Skill'},
          yaxis = {'automargin': True, 'title': 'Count'},
          margin=go.layout.Margin(
              l=2,
              r=2,
              b=90,
              t=30,
              pad=1
              ),
          )

        fig = go.Figure(data=data,layout=layout)


        return fig



                    #### Tab Two: School Semester Assessment ####


    ##############################################################################################
                             #### Part Two: Dash Layout ####
    ##############################################################################################





    date_range = [i for i in range(len(all_files))]

    with server.app_context(), server.test_request_context():
        layout_dash = r"C:\Users\David\Documents\Ideas\Personal website\portfoliowebsite\templates\jobs_app.html.j2"
        with open(layout_dash, "r") as f:
            html_body = render_template_string(f.read())
        comments_to_replace = ("metas", "title", "favicon", "css", "app_entry", "config", "scripts", "renderer")
        for comment in comments_to_replace:
            html_body = html_body.replace(f"<!-- {comment} -->", "{%" + comment + "%}")

        jobs_app.index_string = html_body


    jobs_app.layout = html.Div([
    html.Div([
        html.H1('Overview', style={'marginLeft':20, 'marginTop':20}),
        html.P("Job searches can be long and tedious processes. To find the right employment match, job seekers currently\
        need to read each individual job posting to see if the position is a right fit. This is a necessary part of the process\
        for all types of jobs, but for technical positions which list specific skills, I believe the process can be made more efficient\
        by allowing job seekers to list the specific set of skills they hold, and then sending them jobs that provide a good match.",\
        style={'marginLeft':20,'marginRight':20}),
        html.P("The 'Skills and Certifications' dashboard (tab 1 below) provides an interactive presentation\
        of how skill keywords mentioned in 'Analyst' job postings changed over time. Data was collected from Indeed.com via web\
        scraping on a weekly basis from August 2019 to December 2019.",style={'marginLeft':20,'marginRight':20}),
        html.A('Link to Github repository.', id='Github-link', href="https://github.com/DavidConradMcD/job-database-project",\
        style={'marginLeft':20, 'marginBottom':40}),
    ],className="row",style={'backgroundColor':'#DEDEDE',
            'width':'85%',
            'marginLeft':'5px',
            'marginRight':'5px',
            'borderRadius': '5px',
            'marginBottom':20,
            'paddingBottom':20,
            'display':'inline-block'}),

        # Main app
        html.H2('Job Postings Dashboard',
                style={
                    'marginLeft':'5px'
                }),
        dcc.Tabs(id="tabs-example", value='tab-1-example',
                 children=[
                    dcc.Tab(label='Skills and Certifications', value='tab-1-example',
                            className='custom-tab',
                            selected_className='custom-tab--selected'),
                    dcc.Tab(label='Filter Database', value='tab-2-example',
                            className='custom-tab',
                            selected_className='custom-tab--selected'),
        ],style={
            'width':'85%',
            'marginLeft':'5px'
        }),
        html.Div(id='tabs-content-example')
    ], style = {
        'marginLeft':'10%',
    })
    @jobs_app.callback(Output('tabs-content-example', 'children'),
                  [Input('tabs-example', 'value')])
    def render_content(tab):
        if tab == 'tab-1-example':
            return html.Div([

                            #upper-main Div
                            html.Div([

                                #dropdowns and checklists
                                html.Div([

                                    html.Div([

                                        html.H6('Choose analytical skills',
                                                style={'marginTop':'3px',
                                                'marginBottom':'2px',}),
                                        dcc.Checklist(id='skills-checklist',
                                            #options=[{'label': x, 'value': x} for x in skill_names],
                                            value=[x for x in skill_names[:3]],
                                            style={'marginTop':'0%',
                                                   'verticalAlign':'left',
                                                   'textAlign':'left'},
                                                    labelStyle={'display':'inline-block'}),
                                    ],className="two columns",
                                         style={
                                            'height':'320px',
                                            'width':'90%',
                                            'borderWidth': '1px',
                                            'borderStyle': 'solid',
                                            'borderRadius': '5px',
                                            'marginTop':'5px',
                                            'marginLeft':'5%',
                                            #'marginRight':'1%',
                                            'paddingLeft':'5px',
                                            'marginBottom':'10px',
                                            'textAlign':'center',
                                            'backgroundColor':'white',
                                            #'background-image':'linear-gradient(rgb(162, 242, 242), rgb(96, 221, 252))',
                                            'box-shadow':'2px 2px 5px 0.1px rgba(0, 0, 0, 0.4)'}),

                                    html.Div([

                                        html.H6('Choose Certifications',
                                                style={'marginTop':'3px',
                                                'marginBottom':'2px',}),

                                        dcc.Checklist(id='certif-checklist',
                                            #'white-space': 'nowrap',
                                            #'overflow': 'scroll',


                                            value=[x for x in certifications[:3]],
                                            style={'marginTop':'0%',
                                                   'verticalAlign':'left',
                                                   'textAlign':'left',
                                                   'text-overflow': 'ellipsis',},
                                                    labelStyle={'display':'inline-block'})

                                    ],className="two columns",
                                         style={
                                            'height':'220px',
                                            'width':'90%',
                                            'borderWidth': '1px',
                                            'borderStyle': 'solid',
                                            'borderRadius': '5px',
                                            'marginTop':'10px',
                                            'marginLeft':'5%',
                                            #'marginRight':'1%',
                                            'paddingLeft':'5px',
                                            'marginBottom':'5px',
                                            'textAlign':'center',
                                            'backgroundColor':'white',
                                            #'background-image':'linear-gradient(rgb(162, 242, 242), rgb(96, 221, 252))',
                                            'box-shadow':'2px 2px 5px 0.1px rgba(0, 0, 0, 0.4)'}),

                            ],className="six columns",
                             style={'width':'33%',
                                'height':'515px',
                                'borderRadius': '5px',
                                'marginTop':'8px',
                                'marginLeft':'0.1%',
                                'marginRight':'0.5%',
                                'marginBottom':'15px',
                                'textAlign':'center',
                                'backgroundColor':'white',
                                #'background-image':'linear-gradient(rgb(162, 242, 242), rgb(96, 221, 252))',
                                #'box-shadow':'0px 3px 5px 6px rgba(0, 0, 0, 0.4)'
                                }),

                                #container for graphs (upper-main Div)
                                html.Div([

                                    html.Div([

                                        html.Div([
                                            html.H6('Display Skills or Certifications',
                                                          style={'marginTop':'0.1px',
                                                          'marginBottom':'5px',
                                                          'padding':'1px',
                                                          'font-size': '1em',
                                                          #'overflowX':'scroll',
                                                            }),
                                            dcc.Dropdown(id='skill-or-cert-dropdown',
                                                         options=[{'label':x,'value':x} for x in skill_or_certificaiton],
                                                         value = skill_or_certificaiton[0],
                                                        style={
                                                            "margin-right": "0.1%",
                                                             "margin-left": "0%",
                                                             "marginBottom": "0%",
                                                             #'width':'100%',
                                                             'height':'39.5px'}),
                                                    ],
                                                         style={
                                                            'width':'40%',
                                                            'height':'60px',
                                                            'marginTop':'3px',
                                                            'marginLeft':'5px',
                                                            #'marginRight':'5px',
                                                            'marginBottom':'30px',
                                                            'textAlign':'center',
                                                            }),

                                        html.Div([
                                            html.H6('Change Graph display',
                                                          style={'marginTop':'0.1px',
                                                          'marginBottom':'5px',
                                                          'font-size': '1em'
                                                            }),
                                            dcc.Dropdown(id='graph-sort-dropdown',
                                                         options=[{'label':x,'value':x} for x in graph_sort_options],
                                                         value = graph_sort_options[0],
                                                        style={
                                                            "margin-right": "0%",
                                                             "margin-left": "0.1%",
                                                             "marginBottom": "0.1%",
                                                             #'width':'100%',
                                                             'height':'39.5px',
                                                             #'white-space': 'nowrap',
                                                             #'overflow': 'scroll',
                                                             #'text-overflow': 'ellipsis'
                                                             })
                                                    ],
                                                     style={
                                                        'width':'40%',
                                                        'height':'60px',
                                                        'marginTop':'3px',
                                                        'marginLeft':'5px',
                                                        #'marginRight':'5px',
                                                        'marginBottom':'0.1px',
                                                        'textAlign':'center',
                                                        }),

                                    ],className="two columns",
                                         style={'width':'100%',
                                            'height':'120px',
                                            'marginTop':'5px',
                                            'marginLeft':'5px',
                                            'marginRight':'5px',
                                            'marginBottom':'5px',
                                            'textAlign':'center',
                                            'backgroundColor':'white',
                                            #'background-image':'linear-gradient(rgb(162, 242, 242), rgb(96, 221, 252))',
                                            #'box-shadow':'0px 3px 5px 6px rgba(0, 0, 0, 0.4)'
                                            }),

                                    #graph one
                                    html.Div([
                                        dcc.Graph(id='skills-time-graph',
                                                  figure = create_initial_graph(base_skill_values)

                                    )],className="two columns",
                                         style={#'width':'100%',
                                            'height':'430px',
                                            'borderWidth': '1px',
                                            'borderStyle': 'solid',
                                            'borderRadius': '5px',
                                            'marginTop':'50px',
                                            'marginLeft':'5px',
                                            'marginRight':'5px',
                                            'marginBottom':'200px',
                                            'paddingLeft':'10px',
                                            'paddingRight':'10px',
                                            #'overflowX': 'scroll',
                                            'textAlign':'center',
                                            'backgroundColor':'white',
                                            #'background-image':'linear-gradient(rgb(162, 242, 242), rgb(96, 221, 252))',
                                            'box-shadow':'2px 2px 10px 0.1px rgba(0, 0, 0, 0.4)'}),


                                ],className="two columns",
                                     style={'width':'65%',
                                        'height':'500px',
                                        'borderRadius': '5px',
                                        'marginTop':'8px',
                                        'marginLeft':'0.5%',
                                        'marginRight':'0.5%',
                                        'marginBottom':'20px',
                                        'textAlign':'center',
                                        'backgroundColor':'white',
                                        #'background-image':'linear-gradient(rgb(162, 242, 242), rgb(96, 221, 252))',
                                        #'box-shadow':'0px 3px 5px 6px rgba(0, 0, 0, 0.4)'
                                        }),



                                    html.Div([dcc.Graph(id='bar-chart',
                                                        figure = initial_bar_chart(base_skill_bar_vals))
                                        ],className="two columns",
                                             style={'width':'97%',
                                                'height':'320px',
                                                'borderWidth': '1px',
                                                'borderStyle': 'solid',
                                                'borderRadius': '5px',
                                                'marginTop':'70px',
                                                'marginLeft':'1.5%',
                                                'marginRight':'5px',
                                                'marginBottom':'20px',
                                                'paddingLeft':'5px',
                                                'paddingRight':'5px',
                                                'paddingTop':'5px',
                                                'textAlign':'center',
                                                'backgroundColor':'white',
                                                #'background-image':'linear-gradient(rgb(162, 242, 242), rgb(96, 221, 252))',
                                                'box-shadow':'3px 3px 10px 0.1px rgba(0, 0, 0, 0.4)'}),

                                    #Data Table
                                    html.Div([
                                        html.Div([
                                            html.H6('Explore the Dataset',
                                                    style={'marginTop':'3px',
                                                    'marginBottom':'3px',}),
                                            dcc.Markdown(id='selected-skills'),
                                        ],className='row', style={'marginLeft':'1%'}),

                                        html.Div([
                                            dash_table.DataTable(
                                            id = 'table',
                                            data = base_df.head(5).to_dict('records'),
                                            #columns = ['Job Title', 'Company', 'Location', 'Description', 'Python', 'SQL', ' R '],
                                            columns = [{"name":i, "id":i} for i in base_df.head(5).columns],

                                            #data=rate_chg_df.to_dict('records'),
                                            #columns=name_list,
                                            style_cell={'textAlign': 'left',
                                                        'textOverflow': 'ellipsis',
                                                        'height': '30px',
                                                        'minWidth': '10px', 'maxWidth': '90px',
                                                        'whiteSpace': 'normal',
                                                        'font-family':'calibri'},

                                             style_table={
                                                'maxHeight': '400px',
                                                'marginBottom':'5px',
                                                },
                                             style_cell_conditional=[
                                                    {'if': {'column_id': 'Skills'},
                                                        'textAlign': 'center'},
                                                    {'if': {'column_id':'Name'},
                                                    'width':'10px'},
                                                    {'if': {'column_id':'Description'},
                                                    'width':'30%'},
                                                    ],
                                             row_selectable="single",
                                             row_deletable=False,
                                             selected_columns=[],
                                             selected_rows=[],
                                             style_as_list_view=True,
                                             merge_duplicate_headers=True,
                                             css=[{
                                             'selector': '.dash-cell div.dash-cell-value',
                                             'rule': '''display: inline;
                                                        white-space: inherit;
                                                        overflow: inherit;
                                                        text-overflow: inherit;
                                                        line-height: 30px;
                                                        max-height: 30px; min-height: 30px; height: 30px;
                                                        display: block;
                                                        overflow-y: hidden;
                                                        '''

                                             }],
                                             editable=False,
                                             sort_action="native",
                                             sort_mode="multi",
                                             fixed_rows={ 'headers': True, 'data': 0 }),
                                        ],className='row', style={'display':'inline-block',
                                                                'marginLeft':'1%',
                                                                'width':'98%'}),




                                    ],className="row",
                                         style={'width':'97%',
                                            'height':'550px',
                                            'borderWidth': '1px',
                                            'borderStyle': 'solid',
                                            'borderRadius': '5px',
                                            'marginTop':'20px',
                                            'marginLeft':'1.5%',
                                            'marginRight':'0%',
                                            'marginBottom':'20px',
                                            'textAlign':'center',
                                            #'backgroundColor':'rgb(107, 213, 242)',
                                            #'background-image':'linear-gradient(rgb(162, 242, 242), rgb(96, 221, 252))',
                                            'box-shadow':'3px 3px 10px 0.1px rgba(0, 0, 0, 0.4)'}),

                                # Section to show job description for selected jobs
                                html.Div([
                                    html.Div([
                                        html.Div([
                                            html.Div([
                                                html.H3("Job Title: ")
                                            ],className="two columns", style={'display':'inline-block',
                                                                            'marginLeft':15,
                                                                            'marginTop':20}),
                                            html.Div([
                                                html.H3("", id="selected-job-title"),
                                            ],className="two columns",style={'display':'inline-block',
                                                                            'marginLeft':10,
                                                                            'marginTop':20}),

                                        ],className="row"),
                                        html.Div([
                                            html.Div([
                                                html.H3("Company: ")
                                            ],className="two columns",style={'display':'inline-block',
                                                                            'marginLeft':15}),
                                            html.Div([
                                                html.H3("", id="selected-company"),
                                            ],className="two columns",style={'display':'inline-block',
                                                                            'marginLeft':10}),

                                        ],className="row"),
                                        html.Div([
                                            html.Div([
                                                html.H3("Location: ")
                                            ],className="two columns",style={'display':'inline-block',
                                                                            'marginLeft':15}),
                                            html.Div([
                                                html.H3("", id="selected-location"),
                                            ],className="two columns",style={'display':'inline-block',
                                                                            'marginLeft':10}),

                                        ],className="row"),



                                    ],className="row", style={'display':'inline-block',
                                                            'width':'90%',
                                                            'height':150,
                                                            'marginTop':0,
                                                            'marginLeft':30,
                                                            'marginBottom':0}),
                                    html.Div([
                                        html.H3("Description"),
                                        dcc.Markdown(id='job-description')

                                    ],className="row", style={'display':'inline-block',
                                                            'marginTop':0,
                                                            'marginBottom':10,
                                                            'marginLeft':30,
                                                            'marginRight':30,
                                                            'height':570,
                                                            'overflow-y':'scroll',
                                                            'textAlign':'left',
                                                            'width':'98%'}),

                                ],className="row",
                                     style={'width':'97%',
                                        'height':'800px',
                                        'borderWidth': '1px',
                                        'borderStyle': 'solid',
                                        'borderRadius': '5px',
                                        'marginTop':0,
                                        'marginLeft':'1.5%',
                                        'marginRight':'0%',
                                        'marginBottom':0,
                                        'textAlign':'center',
                                        #'backgroundColor':'rgb(107, 213, 242)',
                                        #'background-image':'linear-gradient(rgb(162, 242, 242), rgb(96, 221, 252))',
                                        'box-shadow':'3px 3px 10px 0.1px rgba(0, 0, 0, 0.4)'}),


                            ],className="row",
                                     style={'backgroundColor':'white',
                                            'height':'2500px',
                                            'width':'99%',
                                            'marginLeft':'1%',
                                            'marginRight':'5px',
                                            'marginBottom':'50px',
                                            'marginTop':'20px'}),


                #main Div
                ],className="row",style={'backgroundColor':'white',
                        'width':'85%',
                        'height':'100%',
                        'borderWidth': '1px',
                        'borderStyle': 'solid',
                        'borderRadius': '5px',
                        'marginLeft':'5px',
                        'marginRight':'5px',
                        'marginBottom':50})


        #Tab two layout
        elif tab == 'tab-2-example':
            print(skill_names)
            return html.Div([
                html.H6('Filter Database',
                        style={'marginTop':'3px',
                        'marginBottom':'3px',}),

                        ],className="two columns",
                         style={'width':'85%',
                            'height':'650px',
                            'borderWidth': '1px',
                            'borderStyle': 'solid',
                            'borderRadius': '5px',
                            'marginTop':'2%',
                            'marginLeft':'0.5%',
                            'marginRight':'0.5%',
                            'marginBottom':'0.5%',
                            'textAlign':'center',
                            'backgroundColor':'white',
                            #'background-image':'linear-gradient(rgb(162, 242, 242), rgb(96, 221, 252))',
                            'box-shadow':'3px 3px 10px 0.1px rgba(0, 0, 0, 0.4)'}),










    ##############################################################################################
                               #### Part Three: App Callbacks ####
    ##############################################################################################




    @jobs_app.callback(Output('table','data'),
                        [Input('skills-checklist','value')])
    def update_table(skill_values):
        # Merge the jobs df and skills df
        main_df = df.merge(skill_df,left_index=True, right_index=True).drop(columns=['Link','File order_x','File order_y'])
        for i in range(len(skill_values)):
            table_df = main_df[main_df[skill_values[i]]==1]
        # Removes all columns that aren't specified in the skills checklist
        table_df =  table_df[list(table_df.columns[0:4])]
        return table_df.reset_index().drop(columns='index').to_dict('records')

    @jobs_app.callback(Output('selected-job-title','children'),
                        Output('selected-company','children'),
                        Output('selected-location','children'),
                        Output('job-description','children'),
                        [Input("table","columns"),
                        Input('table','selected_rows'),
                        Input('skills-checklist','value')])
    def post_job_description(columns,row,skill_values):
        #main_df = df.merge(skill_df,left_index=True, right_index=True).drop(columns=['Link','File order_x','File order_y'])
        print("triggered")
        #selected_rows = [columns[i] for i in selected_rows]
        print(row)

        dff = pd.DataFrame(update_table(skill_values))
        print(type(dff.iloc[row]['Description']))
        return dff.iloc[row]['Job Title'], dff.iloc[row]['Company'], dff.iloc[row]['Location'], dff.iloc[row]['Description']

    # Retrieve selected skills from skills dropdown
    @jobs_app.callback(Output('selected-skills','children'),
                        [Input('skills-checklist','value')])
    def show_selected_skills(skill_values):
        selected_skills = []
        for i in range(len(skill_values)):
            selected_skills.append(skill_values[i])
        return ''' {}'''.format(selected_skills), selected_skills

    @jobs_app.callback(Output('skills-time-graph','figure'),
                  [Input('skills-checklist','value'),
                   Input('certif-checklist','value')])
    def callback_initial_graph(skill_values,certif_values):
        traces = []

        for i in range(len(skill_values)):
            traces.append(go.Scatter(x = date_range,
                               y = skill_counts[skill_values[i]],
                               line=go.scatter.Line(
                                shape="spline",
                                smoothing = 1.0),
                               name = skill_values[i]))
        for j in range(len(certif_values)):
            traces.append(go.Scatter(x = date_range,
                               y = certif_counts[certif_values[j]],
                               line=go.scatter.Line(
                                shape="spline",
                                smoothing = 1.0),
                               name = certif_values[j]))

        data = traces
        layout = go.Layout(
                      title='Skills/Certifications in job postings (August to December)',hovermode='closest',
                      showlegend=True, legend= {'itemsizing': 'constant'},
                      xaxis_title="Weekly scrape of Indeed job postings",
                      yaxis_title="# of mentions",
                      height = 425,
                      font=dict(
                        family="Courier New, monospace",
                        size=11,
                        color="#7f7f7f"),
                      margin=go.layout.Margin(
                          l=5,
                          r=5,
                          b=60,
                          t=50,
                          pad=2
                          ),
                      )

        fig = go.Figure(data=data,layout=layout)


        return fig

    '''
    id='graph-sort-dropdown',
                 options=[{'label':x,'value':x} for x in graph_sort_options],
                 value = graph_sort_options[0],
    '''

    @jobs_app.callback(Output('bar-chart', 'figure'),
                  [Input('skills-checklist','options'),
                   Input('certif-checklist','options'),
                   Input('skill-or-cert-dropdown','value')])
    def update_graph(data, cols, skill_or_cert):
        print(skill_or_cert)
        bar_width = 0.9
        traces = []
        x_values = []
        y_values = []

        if skill_or_cert == skill_or_certificaiton[0]:
            for j in range(len(skill_names)):
                x_values.append(list(skill_counts.keys())[j]),
                y_values.append(np.mean(skill_counts[skill_names[j]])),

            test = pd.DataFrame(zip(y_values, x_values))
            test.columns = ['value','name']
            test = test.sort_values(by = 'value', ascending=False)
            test = test.reset_index()

            traces.append(
                    go.Bar(
                       x = test['name'],
                       y = test[test['value'] > 2]['value'],
                       width=[bar_width],
                       ))


            layout = go.Layout(
              title='Average Value of Skill Per Weekly Job Scrape',
              hovermode='closest',
              showlegend=False, legend= {'itemsizing': 'constant'},
              height = 300,
              font=dict(
                family="Courier New, monospace",
                size=11,
                color="#7f7f7f"),
              xaxis = {'automargin': True, 'title': 'Skill',
                       },
              yaxis = {'automargin': True, 'title': 'Count'},
              margin=go.layout.Margin(
                  l=2,
                  r=2,
                  b=90,
                  t=30,
                  pad=1
                  ),
              )

            data = traces


        else:
            for j in range(len(certifications)):
                x_values.append(list(certif_counts.keys())[j]),
                y_values.append(np.mean(certif_counts[certifications[j]])),

            test = pd.DataFrame(zip(y_values, x_values))
            test.columns = ['value','name']
            test = test.sort_values(by = 'value', ascending=False)
            test = test.reset_index()

            traces.append(
                    go.Bar(
                       x = test['name'],
                       y = test[test['value'] > 2]['value'],
                       width=[bar_width],
                       ))

            layout = go.Layout(
              title='Certification Average Value',
              hovermode='closest',
              showlegend=False, legend= {'itemsizing': 'constant'},
              height = 300,
              font=dict(
                family="Courier New, monospace",
                size=11,
                color="#7f7f7f"),
              xaxis = {'automargin': True, 'title': 'Certification'},
              yaxis = {'automargin': True, 'title': 'Count'},
              margin=go.layout.Margin(
                  l=5,
                  r=5,
                  b=90,
                  t=30,
                  pad=1
                  ),
              )

            data = traces

        fig = go.Figure(data=data,layout=layout)

        return fig

    '''
    #Dropdown One
    @jobs_app.callback([Output('skills-checklist','options'),
                  Output('certif-checklist','options')],
                  [Input('skill-or-cert-dropdown','value'),
                   Input('change-graph-dropdown','value')])
    @cache.memoize
    def line_or_bar(sc_dropdown,line_bar_val):

        if sc_dropdown == skill_or_certificaiton[0]:
            skill_checklist_values = [i for i in skill_names[:3]]
            certif_checklist_values = []

        if sc_dropdown == skill_or_certificaiton[1]:
            skill_checklist_values = []
            certif_checklist_values = [i for i in certifications[:3]]


        return skill_checklist_values, certif_checklist_values
    '''

    #Dropdown Two (part a)
    @jobs_app.callback([Output('skills-checklist','options'),
                  Output('certif-checklist','options')],
                  [Input('skill-or-cert-dropdown','value')])
    def choosing_skills_or_certifs(sc_dropdown):

        if sc_dropdown == skill_or_certificaiton[0]:
            skills_options = [{'label': x, 'value': x} for x in skill_names]
            certif_options = [{'label': x, 'value': x, 'disabled':True} for x in list(certifications)]

        else:
            skills_options = [{'label': x, 'value': x, 'disabled':True} for x in list(skill_names)]
            certif_options = [{'label': x, 'value': x} for x in certifications]


        return skills_options, certif_options

    #Dropdown Two (part b)
    @jobs_app.callback([Output('skills-checklist','value'),
                  Output('certif-checklist','value')],
                  [Input('skill-or-cert-dropdown','value'),
                   Input('graph-sort-dropdown','value'),])
    def selecting_chklist_vals(skill_cert_dropdown, sorting_dropdown):

        if skill_cert_dropdown == skill_or_certificaiton[0]:
            certif_value = [certifications[0]]
            if sorting_dropdown == graph_sort_options[0]:
                skills_value = [x for x in skill_names[:7]]

            if sorting_dropdown == graph_sort_options[1]:
                skills_value = [i for i in skill_pct_chg_df['Skill'][:7]]

            if sorting_dropdown == graph_sort_options[2]:
                skills_value = [i for i in skill_val_chg_df['Skill'][:7]]



        if skill_cert_dropdown == skill_or_certificaiton[1]:
            skills_value = [skill_names[0]]
            if sorting_dropdown == graph_sort_options[0]:
                certif_value = [i for i in certifications[:7]]

            if sorting_dropdown == graph_sort_options[1]:
                certif_value = [i for i in certif_pct_chg_df['Certification'][:7]]

            if sorting_dropdown == graph_sort_options[2]:
                certif_value = [i for i in certif_val_chg_df['Certification'][:7]]



        return skills_value, certif_value








    # Stop the stopwatch / counter
    #t1_stop = process_time()

    #print("Elapsed time:", t1_stop, t1_start)

    #print("Elapsed time during the whole program in seconds:",t1_stop-t1_start)

    return jobs_app.layout
