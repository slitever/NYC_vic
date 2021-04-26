import pandas as pd
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

TITLE = """
            Welcome to use this Data visualization program
            This data is include NYC city 2015-present vehicle crash data.
            ==============================================================
            Select the function you want use:
"""

MENU = """
            [A] Basic report of the entire data
                - Take quick glance for the whole data
                
            [B] Data filter
                - You can use specific filter to better analysis
                
            [C] Map
                - In this function, you can use case unique key to locate
                a specific case on the map
                
"""

FILTER_MENU = """
            Date Filter
            ===============================================
            [T] Time Filter
            [Z] ZIP Code Filter
            [I] Injured Condition Filter
            [U] Unique Key Filter
"""

TIME_MENU = """
            Time Filter
            ===============================================
            [Y] Year        [B] Back
            [M] Month       [Q] Quit
            [D] Day
                 
"""

INJURED_MENU = """
            Injured Condition Filter
            ===============================================
            [1] PERSONS INJURED       [2] PERSONS KILLED
            [3] PEDESTRIANS INJURED   [4] PEDESTRIANS KILLED
            [5] CYCLISTS INJURED      [6] CYCLISTS KILLED
            [7] MOTORISTS INJURED     [8] MOTORISTS KILLED
"""

YES = "yes","Y", "y"
FILTER_OPTIONS = ["T","Z","I","U"]
MENU_OPTIONS = ["/","A","B","C"]
FILENAME = "nyc_veh_crash.csv"

def load_file():
    df = pd.read_csv(FILENAME, index_col=0)
    return df

def basic_report():
    df = load_file()
    df["NEW_TIME"] = df["DATE"] + " " + df["TIME"]
    df["NEW_TIME"] = pd.to_datetime(df["NEW_TIME"])
    # print(df["NEW_TIME"])
    time_order = df.sort_values(by="NEW_TIME")
    time_order1 = time_order["NEW_TIME"]
    st.write(f'This data is started at {time_order1.iloc[1]}')
    st.write(f'This data is end at {time_order1.iloc[-1]}')
    st.write(f'This data record {df.shape[0]} cases')
    df_borough = df["BOROUGH"].value_counts()
    df_borough1 = df["BOROUGH"].value_counts().rename_axis('Time period').to_frame('Number')
    st.write("")
    st.write(f'Number of cases that occurred in different Borough:')
    # st.write(f'{df_borough}')
    st.table(df_borough1)
    st.write(f'Most cases happened in {df_borough.idxmax()}')
    missing_case = df.shape[0] - df_borough.sum()
    st.write(f'There were {missing_case} cases where no specific Borough was recorded')

    df['HOUR'] = pd.to_datetime(df['TIME'], format='%H:%M').dt.hour
    data_hour = df["HOUR"].value_counts().sort_index()
    data_hour1 = df["HOUR"].value_counts().sort_index().rename_axis('Time period').to_frame('Number')
    st.write("")
    st.write(f'\nCase number in different time period')
    st.dataframe(data_hour1)
    st.write(f'Most cases happened during {data_hour.idxmax()}:00 ~ {(data_hour.idxmax())+1}:00')

    dict_injured_condition = {"PERSONS INJURED":[df["PERSONS INJURED"].sum()], "PERSONS KILLED":[df["PERSONS KILLED"].sum()],
            "PEDESTRIANS INJURED":[df["PEDESTRIANS INJURED"].sum()], "PEDESTRIANS KILLED":[df["PEDESTRIANS KILLED"].sum()],
            "CYCLISTS INJURED":[df["CYCLISTS INJURED"].sum()], "CYCLISTS KILLED":[df["CYCLISTS KILLED"].sum()],
             "MOTORISTS INJURED":[df["MOTORISTS INJURED"].sum()], "MOTORISTS KILLED":[df["MOTORISTS KILLED"].sum()]}
    df_injured = pd.DataFrame(dict_injured_condition, index=[0])
    st.write("")
    st.write(f'Injured Condition Summary')
    st.table(df_injured)


    if st.checkbox("Do you want to visualize the above data?"):
        # Plot
        # Borough:
        fig, ax = plt.subplots()
        ax.scatter([1, 2, 3], [1, 2, 3])
        x = df_borough.index
        y = df_borough.values
        # plt.bar(x, y)
        plt.pie(y,labels=x,autopct='%.0f%%')
        plt.title("percentage of cases that occurred in different Borough")
        st.pyplot(fig)

        # Hour:
        fig, ax = plt.subplots()
        ax.scatter([1, 2, 3], [1, 2, 3])
        x = data_hour.index
        y = data_hour.values
        plt.bar(x, y)
        plt.title("Case number in different time period")
        plt.xticks(x)
        plt.xlabel("Time period")
        plt.ylabel("Case Number")
        for a,b in zip(x,y):
            plt.text(a, b+0.05, '%.0f' % b, ha='center', va='bottom',fontsize=7)
        st.pyplot(fig)

        # Injured Condition:
        fig, ax = plt.subplots()
        ax.scatter([1, 2, 3], [1, 2, 3])
        dict_injured_condition = {"PERSONS INJURED":[df["PERSONS INJURED"].sum()], "PERSONS KILLED":[df["PERSONS KILLED"].sum()],
            "PEDESTRIANS INJURED":[df["PEDESTRIANS INJURED"].sum()], "PEDESTRIANS KILLED":[df["PEDESTRIANS KILLED"].sum()],
            "CYCLISTS INJURED":[df["CYCLISTS INJURED"].sum()], "CYCLISTS KILLED":[df["CYCLISTS KILLED"].sum()],
             "MOTORISTS INJURED":[df["MOTORISTS INJURED"].sum()], "MOTORISTS KILLED":[df["MOTORISTS KILLED"].sum()]}
        df_injured = pd.DataFrame(dict_injured_condition, index=[0])
        # print(dict_injured_condition)
        plt.bar(np.arange(8), df_injured.values[0],color="green")
        plt.xticks(np.arange(8), df_injured.columns,rotation=45, ha="right")
        plt.title(f'Injured Condition Summary')
        for a,b in zip(np.arange(8),df_injured.values[0]):
            plt.text(a, b+0.05, '%.0f' % b, ha='center', va='bottom',fontsize=10)
        st.pyplot(fig)

