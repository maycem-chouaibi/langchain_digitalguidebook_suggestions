import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def analyze_seasonality(df):
    """
    Comprehensive seasonality analysis for Airbnb bookings
    
    Parameters:
    df (pandas.DataFrame): Dataframe with Airbnb booking data
    
    Returns:
    dict: Detailed seasonality insights
    """
    # Ensure date columns are in datetime format
    df['booking_date'] = pd.to_datetime(df['booking_date'])
    df['available_date'] = pd.to_datetime(df['available_date'])
    
    # Extract month and season
    df['month'] = df['booking_date'].dt.month
    df['season'] = df['booking_date'].dt.month.map({
        12: 'Winter', 1: 'Winter', 2: 'Winter',
        3: 'Spring', 4: 'Spring', 5: 'Spring',
        6: 'Summer', 7: 'Summer', 8: 'Summer',
        9: 'Autumn', 10: 'Autumn', 11: 'Autumn'
    })
    
    # Seasonality metrics
    seasonality_analysis = {
        # Average booking length by season
        'avg_booking_length_by_season': df.groupby('season')['booking_duration'].mean(),
        
        # Occupancy rates by season
        'occupancy_rates_by_season': df.groupby('season')['is_booked'].mean() * 100,
        
        # Average daily rate by season
        'avg_daily_rate_by_season': df.groupby('season')['price'].mean(),
        
        # Booking patterns by month
        'monthly_booking_distribution': df['month'].value_counts(normalize=True) * 100,
        
        # Seasonal property type performance
        'property_type_seasonality': df.groupby(['season', 'property_type'])['is_booked'].mean().unstack()
    }
    
    # Visualize seasonality
    plt.figure(figsize=(15, 10))
    
    # Seasonal Occupancy Rates
    plt.subplot(2, 2, 1)
    seasonality_analysis['occupancy_rates_by_season'].plot(kind='bar')
    plt.title('Occupancy Rates by Season')
    plt.ylabel('Occupancy Rate (%)')
    
    # Average Daily Rate by Season
    plt.subplot(2, 2, 2)
    seasonality_analysis['avg_daily_rate_by_season'].plot(kind='bar')
    plt.title('Average Daily Rate by Season')
    plt.ylabel('Average Price')
    
    # Monthly Booking Distribution
    plt.subplot(2, 2, 3)
    seasonality_analysis['monthly_booking_distribution'].plot(kind='bar')
    plt.title('Monthly Booking Distribution')
    plt.ylabel('Percentage of Bookings')
    plt.xlabel('Month')
    
    # Seasonal Property Type Performance Heatmap
    plt.subplot(2, 2, 4)
    sns.heatmap(seasonality_analysis['property_type_seasonality'], annot=True, cmap='YlGnBu')
    plt.title('Property Type Performance by Season')
    
    plt.tight_layout()
    plt.savefig('airbnb_seasonality_analysis.png')
    
    return seasonality_analysis

def identify_seasonal_trends(seasonality_data):
    """
    Interpret seasonality analysis results
    
    Parameters:
    seasonality_data (dict): Output from analyze_seasonality function
    
    Returns:
    dict: Key insights and recommendations
    """
    insights = {
        'best_performing_season': seasonality_data['occupancy_rates_by_season'].idxmax(),
        'worst_performing_season': seasonality_data['occupancy_rates_by_season'].idxmin(),
        'highest_avg_daily_rate_season': seasonality_data['avg_daily_rate_by_season'].idxmax(),
        'peak_booking_months': seasonality_data['monthly_booking_distribution'].nlargest(3).index.tolist(),
        'recommendations': []
    }
    
    # Generate recommendations based on analysis
    recommendations = [
        f"Peak booking season is {insights['best_performing_season']}, consider adjusting pricing strategies",
        f"Lowest occupancy is in {insights['worst_performing_season']}, explore promotional activities",
        f"Highest average daily rates occur in {insights['highest_avg_daily_rate_season']}",
        f"Focus marketing efforts on peak months: {', '.join(map(str, insights['peak_booking_months']))}",
        "Consider dynamic pricing model that adapts to seasonal variations"
    ]
    
    insights['recommendations'] = recommendations
    
    return insights

# Example usage comment
"""
# Assuming df is your Airbnb dataset with columns:
# - booking_date
# - available_date
# - booking_duration
# - is_booked
# - price
# - property_type

# seasonality_results = analyze_seasonality(df)
# seasonal_insights = identify_seasonal_trends(seasonality_results)
# print(seasonal_insights)
"""