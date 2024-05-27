import time
import pandas as pd

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    print('Hello! Let\'s explore some US bikeshare data!')
    while True:
        city = input('Would you like to see data for Chicago, New York City, or Washington?\n').strip().lower()
        if city in CITY_DATA:
            break
        else:
            print('Invalid input. Please enter Chicago, New York City, or Washington.')

    while True:
        month = input("Enter the name or number of the month you want to filter by (all, January, February, ..., December), for example: 'January' or '1' or 'Jan': ").strip().lower()
        if month in ['all', 'january', 'jan', '1', 'february', 'feb', '2', 'march', 'mar', '3', 'april', 'apr', '4', 'may', '5', 'june', 'jun', '6', 'july', 'jul', '7', 'august', 'aug', '8', 'september', 'sep', '9', 'october', 'oct', '10', 'november', 'nov', '11', 'december', 'dec', '12']:
            month = month[:3] if len(month) > 3 else month
            if month.isdigit():
                month = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december'][int(month) - 1]
            break
        else:
            print('Invalid input. Please enter a valid month or "all".')

    while True:
        day = input("Which day of the week? All, Monday (Mon), Tuesday (Tue), Wednesday (Wed), Thursday (Thu), Friday (Fri), Saturday (Sat), or Sunday (Sun)?\n").strip().lower()
        if day in ['all', 'monday', 'mon', 'tuesday', 'tue', 'wednesday', 'wed', 'thursday', 'thu', 'friday', 'fri', 'saturday', 'sat', 'sunday', 'sun']:
            day = day[:3] if len(day) > 3 else day
            if day.isdigit():
                print('Please enter the day in a valid format, such as "Mon" for Monday.')
            else:
                break
        else:
            print('Invalid input. Please enter a valid day of the week or "all".')

    print('-'*40)
    return city, month, day

def load_data(city, month, day):
    df = pd.read_csv(CITY_DATA[city])

    # Convert the Start Time column to datetime.
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # Extract month and day of week from Start Time to create new columns.
    df['Month'] = df['Start Time'].dt.month
    df['Day_of_Week'] = df['Start Time'].dt.day_name()

    # Filter by month if applicable.
    if month != 'all':
        # Convert month name to lowercase and check if it's a valid month.
        month = month.lower()
        if month in ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']:
            # Convert month name to month number.
            month_mapping = {
                'january': 1, 'february': 2, 'march': 3, 'april': 4,
                'may': 5, 'june': 6, 'july': 7, 'august': 8,
                'september': 9, 'october': 10, 'november': 11, 'december': 12
            }
            month = month_mapping[month]
            # Filter dataframe to include only the specified month.
            df = df[df['Month'] == month]
        else:
            print('Invalid input. Please enter a valid month or "all".')

    # Filter by day of week if applicable.
    if day != 'all':
        # Convert day name to lowercase and check if it's a valid day.
        day = day.lower()
        if day in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
            # Filter dataframe to include only the specified day of week.
            df = df[df['Day_of_Week'] == day.title()]
        else:
            print('Invalid input. Please enter a valid day of the week or "all".')

    return df


def time_stats(df):
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Convert 'Start Time' to datetime.
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # Extract month and day of week from 'Start Time' to create new columns.
    df['Month'] = df['Start Time'].dt.month
    df['Day_of_Week'] = df['Start Time'].dt.day_name()
    df['Hour'] = df['Start Time'].dt.hour

    # Display the most common month.
    common_month = df['Month'].mode()[0]
    print('Most Common Month:', common_month)

    # Display the most common day of week.
    common_day_of_week = df['Day_of_Week'].mode()[0]
    print('Most Common Day of Week:', common_day_of_week)

    # Display the most common start hour.
    common_start_hour = df['Hour'].mode()[0]
    print('Most Common Start Hour:', common_start_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    # Print a message indicating that the calculation of popular stations and trips is starting.
    print('\nCalculating The Most Popular Stations and Trip...\n')
    
    # Record the start time to measure the duration of the function execution.
    start_time = time.time()

    # Check if the necessary columns exist in the dataframe.
    if 'Start Station' in df.columns and 'End Station' in df.columns:
        # Display the most commonly used start station.
        common_start_station = df['Start Station'].mode()[0]
        print('Most Common Start Station:', common_start_station)

        # Display the most commonly used end station.
        common_end_station = df['End Station'].mode()[0]
        print('Most Common End Station:', common_end_station)

        # Create a new column 'Trip' that concatenates the start and end stations to represent a trip.
        df['Trip'] = df['Start Station'] + ' to ' + df['End Station']
        
        # Display the most frequent combination of start station and end station trip.
        common_trip = df['Trip'].mode()[0]
        print('Most Common Trip:', common_trip)
    else:
        # Print a message if the required station information is not available in the dataframe.
        print('Station information is not available for this dataset.')

    # Print the duration of the function execution.
    print("\nThis took %s seconds." % (time.time() - start_time))
    # Print a separator for readability in the output.
    print('-'*40)

def trip_duration_stats(df):
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Check if necessary column exists in the dataframe.
    if 'Trip Duration' in df.columns:
        # Display total travel time.
        total_travel_time = df['Trip Duration'].sum()
        print('Total Travel Time:', total_travel_time)

        # Display mean travel time.
        mean_travel_time = df['Trip Duration'].mean()
        print('Mean Travel Time:', mean_travel_time)
    else:
        print('Trip duration information is not available for this dataset.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Check if necessary columns exist in the dataframe.
    if 'User Type' in df.columns:
        # Display counts of user types.
        user_types = df['User Type'].value_counts()
        print('Counts of User Types:\n', user_types)
    else:
        print('User type information is not available for this dataset.')

    if 'Gender' in df.columns:
        gender_counts = df['Gender'].value_counts()
        print('Counts of Gender:\n', gender_counts)
    else:
        print('Gender information is not available for this dataset.')

    if 'Birth Year' in df.columns:
        earliest_birth_year = int(df['Birth Year'].min())
        print('Earliest Birth Year:', earliest_birth_year)
        
        most_recent_birth_year = int(df['Birth Year'].max())
        print('Most Recent Birth Year:', most_recent_birth_year)
        
        most_common_birth_year = int(df['Birth Year'].mode()[0])
        print('Most Common Birth Year:', most_common_birth_year)
    else:
        print('Birth year information is not available for this dataset.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_data(df):
    view_data = input("Would you like to view 5 rows of individual trip data? Enter y/n: ").strip().lower()
    start_loc = 0
    while view_data == 'y':
        if start_loc >= len(df):
            print("No more data to display.")
            break
        elif start_loc + 5 >= len(df):
            print(df.iloc[start_loc:])
            print("No more data to display.")
            break
        else:
            print(df.iloc[start_loc:start_loc + 5])
            start_loc += 5
            view_data = input("Do you wish to continue?: ").strip().lower()

def main():
    while True:
        # Get user inputs for city, month, and day to filter the data
        city, month, day = get_filters()
        
        # Load the data based on the user inputs
        df = load_data(city, month, day)

        # Display statistics on the most frequent times of travel
        time_stats(df)
        
        # Display statistics on the most popular stations and trip
        station_stats(df)
        
        # Display statistics on the total and average trip duration
        trip_duration_stats(df)
        
        # Display statistics on bikeshare users
        user_stats(df)
        
        # Optionally display raw data upon user's request
        display_data(df)
        
        # Ask the user if they want to restart the analysis
        restart = input('\nWould you like to restart? Enter y/n.\n')
        
        # Break the loop if the user does not want to restart
        if restart.lower() != 'y':
            break

# Run the main function when the script is executed
if __name__ == "__main__":
    main()

