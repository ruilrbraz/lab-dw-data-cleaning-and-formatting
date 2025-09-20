# cleaning_functions.py

import pandas as pd

def clean_column_names(df):
    """Standardizes all column names to be lowercase and use underscores."""
    df.columns = [col.lower().replace(' ', '_') for col in df.columns]
    df.rename(columns={'st': 'state'}, inplace=True)
    return df

def clean_and_format_data(df):
    """Cleans inconsistent values and formats data types for specific columns."""
    # Clean gender
    gender_map = {'F': 'F', 'M': 'M', 'Male': 'M', 'female': 'F', 'Femal': 'F'}
    df['gender'] = df['gender'].map(gender_map)
    
    # Clean and format customer_lifetime_value
    df['customer_lifetime_value'] = df['customer_lifetime_value'].str.replace('%', '')
    df['customer_lifetime_value'] = pd.to_numeric(df['customer_lifetime_value'], errors='coerce')

    # Clean and format number_of_open_complaints
    df['number_of_open_complaints'] = df['number_of_open_complaints'].fillna('0/0/0')
    df['number_of_open_complaints'] = df['number_of_open_complaints'].apply(lambda x: x.split('/')[1])
    df['number_of_open_complaints'] = pd.to_numeric(df['number_of_open_complaints'])
    
    return df

def handle_null_values(df):
    """Drops empty rows and fills remaining NaN values with appropriate measures."""
    # Drop rows that are completely empty
    df.dropna(how='all', inplace=True)
    
    # Fill categorical columns
    df['gender'].fillna(df['gender'].mode()[0], inplace=True)
    
    # Fill numerical columns
    df['customer_lifetime_value'].fillna(df['customer_lifetime_value'].mean(), inplace=True)
    df['income'].fillna(df['income'].median(), inplace=True)
    df['monthly_premium_auto'].fillna(df['monthly_premium_auto'].mean(), inplace=True)
    
    # Drop any other rows that still have nulls
    df.dropna(inplace=True)
    return df

def convert_to_integer(df):
    """Converts all numeric columns to integer type."""
    numeric_cols = df.select_dtypes(include='number').columns
    for col in numeric_cols:
        df[col] = df[col].astype(int)
    return df


def clean_customer_data(df):
    """Main function to run all data cleaning and formatting steps."""
    df = clean_column_names(df)
    df = clean_and_format_data(df)
    df = handle_null_values(df)
    df = convert_to_integer(df)
    df.drop_duplicates(inplace=True)
    df.reset_index(drop=True, inplace=True)
    
    print("Data cleaning and formatting complete.")
    return df