"""
This is a boilerplate pipeline 'Treinamento'
generated using Kedro 0.19.12
"""
import pandas as pd
from pycaret.classification import ClassificationExperiment
from sklearn.metrics import f1_score, log_loss

# def start_mlflow_run(experiment_name: str) -> str:

#     mlflow.set_experiment(experiment_name)
#     run = mlflow.start_run(run_name="Pipeline Kedro - Modelos")
#     return run.info.run_id

# def end_mlflow_run(run_id: str) -> None:
#     if mlflow.active_run():
#         mlflow.end_run()

def log_reg_model_train(x_train, y_train,session_id):
        
    exp = ClassificationExperiment()
    exp.setup(data=x_train, target=y_train['shot_made_flag'] , session_id=session_id)
    
    lr_model = exp.create_model('lr')       
    tuned_model = exp.tune_model(
        lr_model, 
        n_iter=10, 
        optimize='AUC',
        search_library='scikit-optimize',
        search_algorithm='bayesian',
        choose_better=True,
        early_stopping=True,
        fold=5,
        custom_grid = {
            'C': [0.001, 0.01, 0.1, 1, 10],           # Inverso da regularização L2
            'penalty': ['l2'],  # Tipo de penalização
            'solver': [ 'lbfgs'],       # Algoritmo de otimização
            'max_iter': [100, 200, 500],              # Número máximo de iterações
            'l1_ratio': [0.0, 0.5, 1.0]               # Só usado se penalty = elasticnet
            }
    )
    return tuned_model

def decision_tree_model_train(x_train, y_train,session_id):

    exp = ClassificationExperiment()
    exp.setup(data=x_train, target=y_train['shot_made_flag'], session_id=session_id)
    
    dt_model = exp.create_model('dt')  
    tuned_model = exp.tune_model(
        dt_model, n_iter=10, 
        optimize='AUC', 
        search_library='scikit-optimize',
        search_algorithm='bayesian',
        choose_better=True,
        early_stopping=True,
        fold=5,
        custom_grid={
            'max_depth': [3, 5, 10, 20],
            'min_samples_split': [2, 5, 10],
            'min_samples_leaf': [1, 2, 4]
        }
    )

    return tuned_model

def compute_log_reg_metrics(model, x_test: pd.DataFrame, y_test):
    
    y_predict = model.predict_proba(x_test)

    log_loss_value = log_loss(y_test['shot_made_flag'].values, y_predict[:, 1])

    metrics = {'log_loss_lr': log_loss_value}
    

    return {
        key: {'value': value, 'step': 1}
        for key, value in metrics.items()
    }
    
def compute_decision_tree_metrics(model, x_test: pd.DataFrame, y_test):
 
    y_predict = model.predict(x_test)
    y_predict_scores = model.predict_proba(x_test)
 
    log_loss_value = log_loss(y_test['shot_made_flag'].values, y_predict_scores[:, 1])
    f1_score_value = f1_score(y_test['shot_made_flag'].values, y_predict)
    
    metrics = {
        'log_loss_dt': log_loss_value, 
        'f1_score_dt': f1_score_value
    }

    return {
        key: {'value': value, 'step': 1}
        for key, value in metrics.items()
    }