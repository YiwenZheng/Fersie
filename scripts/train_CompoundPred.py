#!/usr/bin/env python3

import utils, dataset, CompoundPred
import pandas as pd


def read_data(input_file):
    df = pd.read_csv(input_file)
    y = df.iloc[:,2:3]
    X_drug = df.iloc[:,0:1]
    return X_drug, y


def train_model(config):
    #加载数据
    X_drug, y, drug_index = dataset.load_HIV(config["input_file"])
    #X_drug, y = read_data(config.input_file)
    
    #药物编码器
    drug_encoding = config["drug_encoding"]

    if drug_encoding == "Transformer":
        from Transformer import get_model_config
    elif drug_encoding == "CNN":
        from CNN import get_model_config
    elif drug_encoding == "MPNN":
        from MPNN import get_model_config
    elif drug_encoding == "CNN_RNN":
        from CNN_RNN import get_model_config
    elif drug_encoding == "Morgan":
        from Morgan import get_model_config
    elif drug_encoding == "Daylight":
        from Daylight import get_model_config
    elif drug_encoding == "Pubchem":
        from Pubchem import get_model_config
    elif drug_encoding == "rdkit_2d_normalized":
        from rdkit_2d_normalized import get_model_config
    elif drug_encoding == "ESPF":
        from ESPF import get_model_config
    elif drug_encoding == "ErG":
        from ErG import get_model_config    

    #分割训练集、验证集和测试集
    train, val, test = utils.data_process(X_drug = X_drug, y = y,\
                                drug_encoding = drug_encoding,\
                                split_method = 'random', frac = [0.7,0.1,0.2])

    #模型配置生成
    model_config = get_model_config(config)

    #模型初始化
    model = CompoundPred.model_initialize(**model_config)

    #训练模型
    test_result = model.train(train, val, test)

    #保存模型
    model.save_model(config["output_dir"])

    return test_result
