import numpy as np
import pandas as pd
import re

#plotLy
from plotly import __version__
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
from plotly.grid_objs import Grid, Column
import plotly.graph_objs as go
import plotly.plotly as py
from plotly import tools
init_notebook_mode(connected=True)

#LDA
import pyLDAvis
import pyLDAvis.gensim
# import nltk
# nltk.download("stopwords")
from nltk.corpus import stopwords
stop = stopwords.words("english")
# pyLDAvis.enable_notebook()
# from smart_open import open
# from gensim import corpora, models

from scipy import stats

import warnings
warnings.filterwarnings("ignore")
import plotly.offline as pyo
pyo.init_notebook_mode()





twitter_tweets = pd.read_csv("tweets.csv")
fake__users = pd.read_csv("users.csv")
tweets_details = pd.read_csv("tweetdetails.csv")

#clean the date to a Year-Month format
fake__users["Date"] = pd.to_datetime(fake__users["created_at"])
fake__users = fake__users[pd.notnull(fake__users["created_at"])]
fake__users = fake__users.drop_duplicates(subset=["id"])
fake__users["Date"] = fake__users["Date"].apply(lambda x: x.strftime("%y-%m"))


u_name = pd.DataFrame(fake__users.name.str.split(" ",1).tolist(), columns = ["first","last"])
user_name = u_name.groupby("first",as_index=False).size().reset_index(name="counts")
users_name = user_name.sort_values("counts", ascending=False).head(20)


#Task 1:
# bar plot
#first names
first_name = u_name.groupby("first",as_index=False).size().reset_index(name="counts")
first_name = first_name.sort_values("counts", ascending=False).head(20)
trace1_fn = go.Bar(
	x=first_name["counts"],
	y=first_name["first"],
	orientation = "h",
	name = "First Name",
	showlegend=False
)
last_name = u_name.groupby("last",as_index=False).size().reset_index(name="counts")
last_name = last_name.sort_values("counts", ascending=False).head(20)
trace1_ln = go.Bar(
	x=last_name["counts"],
	y=last_name["last"],
	orientation = "h",
	name = "Last Name",
	showlegend=False
)

fig1 = tools.make_subplots(rows=1, cols=2, subplot_titles=("First Name", "Last Name"))
fig1.append_trace(trace1_fn, 1, 1)
fig1.append_trace(trace1_ln, 1, 2)
fig1["layout"].update(height=400, width=500, title="First and Last Names of Fake Accounts")
# plot(fig, filename = "basic-lin")


#Task 2:
#remove the special characters
des = fake__users.description.copy().astype(str)
des = des.str.replace("[^\w\s]"," ")
des = des.str.strip()

tweets_des = tweets_details.copy()
tweets_des.des = des
tweets_des.des = tweets_des.des.apply(lambda x: " ".join([word for word in x.split() if word.lower() not in (stop)]))

# convert sample documents into a list
doc_set = tweets_des.des.values.copy()
# loop through document list
texts = [ text.split(" ") for text in doc_set]


# # turn our tokenized documents into a id <-> term dictionary
# dictionary = corpora.Dictionary(texts)
# # convert tokenized documents into a document-term matrix
# corp = [dictionary.doc2bow(text) for text in texts]
# # generate LDA model
# ldamodel = models.ldamodel.LdaModel(corp, num_topics=30, id2word = dictionary)
# df3 = pyLDAvis.gensim.prepare(ldamodel, corp, dictionary)




#Task 3:
#group by Date, create a count and sort
users = fake__users.groupby("Date",as_index=False).size().reset_index(name="counts")
users = users.sort_values("Date")

trace2 = go.Bar(
	name = "Accounts Created Over Time",
	x=users.Date,
	y=users.counts,
	showlegend=False
)
data = ([trace2])

layout = go.Layout(
	title = "Accounts created 2009-2017",
	yaxis=dict(
		title="No. Of Accounts created",
		range=[0, 100],
		titlefont=dict(size=20)
	),
	xaxis = dict(
		title="Year",
		range = ["2009-01","2017-1"],
		titlefont=dict(size=20)
	)
)
fig2 = go.Figure(data=data, layout=layout)
fig2["layout"].update()
# plot(fig)

#Task 4:

# heat map showing the days and hours of users
m = pd.pivot_table(tweets_details, values = "user_key", index = "created_strDayofweek", columns = "created_strMonth", aggfunc = len, fill_value = 0, dropna = False)
z = m.as_matrix()



trace3 = go.Heatmap(z=z, x=[i for i in np.arange(0, 24)], y=["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"], colorscale="Jet")
layout = go.Layout(title="No. of Tweets per Day per Month", xaxis=dict(nticks=24, title="Month", titlefont=dict(size=20)), yaxis=dict())
data = [trace3]
fig3 = go.Figure(data=data, layout=layout)
fig3["layout"].update()
# plot(fig, filename="tweets.html")


fig = tools.make_subplots(rows=2, cols=2, subplot_titles=('First Names', 'Last Names', 'Accounts Created Over Time', 'No. of Tweets per Day per Month'))

fig.append_trace(trace1_fn, 1, 1)
fig.append_trace(trace1_ln, 1, 2)
fig.append_trace(trace2, 2, 1)
fig.append_trace(trace3, 2, 2)
fig['layout'].update(height=680, width=1500, title="Fake Account Analysis")
plot(fig, filename="result.html")
