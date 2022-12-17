#!/usr/bin/env python
# coding: utf-8

# # General Preato Visualization Engine
# # 12/16/22
# # Shahzad Ansari 

# The `import testData as td` is just a module created to make test data to see how the engine works. comment it and remove the inputs called from it to use your own data. 

#     

# ## Loading Packages
#     

# In[ ]:


from dash import Dash, dcc, Input, Output,dash_table
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash
import plotly.graph_objects as go
import testData as td
import plotly.express as px
from dash import dash_table
import pandas as pd
import statistics


# # Load the data 
# 
# The engine expects specific input detailed below
# 
# 1. The number of dimensions in the Preato Frontier either 2 or 3 set to the `dim` variable  
# 2. The x,y and z axis names if aplicable stord in the `xlab` `ylab` and `zlab` variable.
# 3. The title of the overall dashboard stored in `title` 
# 4. The center of your map in lat long coordinate format stored into `cLat` and `cLong` variables.
# 5. A dataframe contaning the information about the cost etc had no solution been taken. `noSolution`
# 6. The dataframe containing the `x`,`y` and `z` points (if its 3D graph) that will be used to plot on the dynamic graph along with a variable for an id called `SolId` called `preatoFrontier`
# 7. A dataframe containing the coordinate data in the form of lat and long points for the buildings or point of interests on the map 
# 8. A list of size n where n is the amount of points on the frontier. Each element of the list is a dataframe containing a the coordinates along with the upgrade levels and solution ids 
# 9. A list of levels in ascending order with colors for each level. example shown in code. 
# 
# DF Schemas are given below, They are given for 3D. 
#     

# ### Example `noSolution` DataFrame
# 
# 
# | Column      | Description |Data Type|
# | ----------- | ----------- |---------|
# | `x`         | The x variable in this case cost of repair      |`int`|
# | `y`         | The y variable in this case time to  repair              |`int`|
# | `z`         | The z variable in this case population dislocation             |`int`|
# | `b`         | The b variable in this amount of buildings destroyed              |`int`|

# ### Example `preatoFrontier` DataFrame
# 
# 
# | Column      | Description |Data Type|
# | ----------- | ----------- |---------|
# | `x`         | The x variable in this case cost of repair      |`int`|
# | `y`         | The y variable in this case time to  repair              |`int`|
# | `z`         | The z variable in this case population dislocation             |`int`|
# | `SolId`         | A solution ID that can be used to link to the solution DF              |`int`|

# ### Example `coords` DataFrame
# 
# 
# | Column      | Description |Data Type|
# | ----------- | ----------- |---------|
# | `lat`         | The latitude      |`float`|
# | `long`         | The longitude              |`float`|
# 

# ### Example of an Element in the `solutions` List
# `solutions = [ df1,df2,df3...]`
# 
# `solutions[0] = `
# 
# | Column      | Description |Data Type|
# | ----------- | ----------- |---------|
# | `lat`         | The Latitude      |`float`|
# | `long`         | The Longitude              |`float`|
# | `upGrade`         | The Upgrade level for that specific building             |`int`|
# 

# In[ ]:


dim = 3
xlab = "Cost of repair"
ylab = "Time to repair"
zlab = "Population Dislocation"
title = "Preato Frontier for General Analysis - Place your title here"
cLat = td.cLat
cLong = td.cLong
noSolution = td.randomNoSolution(dim)
preatoFrontier= td.randomPreato(dim)
coords = td.coords
solutions = td.solutionList
levels = ['grey','blue','green','red']


# ## Mapbox Token
# you need to create a mapbox token api key and place it in here

# In[ ]:


mapbox_access_token = 'FILLYOURSIN'


# ## Setting up for 3D or 2D 

# In[ ]:


