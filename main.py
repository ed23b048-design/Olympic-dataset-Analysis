import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go


data1=pd.read_csv("Olympic_Athlete_Biography.csv")
data2=pd.read_csv("Olympic_Athlete_Event_Details.csv")
data3=pd.read_csv("Olympic_Country_Profiles.csv")
data6=pd.read_csv("Olympic_Medal_Tally_History.csv")

# data preprocessing

data6.rename(columns={"year":"Year",
              "country" : "Country",
              "country_noc" : "Country_noc",
              "gold":"Gold",
              "silver" : "Silver",
              "bronze" : "Bronze",
              "total":"Total"},inplace=True)


data6["Year"]=data6["Year"].astype(int)

data6[["Year","Season","Waste"]]=data6["edition"].str.split(expand=True)

data2["medal"]=data2["medal"].fillna(0)

data2["pos"]=data2["pos"].str.replace("=","")

# ------------------------------------------------------------------------------ #
def sport_count(m):
    data2[["year", "season", "waste"]] = data2["edition"].str.split(expand=True)
    dummy_2 = data2.drop(["edition", "waste"], axis=1)
    sport = dummy_2.groupby("year")
    b=sport.get_group(str(m))["sport"].drop_duplicates().value_counts().sum()
    st.subheader(f"Sport list in Olympic year {year}: ")
    st.dataframe(sport.get_group(str(m))["sport"].drop_duplicates().sort_values().reset_index(drop=True),hide_index=True)
    st.write(f"Sports count in Olympic year {year} : {b}")
def medal_tally_summer(year,country):
    mask1 = data6["Year"] == year
    mask2 = data6["Country"] == ctry
    mask3 = data6["edition"].str.contains("Summer")
    a=data6[mask1 & mask2 & mask3][["Year", "Country", "Country_noc", "Gold", "Silver", "Bronze", "Total"]]

    if a["Gold"].empty==False & a["Silver"].empty==False & a["Bronze"].empty==False:
        value = [int(a["Gold"]), int(a["Silver"]), int(a["Bronze"])]
        label = ['Gold', 'Silver', 'Bronze']

        fig = go.Figure(
            data=[go.Pie(labels=label, values=value, textinfo='label+percent')])

        fig.update_layout(

            paper_bgcolor="Cyan",
            font_color="Green",
            legend=dict(
                font=dict(color="white"),
                font_size=20
            )
        )

        st.plotly_chart(fig)

    st.dataframe(a, hide_index=True)

def medal_tally_winter(year,country):
    mask1 = data6["Year"] == year
    mask2 = data6["Country"] == ctry
    mask3 = data6["edition"].str.contains("Winter")
    a = data6[mask1 & mask2 & mask3][["Year", "Country", "Country_noc", "Gold", "Silver", "Bronze", "Total"]]

    if a["Gold"].empty==False & a["Silver"].empty==False & a["Bronze"].empty==False:
        value = [int(a["Gold"]), int(a["Silver"]), int(a["Bronze"])]
        label = ['Gold', 'Silver', 'Bronze']

        fig = go.Figure(
            data=[go.Pie(labels=label, values=value, textinfo='label+percent', insidetextorientation='radial')])

        fig.update_layout(

            paper_bgcolor="Cyan",
            legend=dict(
                font=dict(color="White"),
                font_size=20

            )
        )

        st.plotly_chart(fig)

    st.dataframe(a, hide_index=True)


def medal_tally_intercalated(country):

    mask2 = data6["Country"] == ctry
    mask3 = data6["edition"].str.contains("Intercalated")
    a = data6[mask2 & mask3][["Year", "Country", "Country_noc", "Gold", "Silver", "Bronze", "Total"]]
    if a["Gold"].empty==False & a["Silver"].empty==False & a["Bronze"].empty==False:
        label = [int(a["Gold"]), int(a["Silver"]), int(a["Bronze"])]
        value = ['Gold', 'Silver', 'Bronze']

        fig = go.Figure(
            data=[go.Pie(labels=label, values=value, textinfo='label+percent', insidetextorientation='radial')])

        st.plotly_chart(fig)
    st.dataframe(a, hide_index=True)

