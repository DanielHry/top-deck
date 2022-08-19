# Daniel Hryniewski 08/2022

import streamlit as st
import pandas as pd
import random

from data import load_data

import plotly.express as px

# streamlit run topDeck/topDeck.py


def count_df(df: pd.DataFrame, col: str, norm: bool = False, limit: tuple = None) -> pd.DataFrame:
    df = pd.DataFrame(df[col].value_counts(normalize=norm))
    if limit is not None:
        df = df[limit[0]: limit[1]]
    return df.reset_index().rename(columns={'index': col, col:'count'})



# =============================================================================
# =============================== PAGE SETTING ================================

mtgred = 'https://cdn3.emoji.gg/emojis/5593_mtgred.png'
mtgblack = 'https://cdn3.emoji.gg/emojis/3529_mtgblack.png'
mgtblue = 'https://cdn3.emoji.gg/emojis/8017_mgtblue.png'
mtggreen = 'https://cdn3.emoji.gg/emojis/9952_mtggreen.png'
mtgwhite = 'https://cdn3.emoji.gg/emojis/7496_mtgwhite.png'
mtgcards = 'https://cdn3.emoji.gg/emojis/4620-cardboardcrack.png'
icone = random.choice([mtgred, mtgblack, mgtblue, mtggreen, mtgwhite, mtgcards])
st.set_page_config(page_title='MTG TopDeck', layout='wide', page_icon=icone)

DATA = load_data()

# =============================================================================
# ================================== SIDEBAR ==================================
st.sidebar.title("Top Decks")
st.sidebar.write("")
st.sidebar.write("")
st.sidebar.write("")

st.sidebar.markdown("**First select the data range you want to analyze:** 👇")
st.sidebar.write("")
list_lears = DATA['year'].unique()
list_lears.sort()
start_time, end_time = st.sidebar.select_slider(
     "Select the period of years:",
     options=list_lears,
     value=(min(list_lears)+16, max(list_lears)))
st.sidebar.write("")

df = DATA[DATA['year'] <= end_time]
DATA = None
df_date = df[start_time <= df['year']]
format_list = df_date['format'].unique().tolist()
format_list.insert(0, 'All formats')
format_list.sort()
format = st.sidebar.selectbox('Select your format:', format_list)

if format != 'All formats':
    df = df_date[df_date['format'] == format]
else:
    df = df_date

st.sidebar.write("")
st.sidebar.write(
    f'Find', len(df), 'decks in', len(df['title_date'].unique()), 'competitions.')


# =============================================================================
# ================================= DATABASE ==================================

st.title(f'{format} ({start_time} - {end_time}) :')
st.write("")
st.write("")
t1, t2 = st.columns(2)

t1.write("Database: ")
df = df.sort_values(by=['year', 'month', 'day'], ascending=False)
df = df.reset_index(drop=True)
data_to_show = df[['title', 'format', 'date', 'player', 'ranking', 'deck_name']]
data_to_show = data_to_show.rename(columns={'title': 'competition'})
t1.dataframe(data_to_show)




# =============================================================================
# ========================= PIE FORMAT DISTRIBUTION ===========================

df_format_count = count_df(df_date, 'format')
fig = px.pie(df_format_count, values='count', names='format', color='format')
fig.update_layout(title=f'Decks distribution of All Formats ({start_time}-{end_time}):')
t1.plotly_chart(fig)



# =============================================================================
# ============================ BAR COMPETITIONS ===============================

for year in range(start_time, end_time +1):
    dyear = df[df['year'] == year][['title_date', 'format']].value_counts().reset_index()
    dd = count_df(dyear, 'format')
    dd['year'] = [year] * len(dd)
    if start_time == year:
        df_mix = dd
    else:
        df_mix = pd.concat([df_mix, dd], axis=0)

fig = px.bar(df_mix, x='year', y='count', color='format')
fig.update_layout(
    height=900,
    title='Number of copetitions per year :',
    yaxis=dict(
        title='Count competitions',
        titlefont_size=16,
        tickfont_size=14,
    ),
    xaxis=dict(
        title='Years',
        titlefont_size=16,
        tickfont_size=14,
    ),)
t2.plotly_chart(fig)



# =============================================================================
# ====================== MULTI SELECT & SELECT SLIDER =========================

st.markdown("<hr />", unsafe_allow_html=True)
t1, t2 = st.columns(2)

options = t2.multiselect(
     'Select Classement :',
     ['1st', '2nd', '3rd', '4th'],
     ['1st', '2nd'])

intopt = [int(o[0]) for o in options]
intopt.sort()
if len(intopt) == 0:
    intopt = [-1]

list_lears = range(1, 201)
show_start, show_end = t1.select_slider(
     "Select the range",
     options=list_lears,
     value=(min(list_lears), min(list_lears)+20))



# =============================================================================
# ============================ BAR 30 BEST DECK ===============================

t1, t2 = st.columns(2)
df_names_count = count_df(df, 'deck_name', False, (show_start-1, show_end))
ratio_height = 26 * (show_end - show_start)
ratio_height = round(ratio_height/10 + 10)*10
if ratio_height < 300:
    ratio_height = 300
fig1 = px.bar(df_names_count[::-1], y='deck_name', x='count',
             orientation='h', color='count')
fig1.update_layout(
    height=ratio_height,
    title=f'Best {show_start} to {show_end} decks most played (all classement):',
    yaxis=dict(
        title='Decks Names',
        titlefont_size=16,
        tickfont_size=14,
    ),
    xaxis=dict(
        title='Count',
        titlefont_size=16,
        tickfont_size=14,
    ),)
t1.plotly_chart(fig1)



# =============================================================================
# ========================= BAR 30 BEST DECK PLACE ============================

df_rank = pd.concat([df[df['ranking_min'] == op] for op in intopt], axis=0)
df_rank_count = count_df(df_rank, 'deck_name', False, (show_start-1, show_end))
fig2 = px.bar(df_rank_count[::-1], y='deck_name', x='count',
             orientation='h', color='count')
fig2.update_layout(
    height=ratio_height,
    title=f"Best {show_start} to {show_end} decks finished in {', '.join(options)} place :",
    yaxis=dict(
        title='Decks Names',
        titlefont_size=16,
        tickfont_size=14,
    ),
    xaxis=dict(
        title='Count',
        titlefont_size=16,
        tickfont_size=14,
    ),)
t2.plotly_chart(fig2)

st.markdown("<hr />", unsafe_allow_html=True)



# =============================================================================
# ============================== RANDOM DECK ==================================

option = st.selectbox('Choose the deck :', df_rank_count['deck_name'].unique())
deck_choice = df_rank[df_rank['deck_name'] == option]

decks_df = {}
decks_df['competition'] = []
decks_df['player'] = []
decks_df['date'] = []
decks_df['url'] = []

for n, d in enumerate(deck_choice.sample(frac = 1).iloc): 
    decks_df['competition'].append(d.title.strip(' '))
    decks_df['player'].append(d.player.strip(' '))
    decks_df['date'].append(d.date.strip(' '))
    
    deck_name = d.deck_name.strip(' ')
    url = d.deck_url.strip(' ')
    
    decks_df['url'].append(f'<a target="_blank" href="{url}">Magic-Ville</a>')

    if n == 20:
        break

decks_df = pd.DataFrame(decks_df)
decks_df = decks_df.to_html(escape=False)
st.write(decks_df, unsafe_allow_html=True)