if dim == 3:
    stats_df = pd.DataFrame() # a data frame containing the statistical data on the preato forntier
    noSolution = noSolution.rename(columns={"x": xlab, "y": ylab,"z":zlab,"b":"Buildings"})
    # finding the max and min of each of the axis' in the forntier
    xmin = preatoFrontier['x'].min()
    ymin = preatoFrontier['y'].min()
    zmin = preatoFrontier['z'].min()
    xmax = preatoFrontier['x'].max()
    ymax = preatoFrontier['y'].max()
    zmax = preatoFrontier['z'].max()
    # finding the midpoint 
    xmid = (xmax-xmin)/2
    ymid = (ymax-ymin)/2
    zmid = (zmax-zmin)/2
    # Adding the information to the dataframe
    stats_df['Variable'] = [xlab,ylab,zlab]
    stats_df['minimum'] = [xmin,ymin,zmin]
    stats_df['midpoint'] = [xmid,ymid,zmid]
    stats_df['maximum'] = [xmax,ymax,zmax]
    # Getting the mean, Standard Deviation and Variance 
    stats_df['mean'] = [statistics.mean(preatoFrontier['x']),statistics.mean(preatoFrontier['y']),statistics.mean(preatoFrontier['z'])]
    stats_df['SD'] = [statistics.pstdev(preatoFrontier['x']),statistics.pstdev(preatoFrontier['y']),statistics.pstdev(preatoFrontier['z'])]
    stats_df['Variance'] = [statistics.pvariance(preatoFrontier['x']),statistics.pvariance(preatoFrontier['y']),statistics.pvariance(preatoFrontier['z'])]
    # creating an instance of the px figure for the forntier
    preatoFig = px.scatter_3d(preatoFrontier,x = "x",y = "y",z = "z")
    # creating the download button object 
    downloadButton = dcc.Download(id="download-dataframe-csv")
    # creating the dialouge object to warn user that they need to select data before it can download
    dialog = dcc.ConfirmDialog(id='confirm-danger-3d',message='You need to select a point on the Frontier before you can download')
else:
    stats_df = pd.DataFrame()# a data frame containing the statistical data on the preato forntier
    noSolution = noSolution.rename(columns={"x": xlab, "y": ylab,"b":"Buildings"})
     # finding the max and min of each of the axis' in the forntier
    xmin = preatoFrontier['x'].min()
    ymin = preatoFrontier['y'].min()
    xmax = preatoFrontier['x'].max()
    ymax = preatoFrontier['y'].max()
    # finding the midpoint 
    xmid = (xmax-xmin)/2
    ymid = (ymax-ymin)/2
     # Adding the information to the dataframe
    stats_df['Variable'] = [xlab,ylab]
    stats_df['minimum'] = [xmin,ymin,]
    stats_df['midpoint'] = [xmid,ymid]
    stats_df['maximum'] = [xmax,ymax]
    # Getting the mean, Standard Deviation and Variance 
    stats_df['mean'] = [statistics.mean(preatoFrontier['x']),statistics.mean(preatoFrontier['y'])]
    stats_df['SD'] = [statistics.pstdev(preatoFrontier['x']),statistics.pstdev(preatoFrontier['y'])]
    stats_df['Variance'] = [statistics.pvariance(preatoFrontier['x']),statistics.pvariance(preatoFrontier['y'])]
     # creating an instance of the px figure for the forntier
    preatoFig = px.scatter(preatoFrontier,x = "x",y = "y")
     # creating the download button object 
    downloadButton = dcc.Download(id = 'd2d')
    # creating the dialouge object to warn user that they need to select data before it can download
    dialog = dcc.ConfirmDialog(id='confirm-danger-2d',message='You need to select a point on the Frontier before you can download')  


# ## External sytle sheet
# The style sheet pulls formatting data for how the html and css will render.

# In[ ]:


external_stylesheets = [
    'https://codepen.io/chriddyp/pen/bWLwgP.css',
    {
        'href': 'https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css',
        'rel': 'stylesheet',
        'integrity': 'sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO',
        'crossorigin': 'anonymous'
    }
]
app = Dash(__name__,external_stylesheets=[dbc.themes.BOOTSTRAP],suppress_callback_exceptions=True)


# Creating the html objects and layout on screen. 

# In[ ]:


#--------------------------------------------------------------------------------
jumbotronStyle = {
    "position" : "fixed",
    "background-color":"#92a8d1"    
}
#--------------------------------------------------------------------------------
card = dbc.Card(
    [
        dbc.CardImg(
            src="assets/incore-logo.png",
            top=True,
            style={"opacity": 1},
        ),  
    ],
    style={
            "width": "10rem",
    },
)
#--------------------------------------------------------------------------------
button = html.Div([
    dbc.Row(
        dbc.Row(
            dbc.Col(
                [dbc.Button("Download Data", id="download button", className="me-2", n_clicks=0),
                 dialog,
                 downloadButton],
                width={"size": 3, "order": 1, "offset": 5},
                align="end"
             )
        )
    )  
]),
#--------------------------------------------------------------------------------
img = dbc.Card(
        [
                dbc.CardImg(
                src="assets/Figure_1.png",
                top=True,
                style={"opacity": 1},
            ),
            
        ]
    )
