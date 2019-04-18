import json
import os


def concat_doc(dirpath: str = './DoG/WikiData/') -> None:
    filename_list = next(os.walk(dirpath))[2]
    with open('./DoG/documents.json', 'w') as doc_fp:
        documents_dict = dict()
        for filename in filename_list:
            with open(os.path.join(dirpath, filename), 'r') as fp:
                file_json = json.load(fp)
                metadata = file_json["0"]
                concat_metadata = []
                for key, value in metadata.items():
                    if isinstance(value, list):
                        value.insert(0, key + ':')
                        concat_metadata.append(' '.join(value))
                    else:
                        concat_metadata.append(key + ': ' + value)
                concat_metadata = '. '.join(concat_metadata) + '.'

                documents_dict[file_json['wikiDocumentIdx']] = {"0": concat_metadata,
                                                                "1": file_json["1"],
                                                                "2": file_json["2"],
                                                                "3": file_json["3"]}
        json.dump(documents_dict, doc_fp)


if __name__ == "__main__":
    concat_doc()
