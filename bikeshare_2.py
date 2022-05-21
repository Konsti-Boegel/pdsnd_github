import time
import pandas as pd
import numpy as np
import pprint

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

cities = ['chicago', 'new york city', 'washington']
months = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
days = ['all', 'm', 'tu', 'w', 'th', 'f', 'sa', 'su']

chosen_city = ''

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

    valid = True

    while valid:
        city = input('Do you want to analyze Chicago, New York City or Washington?\n').lower()
        if city in cities:
            valid = False
            break
        else:
            print('Invalid answer. Please try again.')

    # get user input for month (all, january, february, ... , june)

    valid = True

    while valid:
        month = input('Which month do you want to filter? All, January, February, March, April, May or June.\n').lower()
        if month in months:
            valid = False
            break
        else:
            print('Invalid answer. Please try again.')

    # get user input for day of week (all, monday, tuesday, ... sunday)

    valid = True

    while valid:
        day = input('Which day do you want to filter? All, M, Tu, W, Th, F, Sa or Su.\n').lower()
        if day in days:
            valid = False
            break
        else:
            print('Invalid answer. Please try again.')

    global chosen_city
    chosen_city = city

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

    df = pd.read_csv(CITY_DATA[city])

    # Handle NaN Values

    if city != 'washington':
        df['Birth Year'] = df['Birth Year'].fillna(value=0)

    # Convert Start Time and End Time to Date-type

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])

    # Convert remaining Columns to fitting Data Types

    if city != 'washington':
        df = df.astype({'Trip Duration': int, 'Start Station': str, 'End Station': str, 'User Type': str, 'Gender': str, 'Birth Year': int})
    else:
        df = df.astype({'Trip Duration': int, 'Start Station': str, 'End Station': str, 'User Type': str})

    # Extract Month and Weekday (Monday=0 ... Sunday=6) to separate columns

    df['month'] = df['Start Time'].dt.month
    df['day'] = df['Start Time'].dt.weekday
    df['hour'] = df['Start Time'].dt.hour

    # Filter df for month

    if month == 'january':
        filter_month = df['month'] == 1
    elif month == 'february':
        filter_month = df['month'] == 2
    elif month == 'march':
        filter_month = df['month'] == 3
    elif month == 'april':
        filter_month = df['month'] == 4
    elif month == 'may':
        filter_month = df['month'] == 5
    elif month == 'june':
        filter_month = df['month'] == 6
    elif month == 'all':
        filter_month = df['month'] >= 1
    else:
        print('Somethin went wrong: Month Filter')

    df = df[filter_month]

    # Filter df for day of week

    if day == 'm':
        filter_day = df['day'] == 0
    elif day == 'tu':
        filter_day = df['day'] == 1
    elif day == 'w':
        filter_day = df['day'] == 2
    elif day == 'th':
        filter_day = df['day'] == 3
    elif day == 'f':
        filter_day = df['day'] == 4
    elif day == 'sa':
        filter_day = df['day'] == 5
    elif day == 'su':
        filter_day = df['day'] == 6
    elif day == 'all':
        filter_day = df['day'] >= 0
    else:
        print('Somethin went wrong: Day Filter')

    df = df[filter_day]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    temp_month = ['January', 'February', 'March', 'April', 'May', 'June']
    temp_day = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    # display the most common month

    popular_month = df['month'].mode()[0]
    print('Most popular start month: ', temp_month[popular_month-1])

    # display the most common day of week

    popular_day = df['day'].mode()[0]
    print('Most popular start day: ', temp_day[popular_day])

    # display the most common start hour

    popular_hour = df['hour'].mode()[0]
    print('Most popular start hour: ', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station

    popular_start_station = df['Start Station'].mode()[0]
    print('Most popular start station: ', popular_start_station)

    # display most commonly used end station

    popular_end_station = df['End Station'].mode()[0]
    print('Most popular end station: ', popular_end_station)

    # display most frequent combination of start station and end station trip

    popular_station_comb = (df['Start Station'] + ' and ' + df['End Station']).mode()[0]
    print('Most popular start station and end station combination: ', popular_station_comb)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time

    total_travel_time = df['Trip Duration'].sum(0)
    print('The total travel time is: ', total_travel_time, ' seconds')

    # display mean travel time

    mean_travel_time = df['Trip Duration'].mean(0).round(2)
    print('The total travel time is: ', mean_travel_time, ' seconds')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types

    user_types = df['User Type'].value_counts()
    print('User Types:\n', user_types, '\n')

    # Display counts of gender
    if chosen_city != 'washington':
        genders = df['Gender'].value_counts()
        print('Genders:\n', genders, '\n')

    # Display earliest, most recent, and most common year of birth

    if chosen_city != 'washington':
        earliest_year = df['Birth Year'][df['Birth Year'] > 0].min(0)
        latest_year = df['Birth Year'].max(0)
        common_year = df['Birth Year'][df['Birth Year'] > 0].mode()[0]
        print('The earliest birth year is: {}\nThe most recent birth year is: {}\nThe most common birth year is: {}'.format(earliest_year, latest_year, common_year))

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

        keep_going = True

        raw_input = input('\nWould you like to see the raw data? Enter yes or no.\n')
        if raw_input.lower() == 'yes':
            index = [0,5]
            while keep_going:
                print(df.iloc[index[0]:index[1]])
                index[0] += 5
                index[1] += 5

                more = input('Do you want to see 5 more rows? Enter yes or no.\n')
                if more.lower() != 'yes':
                    keep_going = False
                    break

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
    