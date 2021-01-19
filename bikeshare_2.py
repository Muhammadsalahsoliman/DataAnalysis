import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
cities = ['chicago','new york city', 'washington']
months = ['all', 'january', 'february','march', 'april', 'may', 'june' ]
days = ['all','monday', 'tuesday', 'wednesday','thursday', 'friday', 'saturday', 'sunday' ]
yes_no_answer = ['yes','no']
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
    global city, month, day
    city = input("Which city would you like to analyze \n(chicago), (new york city) or (washington): ").lower()

    while city not in  cities :
        city = input("Wrong entry - please re-enter the city you would like to analyze: ").lower()


    # get user input for month (all, january, february, ... , june)
    month = input("Which month would you like to analyze \n(all, january, february, ... , june): ").lower()

    while month not in months :
        month = input("Wrong entry - please re-enter the month you would like to analyze: ").lower()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = input("Which day would you like to analyze \n(all, monday, tuesday, ... sunday): ").lower()

    while day not in days :
        day = input("Wrong entry - please re-enter the day you would like to analyze: ").lower()

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
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['Hour'] = df['Start Time'].dt.hour

    if month != 'all' :

        df = df[df['month'] == months.index(month)]

    if day != 'all':

        df = df[df['day_of_week'] == day.title()]

    return df

def display_raw_data(df):
    """
    Asks the users if they would like to view raw Data

    args:
        DataFrame
    Returns
        1st five rows of the raw Data, then next 5, then the five after as per user request
    """
    i = 0
    raw = input('\nWould you view raw data? Enter yes or no.\n').lower()
    while raw not in yes_no_answer :
        raw = input("Wrong entry - Please Enter yes or no: ").lower()

    pd.set_option('display.max_rows',200)

    while True:
        if raw == 'no':
            break

        print(df.loc[[i, i+1, i+2, i+3, i+4]]) # TO DO: appropriately subset/slice your dataframe to display next five rows
        raw = input('Would you like to see more raw data: ' ).lower()
        i += 5

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common monthg
    if month == 'all' :
        most_month = df['month'].mode()[0]
        print('The most common month was: {}'.format(most_month))
    else :
        print('you filtered by {}'.format(month))

    # display the most common day of week
    if day == 'all' :
        most_day = df['day_of_week'].mode()[0]
        print('The most common day was: {}'.format(most_day))
    else :
        print('you filtered by {}'.format(day))

    # display the most common start hour

    most_hour = df['Hour'].mode()[0]
    print('The most common hour was: {}'.format(most_hour))

    print("\nThis took %s seconds." % (time.time() - round((time.time() -start_time),2)))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_start = df['Start Station'].mode()[0]
    print('The most commonly used start station was: {}'.format(most_start))

    # display most commonly used end station
    most_end = df['End Station'].mode()[0]
    print('The most commonly used end station was: {}'.format(most_end))

    # display most frequent combination of start station and end station trip
    df['startend'] = df['Start Station'] + " - " + df['End Station']
    most_combination = df['startend'].mode()[0]
    print('The most frequent combination of start station and end station trip was: {}'.format(most_combination))

    print("\nThis took %s seconds." % (time.time() - round((time.time() -start_time),2)))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_time = round(df['Trip Duration'].sum(),2)
    print('Total Travel Time = {},'.format(total_time))
    # display mean travel time
    mean_time = round(df['Trip Duration'].mean(),1)
    print('Mean Travel Time = {},'.format(mean_time))
    print("\nThis took %s seconds." % (time.time() - round((time.time() -start_time),2)))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    countusertype = df['User Type'].value_counts()
    print('Users\' Types =\n {},'.format(countusertype))

    # Display counts of gender
    if city == 'washington' :
        print('there is no Gender and Year of Birth Data for the city of {}'.format(city))

    else:
        countgender = df['Gender'].value_counts()
        print('Users\' Gender =\n {},'.format(countgender))

    # Display earliest, most recent, and most common year of birth

        oldest = int(df['Birth Year'].max())
        youngest = int(df['Birth Year'].min())
        most_year = int(df['Birth Year'].mode())
        print('The earliest year of birth was: {}\n The most recent year of birth was: {}\n The most common year of birth was = {},'.format(oldest, youngest, most_year))

    print("\nThis took %s seconds." %  round((time.time() -start_time),2))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n').lower()
        while restart not in yes_no_answer :
            restart = input("Wrong entry - Please Enter yes or no: ").lower()
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
