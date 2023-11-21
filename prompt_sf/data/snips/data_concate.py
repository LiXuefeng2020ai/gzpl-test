import json
import os
domain2slot = {
    "AddToPlaylist": ['music_item', 'playlist_owner', 'entity_name', 'playlist', 'artist'],
    "BookRestaurant": ['city', 'facility', 'timeRange', 'restaurant_name', 'country', 'cuisine', 'restaurant_type', 'served_dish', 'party_size_number', 'poi', 'sort', 'spatial_relation', 'state', 'party_size_description'],
    "GetWeather": ['city', 'state', 'timeRange', 'current_location', 'country', 'spatial_relation', 'geographic_poi', 'condition_temperature', 'condition_description'],
    "PlayMusic": ['genre', 'music_item', 'service', 'year', 'playlist', 'album','sort', 'track', 'artist'],
    "RateBook": ['object_part_of_series_type', 'object_select', 'rating_value', 'object_name', 'object_type', 'rating_unit', 'best_rating'],
    "SearchCreativeWork": ['object_name', 'object_type'],
    "SearchScreeningEvent": ['timeRange', 'movie_type', 'object_location_type','object_type', 'location_name', 'spatial_relation', 'movie_name']
}
import pdb

def types2list(span):
    record = span.split()
    record = [i.split("-")[1] for i in record]
    return record

# 只保存实体
def concate():
    for domain in domain2slot.keys():
        json_data = []
        with open(f"{domain}/{domain}.txt","r") as file:

            for i,line in enumerate(file):
                sentence_dict = {}
                slot_types = []
                slot_entities = []
                sentence_label_list = line.split('\t')
                sentence_dict["sentence"] = sentence_label_list[0]
                sentences = sentence_label_list[0].strip().replace("  ",' ').split(" ")
                labels = sentence_label_list[1].strip().split(" ")
                # print(i)
                # print(sentences,labels)
                assert len(labels)==len(sentences)
                start = -1
                # end = -1
                for i in range(len(labels)):
                    if labels[i]=="O" and start==-1:
                        continue
                    elif labels[i] == "O" and start !=-1:

                        slot_types.append(labels[start].split("-")[1])
                        slot_entities.append(" ".join(sentences[start:i]))
                        start = -1
                        
                    elif labels[i].split("-")[0]=="B":
                        if start!=-1:
                            slot_types.append(labels[start].split("-")[1])
                            slot_entities.append(" ".join(sentences[start:i]))
                        start = i
                    
                    else:
                        continue
                
                if start!=-1:
                    slot_types.append(labels[start].split("-")[1])
                    slot_entities.append(" ".join(sentences[start:])) 
                
                sentence_dict["slot_type"] = slot_types
                sentence_dict["label"] = slot_entities
                
                json_data.append(sentence_dict)

        with open(f"{domain}/con_{domain}.json","w") as j:
            json.dump(json_data,j,indent=3)

# 将实体和非实体信息全部记录下来
def universal_samples():
    for domain in domain2slot.keys():
        json_data = []
        with open(os.path.join(domain,f"con_{domain}.json")) as f:
            lines = json.load(f)
            slot_types = domain2slot[domain]
            for line in lines:
                sentence_dict = {}
                slot2entities = {}
                entities = ['none']*len(slot_types)
                for i,slot_type in enumerate(line['slot_type']):
                    if slot_type not in slot2entities:
                        slot2entities[slot_type] = [line['label'][i]]
                    else:
                        slot2entities[slot_type].append(line['label'][i])
                for slot,ent in slot2entities.items():
                    inx = slot_types.index(slot)
                    entities[inx] = ",".join(ent)
                # print(line['sentence'])
                # assert len(line['slot_type'])+entities.count('None')==len(slot_types)
                sentence_dict['sentence'] = line['sentence']
                sentence_dict['slot_types'] = slot_types
                sentence_dict['entities'] = entities
                json_data.append(sentence_dict)
        
        with open(f"{domain}/universal_{domain}.json","w") as j:
            json.dump(json_data,j,indent=3)
            
        


def check_concate():
    for domain in domain2slot.keys():
        cnt = 0
        cnt_entity = 0
        with open(os.path.join(domain,f"con_{domain}.json")) as f:
            # for line in f.read():
            lines = json.load(f)
            for data in lines:
                cnt += len(data['slot_type'])
                for i in data['label']:
                    # print(i)
                    cnt_entity += len(i.strip().split())
        print(f'{domain}:{cnt}')
        print(f'{domain}:{cnt_entity}')

def check_universal():
    for domain in domain2slot.keys():
        cnt = 0
        cnt_entities = 0
        with open(os.path.join(domain,f"universal_{domain}.json")) as f:
            lines = json.load(f)
            for line in lines:
                for entity in line['entities']:
                    if entity!='none':
                        cnt += len(entity.split(','))
                        cnt_entities += len(entity.split())
        print(f'{domain}:{cnt}')
        print(f'{domain}:{cnt_entities}')

if __name__ == "__main__":
    # check()
    # concate()
    universal_samples()
    check_concate()
    check_universal()