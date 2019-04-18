allennlp train experiments/multi_turn_hred.json -s outputs/multi_turn_hred/ --include-package my_library --recover

allennlp predict 模型model.tar.gz DoG/test.jsonl --include-package my_library --predictor  multi_hred_predictor --output-file 输出路径 --silent --use-dataset-reader