#--------------------------------------------------------------------------------
jumbotron = html.Div(
    dbc.Container(
        [
            dbc.Row([
                dbc.Col(
                    html.Div("General Visualization IN-CORE Dashbord App", className="display-5"),
                    width = "auto"
                ),
                dbc.Col(card,width = {"size": 3, "order": "last", "offset": 3})
            ],justify ="between"),
            html.Br(),
            html.Br(),
            html.Br(),
            html.P(
                "Data visualization dashboard for general data sets. Model created by general visualizations created by Shahzad Ansari",
                className="lead",
            ),
            html.Hr(className="my-2"),
        ],
        fluid=True,
        className="py-3",
    ),
    className="p-3 bg-dark text-light rounded-3",
)
#--------------------------------------------------------------------------------    


# ## Depending on if it is 3D or 2D format the HTML accordingly 

# In[ ]:


if dim == 3:
    ThreeContainer = html.Div(
        dbc.Container([
            html.Hr(),
            html.H3("{title}".format(title = title)), # title 
            # The preato Frontier 
            dcc.Graph(
                id='graph',
                figure = preatoFig
            ),
            html.P(id='3dresult'),
            dbc.Row([
                # Lables and sliders to filter down how much of each dimension you want to see
                html.P("{xlab} slider".format(xlab = xlab)),
                dcc.RangeSlider(
                        id='x-range-slider',
                        min = preatoFrontier['x'].min(),
                        max = preatoFrontier['x'].max(),
                        step =1,
                        tooltip={"placement": "bottom", "always_visible": True} , 
                        marks = None,
                        value=[preatoFrontier['x'].min(), preatoFrontier['x'].max()]
                        ),
                  html.P("{ylab} slider".format(ylab = ylab)),
                  dcc.RangeSlider(
                      id='y-range-slider',
                      min=preatoFrontier['y'].min(), max=preatoFrontier['y'].max(), step=1, tooltip={"placement": "bottom", "always_visible": True},
                      marks =None,
                      value=[preatoFrontier['y'].min(), preatoFrontier['y'].max()]
                  ),
                  html.P("{zlab} slider".format(zlab = zlab)),
                  dcc.RangeSlider(
                      id='z-range-slider',
                      min=preatoFrontier['z'].min(), max=preatoFrontier['z'].max(), step=1, tooltip={"placement": "bottom", "always_visible": True},
                      marks = None,
                      value=[preatoFrontier['z'].min(), preatoFrontier['z'].max()]
                  ),
            ]),
           
            # table showing your no solution data frame
            html.Hr(),
            dbc.Row([
                dbc.Col([
                    html.H6("Metrics with no mitigation steps taken"),
                    dbc.Table.from_dataframe(noSolution,striped=True,bordered=True,hover=True)
                       
                ]),
            ]),
            
            # Having chosen a point on the preato frontier, this object contains the data in a table
            dbc.Row([
                dbc.Col([
                    html.Div(id = 'metricsWBudget'), 
                ]),
            ]),  
        ])
    )
    
    # a graph object that will be used to display the map
    maps = html.Div(
            dbc.Container([
                    dbc.Row([
                        dbc.Col(
                           dcc.Graph(id='map'),
                           width = {"size": 6, "offset": -5},
                        ),
                    ])
    
                ])
        )
    # set this to main container
    MainContainer = ThreeContainer
    
