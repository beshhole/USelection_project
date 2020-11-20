import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

pd.set_option('display.width', 500)
pd.set_option('display.max_columns', 12)

data = pd.read_csv('E:/Besha/belajar/pandas exercise/exercise 13/president_county_candidate.csv')
datausa = pd.read_csv('E:/Besha/belajar/pandas exercise/exercise 13/world_country_and_usa_states_latitude_and_longitude_values.csv')

print(data.info())
print(data.head())

trumpvotes = data[data['candidate'] == 'Donald Trump']
bidenvotes = data[data['candidate'] == 'Joe Biden']
data = data[(data['candidate'] == 'Donald Trump') | (data['candidate'] == 'Joe Biden')]
usa = data.groupby(['state', 'candidate']).sum().unstack().reset_index()
# print(usa)

trumptotal = trumpvotes.groupby('state').sum().reset_index()
bidentotal = bidenvotes.groupby('state').sum().reset_index()
# print(trumptotal)

print(datausa.info())
print(datausa.head())

usacol = ['usa_state_code', 'usa_state_latitude', 'usa_state_longitude', 'usa_state']
datausa = datausa[usacol].sort_values(by='usa_state', axis=0, ascending=True).reset_index(drop=True)
datausa.dropna(axis=0, how='any', inplace=True)
datausa.drop(index=39, inplace=True)
print(datausa.info())
print(datausa.head(55))

trumptotal = trumptotal.merge(datausa, left_on='state', right_on='usa_state')
bidentotal = bidentotal.merge(datausa, left_on='state', right_on='usa_state')

total = usa.merge(datausa, left_on='state', right_on='usa_state')
total.rename(columns={('state', ''): 'state', ('votes', 'Donald Trump'): 'Donald Trump', ('votes', 'Joe Biden'): 'Joe Biden'}, inplace=True)
# print(total)
percent = (total['Joe Biden'] / (total['Donald Trump'] + total['Joe Biden'])) * 100

fig = px.choropleth(total, locations='usa_state_code', color=percent, locationmode='USA-states', hover_name='usa_state', color_continuous_scale='RdBu', range_color=[25, 75], scope='usa')
# fig.update_layout(coloraxis_colorbar=dict(tickmode='array', tickvals=[30, 40, 50, 60, 70],
#                                           ticktext=['30%', '40%', '50%', '60%', '70%']))
fig.show()

percenttrump = (total['Donald Trump'] / (total['Donald Trump'] + total['Joe Biden'])) * 100
percentbiden = (total['Joe Biden'] / (total['Donald Trump'] + total['Joe Biden'])) * 100

fig = px.choropleth(trumptotal, locations='usa_state_code', color=percenttrump, locationmode='USA-states', hover_name='state', color_continuous_scale='reds', range_color=[25, 75], scope='usa')
# fig.update_layout(coloraxis_colorbar=dict(tickmode='array', tickvals=[2500000, 5000000, 7500000, 10000000],
#                                           ticktext=['2,5M', '5M', '7,5M', '10M']))
fig.show()

fig = px.choropleth(bidentotal, locations='usa_state_code', color=percentbiden, locationmode='USA-states', hover_name='state', color_continuous_scale='blues', range_color=[25, 75], scope='usa')
# fig.update_layout(coloraxis_colorbar=dict(tickmode='array', tickvals=[2500000, 5000000, 7500000, 10000000],
#                                           ticktext=['2,5M', '5M', '7,5M', '10M']))
fig.show()

usa = pd.concat([usa, percenttrump, percentbiden], axis=1)
usa.rename(columns={('state', ''): 'state', ('votes', 'Donald Trump'): 'Donald Trump',
                    ('votes', 'Joe Biden'): 'Joe Biden', 0: "Trump(%)", 1: 'Biden(%)'}, inplace=True)
usa['Trump(%)'] = usa['Trump(%)'].astype('int64')
usa['Biden(%)'] = usa['Biden(%)'].astype('int64')
# print(usa)

def fillwinner(cols):
    trumpcol = cols[0]
    bidencol = cols[1]
    if trumpcol > bidencol:
        return 'Trump'
    else:
        return 'Biden'


usa['Winner'] = usa[['Donald Trump', 'Joe Biden']].apply(fillwinner, axis=1)
print(usa)

trumpsum = usa['Donald Trump'].sum()
bidensum = usa['Joe Biden'].sum()
trumpperc = (trumpsum / (bidensum + trumpsum)) * 100
bidenperc = (bidensum / (bidensum + trumpsum)) * 100

totaldf = pd.DataFrame({'Candidate': ['Donald Trump', 'Joe Biden'], 'Total Votes': [trumpsum, bidensum], '% Votes': [trumpperc, bidenperc]})
# totaldf.set_index('Candidate', inplace=True)
print(totaldf)

totalgra = sns.barplot(x='Candidate', y='Total Votes', data=totaldf)
for bar in totalgra.patches:
    if bar.get_height() < 73000000:
        bar.set_color('firebrick')
    else:
        bar.set_color('royalblue')
totalgra.set(ylabel='Total Votes in 10 Millions')
plt.show()

totalgraperc = sns.barplot(x='Candidate', y='% Votes', data=totaldf)
for bar in totalgraperc.patches:
    if bar.get_height() < 50:
        bar.set_color('firebrick')
    else:
        bar.set_color('royalblue')
plt.show()
