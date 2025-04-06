import pandas as pd
import requests
import mlflow
from sklearn.metrics import log_loss, f1_score
# 1. Carregar dados de produção
df = pd.read_parquet("/Users/anapaula/projects/infnet_mle/data/01_raw/dataset_kobe_prod.parquet")

df = df[['lat','lon','minutes_remaining','period','playoffs','shot_distance','shot_made_flag']]
df = df.dropna()
df['shot_made_flag'] = df['shot_made_flag'].astype(int)

mlflow.set_experiment("PipelineAplicacao")
with mlflow.start_run(run_name="PipelineAplicacao"):
    
    model = mlflow.sklearn.load_model("models:/decision_tree_model/9")
    x= df.drop('shot_made_flag', axis=1)  
    y = df['shot_made_flag'] 

    y_predict = model.predict(x)
    y_predict_scores = model.predict_proba(x)
    df_pred = pd.DataFrame(y_predict, columns=["prediction"])
    df_pred.to_parquet("data/06_models/predicoes_aplicacao.parquet", index=False)

    
    logloss= log_loss(y.values, y_predict_scores[:, 1])
    f1= f1_score(y.values, y_predict)

    metrics = {
            'log_loss': logloss, 
            'f1_score': f1
        }

    print(metrics)
    mlflow.log_metric("log_loss", logloss)
    mlflow.log_metric("f1_score", f1)
    mlflow.log_artifact("data/06_models/predicoes_aplicacao.parquet")