else:
    TwoContainer = html.Div(
        dbc.Container([
            html.Hr(),
            html.P("{title}".format(title = title)), # the title
            # The figure for the preato frontier
            dcc.Graph(
                id='2dgraph',
                figure = preatoFig
            ),
            # The Titles of each slider and the sliders to filter the data
            html.P(id='2dresult'),
            dbc.Row([
                html.P("{xlab} slider".format(xlab = xlab)),
                dcc.RangeSlider(
                    id='x-range-slider',
                    min=preatoFrontier['x'].min(), max=preatoFrontier['x'].max(), step=1, tooltip={"placement": "bottom", "always_visible": True} ,
                    marks = None,
                    value=[preatoFrontier['x'].min(), preatoFrontier['x'].max()]
                ),
                  html.P("{ylab} slider".format(ylab = ylab)),
                  dcc.RangeSlider(
                      id='y-range-slider',
                      min=preatoFrontier['y'].min(), max=preatoFrontier['y'].max(), step=1, tooltip={"placement": "bottom", "always_visible": True},
                      marks = None,
                      value=[preatoFrontier['y'].min(), preatoFrontier['y'].max()]
                  ),
            ]),
           
            # Title and table for no solution data
            html.Hr(),
            dbc.Row([
                dbc.Col([
                    html.H6("Metrics with no mitigation steps taken"),
                    dbc.Table.from_dataframe(noSolution,striped=True,bordered=True,hover=True),
                    
                       
                ]),
            ]),
            # Table with solution data 
            dbc.Row([
                dbc.Col([
                    html.Div(id = 'metricsWBudget'), 
                      
                ]),
            ]),  
        ])
    )
    # html obj for the map 
    maps = html.Div(
            dbc.Container([
                    dbc.Row([
                        dbc.Col(
                           dcc.Graph(id='2dmap'),
                           width = {"size": 6, "offset": -5},
                        ),
                    ])
    
                ])
        
        )
    MainContainer = TwoContainer


# ## Setup the main display container

# In[ ]:


mainDisplay = dbc.Row([   
    dbc.Col([
        MainContainer
    ]),
    dbc.Col([
        maps,
        dbc.Row([
            dbc.Col(
                button,
                width={"size": 3, "order": 1, "offset": 0}
            ),
            dbc.Col(
                dcc.Checklist(
                id = 'checklist',
                options=levels,
                value=levels,
                inline = True),
                width={"size": 3, "order": 2, "offset": 6}
            ),
        ]),
        html.H6("Statistics over solution set"),
        dbc.Table.from_dataframe(stats_df,striped=True,bordered=True,hover=True),
        dbc.Row([
            html.H6("Resulting Dataset"),
            dbc.Table(id='container-button-basic',bordered = True,striped=True),
            dbc.Table(id='container-button-basic2')
        ])
    ]),
])
        


# # Callbacks

# ## Updating the 3d preato frontier 
# 
# ### Callback Input 
# * The slider values for the x range
# * The slider values for the y range
# * The slider values for the z range
# 
# ### Callback Output
# * The graph 

# In[ ]:


@app.callback(
    Output("graph", "figure"), 
    Input("x-range-slider", "value"),
    Input("y-range-slider", "value"),
    Input("z-range-slider", "value"))
def update_frontier_3d(x_range,y_range,z_range):
    # getting the ranges for each slider and filtering the dataframe 
    df = preatoFrontier 
    xlow, xhigh = x_range
    ylow, yhigh = y_range
    zlow, zhigh = z_range
    xmask = (df.x > xlow) & (df.x < xhigh)
    ymask = (df['y']> ylow) & (df['y'] < yhigh)
    zmask = (df['z']> zlow) & (df['z'] < zhigh)
    df = df[xmask]
    df = df[ymask]
    df = df[zmask]
        
    fig = go.Figure() # create a figure
  
    fig.add_trace(go.Scatter3d(
                x = df['x'], # x dim for scatter plot
                y = df['y'], # y dim for scatter plot
                z = df['z'], # z dim for scatter plot
                mode = 'markers', # type of points on scatterplot
                name = 'markers', # name of the points on the scatterplot
                # settings for the scatterplot
                marker=dict(
                    size=10, # The size of the markers are set by this 
                    color=df['x'], # set color to an array/list of desired values
                    colorscale='Viridis',   # choose a colorscale
                    opacity=0.8 # opacity 
                )
            ))
        
    # 3D Scatter plot 
    fig.update_layout(clickmode='event+select') #What happens when you click on a point
    # titles and dimensions
    fig.update_layout(scene = dict(
                        xaxis_title=xlab,
                        yaxis_title=ylab,
                        zaxis_title=zlab),
                        width=900,
                        height=900)

    return fig
 


# ## Updating the 2D preato frontier 
# 
# ### Callback Input 
# * The slider values for the x range
# * The slider values for the y range
# 
# ### Callback Output
# * The graph 

# In[ ]:


@app.callback(
    Output("2dgraph", "figure"), 
    Input("x-range-slider", "value"),
    Input("y-range-slider", "value"))