def athlete_analysis(ctry):
    data2.rename(columns={
        "edition":"EDITION",
        "country_noc":"COUNTRY_NOC",
        "sport":"SPORT",
        "event":"EVENT",
        "pos":"POSITION",
        "medal":"MEDAL"},
        inplace=True
    )

    country=data2.groupby("COUNTRY_NOC")
    a=country.get_group(ctry)
    st.dataframe(a["athlete"])


def overall(ctry):

    m1=data6["edition"].str.contains("Summer")
    m2=data6["edition"].str.contains("Winter")

    dummy=data6[m1 | m2]

    overall = {"Country": [ctry],
               "Gold": [dummy[dummy["Country"] == ctry]["Gold"].sum()],
               "Silver": [dummy[dummy["Country"] == ctry]["Silver"].sum()],
               "Bronze": [dummy[dummy["Country"] == ctry]["Bronze"].sum()],
               "Total": [dummy[dummy["Country"] == ctry]["Total"].sum()]}

    a=pd.DataFrame(overall)

    fig1 = px.bar(
        data6[data6["Country"] == ctry],
        x='Year',
        y='Total',
        color='Season',
        barmode='group',
        title='Medals at Summer vs Winter Olympics'


    )



    fig2 = px.line(
        data6[data6["Country"] == ctry].sort_values(by="Year"),
        x='Year',
        y='Total',
        markers=True,
        title='Medal count'
    )


    fig2.update_layout(
        xaxis=dict(
            title="Year"
        ),
        yaxis=dict(
            title="Total medal counts"
        ),
        #paper_bgcolor="white",
        #plot_bgcolor="white",

    )

    st.plotly_chart(fig1,use_container_width=True)
    st.plotly_chart(fig2)

    return a



st.header("126 years of Olympic Analysis (upto 2022)")


opt=st.sidebar.radio("Select analysis type",["Sport Analysis","Athlete Analysis","Medal Analysis","Overall Medal Analysis"])

if opt=="Sport Analysis":
    year=st.sidebar.selectbox("Select an year",data6["Year"].drop_duplicates())

    sport_count(year)

if opt=="Medal Analysis":
    season=st.sidebar.selectbox("Select season",["None","Summer","Winter"])

    if season=="Summer":
        year=st.sidebar.selectbox("Select an year",data6[data6["edition"].str.contains("Summer")]["Year"].drop_duplicates())
        ctry=st.sidebar.selectbox("Select a country",data6["Country"].drop_duplicates().sort_values())

        st.subheader(f"Summer Olympic medal analysis of {ctry} in the year {year}")
        medal_tally_summer(year,ctry)




    if season=="Winter":
        year=st.sidebar.selectbox("Select an year",data6[data6["edition"].str.contains("Winter")]["Year"].drop_duplicates())
        ctry=st.sidebar.selectbox("Select a country",data6["Country"].drop_duplicates().sort_values())

        st.subheader(f"Winter Olympic medal analysis of {ctry} in the year {year}")
        medal_tally_winter(year,ctry)


    #if season=="Intercalated":
    #    st.sidebar.write("Intercalated Olympic happened in 1906")
    #    ctry=st.sidebar.selectbox("Select a country",data6["Country"].drop_duplicates().sort_values())

    #     st.subheader(f"Intercalated Olympic medal analysis of {ctry} in the year 1906")
    #    medal_tally_intercalated(ctry)
        


if opt=="Overall Medal Analysis" :
    ctry = st.sidebar.selectbox("Select a country", data6["Country"].drop_duplicates().sort_values())
    st.subheader(f"Overall medal analysis of {ctry}")
    st.dataframe(overall(ctry),hide_index=True)

if opt=="Athlete Analysis":
    ctry=st.sidebar.selectbox("Select an country",data3)
    #athlete = st.sidebar.selectbox("Select an Athlete", data2["athlete"].drop_duplicates().sort_values())
    athlete_analysis(ctry)


