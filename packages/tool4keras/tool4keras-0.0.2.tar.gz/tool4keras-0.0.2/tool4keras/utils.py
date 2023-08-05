import numpy as np
import keras.backend as K
import keras
import time
import os
import logging
from pathlib import Path


def gen_output_fold(output_path):
    EXPERIENCE_PATH = '{}/ex_{}'.format(output_path, time.strftime("%Y-%m-%d-%H:%M:%S", time.localtime()))
    os.makedirs(EXPERIENCE_PATH)
    print('created EXPERIENCE_PATH')


def init_logger(log_file=None, log_file_level=logging.NOTSET):
    '''
    Example:
        >>> init_logger(log_file)
        >>> logger.info("abc'")
    '''
    if isinstance(log_file, Path):
        log_file = str(log_file)
    log_format = logging.Formatter(fmt='%(asctime)s - %(levelname)s - %(name)s -   %(message)s',
                                   datefmt='%m/%d/%Y %H:%M:%S')
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_format)
    logger.handlers = [console_handler]
    if log_file and log_file != '':
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(log_file_level)
        # file_handler.setFormatter(log_format)
        logger.addHandler(file_handler)
    logger.info('start time : {}'.format(time.strftime("%Y-%m-%d-%H:%M:%S", time.localtime())))
    return logger


def count_word_len(len_seq):
    distribute_count = {'i < 64': 0, '64 <= i < 128': 0, '128 <= i < 256': 0, '256 <= i < 512': 0, 'i>512': 0}
    for i in sorted(len_seq):
        if i < 64:
            distribute_count['i < 64'] += 1
        elif 64 <= i < 128:
            distribute_count['64 <= i < 128'] += 1
        elif 128 <= i < 256:
            distribute_count['128 <= i < 256'] += 1
        elif 256 <= i < 512:
            distribute_count['256 <= i < 512'] += 1
        else:
            distribute_count['i>512'] += 1
    per_dict = {key: value / len(len_seq) for key, value in distribute_count.items()}
    print('=' * 50)
    print('the num of len_seq is {}'.format(len(len_seq)))
    for key in distribute_count.keys():
        print('({}) num : {} per: {:.4f}'.format(key, distribute_count[key], per_dict[key]))
    print('=' * 50)


def search_layer(inputs, name, exclude_from=None):
    """根据inputs和name来搜索层
    说明：inputs为某个层或某个层的输出；name为目标层的名字。
    实现：根据inputs一直往上递归搜索，直到发现名字为name的层为止；
         如果找不到，那就返回None。
    """
    if exclude_from is None:
        exclude_from = set()

    if isinstance(inputs, keras.layers.Layer):
        layer = inputs
    else:
        layer = inputs._keras_history[0]

    if layer.name == name:
        return layer
    elif layer in exclude_from:
        return None
    else:
        exclude_from.add(layer)
        if isinstance(layer, keras.models.Model):
            model = layer
            for layer in model.layers:
                if layer.name == name:
                    return layer
        inbound_layers = layer._inbound_nodes[0].inbound_layers
        if not isinstance(inbound_layers, list):
            inbound_layers = [inbound_layers]
        if len(inbound_layers) > 0:
            for layer in inbound_layers:
                layer = search_layer(layer, name, exclude_from)
                if layer is not None:
                    return layer


def adversarial_training(model, embedding_name, epsilon=1):
    """给模型添加对抗训练
    其中model是需要添加对抗训练的keras模型，embedding_name
    则是model里边Embedding层的名字。要在模型compile之后使用。
    """
    if model.train_function is None:  # 如果还没有训练函数
        model._make_train_function()  # 手动make
    old_train_function = model.train_function  # 备份旧的训练函数

    # 查找Embedding层
    for output in model.outputs:
        embedding_layer = search_layer(output, embedding_name)
        if embedding_layer is not None:
            break
    if embedding_layer is None:
        raise Exception('Embedding layer not found')

    # 求Embedding梯度
    embeddings = embedding_layer.embeddings  # Embedding矩阵
    gradients = K.gradients(model.total_loss, [embeddings])  # Embedding梯度
    gradients = K.zeros_like(embeddings) + gradients[0]  # 转为dense tensor

    # 封装为函数
    inputs = (model._feed_inputs +
              model._feed_targets +
              model._feed_sample_weights)  # 所有输入层
    embedding_gradients = K.function(
        inputs=inputs,
        outputs=[gradients],
        name='embedding_gradients',
    )  # 封装为函数

    def train_function(inputs):  # 重新定义训练函数
        grads = embedding_gradients(inputs)[0]  # Embedding梯度
        delta = epsilon * grads / (np.sqrt((grads ** 2).sum()) + 1e-8)  # 计算扰动
        K.set_value(embeddings, K.eval(embeddings) + delta)  # 注入扰动
        outputs = old_train_function(inputs)  # 梯度下降
        K.set_value(embeddings, K.eval(embeddings) - delta)  # 删除扰动
        return outputs

    model.train_function = train_function  # 覆盖原训练函数