def update_frontier_2d(x_range,y_range):
    # Filtering the data frame using the x and y slider information
    df = preatoFrontier 
    xlow, xhigh = x_range
    ylow, yhigh = y_range
    xmask = (df.x > xlow) & (df.x < xhigh)
    ymask = (df['y']> ylow) & (df['y'] < yhigh)
    df = df[xmask]
    df = df[ymask]
    fig = go.Figure() # create a figure
  
    fig.add_trace(go.Scatter(
                x = df['x'], # x dim for scatter plot
                y = df['y'], # y dim for scatter plot
                mode = 'markers', # type of points on scatterplot
                name = 'markers', # name of the points on the scatterplot
                # settings for the scatterplot
                marker=dict(
                    size=10, # The size of the markers are set by this 
                    color=df['x'], # set color to an array/list of desired values
                    colorscale='Viridis',   # choose a colorscale
                    opacity=0.8 # opacity 
                )
            ))
        
    # 2D Scatter plot 
    fig.update_layout(clickmode='event+select') #What happens when you click on a point
    # titles and dimensions
    fig.update_layout(
                        xaxis_title= xlab,
                        yaxis_title= ylab,
                        width=900,
                        height=900
                    )

    return fig


# ## Displaying the Chosen point
# ### Input
# * The coordinates of the clicked point
# 
# ### Output 
# * The string returned to the text box

# In[ ]:


@app.callback(
    Output('3dresult','children'),
    Input('graph', 'clickData'))
def show_coords_3d(clickData):

        # if there has been no click return nothing 
        if clickData is None: 
            return ""
        else:
            xCoord = clickData['points'][0]['x'] 
            yCoord = clickData['points'][0]["y"]
            zCoord = clickData['points'][0]["z"]
             
            #add flush = True or it wont display the message.
            #print(f'Selected [{xCoord},{yCoord}]',flush=True)
           
            return "Selected : [{},{},{}]".format(xCoord,yCoord,zCoord,type1)
        


# ## for 2D 

# In[ ]:


@app.callback(
    Output('2dresult','children'),
    Input('2dgraph', 'clickData'))
def show_coords_2d(clickData):

        if clickData is None: 
            return ""
        else:
            xCoord = clickData['points'][0]['x'] 
            yCoord = clickData['points'][0]["y"]
           
            
            #add flush = True or it wont display the message.
            print(f'Selected [{xCoord},{yCoord}]',flush=True)
           
            return "Selected : [{},{}]".format(xCoord,yCoord)


# ## Updating the Maps

# ## Displaying the Chosen point
# ### Input
# * The coordinates of the clicked point
# * The Values of the checklist chosen - this being the 
# 
# ### Output 
# * The map with the poins and specified levels you want to be shown

# In[ ]:


@app.callback(
    Output('map','figure'),
    [Input('graph', 'clickData'),
    Input('checklist', 'value')])
def update_map_3d(clickData,checklist):
    # If no solution on the frontier has been chosen, Show the coordinates with no levels 
    if clickData is None:
        maps = go.Figure(go.Scattermapbox(
            lat=coords['lat'], # set lat and long
            lon=coords['long'],
            mode='markers', 
            marker =({'size':5.5}) # make markers size variable 
        ))
    
        # set up map layout
        maps.update_layout(
            autosize=True, # Autosize
            hovermode='closest', # Show info on the closest marker
            showlegend=True, # show legend of colors
            mapbox=dict(
                accesstoken=mapbox_access_token, # token
                bearing=0, # starting facing direction
                # starting location
                center=dict(
                    lat=td.cLat,
                    lon=td.cLong
                ),
                #angle and zoom
                pitch=0,
                zoom=12
            ),
            #height and width
            width=1000,
            height=1000
        )
        return maps
    else:
        # if a solution has been chosen 
        xCoord = int(clickData['points'][0]['x'])
        yCoord = int(clickData['points'][0]["y"])
        zCoord = int(clickData['points'][0]["z"])
        # get the row where this solution exists within the preatoFrontier DF 
        solutionRow = preatoFrontier.loc[(preatoFrontier['x'] == xCoord)&(preatoFrontier['y'] == yCoord)&(preatoFrontier['z'] == zCoord)]
        # get the ID of that row
        solId = int(solutionRow['SolId'])
        # from the solutions dataframe get solutions[solID], the bellow is a function from the testing module
        # create your own solution variable using what method you want like solutions[solID]
        #solution = td.getSolution(solutions, solId)       

        # This needs to be changed to match how many levels there are which code is for each color
        color = []
        for row in solution['upGrade']:
            if row == 0:
                color.append('grey')
            if row == 1:
                color.append('green')
            if row == 2:
                color.append('blue')
            if row == 3:
                color.append('red')

        # add the colors to your local solution dataframe
        solution['color'] = color
        # select only rows with colors checked in checklist
        solution2 = solution[solution['color'].isin(checklist)]
        
        #create map object 
        maps = go.Figure(go.Scattermapbox(
            lat=solution2['lat'],
            lon=solution2['long'],
            mode='markers', 
            marker=dict(
                        size=12,
                        color=solution2['color'], #set color equal to a variable
                        colorscale='Viridis', # one of plotly colorscales
                        showscale=True
                    )

        ))
        

        #set up map layout
        maps.update_layout(
            autosize=True, # Autosize
            hovermode='closest', # Show info on the closest marker
            showlegend=True, # show legend of colors
            mapbox=dict(
                accesstoken=mapbox_access_token, # token
                bearing=0, # starting facing direction
                # starting location
                center=dict(
                    lat=td.cLat,
                    lon=td.cLong
                ),
                #angle and zoom
                pitch=0,
                zoom=10
            ),
            #height and width
            width=1000,
            height=1000
        )

        return maps
            


