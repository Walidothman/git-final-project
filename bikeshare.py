# This is the bikeshare python project
#Refactor 1 
import time
import pandas as pd
import numpy as np
import calendar
from datetime import datetimm

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
def get_filters():

    def checkIfMatch(user_input,lst):

        if len(elem) == 5:
            return True;
        else :
            return False;

    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = str(input("Please specify as city (chicago, new york city, washington): ")).lower()

    while city not in CITY_DATA:
        print('invalid entry')
        city = str(input("Please specify another city: "))
        if city in CITY_DATA:
            break;

    lst_months = ("all", "january","february","march","april","may","june","july","august",
                  "september","october","november","december")

    # TO DO: get user input for month (all, january, february, ... , june)
    month = str(input("Please specify a month or type all: ")).lower()
    while month not in lst_months:
        print('invalid entry')
        month = str(input("Please specify a valid month or type all: "))
        if month in lst_months:
            break;

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    lst_days = ("all","monday","tuesday","wednesday","thursday","friday","saturday","sunday")

    day = str(input("Please specify a day or type all: ")).lower()
    while day not in lst_days:
        print('invalid entry')
        day = str(input("Please specify a valid day or type all: "))
        if day in lst_days:
            break;

    print('-'*40)
    return city, month, day


# In[3]:


def load_data(city, month, day):

#     lst_d = ["monday","tuesday","wednesday","thursday","friday","saturday","sunday"]
    lst_m = ["january","february","march","april","may","june","july","august",
                  "september","october","november","december"]

    def index_convertor(lst_d,txt):
        return lst_d.index(txt) + 1

    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
#     dateparse = lambda x: pd.datetime.strptime(x, '%Y-%m-%d %H:%M:%S')
#     df = pd.read_csv(city +'.csv',parse_dates=['Start Time'],date_parser=dateparse)
    fname = CITY_DATA[city]
    df = pd.read_csv(fname,parse_dates=['Start Time'])

    df['Start Time']= pd.to_datetime(df['Start Time'])
    df['End Time']= pd.to_datetime(df['End Time'])

#     df['End Station']= pd.to_datetime(df['End Station'])

    df['Start_Month'] = df['Start Time'].dt.month
    df['End_Month'] = df['End Time'].dt.month

    df['Start_DayName'] = df['Start Time'].dt.weekday_name
    df['End_DayName'] = df['End Time'].dt.weekday_name

    df['Start_Hour'] = df['Start Time'].dt.hour


    df['Start_Month'] = df['Start_Month'].apply(lambda x: calendar.month_name[x])
    df['End_Month'] = df['End_Month'].apply(lambda x: calendar.month_name[x])

    df['diff_minutes'] = df['End Time'] - df['Start Time']
    df['diff_minutes']=df['diff_minutes']/np.timedelta64(1,'m')

    if (month != 'all'):
        month_nb = index_convertor(lst_m,month)
        df = df[df['Start_Month'].str.lower() == month]
        df = df[df['End_Month'].str.lower() == month]

    if (day != 'all'):
#         day_nb = index_convertor(lst_d,day)
        df = df[df['Start_DayName'].str.lower() == day]
        df = df[df['End_DayName'].str.lower() == day]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    print('the most common month is',df['Start_Month'].value_counts().idxmax())

    # TO DO: display the most common day of week
    print('the most common day of week is',df['Start_DayName'].value_counts().idxmax())

    # TO DO: display the most common start hour
    hr = df['Start_Hour'].value_counts().idxmax()
    d = datetime.strptime(str(hr), "%H")
    d = d.strftime("%I %p")

    print('the most common hour is',d)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    print('the most commonly used start station is',df['Start Station'].value_counts().idxmax())

    # TO DO: display most commonly used end station
    print('the most commonly used end station is',
          df.groupby(['End Station']).size().idxmax())
#           df['End Station'].value_counts().idxmax())

    # TO DO: display most frequent combination of start station and end station trip
    print('the most frequent combination of start station and end station trip',
          df.groupby(['Start Station','End Station']).size().idxmax())


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()


    print('total travel time is ',df['diff_minutes'].sum())

    print('mean travel time is ',df['diff_minutes'].mean())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    try:
    # TO DO: Display counts of user types
        print(df['User Type'].value_counts())
    except:
        print("Missing Type")

    print('---------------------------------------------------')
    # TO DO: Display counts of gender


    try:
        print(df['Gender'].value_counts())
    except:
        print("Missing Gender")

    print('---------------------------------------------------')

    try:

    #     # TO DO: Display earliest, most recent, and most common year of birth
        print('earliest year of birth is',str(df['Birth Year'].min()).replace('.0', ''))

        print('most recent year of birth is',str(df['Birth Year'].max()).replace('.0', ''))

        print('common year of birth is',str(df['Birth Year'].value_counts().idxmax()).replace('.0', ''))

    except:
        print("Missing Birth Year")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
    main()
