from numpy import rint
import pandas as pd
import os
from pathlib import Path
base_dir = os.path.dirname(os.path.abspath(__file__))
from datetime import datetime

def load_data(file_path):
    try:
        df = pd.read_csv(file_path)
        print("Dataset loaded successfully.\n")
        return df
    except Exception as e:
        print(f"Error loading file: {e}")
        return None


def filter_data(df, sentiment=None, 
                start_date=None, end_date=None):
    
    filtered_df = df.copy()

    if sentiment:
        filtered_df = filtered_df[filtered_df["Sentiment"] == sentiment]

    if start_date:
        filtered_df = filtered_df[pd.to_datetime(filtered_df["Date"]) >= pd.to_datetime(start_date)]

    if end_date:
        filtered_df = filtered_df[pd.to_datetime(filtered_df["Date"]) <= pd.to_datetime(end_date)]

    return filtered_df


def sort_data(df, column_name, ascending=True):
    try:
        return df.sort_values(by=column_name, ascending=ascending)
    except KeyError:
        print("Invalid column name for sorting.")
        return df


def sentiment_ratio(df):
    positive_count = len(df[df["Sentiment"].str.lower() == "positive"])
    negative_count = len(df[df["Sentiment"].str.lower() == "negative"])

    if positive_count == 0:
        ratio = "Undefined (no positive reviews)"
    else:
        ratio = negative_count / positive_count

    print("\n--- Sentiment Analysis ---")
    print(f"Positive Reviews: {positive_count}")
    print(f"Negative Reviews: {negative_count}")
    print(f"Negative to Positive Ratio: {ratio}")

    return ratio


def main():
    file_name = 'EuropeanRestaurantReviews.csv'
    file_path = os.path.join(base_dir, file_name)
    df = load_data(file_path)

    if df is None:
        return

    print("\nAvailable columns:", df.columns.tolist())

    sentiment = input("Filter by Sentiment (Positive/Negative or press Enter to skip): ") or None
    start_date = input("Start Date (YYYY-MM-DD or press Enter to skip): ") or None
    end_date = input("End Date (YYYY-MM-DD or press Enter to skip): ") or None

    filtered_df = filter_data(df, sentiment, start_date, end_date)

    print(f"\nFiltered Results: {len(filtered_df)} rows found.")

    sort_column = input("Enter column to sort by (or press Enter to skip): ")
    if sort_column:
        order = input("Sort ascending? (yes/no): ").lower()
        ascending = True if order == "yes" else False
        filtered_df = sort_data(filtered_df, sort_column, ascending)

    print("\nPreview of Data:")
    print(filtered_df.head())

    sentiment_ratio(filtered_df)


if __name__ == "__main__":
    main()