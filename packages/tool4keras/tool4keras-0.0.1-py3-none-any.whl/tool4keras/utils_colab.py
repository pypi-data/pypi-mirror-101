import os


def set_init_enviroment():
    os.system('% tensorflow_version 1.14')
    os.system('pip install keras == 2.3.1')
    os.system('pip install bert4keras == 0.8.8')


def download_chinese_roberta_wwm_ext():
    from google_drive_downloader import GoogleDriveDownloader
    GoogleDriveDownloader.download_file_from_google_drive(file_id='1jMAKIJmPn7kADgD3yQZhpsqM-IRM1qZt',
                                                          dest_path='/content/chinese_roberta_wwm_ext/chinese_roberta_wwm_ext_L-12_H-768_A-12.zip',
                                                          unzip=True)
    print(
        'chinese_roberta_wwm_ext_L-12_H-768_A-12.zip has been download d unpacked to /content/chinese_roberta_wwm_ext')


def download_albert_xlarge_zh_183k():
    s1 = 'wget https://storage.googleapis.com/albert_zh/albert_xlarge_zh_183k.zip'
    s2 = 'unzip /content/albert_xlarge_zh_183k.zip -d /content/albert_xlarge_zh_183k'
    os.system(s1)
    print('albert_xlarge_zh_183k has been download')
    os.system(s2)
    print('albert_xlarge_zh_183k.zip has been unpack to /content/albert_xlarge_zh_183k')


def download_glove_en():
    os.system('wget http://downloads.cs.stanford.edu/nlp/data/wordvecs/glove.6B.zip')
    print('download to sucessfully')
    os.system('unzip /content/glove.6B.zip -d /content/glove')
    print('unzip /content/glove.6B.zip to ')


def download_GoogleNews_en():
    os.system('wget https://s3.amazonaws.com/dl4j-distribution/GoogleNews-vectors-negative300.bin.gz')
    print('download sucessfully')


def download_base_bert_en():
    os.system('wget https://storage.googleapis.com/bert_models/2020_02_20/uncased_L-12_H-768_A-12.zip')
    print('uncased_L-12_H-768_A-12 has been download')
    print('download sucessfully')
    s2 = 'unzip /content/uncased_L-12_H-768_A-12.zip -d /content/uncased_L-12_H-768_A-12'
    os.system(s2)
    print('uncased_L-12_H-768_A-12.zip has been unpack to /content/uncased_L-12_H-768_A-12')