import json
import os

def statistic(dirpath: str = './DoG/Conversations/') -> None:
    info_dict = dict()
    root, dirs, files = next(os.walk(dirpath))
    for dir in dirs:
        info_dict[dir] = {'max_turns': 0, 'min_turns': 99, 'user1_saw': 0, 'user2_saw': 0, 'both_saw': 0, 'rating>1': 0}
        filename_list = next(os.walk(os.path.join(root, dir)))[2]
        total_turns = 0
        for filename in filename_list:
            with open(os.path.join(root, dir, filename), 'r') as fp:
                file_json = json.load(fp)
            if file_json['rating'] > 1:
                info_dict[dir]['rating>1'] += 1
                turns = 0
                user = None
                for utterance in file_json['history']:
                    if utterance['uid'] != user:
                        user = utterance['uid']
                        turns += 1
                info_dict[dir]['max_turns'] = max(info_dict[dir]['max_turns'], turns)
                info_dict[dir]['min_turns'] = min(info_dict[dir]['min_turns'], turns)
                total_turns += turns

                whoSawDoc = file_json['whoSawDoc']
                if len(whoSawDoc) < 2:
                    if whoSawDoc[0] == 'user1':
                        info_dict[dir]['user1_saw'] += 1
                    else:
                        info_dict[dir]['user2_saw'] += 1
                else:
                    info_dict[dir]['both_saw'] += 1
        info_dict[dir]['total_turns'] = total_turns



    with open('statistic.json', 'w') as fp:
        json.dump(info_dict, fp, indent=2)


if __name__ == "__main__":
    statistic()
