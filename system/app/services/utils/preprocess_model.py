

import joblib
import os
import numpy as np
from sklearn.preprocessing import LabelEncoder

#class model: model type

def prepare_model_and_predict(df):
    model_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),'./xgboost_model.pkl')

    if not os.path.exists(model_path):
        print("no model")
    model = joblib.load(model_path)
    le = LabelEncoder()
    categorical_columns = df.select_dtypes(include=['object']).columns

    for col in categorical_columns:
        df[col] = le.fit_transform(df[col])

    X = df.drop(['id','Employee code/number'], axis=1)

    predictions = model.predict(X)
    df['predictions'] = predictions

    return predictions


def estimate_survival_time(rsf, X):
    surv_funcs = rsf.predict_survival_function(X)
    median_survival_times = []

    for surv_func in surv_funcs:
        time_points = surv_func.x
        survival_probs = surv_func.y
        median_index = next((i for i, prob in enumerate(survival_probs) if prob <= 0.5), len(survival_probs) - 1)
        median_time = time_points[median_index]
        median_survival_times.append(median_time)

    return median_survival_times

def provide_recommendation(prob, time, threshold):
    if prob > threshold * 1.5:
        return f"High risk: There is a {prob:.1%} probability that this employee will leave within the next {time:.1f} years. It is recommended to take retention measures immediately."
    elif prob >= threshold:
        return f"Medium risk: The employee has a {prob:.1%} probability of leaving within the next {time:.1f} years. It is recommended to closely monitor and consider taking preventive measures."
    else:
        return f"Low risk: This employee has a {prob:.1%} probability of leaving within the next {time:.1f} years. Currently, the risk is low, but regular monitoring is still necessary."


def predict_employee_turnover(employee_data):

    base_path = os.path.dirname(os.path.abspath(__file__))

    selector = joblib.load(os.path.join(base_path, 'RFRSFmodel', 'feature_selector.joblib'))
    scaler = joblib.load(os.path.join(base_path, 'RFRSFmodel', 'scaler.joblib'))
    rf = joblib.load(os.path.join(base_path, 'RFRSFmodel', 'random_forest_classifier.joblib'))
    rsf = joblib.load(os.path.join(base_path, 'RFRSFmodel', 'random_survival_forest.joblib'))
    optimal_threshold = np.load(os.path.join(base_path, 'RFRSFmodel', 'optimal_threshold.npy'))

    feature_select=os.path.join(base_path, 'RFRSFmodel', 'selected_features.txt')

    with open(feature_select, 'r') as f:
        selected_features = [line.strip() for line in f]

    le =joblib.load(os.path.join(base_path,'RFRSFmodel','label_encoder.joblib'))

    print("Expected features:", selected_features)
    print("Actual features:", employee_data.columns.tolist())

    print(employee_data)
    X = employee_data[selected_features].copy()

    categorical_columns = X.select_dtypes(include=['object']).columns
    for col in categorical_columns:
        if col in selected_features:
            if set(X[col].unique()) - set(le.classes_):
                print(f"Warning: New categories found in {col}. Treating them as the most frequent category.")
                X[col] = X[col].map(lambda x: x if x in le.classes_ else le.classes_[0])
            X[col] = le.transform(X[col])

    X_scaled = scaler.transform(X)

    surv_prob = rsf.predict(X_scaled)

    X_with_surv = np.column_stack((X_scaled, surv_prob))

    turnover_prob = rf.predict_proba(X_with_surv)[:, 1]

    predicted_label = (turnover_prob >= optimal_threshold).astype(int)

    survival_times = estimate_survival_time(rsf, X_scaled)

    recommendations = [provide_recommendation(prob, time, optimal_threshold)
                       for prob, time in zip(turnover_prob, survival_times)]

    results_dict = {
        'Predicted_Label': int(predicted_label[0]),
        'Turnover_Probability': float(turnover_prob[0]),
        'Estimated_Survival_Time': float(survival_times[0]),
        'Recommendation': recommendations[0]
    }
    print("Results Dictionary:")
    print(f"Predicted_Label: {results_dict['Predicted_Label']}")
    print(f"Turnover_Probability: {results_dict['Turnover_Probability']}")
    print(f"Estimated_Survival_Time: {results_dict['Estimated_Survival_Time']}")
    print(f"Recommendation: {results_dict['Recommendation']}")
    return results_dict