# for 2D map its essentially the same logic, refer to above comments for details. The only changes are that there is no z dimension

# In[ ]:



@app.callback(
    Output('2dmap','figure'),
    [Input('2dgraph', 'clickData'),
    Input('checklist', 'value')])
def update_map_2d(clickData,checklist):
    if clickData is None:
        #make a map
        maps = go.Figure(go.Scattermapbox(
 lat=coords['lat'], # set lat and long
 lon=coords['long'],
 mode='markers', 
 marker =({'size':5.5}) # make markers size variable 
        ))
    
        # set up map layout
        maps.update_layout(
 autosize=True, # Autosize
 hovermode='closest', # Show info on the closest marker
 showlegend=True, # show legend of colors
 mapbox=dict(
     accesstoken=mapbox_access_token, # token
     bearing=0, # starting facing direction
     # starting location
     center=dict(
         lat=td.cLat,
         lon=td.cLong
     ),
     #angle and zoom
     pitch=0,
     zoom=12
 ),
 #height and width
 width=1000,
 height=1000
        )
        return maps
    else:
        xCoord = int(clickData['points'][0]['x'])
        yCoord = int(clickData['points'][0]["y"])

        solutionRow = preatoFrontier.loc[(preatoFrontier['x'] == xCoord)&(preatoFrontier['y'] == yCoord)]
        solId = int(solutionRow['SolId'])
        solution = td.getSolution(solutions, solId)       

        color = []
        for row in solution['upGrade']:
 if row == 0:
     color.append('grey')
 if row == 1:
     color.append('green')
 if row == 2:
     color.append('blue')
 if row == 3:
     color.append('red')

        solution['color'] = color
        solution2 = solution[solution['color'].isin(checklist)]
         
        maps = go.Figure(go.Scattermapbox(
 lat=solution2['lat'],
 lon=solution2['long'],
 mode='markers', 
 marker=dict(
             size=12,
             color=solution2['color'], #set color equal to a variable
             colorscale='Viridis', # one of plotly colorscales
             showscale=True
         )

        ))
        maps.update_layout(
 autosize=True, # Autosize
 hovermode='closest', # Show info on the closest marker
 showlegend=True, # show legend of colors
 mapbox=dict(
     accesstoken=mapbox_access_token, # token
     bearing=0, # starting facing direction
     # starting location
     center=dict(
         lat=td.cLat,
         lon=td.cLong
     ),
     #angle and zoom
     pitch=0,
     zoom=10
 ),
 #height and width
 width=1000,
 height=1000
        )

        return maps    


# ## Downloading the Data

# ## Getting the Solution data in a csv
# ### Input
# * The amount of clicks for the download button
# * The point clicked in the graph  
# 
# ### Output 
# * The csv containing the `solution[x]` data 

# In[ ]:


