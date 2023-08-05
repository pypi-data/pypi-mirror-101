"""
The module contains base embeddings,such as glove , word2vec....

"""
import numpy as np
from tqdm import tqdm
from gensim.models import KeyedVectors


def build_matrix(max_features, feature_dim, embeddings_index, word_index):
    embedding_matrix = np.zeros((max_features, feature_dim))
    for word, i in tqdm.tqdm(word_index.items()):
        if i >= max_features: continue
        try:
            embedding_vector = embeddings_index[word]
        except:
            embedding_vector = embeddings_index["unknown"]
        if embedding_vector is not None:
            embedding_matrix[i] = embedding_vector
    return embedding_matrix


def load_glove(max_features, embedding_file, word_index, feature_dim=300):
    """

    :param MAX_FEATURES: max word num
    :param EMBEDDING_FILE: path of the glove.6B/glove.6B.300d.txt
    :param WORD_INDEX: data word index
    :param FEATURE_DIM: default 300
    :return: glove_embedding_matrix

    example
    from keras.preprocessing.text import Tokenizer
    from keras.preprocessing.sequence import pad_sequences

    MAX_FEATURES = 10000
    EMBEDDING_FILE = ./glove.6B/glove.6B.300d.txt

    tokenizer = Tokenizer(num_words=MAX_FEATURES, lower=True)
    all_text = ['hello word !','I am a programer.']  # data_set
    tokenizer.fit_on_texts(all_text)
    WORD_INDEX = tokenizer.word_index
    glove_embedding_matrix = load_glove(max_features, EMBEDDING_FILE, WORD_INDEX, FEATURE_DIM=300)
    """

    def get_coefs(word, *arr):
        return word, np.asarray(arr, dtype='float32')

    embeddings_index = dict(get_coefs(*o.split(" ")) for o in open(embedding_file))
    glove_embedding_matrix = build_matrix(max_features, feature_dim, embeddings_index, word_index)
    return glove_embedding_matrix


def load_google_news_word2vec(max_features, embedding_file, word_index, feature_dim=300):
    word2vec = KeyedVectors.load_word2vec_format(embedding_file, binary=True)
    embeddings_index = {}
    for i, vec in tqdm(enumerate(word2vec.wv.vectors)):
        embeddings_index[word2vec.wv.index2word[i]] = vec
    word2vec_embedding_matrix = build_matrix(max_features, feature_dim, embeddings_index, word_index)
    return word2vec_embedding_matrix
