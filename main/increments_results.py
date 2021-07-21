
from ChinookSalmonResearchProject.IncrementsRegression import increments_processing, model

def increments_correlations(datafolder_path, datafile_names):
    for identifier in datafile_names:
        full_data = increments_processing.import_data(datafolder_path, identifier)
        X_train, X_test, y_train, y_test = increments_processing.data_preprocessing(full_data, ['stock'], ['year'])

        random_forest, rsquared = model.train_model(
            {
                "n_estimators":100,
                "oob_score":True,
                "min_impurity_decrease":0.1
            },
            X_train,
            y_train,
            epochs=10
        )

        print(f"Dataset: {identifier}; Average R-Squared {rsquared}")

def simulation_model_results(sim_data_path):
    pass


if __name__ == '__main__':
    datafolder_path = "..\\data\\"
    datafile_names = [
        "spring_age",
        "spring_age_2_3",
        "spring_age_3_4",
        "spring_age_4_5",
        "GOA_fall_age",
        "GOA_fall_age_1_2",
        "GOA_fall_age_2_3",
        "GOA_fall_age_3_4",
        "GOA_fall_age_4_5",
        "increments_NCC",
        "NCC_fall_age_1_2",
        "NCC_fall_age_2_3",
        "NCC_fall_age_3_4",
        "NCC_fall_age_4_5",
        "fall_age",
        "fall_age_1_2",
        "fall_age_2_3",
        "fall_age_3_4",
        "fall_age_4_5",
        "2_3",
        "3_4",
        "4_5"
    ]

    #increments_correlations(datafolder_path, datafile_names)

    params = {
        "n_estimators": 100,
        "oob_score": True,
        "min_impurity_decrease": 0.1
    }
    test_rf = model.RFRegressor(params=params)

    data = increments_processing.import_data(datafolder_path, "spring_age")
    X_train, X_test, y_train, y_test = increments_processing.data_preprocessing(data, ['stock'], ['year'])
    test_rf.fit(X_train, y_train)
    test_rf.pd_plot(X_train, 2)