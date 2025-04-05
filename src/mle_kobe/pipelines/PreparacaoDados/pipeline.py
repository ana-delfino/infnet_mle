"""
This is a boilerplate pipeline 'PreparacaoDados'
generated using Kedro 0.19.12
"""
from kedro.pipeline import node, Pipeline, pipeline
from . import nodes

def create_pipeline(**kwargs) -> Pipeline:
    return pipeline([
        node(
            func=nodes.filter_dataset,
            name='filter_dataset',
            inputs=[
                'data_raw'
            ],
            outputs='data_filtered',
        ),
        node(
            func=nodes.split_data,
            name='split_data',
            inputs=[
                'data_filtered', 
                'params:test_size',
                'params:random_state'
        ],
        outputs=[
            'x_train', 
            'x_test', 
            'y_train', 
            'y_test'],
        ),
        node(
        func=nodes.dataset_metrics,
        name='dataset_metrics',
        inputs=['x_train','x_test','params:test_size'],
        outputs='train_test_metrics',
        )
    ])