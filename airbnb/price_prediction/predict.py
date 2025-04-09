import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.decomposition import PCA
from sklearn.model_selection import RandomizedSearchCV

categorical_features = ["property_type", "room_type", "neighbourhood_cleansed"]
features = ["neighborhood_cluster", "bathrooms", "bedrooms", "beds", 
            "review_scores_value", "review_scores_accuracy", "amenities_count",
            "review_scores_cleanliness", "review_scores_location", 
            "accommodates", "minimum_nights", "maximum_nights", "number_of_reviews",
            "host_is_superhost"]
    
def amenities_n_components(amenities: list) -> int:
    scaler = StandardScaler()
    amenities_scaled = scaler.fit_transform(amenities)
    pca = PCA()

    pca.fit(amenities_scaled)
    explained_variance_ratio = pca.explained_variance_ratio_

    cumulative_explained_variance = np.cumsum(explained_variance_ratio)
    n_components = np.argmax(cumulative_explained_variance >= 0.90) + 1

    return n_components

def clean_amenities(listings_data: pd.DataFrame) -> pd.DataFrame:
    mlb = MultiLabelBinarizer()
    amenities_encoded = pd.DataFrame(mlb.fit_transform(listings_data["amenities"]), columns=mlb.classes_)
    n_components = amenities_n_components(amenities_encoded)

    scaler = StandardScaler()
    amenities_scaled = scaler.fit_transform(amenities_encoded)

    pca = PCA(n_components=n_components)
    amenities_pca = pca.fit_transform(amenities_scaled)
    amenities_pca_df = pd.DataFrame(amenities_pca, columns=[f"amenity_pca_{i}" for i in range(n_components)])

    return amenities_pca_df

def encode_categorical_features(listings_data: pd.DataFrame, categorical_features: list) -> pd.DataFrame:
    categorical_transformer = OneHotEncoder(handle_unknown="ignore", sparse_output=False)
    preprocessor = ColumnTransformer(transformers=[("cat", categorical_transformer, categorical_features)], 
                                     remainder="passthrough")
    
    encoded_features = preprocessor.fit_transform(listings_data[categorical_features])
    encoded_feature_names = (preprocessor.named_transformers_['cat'].get_feature_names_out(categorical_features).tolist())
    encoded_df = pd.DataFrame(encoded_features, columns=encoded_feature_names, index=listings_data.index)
    
    return encoded_df

def prepare_data(file_path: str) -> tuple:
    listings_data = pd.read_csv(file_path)

    listings_data["price"] = listings_data["price"].replace(r"[$,]", "", regex=True).astype(float)
    listings_data["price"] = listings_data["price"].fillna(listings_data["price"].median())
    listings_data["log_price"] = np.log1p(listings_data["price"])   
    listings_data["instant_bookable"] = listings_data["instant_bookable"].replace("f", 0).replace("t", 1)
    listings_data["host_identity_verified"] = listings_data["host_identity_verified"].replace("f", 0).replace("t", 1)
    listings_data["host_has_profile_pic"] = listings_data["host_has_profile_pic"].replace("f", 0).replace("t", 1)
    listings_data["host_is_superhost"] = listings_data["host_is_superhost"].replace("f", 0).replace("t", 1)
    listings_data["amenities_count"] = listings_data['amenities'].apply(len)

    kmeans = KMeans(n_clusters=10, random_state=42)
    listings_data["neighborhood_cluster"] = kmeans.fit_predict(listings_data[["latitude", "longitude"]])
    
    amenities_pca = clean_amenities(listings_data)
    
    encoded_categorical = encode_categorical_features(listings_data, categorical_features)
    
    X = pd.concat([listings_data[features], encoded_categorical, amenities_pca], axis=1)
    X = X.dropna()
    y = listings_data.loc[X.index, "log_price"]
    
    return X, y

def tune_fit_model(X_train, y_train):
    param_dist = {
        'n_estimators': [100, 200, 300, 400],
        'learning_rate': [0.01, 0.1, 0.3],
        'max_depth': [3, 4, 5, 6],
        'min_samples_split': [2, 5, 10],
        'min_samples_leaf': [1, 2, 4],
        'max_features': ['log2', 'sqrt', None],
        'subsample': [0.8, 0.9, 1.0],
        'alpha': [0.7, 0.9]
    }
    gb_random_search = RandomizedSearchCV(
        estimator=GradientBoostingRegressor(random_state=42),
        param_distributions=param_dist,
        n_iter=10,
        cv=5,
        scoring='neg_mean_absolute_error',
        random_state=42
    )
    gb_random_search.fit(X_train, y_train)

    best_gb_model = gb_random_search.best_estimator_
    return best_gb_model

def evaluate_model(y_test, y_pred, model, X, y):
    
    mae = mean_absolute_error(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_test, y_pred)
    
    cv_scores = cross_val_score(model, X, y, cv=5, scoring='neg_mean_absolute_error')
    
    return {
        "MAE": mae,
        "RMSE": rmse,
        "R2 Score": r2,
        "Cross-Val MAE": -cv_scores.mean(),
        "Cross-Val MAE Std": cv_scores.std()
    }

def predict_price(listing: dict) -> float:
    
    return

def main():
    X, y = prepare_data("listings.csv")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = tune_fit_model(X_train, y_train)
    predicted = model.predict(X_test)
    results = evaluate_model(y_test, predicted, model, X, y)

    print("Model Performance Metrics:")
    for metric, value in results.items():
        print(f"{metric}: {value}")
    

if __name__ == "__main__":
    main()