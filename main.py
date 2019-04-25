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


twitter_tweets = pd.read_csv("tweets.csv")
fake_users = pd.read_csv("users.csv")
tweets_details = pd.read_csv("tweetdetails.csv")

#clean the date to a Year-Month format
fake_users["Date"] = pd.to_datetime(fake_users["created_at"])
fake_users = fake_users[pd.notnull(fake_users["created_at"])]
fake_users = fake_users.drop_duplicates(subset=["id"])
fake_users["Date"] = fake_users["Date"].apply(lambda x: x.strftime("%y-%m"))

u_name = pd.DataFrame(fake_users.name.str.split(" ",1).tolist(), columns = ["first","last"])
user_name = u_name.groupby("first",as_index=False).size().reset_index(name="counts")
users_name = user_name.sort_values("counts", ascending=False).head(20)


#Task 1:
# bar plot
def get_first_and_last_name_trace():
	first_name = u_name.groupby("first",as_index=False).size().reset_index(name="counts")
	first_name = first_name.sort_values("counts", ascending=False).head(20)
	trace_fn = go.Bar(
		x=first_name["counts"],
		y=first_name["first"],
		orientation = "h",
		name = "First Name",
		showlegend=False
	)
	last_name = u_name.groupby("last",as_index=False).size().reset_index(name="counts")
	last_name = last_name.sort_values("counts", ascending=False).head(20)
	trace_ln = go.Bar(
		x=last_name["counts"],
		y=last_name["last"],
		orientation = "h",
		name = "Last Name",
		showlegend=False
	)
	return trace_fn, trace_ln


#Task 3:
#group by Date, create a count and sort
def get_accounts_created_trace():
	users = fake_users.groupby("Date",as_index=False).size().reset_index(name="counts")
	users = users.sort_values("Date")

	trace = go.Bar(
		name = "Accounts Created Over Time",
		x=users.Date,
		y=users.counts,
		showlegend=False
	)
	return trace


#Task 4:
# heat map showing the days and hours of users
def get_tweets_activity_trace():
	m = pd.pivot_table(tweets_details, values="user_key", index="created_strDayofweek",
			columns="created_strMonth", aggfunc=len, fill_value=0, dropna=False)
	z = m.values
	trace = go.Heatmap(z=z, x=[i for i in np.arange(0, 24)], y=["Sunday","Monday",
			"Tuesday","Wednesday","Thursday","Friday","Saturday"], colorscale="Jet")
	return trace


fig = tools.make_subplots(rows=2, cols=2, subplot_titles=("First Names", "Last Names",
		"Accounts Created Over Time", "No. of Tweets per Day per Month"))

first_name_trace, last_name_trace = get_first_and_last_name_trace()
accounts_created_trace = get_accounts_created_trace();
tweets_activity_trace = get_tweets_activity_trace()

fig.append_trace(first_name_trace, 1, 1)
fig.append_trace(last_name_trace, 1, 2)
fig.append_trace(accounts_created_trace, 2, 1)
fig.append_trace(tweets_activity_trace, 2, 2)
fig["layout"].update(height=680, width=1500, title="Fake Account Analysis")
plot(fig, filename="dashboard.html")