@app.callback(
    Output("download-dataframe-csv", "data"),
    Input("download button", "n_clicks"),
    Input('graph', 'clickData'),
    prevent_initial_call=True,
    prevent_update = True
)
def download_3d(n_clicks,clickData):
    # since n_clicks only records how many times its been clicked and we only want to know IF the button has been clicked.
    # we use this below.
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if clickData is None:
        n_clicks = 0
    else:
        # if you have clicked the the download button
        if 'n_clicks' in changed_id:
            # you will notice the logic is essentally the same as many above. Unfortunatly due to how DASH is 
            # and probably my lack on knowledge on better methods there is A LOT of repeated code. 
            xCoord = int(clickData['points'][0]['x'])
            yCoord = int(clickData['points'][0]["y"])
            zCoord = int(clickData['points'][0]["z"])
            
            solutionRow = preatoFrontier.loc[(preatoFrontier['x'] == xCoord)&(preatoFrontier['y'] == yCoord)&(preatoFrontier['z'] == zCoord)]
            solId = int(solutionRow['SolId'])
            solution = td.getSolution(solutions, solId)       
    
            color = []
            for row in solution['upGrade']:
                if row == 0:
                    color.append('grey')
                if row == 1:
                    color.append('green')
                if row == 2:
                    color.append('blue')
                if row == 3:
                    color.append('red')
    
            solution['color'] = color
            
            # create a file name 
            fileName = "solution_" + str(xCoord) +"_"+ str(yCoord) +"_"+str(yCoord)+".csv"
            n_clicks = 0
            # export the dataframe to csv with the file name
            return dcc.send_data_frame(solution.to_csv, fileName)
   
    


# For 2d the logic is the same as above 

# In[ ]:


@app.callback(
    Output("d2d", "data"),
    Input("download button", "n_clicks"),
    Input('2dgraph', 'clickData'),
    prevent_initial_call=True,
    prevent_update = True
)
def download_2d(n_clicks,clickData):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]

    if clickData is None:
        n_clicks = 0
    else:
        if 'n_clicks' in changed_id:
            xCoord = int(clickData['points'][0]['x'])
            yCoord = int(clickData['points'][0]["y"])
            solutionRow = preatoFrontier.loc[(preatoFrontier['x'] == xCoord)&(preatoFrontier['y'] == yCoord)]
            solId = int(solutionRow['SolId'])
            solution = td.getSolution(solutions, solId)       

            color = []
            for row in solution['upGrade']:
                if row == 0:
                    color.append('grey')
                if row == 1:
                    color.append('green')
                if row == 2:
                    color.append('blue')
                if row == 3:
                    color.append('red')
    
            solution['color'] = color
            fileName = "solution_" + str(xCoord) +"_"+ str(yCoord)+".csv"
            solFile = dcc.send_data_frame(solution.to_csv, fileName)
            return solFile


# # Ensuring that data exists to be downloaded

# ## Returning download error 
# ### Input
# * The amount of clicks for the download button
# * The point clicked in the graph  
# 
# ### Output 
# * A boolean on if the danger notification should be displayed 

# In[ ]:


@app.callback(Output('confirm-danger-3d', 'displayed'),
              Input("download button", "n_clicks"),
              Input('graph', 'clickData'))
def noData3d(clicks, clickData):
    
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]

    # If there has been no soluiton in the preato frontier chosen 
    if clickData is None:
        # and someone has pressed download data 
        if 'clicks' in changed_id:
            # show error flag 
            return True
    # else do not show flag
    else:
        return False


# Same logic as 3D for 2D

# In[ ]:


@app.callback(Output('confirm-danger-2d', 'displayed'),
              Input("download button", "n_clicks"),
              Input('2dgraph', 'clickData'))
def noData2d(clicks, clickData):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if clickData is None:
        if 'clicks' in changed_id:
            return True
    else:
        return False


# # Get Statistics on Map 

# ## Dynamic Solution Statistics Table 
# ### Input
# * The coordinate of the point clicked on the preato frontier
# ### Output 
# * The dynamic dash table with the updating statistics 

# In[ ]:


@app.callback(
    dash.dependencies.Output('container-button-basic', 'children'),
    [dash.dependencies.Input('graph', 'clickData')],
    prevent_initial_call=True
    )
