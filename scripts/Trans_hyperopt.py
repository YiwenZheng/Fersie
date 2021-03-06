#!/usr/bin/env python3

from hyperopt import hp, fmin, tpe
from train_CompoundPred import train_model
from argparse import ArgumentParser


def objective(args):
    parser = ArgumentParser()
    parser.add_argument("-i", "--input_file", type = str, required = True,
        help = "Path to data file")
    parser.add_argument("-o", "--output_dir", type = str, required = True,
        help = "Directory where model will be saved")
    parser.add_argument("-r", "--result_folder", type = str, 
        default = "./result/", required = False, help = "Folder of result") 
    parser.add_argument("-d_e", "--drug_encoding", type = str, 
        default = "Transformer", required = False, help = "Drug encoding")
    tmp = parser.parse_args()
    base_config = vars(tmp)  #把参数转换为字典格式

    params = {
        "input_file": base_config["input_file"],
        "output_dir": base_config["output_dir"],
        "result_folder": base_config["result_folder"],
        "drug_encoding": base_config["drug_encoding"],
        "input_dim_drug": args["input_dim_drug"],
        "input_dim_protein": args["input_dim_protein"],
        "hidden_dim_drug": args["hidden_dim_drug"],
        "hidden_dim_protein": args["hidden_dim_protein"],
        "cls_hidden_dims": [1024, 1024, 512],
        "batch_size": args["batch_size"],
        "train_epoch": 10,
        "test_every_X_epoch": 20,
        "LR": 0.0001,
        "decay": 0,
        "num_workers": 0,
        "transformer_dropout_rate": args["transformer_dropout_rate"],
        "transformer_emb_size_drug": args["transformer_emb_size_drug"],
        "transformer_n_layer_drug": args["transformer_n_layer_drug"],
        "transformer_intermediate_size_drug": 
            args["transformer_intermediate_size_drug"],
        "transformer_num_attention_heads_drug": 
            args["transformer_num_attention_heads_drug"],
        "transformer_attention_probs_dropout": 
            args["transformer_attention_probs_dropout"],
        "transformer_hidden_dropout_rate": 
            args["transformer_hidden_dropout_rate"],
        "transformer_emb_size_target": args["transformer_emb_size_target"],
        "transformer_n_layer_target": args["transformer_n_layer_target"],
        "transformer_intermediate_size_target": 
            args["transformer_intermediate_size_target"],
        "transformer_num_attention_heads_target": 
            args["transformer_num_attention_heads_target"]
    }
    test_result = train_model(params)
    return 1-test_result["AUROC"]

space = {
    "input_dim_drug": hp.choice("input_dim_drug", range(1,5000,5)),
    "input_dim_protein": hp.choice("input_dim_protein", range(1,5000,5)),
    "hidden_dim_drug": hp.choice("hidden_dim_drug", [128, 256, 512]),
    "hidden_dim_protein": hp.choice("hidden_dim_protein", [128, 256, 512]),
    "batch_size": hp.choice("batch_size", [32, 64, 128, 256, 512]),
    "transformer_dropout_rate": hp.choice("transformer_dropout_rate", [0.1]),
    "transformer_emb_size_drug":hp.choice("transformer_emb_size_drug",[128,256]),
    "transformer_n_layer_drug":hp.choice("transformer_n_layer_drug",range(1,10)),
    "transformer_intermediate_size_drug": 
        hp.choice("transformer_intermediate_size_drug", [128, 256, 512]),
    "transformer_num_attention_heads_drug": 
        hp.choice("transformer_num_attention_heads_drug", [2, 4, 8]),
    "transformer_attention_probs_dropout": 
        hp.choice("transformer_attention_probs_dropout", [0.1]),
    "transformer_hidden_dropout_rate": 
        hp.choice("transformer_hidden_dropout_rate", [0.1]),
    "transformer_emb_size_target": 
        hp.choice("transformer_emb_size_target", [32, 64, 128]),
    "transformer_n_layer_target": 
        hp.choice("transformer_n_layer_target", range(1,10)),
    "transformer_intermediate_size_target": 
        hp.choice("transformer_intermediate_size_target", [128, 256, 512]),
    "transformer_num_attention_heads_target": 
        hp.choice("transformer_num_attention_heads_target", [2, 4, 8])
}

best = fmin(fn = objective, space = space, algo = tpe.suggest, max_evals = 100)
print(best)
train_model(best)
