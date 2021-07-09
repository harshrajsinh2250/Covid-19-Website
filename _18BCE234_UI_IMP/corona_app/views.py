#Created by:-18BCE234-Solanki Harshrajsinh Surpalsinh
#Importing Required APIS For Work:-
from django.shortcuts import render
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import urllib, base64
import io
#Code For Reading and Storing the 3 CSV files:-(Part-2)
country_file = open("corona_data/Countrywise.csv","r")
country_data = pd.read_csv(country_file,delimiter=",")
df2 = open("corona_data/Areawise.csv", "r")
df2 = pd.read_csv(df2, delimiter=",")
zone_file = open("corona_data/Zonewise.csv", "r")
zone_data = pd.read_csv(zone_file,delimiter=",")
#Code For Homepage/Base Page (Part-1):-
def homepage(request):
    data_list = list()
    df2.set_index('Date')
    last_date = df2.Date.max()
    for i in range(len(country_data)):
        isStates = False

        if df2['Country_code'].str.contains(country_data['Country_code'].values[i]).any():
            isStates = True
        item = {'no':country_data['Serial_number'].values[i], 'name':country_data['Country_name'].values[i],
                'Country_code':country_data['Country_code'].values[i],'Infected_count':country_data['infected_count'].values[i],
                'Death_count':country_data['death_count'].values[i],'Recovered_count':country_data['recovered_count'].values[i],
                'Test_conducted_count':country_data['test_conducted_count'].values[i], 'isStates':isStates}
        data_list.append(item)
    return render(request, 'index.html', {'data': data_list, 'updated': last_date})
#Code For State Page (Part-1):-
def statepage(request):
    global df2
    df2.set_index('Date')
    a = df2.Date.max()
    temp = df2[df2['Country_code'].str.contains(request.GET['id'])]
    temp = temp[temp['Date'].str.contains(a)]
    k= list()
    for i in range(len(temp)):
        ctr_code = temp['Country_code'].values[i]
        area_code = temp['Area_code'].values[i]

        class_name = zone_data.query('Country_code == "'+ctr_code+'" and Area_code == "'+area_code+'"')['Zone']
        j=  {'Date': temp['Date'].values[i], 'Country_code': ctr_code,'Area_name': temp['Area_name'].values[i],
                'Area_code': area_code,'infected_count': temp['infected_count'].values[i],
                'death_count': temp['death_count'].values[i],'recovered_count': temp['recovered_count'].values[i],
                'test_conducted_count': temp['test_conducted_count'].values[i], 'Class':class_name}
        k.append(j)
    return render(request, 'state.html', {'data': k, 'area_graph': get_area_graph(df2['Date'].values),'updated':a})
#Code For Graph Representation:-(Part-4)
def get_area_graph(dates):
    for i in range(len(country_data)):
        isStates = False
        if df2['Country_code'].str.contains(country_data['Country_code'].values[i]).any():
            isStates = True
            main_fig = plt.figure(figsize=(8, 8), dpi=200)
            infected = main_fig.add_subplot(311)
            infected.bar(df2['Date'], df2['infected_count'])
            plt.xlabel("Weekwise date->")
            plt.ylabel("infected count->")

            deaths = main_fig.add_subplot(313)
            deaths.bar(df2['Date'], df2['death_count'])
            plt.xlabel("Weekwise date->")
            plt.ylabel("deaths count->")

            fig = plt.gcf()
            # Create buffer to store binary data of PNG image(represents graph image)
            buffer = io.BytesIO()
            fig.savefig(buffer, format='png')
            buffer.seek(0)
            fig2 = urllib.parse.quote(base64.b64encode(buffer.read()))
            plt.close()
            return fig2