def levelsData3d(clickData):
    
    if clickData is None:
        pass
    else:
        # you have already seen this many times before, you can either change the solution variable to a method 
        # you want to use, or you can use the same function with your own data. 
        xCoord = int(clickData['points'][0]['x'])
        yCoord = int(clickData['points'][0]["y"])
        zCoord = int(clickData['points'][0]["z"])
        solutionRow = preatoFrontier.loc[(preatoFrontier['x'] == xCoord)&(preatoFrontier['y'] == yCoord)&(preatoFrontier['z'] == zCoord)]
        solId = int(solutionRow['SolId'])
        solution = td.getSolution(solutions, solId)       

        color = []
        for row in solution['upGrade']:
            if row == 0:
                color.append('grey')
            if row == 1:
                color.append('green')
            if row == 2:
                color.append('blue')
            if row == 3:
                color.append('red')

        solution['color'] = color
        # getting stats on each of the values. 
        df = pd.DataFrame(solution.color.value_counts())
        df.reset_index(inplace = True)
        df.rename(columns={'index' : 'Level', 'color' : 'Count'},inplace = True)
        total = df['Count'].sum()
        df['Ratio'] = df['Count']/total
        df2 = {'Level': 'Total', 'Count': total,'Ratio':'1'}
        df = df.append(df2, ignore_index = True)
        return dbc.Table.from_dataframe(df,bordered = True,striped=True)  
   
    


# Exact same logic as 3D for 2D

# In[ ]:


@app.callback(
    dash.dependencies.Output('container-button-basic2', 'children'),
    [dash.dependencies.Input('2dgraph', 'clickData')],
    prevent_initial_call=True
    )
def levelsData2d(clickData):
    
    if clickData is None:
        pass
    else:
        
        xCoord = int(clickData['points'][0]['x'])
        yCoord = int(clickData['points'][0]["y"])
        solutionRow = preatoFrontier.loc[(preatoFrontier['x'] == xCoord)&(preatoFrontier['y'] == yCoord)]
        solId = int(solutionRow['SolId'])
        solution = td.getSolution(solutions, solId)       

        color = []
        for row in solution['upGrade']:
            if row == 0:
                color.append('grey')
            if row == 1:
                color.append('green')
            if row == 2:
                color.append('blue')
            if row == 3:
                color.append('red')

        solution['color'] = color

        df = pd.DataFrame(solution.color.value_counts())
        df.reset_index(inplace = True)
        df.rename(columns={'index' : 'Level', 'color' : 'Count'},inplace = True)
        
        total = df['Count'].sum()
        df['Ratio'] = df['Count']/total
        df2 = {'Level': 'Total', 'Count': total,'Ratio':'1'}
        df = df.append(df2, ignore_index = True)
        return dbc.Table.from_dataframe(df,bordered = True,striped=True)    
    


# # Run the Server

# In[ ]:


if __name__ == '__main__':
    app.run_server(debug=True,use_reloader=False)


# I will enclose a youtube video with an explanation on how this program works along with ideas on how you can improve the code ye how maintains this beast. 

# Author: Shahzad Ansari
# 
# Email: Shahzad1611@gmail.com 
# - Please put 'GeneralPreatoVisualizationEngine' in the subject of the email. Otherwise i might miss it.
# 
# Phone: 9727433492
# - You can text me if needed but email me first. 
# 
# This was done under the supervision of Dr.Charles Nicholson of The University of Oklahoma. 

# # Things you might want to add
# * There is a lot of code duplication, if there is a way to reduce that that would be amazing especially with changing from 3D to 2d. It litterally doubles the code amount. From what i gather you might be able to do so with something called 'States' in Dash but there werent too many tutorials on it as of yet. 
# * Potentially you could have the files be uploaded by the user in the UI itself.
# * You could connect to the IN-CORE website to actually PULL the data from the website itself instead of having to pass itin manually. 
# * The UI doesnt scale very good. This is probably because i have no idea how to do CSS so if you have some web dev experience you probably can add your custom CSS to make it look better. 
# * You could use Google maps API but it was a pretty complicated if even techincally possible. 
# * Note: If you try to deploy to a server you might see somethign about a dash-tools library, if you try this make sure you create a seperate virtual environment to try this in. For what ever reason when you install this lib it breaks mapbox you can see my stack overflow post where i go over this. I dont think many people use DASH and Mapbox because no one responded but i figured it out. It was painful and took me 14 hours to debug. I almost gave up. 
# https://stackoverflow.com/questions/74767587/plotly-go-scattermapbox-is-not-showing-markers

# In[ ]:




