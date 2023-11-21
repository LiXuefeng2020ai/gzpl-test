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

# with open('AddToPlaylist/AddToPlaylist.json') as data_file:
#     data = json.load(data_file)


result=[]
for root, dirs, files in os.walk('.'):
    for file in files:
        if 'json' in file and 'tran' not in file:   #筛选是json后缀的文件
            print(file[:-5])  #打出他的domain
            domain=str(file[:-5])    
            slots =domain2slot[domain]
            slot=""
            for i in slots:
                slot+=str(i)+" "               #将slot type拼成一个字符串
            print(slot)   
                
            with open(os.path.join(root, file)) as data_file:

                data = json.load(data_file)  
                print(len(data)) 
                # print(data[0]["label"])
                for dict in data:
                    if dict['label']==[]:      #空掉空着的
                        continue
                    else:
                        entity=""
                        for i in dict["label"][0]:
                            entity+=str(i)+" "
                        entity=entity[:-1]
                        dict["label"]=entity
                        a = dict["slot_type"]
                        dict["slot_type"]=dict["label"]     #slot type label换位置
                        dict["label"]=a
                        dict["sentence"]=str(dict["sentence"])+'.'
                        result.append(dict)
                
                print(len(result))
                print(result[0])
                tran="tran0_"+file
                
                with open(os.path.join(root,tran),"w") as f:
                    json.dump(result,f,indent=4)
                result=[]
               
# i="AddToPlaylist"
# res =domain2slot[i]
# print(res)

# h=[['fish', 'story']]
# print(h[0])
                
                
        


