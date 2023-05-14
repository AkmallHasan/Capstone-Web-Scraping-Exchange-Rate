from flask import Flask, render_template
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from bs4 import BeautifulSoup 
import requests

#don't change this
matplotlib.use('Agg')
app = Flask(__name__) #do not change this

#insert the scrapping here
url_get = requests.get('https://www.exchange-rates.org/history/IDR/USD/T')
soup = BeautifulSoup(url_get.content,"html.parser")

#find your right key here
table  = soup.find('table', attrs={'class':'history-rates-data'})
rows = len(table.find_all('a',attrs={'class':'n'}))

temp = [] #initiating a list 

for i in range(0, rows):

    #scrapping process
    #get period
    date_all = soup.find_all('a', attrs={'class':'n'})[i].text
    date_all = date_all.strip() # to remove excess white space
    
    #get exchange_rate
    exchangerate_all = soup.find_all('span', attrs={'class':'w'})[i].text
    exchangerate_all = exchangerate_all.strip() # to remove excess white space
    
    temp.append((date_all,exchangerate_all)) 

temp = temp[::-1]

#change into dataframe
df = pd.DataFrame(temp, columns = ('date','exchange_rate'))

#insert data wrangling here
df['date'] = df['date'].astype('datetime64[ns]')
df['exchange_rate'] = df['exchange_rate'].str.replace("$1 = Rp",' ')
df['exchange_rate'] = df['exchange_rate'].str.replace(',','.')
df['exchange_rate'] = df['exchange_rate'].astype('float64')
df = df.set_index('date')
#end of data wranggling 

@app.route("/")
def index(): 
	
	card_data = f'{df["exchange_rate"].mean().round(3)}' #be careful with the " and ' 

	# generate plot
	ax = df.plot(figsize = (20,9)) 
	
	# Rendering plot
	# Do not change this
	figfile = BytesIO()
	plt.savefig(figfile, format='png', transparent=True)
	figfile.seek(0)
	figdata_png = base64.b64encode(figfile.getvalue())
	plot_result = str(figdata_png)[2:-1]

	# render to html
	return render_template('index.html',
		card_data = card_data, 
		plot_result=plot_result
		)


if __name__ == "__main__": 
    app.run(debug=True)