def data_filter_time():
    df = load_file()
    df["DATE"] = pd.to_datetime(df["DATE"])
    df["YEAR"] = pd.DatetimeIndex(df["DATE"]).year
    df["MONTH"] = pd.DatetimeIndex(df["DATE"]).month
    df["DAY"] = pd.DatetimeIndex(df["DATE"]).day

    year_list = ['/'] + list(np.sort(df["YEAR"].unique()))
    month_list = ['/'] + list(np.sort(df["MONTH"].unique()))
    day_list = ['/'] + list(np.sort(df["DAY"].unique()))

    year_type = st.sidebar.selectbox("filter-Year", year_list )
    month_type = st.sidebar.selectbox("filter-Month", month_list )
    day_type = st.sidebar.selectbox("filter-day", day_list )
    data_line = st.sidebar.selectbox("How much line data you want to see", [5, 10, 20, "all"])

    temp = df.iloc[:, :]
    if year_type != '/':
        temp = temp[temp["YEAR"] == year_type]
    if month_type != '/':
        temp = temp[temp["MONTH"] == month_type]
    if day_type != '/':
        temp = temp[temp["DAY"] == day_type]

    if data_line != "all":
        st.dataframe(temp.head(data_line))
    else:
        st.dataframe(temp)

    st.write(f"Base on your filter, there is {len(temp)} case fit your search" )

def data_filter_zip():
    df = load_file()
    comp = st.text_input("Enter the ZIP CODE: ")

    if comp == "":
        st.table(df.head())
    else:
        comp = int(comp)
        df_group = df.groupby(["ZIP CODE"]).get_group(comp)
        st.dataframe(df_group)
        st.write(f"Base on your filter, there is {len(df_group)} case fit your search" )

