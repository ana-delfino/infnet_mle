"""
This is a boilerplate pipeline 'Treinamento'
generated using Kedro 0.19.12
"""

from kedro.pipeline import node, Pipeline, pipeline  # noqa
from . import nodes

def create_pipeline(**kwargs) -> Pipeline:
    return pipeline([
        node(
            func=nodes.log_reg_model_train,
            name="train_log_reg_model",
            inputs=dict(
                x_train="x_train",
                y_train="y_train",
                session_id="params:session_id"
            ),
            outputs="log_reg_model",
            tags=['treinamento']
        ),
        node(
            func=nodes.decision_tree_model_train,
            name="train_decision_tree_model",
            inputs=dict(
                x_train="x_train",
                y_train="y_train",
                session_id="params:session_id"
            ),
            outputs="decision_tree_model",
            tags=['treinamento']
        ),
        node(
            func=nodes.compute_log_reg_metrics,
            name="compute_reg_log_metrics",
            inputs=dict(
                model="log_reg_model",
                x_test="x_test",
                y_test="y_test",
            ),
            outputs="log_reg_metrics",
            tags=['treinamento']
        ),
        node(
            func=nodes.compute_decision_tree_metrics,
            name="compute_decision_tree_metrics",
            inputs=dict(
                model="decision_tree_model",
                x_test="x_test",
                y_test="y_test",
            ),
            outputs="decision_tree_metrics",
            tags=['treinamento']
            )
        ]
    )
