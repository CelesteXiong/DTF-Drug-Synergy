import os
import pandas as pd
import matplotlib.pyplot as plt

def plot_metric(result_root, model_name, train_metric, val_metric, metric_name):
    plt.plot(train_metric)
    plt.plot(val_metric)
    plt.title(f'model {metric_name}')
    plt.ylabel(f'{metric_name}')
    plt.xlabel('epoch')
    plt.legend(['train', 'test'], loc='upper left')
    plt.savefig(os.path.join(result_root, f'{model_name}_{metric_name}.png'))
    # plt.show()
