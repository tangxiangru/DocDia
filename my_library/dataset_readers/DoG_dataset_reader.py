from typing import Dict, Iterable, List

from overrides import overrides

from allennlp.data.dataset_readers.dataset_reader import DatasetReader
from allennlp.data import Token
from allennlp.data.fields import Field, TextField, ListField, MetadataField
from allennlp.data.tokenizers import Tokenizer, WordTokenizer
from allennlp.data.tokenizers.sentence_splitter import SpacySentenceSplitter
from allennlp.data.token_indexers import TokenIndexer, SingleIdTokenIndexer
from allennlp.data.instance import Instance
from allennlp.common.util import END_SYMBOL, START_SYMBOL

import os
import json


@DatasetReader.register("DoG_dataset_reader")
class DoGDatasetReader(DatasetReader):
    def __init__(self,
                 lazy: bool = True,
                 tokenizer: Tokenizer = None,
                 token_indexers: Dict[str, TokenIndexer] = None,
                 split_sentence_in_doc: bool = False):
        super().__init__(lazy)
        self.tokenizer = tokenizer or WordTokenizer()
        self.token_indexers = token_indexers or {"tokens": SingleIdTokenIndexer(lowercase_tokens=True)}
        if split_sentence_in_doc:
            self.sentence_splitter = SpacySentenceSplitter()
        else:
            self.sentence_splitter = None

    @overrides
    def _read(self, file_path: str) -> Iterable[Instance]:
        with open(os.path.join(os.path.split(file_path)[0], 'documents.json'), 'r') as doc_file:
            doc_json = json.load(doc_file)
        doc_field_dict = self.get_doc_field_dict(doc_json)

        with open(file_path, 'r') as data_file:
            for line in data_file:
                line = line.strip()
                dialog_json = json.loads(line)
                yield self.text_to_instance(dialog_json['dialogue'],
                                            doc_field_dict[dialog_json['docId']],
                                            dialog_json['whoSawDoc'])

    @overrides
    def text_to_instance(self, dialogs: List[str], doc_field: Field, who_saw_doc: int):
        tokenized_dialogs = [self.tokenizer.tokenize(dialog) for dialog in dialogs]
        for tokenized_dialog in tokenized_dialogs:
            tokenized_dialog.insert(0, Token(START_SYMBOL))
            tokenized_dialog.append(Token(END_SYMBOL))
        dialogue_field = ListField([TextField(tokenized_dialog, self.token_indexers)
                                   for tokenized_dialog in tokenized_dialogs])
        # who_saw_doc_field = MetadataField(who_saw_doc)
        # return Instance({'dialogue': dialogue_field, 'document': doc_field, 'who_saw_doc': who_saw_doc_field})
        return Instance({'dialogue': dialogue_field, 'document': doc_field})

    def get_doc_field_dict(self, doc_json: Dict) -> Dict[int, Field]:
        doc_field_dict = {}
        for idx, doc in doc_json.items():
            if self.sentence_splitter is not None:
                doc_sentence_list: List[str] = []
                for i in ('0', '1', '2', '3'):
                    doc_sentence_list.extend(self.sentence_splitter.split_sentences(doc[i]))
                tokenized_doc_sentence_list = [self.tokenizer.tokenize(doc_sequence) for doc_sequence in doc_sentence_list]
                doc_field = ListField([TextField(tokenized_doc_sentence, self.token_indexers)
                                       for tokenized_doc_sentence in tokenized_doc_sentence_list])
            else:
                doc_sequence = ' '.join(doc[i] for i in ('0', '1', '2', '3'))
                tokenized_doc = self.tokenizer.tokenize(doc_sequence)
                doc_field = TextField(tokenized_doc, self.token_indexers)

            doc_field_dict[int(idx)] = doc_field

        return doc_field_dict
