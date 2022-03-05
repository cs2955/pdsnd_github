# 6 February 2022

import time
import pandas as pd
import numpy as np
import calendar

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = ""
    while city not in ['chicago','washington','new york']:
        city = input("Would you like to see data for Chicago, New York, or Washington? ").lower()
    if city == "new york":
        city = "new york city"

    # get user input for month, day, or no filtering
    date_filter = ""
    while date_filter not in ["month", "day","none"]:
        date_filter = input("Would you like to filter the data by month, day, or not at all? Type \"none\" for no time filter. ").lower()
    
    # get user input for month (all, january, february, ... , june)
    if date_filter == 'month':
        month = ""
        while month not in ['january', 'february', 'march', 'april', 'may', 'june']:
            month = input("Which month - January, February, March, April, May, or June? ").lower()
    else:
        month = "all"

   # get user input for day of week (all, monday, tuesday, ... sunday)
    if date_filter == 'day':
        day = ""
        while day not in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
            day = input("Which day - Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday? ").lower()
    else:
        day = "all"

    print('-'*40)
    return city, month, day
    


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    # load data file into a dataframe
    try:
        df = pd.read_csv(CITY_DATA[city])
    except Exception as e:
        print("{}\nError reading input file: {}".format(e,CITY_DATA[city]))
        exit()

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month)+1
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        days = ['monday','tuesday','wednesday','thursday','friday','saturday','sunday']
        day = days.index(day)
        df = df[df['day_of_week'] == day]


    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    # if filtering by month, then do not display
    if (len(df['month'].unique()) != 1):
        most_common_month = df['month'].mode()[0]
        print("Most popular month: ", calendar.month_name[most_common_month])

    # display the most common day of week
    # if filtering by day, then do not display
    # check if data is from same day of week
    if (len(df['day_of_week'].unique()) != 1):
        most_common_day = df['day_of_week'].mode()[0]
        print("Most common day of week: ", calendar.day_name[most_common_day])

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    most_common_start_hour = df['hour'].mode()[0]
    print("Most popular start hour: ", most_common_start_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    start_station_counts = df['Start Station'].value_counts()
    count = max(start_station_counts)
    station = start_station_counts[start_station_counts == count].index[0]
    print("Most common start station: {} (Count: {})".format(station,count))

    # display most commonly used end station
    end_station_counts = df['End Station'].value_counts()
    count = max(end_station_counts)
    station = end_station_counts[end_station_counts == count].index[0]
    print("Most common end station: ", station, " (Count: ",count,")")

    # display most frequent combination of start station and end station trip
    start_end_counts = df[['Start Station','End Station']].value_counts()
    count = max(start_end_counts)
    station = start_end_counts[start_end_counts == count].index[0]
    print("Most common trip from {} to {} (Count: {})".format(station[0],station[1],count))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    # convert time to Timedelta object (ns) to display days hh:mm:ss.sss
    # Trip Duration is specified in seconds
    travel_time = df['Trip Duration'].sum()
    travel_time = pd.Timedelta(travel_time*1e9)
    print("Total travel time: ", travel_time)

    # display mean travel time
    # convert time to Timedelta object (ns) to display days hh:mm:ss.sss
    mean_travel_time = df['Trip Duration'].mean()
    mean_travel_time = pd.Timedelta(mean_travel_time*1e9)
    print("Average travel time: ", mean_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print("User Types:")
    for i in user_types.index:
        print(i, user_types[i])

    # Display counts of gender
    if "Gender" in df.columns:
        genders = df['Gender'].value_counts()
        print("\nGenders:")
        for i in genders.index:
            print(i, genders[i])

    # Display earliest, most recent, and most common year of birth
    if "Birth Year" in df.columns:
        birth_year = df['Birth Year']
        print("\nBirth Year:\nMin: ", int(birth_year.min()), "\nMax: ", int(birth_year.max()), "\nMost common: ", int(birth_year.mode()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_raw_data(df):
    """Prompt user to display raw bikeshare data"""

    # set starting rows
    row = 0
    # display 5 rows at a time
    num_rows = 5
    max_rows = df.shape[0]
    while input('Would you like to view individual trip data? Type yes or no ').lower() != 'no':
        # if the end of the frame will be reached, display to end
        if (row+num_rows) > max_rows:
            print(df[row:].to_string())
        else:
            print(df[row:row+num_rows].to_string())
        row += 5
        if (row >= max_rows):
            break


def main():
    print(pd.__version__)
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        print("Displaying Data for: {}, Month: {}, Day: {}".format(city.title(),month.title(),day.title()))

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
