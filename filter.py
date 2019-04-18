from typing import List

import json
import os


def filtering(dirpath: str = './DoG/Conversations/') -> None:
    root, dirs, files = next(os.walk(dirpath))
    for dir in dirs:
        filtered_fp = open('./DoG/' + dir + '.jsonl', 'w')
        filename_list = next(os.walk(os.path.join(root, dir)))[2]
        print(len(filename_list))
        print(filename_list[:10])
        for filename in filename_list:
            with open(os.path.join(root, dir, filename), 'r') as fp:
                file_json = json.load(fp)
                if file_json['rating'] > 1:
                    file_dict = get_file_dict(file_json)
                    filtered_fp.write(json.dumps(file_dict))
                    filtered_fp.write('\n')

        filtered_fp.close()


def get_file_dict(file_json):
    # A instance should consist of 'dialogue', 'docId' and 'whoSawDoc'
    file_dict = {'dialogue': list()}
    file_dict['docId'] = file_json['wikiDocumentIdx']

    if len(file_json['whoSawDoc']) == 2:
        file_dict['whoSawDoc'] = 3
    else:
        if file_json['whoSawDoc'][0] == 'user1':
            file_dict['whoSawDoc'] = 1
        else:
            file_dict['whoSawDoc'] = 2

    user = file_json['history'][0]['uid']
    utterance_list: List[str] = list()
    # Concat continuous utterance of one user
    for utterance in file_json['history']:
        if utterance['uid'] == user:
            utterance_list.append(utterance['text'])
        else:
            user = utterance['uid']
            file_dict['dialogue'].append(' '.join(utterance_list))
            utterance_list = [utterance['text']]

    return file_dict


if __name__ == "__main__":
    filtering()
