import time
import pandas as pd
import numpy as np


CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }

MONTHS = ['january',
              'february',
              'march',
             'april',
             'may',
             'june',
             'all']

WRONG_MONTHS = ['july',
                'august',
                'september',
                'october',
                'november',
                'december']

CITIES = ['chicago',
          'new york',
          'washington']

DAYS = ['monday',
              'tuesday',
              'wednesday',
             'thursday',
             'friday',
             'saturday',
            'sunday',
            'all']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.
    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    
    try:
        city = input('Which city\'s data would you like to see? - Chicago, New York or Washington?: ').lower()
        while city not in CITIES:
            print('Looks like your input is not in our list. Wanna check your spelling, including spaces and try again?')
            city = input('Which city\'s data would you like to see? - Chicago, New York or Washington?: ').lower()
           
        month = input('Would you like to filter by a specific month? Enter the month(in words) or \"all\" to apply no filter: ').lower()
        while month not in MONTHS:
            if month in WRONG_MONTHS:
                print('Oops, we only have data from January to June. Wanna try again?')
            else:
                print('Can you cross check your spelling? Make sure you are spelling the month name, and not using a number')  
            month = input('Would you like to filter by a specific month? Enter the month(in words) or \"all\" to apply no filter: ').lower()        
    
        day = input('Would you like to filter by a specific day? Enter the day(in words) or \"all\" to apply no filter: ').lower()
        while day not in DAYS:
            print('Not sure the day is correctly spelled. Check again?')  
            day = input("Would you like to filter by a specific day? Enter the day(in words) or \"all\" to apply no filter: ").lower()
            
        return city, month, day
        print(f"\nSelected variables: city: {city.title()}, month: {month.title()} and day: {day.title()}.")
        
    except Exception as e:
        print('An error with your inputs occured: {}'.format(e))
    print('-'*40)
    

        
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
    df['End Time'] = pd.to_datetime(df['End Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name 
    df['hour'] = df['Start Time'].dt.hour

        # filter by month if applicable
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = MONTHS.index(month) + 1 
    
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()] 
    return df
    

def time_stats(df, city):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    
    # display the most common month
    popular_month_num = df['Start Time'].dt.month.mode()[0]
    popular_month = MONTHS[popular_month_num-1].title()
    print('The most popular month in {} is {}'.format(city.title(), popular_month))

    # display the most common day of week
    pop_weekday = df['day_of_week'].mode()[0]
    print('The most popular week day in {} is {}'.format(city.title(), pop_weekday))

    # display the most common start hour
    pop_hour = df['hour'].mode()[0]
    print('The most popular starting hour in {} is {}'.format(city.title(),pop_hour))
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
    
def station_stats(df, city):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    df['Full_routes'] = df['Start Station']+ " to " + df['End Station']
    
    Common_start_station = df['Start Station'].mode()[0]
    Common_end_station = df['End Station'].mode()[0]
    Common_route = df['Full_routes'].mode()[0]

    print('For {},'.format(city.title()))   
    print('The most popular start station is {}'.format(Common_start_station))
    print('The most popular end station is {}'.format(Common_end_station))
    print('The most popular route is from {}'.format(Common_route))        

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
  

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    df['duration'] = df['End Time'] - df['Start Time']
    sum_travel_time = df['duration'].sum()   
    print(f"The total trip duration is {sum_travel_time} hours, minutes and seconds.")
    mean_travel_time = df['duration'].mean()
    print(f"The average trip duration is {mean_travel_time} hours, minutes and seconds.")
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


    
def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()
    user_type = df['User Type'].value_counts()

    print(f"Types of users in {city.title()} by number:\n\n{user_type}")

    #Washington has no gender column, therefore
    try:
        gender = df['Gender'].value_counts()
        print(f"\nTypes of users in {city.title()} by gender:\n\n{gender}")
    except:
        print(f"\nNo 'Gender' column in {city.title()} file.")

    #Same scenario here
    try:
        earliest = int(df['Birth Year'].min())
        most_recent = int(df['Birth Year'].max())
        common_year = int(df['Birth Year'].mode()[0])
        print(f"\nThe earliest year of birth: {earliest}\nThe most recent year of birth: {most_recent}\nThe most common year of birth: {common_year}")
    except:
        print(f"No birth year details in {city.title()} file.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
def display_csv_data(df):
    """Displays raw data to user """
     
    counter = 0
    accepted_answers = ['yes','no']
    response = ''
    while response not in accepted_answers:
        response = input("Do you want to see the raw data? Enter 'yes' or 'no': ").lower()    
        if response == 'yes':
            print(df.head())
        elif response not in accepted_answers:
            print('Please ensure you\'re choosing yes or no')
            print('Let\'s try again!')
            
    while response == 'yes':  
        counter += 5
        stop_display = input("Do you wish to continue? Enter 'yes' or 'no': ").lower()
        if stop_display == 'yes':
            print(df[counter:counter+5])       
        elif stop_display != 'yes':
            break
print('-'*40)

    
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df, city)
        station_stats(df, city)
        trip_duration_stats(df)
        user_stats(df, city)
        display_csv_data(df)
        
        restart = input("\nWould you like to restart? Enter 'y' for 'yes', 'n' for 'no': \n")
        if restart.lower() != 'y':
            break


if __name__ == "__main__":
	main()