def data_filter_injured():
    df = load_file()
    dict_injured_condition = {1: "PERSONS INJURED", 2: "PERSONS KILLED",
                              3: "PEDESTRIANS INJURED", 4: "PEDESTRIANS KILLED",
                              5: "CYCLISTS INJURED", 6: "CYCLISTS KILLED",
                              7: "MOTORISTS INJURED", 8: "MOTORISTS KILLED"}
    st.text(INJURED_MENU)
    injured_condition = []
    for i in dict_injured_condition.keys():
        injured_condition.append(dict_injured_condition[i])
    choice = st.sidebar.selectbox("Injured Condition: ", injured_condition)
    st.write(f'Filter: {choice}')
    st.dataframe(df.loc[df[choice] != 0])
    st.write(f"Base on your filter, there is {len(df.loc[df[choice] != 0])} case fit your search" )

def data_key_filter():
    df = load_file()

    df.rename(columns={'LATITUDE':'lat', 'LONGITUDE':'lon'}, inplace=True)
    comp = st.text_input("Enter the Unique key to search: ")

    if comp == "":
        st.table(df.head())
    else:
        comp = int(comp)
        temp = df.loc[comp]

        st.dataframe(temp)

def data_map_locate():
    df = load_file()
    df.rename(columns={'LATITUDE':'lat', 'LONGITUDE':'lon'}, inplace=True)
    df["DATE"] = pd.to_datetime(df["DATE"])
    df["YEAR"] = pd.DatetimeIndex(df["DATE"]).year
    df["MONTH"] = pd.DatetimeIndex(df["DATE"]).month
    df["DAY"] = pd.DatetimeIndex(df["DATE"]).day

    year_list = ['/'] + list(np.sort(df["YEAR"].unique()))
    month_list = ['/'] + list(np.sort(df["MONTH"].unique()))
    day_list = ['/'] + list(np.sort(df["DAY"].unique()))
    borough_list = ['/'] + list(df["BOROUGH"].unique())
    del borough_list[2]


    year_type = st.sidebar.selectbox("filter-Year", year_list )
    month_type = st.sidebar.selectbox("filter-Month", month_list )
    day_type = st.sidebar.selectbox("filter-day", day_list )
    borough_type = st.sidebar.selectbox("filter-Borough", borough_list )
    data_line = st.sidebar.selectbox("How much line data you want to see", [5, 10, 20, "all"])


    temp = df.iloc[:, :]
    if year_type != '/':
        temp = temp[temp["YEAR"] == year_type]
    if month_type != '/':
        temp = temp[temp["MONTH"] == month_type]
    if day_type != '/':
        temp = temp[temp["DAY"] == day_type]
    if borough_type != "/":
        temp = temp[temp["BOROUGH"] == borough_type]


    if data_line != "all":
        st.table(temp.head(data_line))
    else:
        st.table(temp)

    st.write(f"Base on your filter, there is {len(temp)} case fit your search" )

    st.map(temp[['lat', 'lon']].dropna())

def data_borough_locate():
    df = load_file()
    df.rename(columns={'LATITUDE':'lat', 'LONGITUDE':'lon'}, inplace=True)
    borough_list = list(df["BOROUGH"].unique())
    borough_type = st.sidebar.selectbox("filter-Borough", borough_list )
    data_line = st.sidebar.selectbox("How much line data you want to see", [5, 10, 20, "all"])

    temp = df[df["BOROUGH"] == borough_type]

    if data_line != "all":
        st.table(temp.head(data_line))
    else:
        st.table(temp)

    st.map(temp[['lat', 'lon']].dropna())


    pass


def main() :
    df = load_file()
    st.text(TITLE)
    st.text(MENU)
    choice = st.selectbox("Enter your choice: ", MENU_OPTIONS)
    if choice == "/":
        st.write(df.head())

    if choice == "A" :
        basic_report()

    if choice == 'B' :
        st.text(FILTER_MENU)
        filter_choice = st.selectbox("Enter the filter you want to use:", FILTER_OPTIONS)
        if filter_choice == "T":
            data_filter_time()
        if filter_choice == "Z":
            data_filter_zip()
        if filter_choice == "I":
            data_filter_injured()
        if filter_choice == "U":
            data_key_filter()

    if choice == 'C' :
        choice = st.selectbox("Enter your choice: ", ["Time", "Borough"])
        if choice == "Time":
            data_map_locate()
        if choice == "Borough":
            data_borough_locate()


main()
