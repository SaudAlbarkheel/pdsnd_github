import time
import pandas as pd
import numpy as np

# Dictionary containing city data files
CITY_DATA = {
    'chicago': 'chicago.csv',
    'new york city': 'new_york_city.csv',
    'washington': 'washington.csv'
}

def get_user_input(prompt, valid_options):
    """Handles user input and ensures it matches valid options."""
    while True:
        user_input = input(prompt).strip().lower()
        if user_input in valid_options:
            return user_input
        print("Invalid input. Please try again.")

def get_filters():
    """Gets user input for city, month, and day to analyze."""
    print("\nWelcome! Let's analyze some US bikeshare data!\n")
    
    city = get_user_input("Choose a city (Chicago, New York City, Washington): ", CITY_DATA.keys())
    months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
    month = get_user_input("Select a month (January to June) or 'all': ", months)
    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']
    day = get_user_input("Pick a day (Monday to Sunday) or 'all': ", days)
    
    print('-'*40)
    return city, month, day

def load_data(city, month, day):
    """Loads data for the selected city and applies month and day filters."""
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour
    
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        df = df[df['month'] == (months.index(month) + 1)]
    
    if day != 'all':
        df = df[df['day_of_week'] == day.title()]
    
    return df

def display_common_value(df, column, description):
    """Prints the most common value for a given column."""
    print(f"{description}: {df[column].mode()[0]}")

def time_stats(df):
    """Displays statistics on the most frequent travel times."""
    print('\nAnalyzing Travel Time Statistics...\n')
    display_common_value(df, 'month', "Most Frequent Month")
    display_common_value(df, 'day_of_week', "Most Frequent Day")
    display_common_value(df, 'hour', "Most Frequent Start Hour")
    print('-'*40)

def station_stats(df):
    """Displays statistics on popular start and end stations, and trips."""
    print('\nAnalyzing Station Usage...\n')
    display_common_value(df, 'Start Station', "Most Popular Start Station")
    display_common_value(df, 'End Station', "Most Popular End Station")
    df['Trip Route'] = df['Start Station'] + " to " + df['End Station']
    display_common_value(df, 'Trip Route', "Most Common Trip Route")
    print('-'*40)

def trip_duration_stats(df):
    """Calculates total and average trip durations."""
    print('\nAnalyzing Trip Durations...\n')
    print(f"Total Duration: {df['Trip Duration'].sum()} seconds")
    print(f"Average Duration: {df['Trip Duration'].mean()} seconds")
    print('-'*40)

def user_stats(df):
    """Provides statistics on bikeshare users."""
    print('\nAnalyzing User Demographics...\n')
    print(f"User Types Count:\n{df['User Type'].value_counts()}")
    if 'Gender' in df:
        print(f"Gender Count:\n{df['Gender'].value_counts()}")
    if 'Birth Year' in df:
        print(f"Earliest Birth Year: {int(df['Birth Year'].min())}")
        print(f"Latest Birth Year: {int(df['Birth Year'].max())}")
        print(f"Most Frequent Birth Year: {int(df['Birth Year'].mode()[0])}")
    print('-'*40)

def display_data(df):
    """Displays raw data upon user request in 5-row increments."""
    start_loc = 0
    while True:
        show_data = input("Would you like to view 5 rows of raw data? Enter yes or no: ").strip().lower()
        if show_data == 'yes':
            print(df.iloc[start_loc:start_loc + 5])
            start_loc += 5
            if start_loc >= len(df):
                print("No more data available.")
                break
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
        display_data(df)
        
        restart = input('\nWould you like to restart the analysis? Enter yes or no.\n').strip().lower()
        if restart != 'yes':
            break

if __name__ == "__main__":
    main()
