import requests, pandas as pd
from bs4 import BeautifulSoup
from time import sleep
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import os
import re
import math


def main():
    # your code here
    url = "https://www.ncei.noaa.gov/data/local-climatological-data/access/2021/"
    
    #set this to make sure we have appropriate webdriver
    driver = webdriver.Chrome(ChromeDriverManager().install())

    #create directory if does not exist
    cwd = os.getcwd()
    directory =  cwd + "/data"
    if not os.path.exists(directory):
        os.makedirs(directory)

    #the wait allows the code to work despite the javascript on the page
    def parse(url):
        response = driver
        response.get(url)
        sleep(3)
        sourcecode = response.page_source
        return sourcecode

    #beautifulsoup to download the data, find the table element required
    soup = BeautifulSoup(parse(url),'lxml')
    table = soup.find('table')
    data = []
    table_body = table.find('tbody')
    rows = table_body.find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        data.append([ele for ele in cols if ele]) # Get rid of empty values

    #get the date specified for the exercise
    date = "2022-02-07 14:03"
    answer = []
    for i in data:
        for j in i:
            if j == date:
                answer = i

    #url for downloading   
    url2 = url + answer[0]

    filename = requests.get(url2)
    with open(directory + "/datafile.csv", 'wt')as file:
        file.write(filename.text)

    df = pd.read_csv(directory + "/datafile.csv")
    df = df.dropna(axis =0, subset = ['HourlyDryBulbTemperature'])

    df_column = []
    for x in df['HourlyDryBulbTemperature']:
        if isinstance(x, str)==True:
            x = re.sub("[^0-9]","",x)
            if x!= "":
                df_column.append(int(x))
            else:
                df_column.append(0)
        else:
            df_column.append(int(x))

    df['HourlyDryBulbTemperature'] = df_column

    df = df.sort_values('HourlyDryBulbTemperature', axis=0, ascending=False)
    print(df[['NAME','HourlyDryBulbTemperature']].head())
    pass


if __name__ == '__main__':
    main()
