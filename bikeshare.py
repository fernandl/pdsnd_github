import time
import pandas as pd

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city (Chicago, Washington, New Yor City), month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    
    while True:
        city = input('Please, enter a city between Chicago, New York City and Washington to inquire about:\n').lower()
        if city not in CITY_DATA:
            print('\nYou have entered an invalid city.\nPlease chose a city between Chicago, New York City and Washington\n')
            continue
        else:
            break

    # get user input for month (all, january, february, ... , june)
    month_check = ['january','february','march','april','may','june','all']
    while True:
        month = input('Please, enter a month between january and june, or "all" to apply no filter:\n').lower()
        if month not in month_check:
            print('\nYou have entered an invalid month.\nPlease chose a month between january and june or "all"\n')
            continue
        else:
            break  

    # get user input for day of week (all, monday, tuesday, ... sunday)
    DAY_DATA = {'1':'Sunday','2':'Monday','3':'Tuesday','4':'Wednesday','5':'Thursday','6':'Friday','7':'Saturday','all':'all'}
    while True:
        day = input('Please, enter a day of the week as an integer (1=Sunday, 2=Monday, 3=Tuesday, 4=Wednesday, 5=Thursday, 6=Friday and 7=Saturday) or "all" to apply no filter: \n').lower()
        if day not in DAY_DATA:
            print('\nYou have entered an invalid choice.\nPlease chose a day between 1 and 7 or "all"\n')
            continue
        else:
            day = DAY_DATA[day]
            break     

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
    
    # Convert col to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
    # Create new columns
    df['month'] = df['Start Time'].dt.month    
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel, based in df from load_data fonction."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

     # display the most common month
    month_check = ['january','february','march','april','may','june','all']
    common_month = df['month'].mode()[0]
    print('The most common month is:', month_check[common_month-1].capitalize())
    
    # display the most common day of week
    common_day = df['day_of_week'].mode()[0]
    print('\nThe most common day is:',common_day)

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    common_hour = df['hour'].mode()[0]
    print('\nThe most common start hour is:',common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip, based in df from load_data fonction."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

   # display most commonly used start station
    common_st_station = df['Start Station'].mode()[0]
    print('The most commonly used start station is:',common_st_station)

    # display most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    print('\nThe most commonly used end station is:',common_end_station)

    # display most frequent combination of start station and end station trip
    df['conc_stations'] = df['Start Station']+' with '+df['End Station']
    common_conc_stations = df['conc_stations'].mode()[0]
    print('\nThe most frequent combination of start station and end station trip is:',common_conc_stations)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration, based in df from load_data fonction."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

     # display total travel time
    total_trip_duration = df['Trip Duration'].sum()
    print('Total travel time is: ',total_trip_duration)

    # display mean travel time
    mean_trip_duration = df['Trip Duration'].mean()
    print('\nMean travel time is: ',mean_trip_duration)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users, based in df from load_data fonction."""

    print('\nCalculating User Stats...')
    start_time = time.time()

    # Display counts of user types
    user_count = df['User Type'].value_counts() 
    for user in range(len(user_count)):
        print('\nType of user: "{}", has {} counts'.format(user_count.index[user],user_count[user]))
        

    # Display counts of gender
    try:
        gender_count = df['Gender'].value_counts() 
        for user in range(len(gender_count)):
            print('\nType of user {}, has {} counts'.format(gender_count.index[user],gender_count[user]))
    except(KeyError):
        print('\nSorry, no information about "Gender" was provided on the source file')            

    # Display earliest, most recent, and most common year of birth
    try:
        print('\nEarliest year of birth is: ', int(df['Birth Year'].min()))
        print('\nMost recent year of birth is: ', int(df['Birth Year'].max()))
        print('\nMost common year of birth is: ', int(df['Birth Year'].mode()))
    except(KeyError):
        print('\nSorry, no information about "Birth Year" was provided on the source file')            
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data(df):
    """Displays raw data based on user decision, based in df from load_data fonction"""
     
    counter = 0
    while True:
        counter = counter +5 
        show = input('Do you want to see somme raw data, five rows at a time? "Y" for yes or anything else for no\n').lower()        
        if show == 'y':
            print('Raw data:\n',df[counter-5:counter])
        else:
            break
  
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()