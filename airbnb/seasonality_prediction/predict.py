import pandas as pd
from sklearn.preprocessing import OrdinalEncoder

calendar_data = pd.read_csv("calendar.csv")
listings_data = pd.read_csv("listings.csv")
encoder = OrdinalEncoder()

calendar_data["price"] = pd.to_numeric(calendar_data["price"].replace(r"[\$,€£,]", "", regex=True), errors="coerce")
calendar_data["adjusted_price"] = pd.to_numeric(calendar_data["adjusted_price"].replace(r"[$,]", "", regex=True), errors="coerce")
calendar_data["adjusted_price"] = calendar_data["adjusted_price"].fillna(calendar_data["price"])

calendar_data[["available"]] = encoder.fit_transform(calendar_data[["available"]])
calendar_data["date"] = pd.to_datetime(calendar_data["date"], format="mixed")
calendar_data["adjusted_price"] = calendar_data["adjusted_price"].fillna(calendar_data["price"])

calendar_data["month"] = calendar_data["date"].dt.month
calendar_data["season"] = calendar_data["date"].dt.month.map({
        12: "Winter", 1: "Winter", 2: "Winter",
        3: "Spring", 4: "Spring", 5: "Spring",
        6: "Summer", 7: "Summer", 8: "Summer",
        9: "Autumn", 10: "Autumn", 11: "Autumn"
    })
calendar_data["booking_duration"] = calendar_data.groupby(
                                            (calendar_data["available"] != calendar_data["available"].shift())
                                            .cumsum())["available"].transform('sum')

calendar_data = calendar_data.merge(listings_data[['id', 'property_type']], 
                                     left_on='listing_id', right_on='id', how='left')
calendar_data["property_type"] = calendar_data["property_type"].fillna("Unknown")

calendar_data[["property_type"]] = encoder.fit_transform(calendar_data[["property_type"]])

calendar_data = calendar_data[:400]

seasonality_data = {
        'avg_booking_length_by_season': calendar_data.groupby('season')['booking_duration'].mean(),
        'occupancy_rates_by_season': calendar_data.groupby('season')['available'].mean() * 100,
        'avg_daily_rate_by_season': calendar_data.groupby('season')['price'].mean(),
        'monthly_booking_distribution': calendar_data['month'].value_counts(normalize=True) * 100,
        'property_type_seasonality': calendar_data.groupby(['season', 'property_type'])['available'].mean().unstack()
    }

best_performing_by_season = seasonality_data['property_type_seasonality'].idxmin(axis=1)
best_performing_by_season_inversed = encoder.inverse_transform(best_performing_by_season.values.reshape(-1, 1))

insights = {
        'best_season': seasonality_data['occupancy_rates_by_season'].idxmax(),
        'worst_season': seasonality_data['occupancy_rates_by_season'].idxmin(),
        'highest_avg_daily_rate_season': seasonality_data['avg_daily_rate_by_season'].idxmax(),
        'peak_booking_months': seasonality_data['monthly_booking_distribution'].nlargest(2).index.tolist(),
        'property_type_highest_occupency_rate_season': {season: property_type[0]
                                                        for season, property_type in zip(best_performing_by_season.index, best_performing_by_season_inversed)}
    }

print(insights)