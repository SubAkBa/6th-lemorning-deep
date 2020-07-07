import os

from deep.model import DeepModel
from search_engine.milvusdb import SearchEngine

if __name__ == '__main__':
    model = DeepModel()
    path_root = 'data/audio/test/'
    path_audios = [os.path.join(path_root, file) for file in os.listdir(path_root)]
    path_new_audio = 'data/audio/joram-moments_of_clarity-08-solipsism-59-88.mp3'

    HOST = 'localhost'
    PORT = 19530

    # 1. set engine
    engine = SearchEngine(HOST, PORT)

    ##############################
    # Collection
    ##############################
    # 2-1. create collection 
    engine.create_engine('musicDB', 753)

    # 2-2. show info of collection 
    engine.get_collection_stats()

    # 2-3. delete collection
    engine.drop_collection('musicDB')

    ##############################
    # CRUD Data
    ##############################
    engine.create_engine('musicDB', 753)
    engine.set_collection('musicDB')

    # 3-1. insert data
    for i, path_audio in enumerate(path_audios):
        feature = model.extract_info(path_audio, mode='feature')
        engine.insert_data(i, feature)
    engine.get_collection_stats()

    # 3-3. update data
    feature = model.extract_info(path_new_audio, mode='feature')
    engine.update_data(len(path_audio), feature)
    engine.get_collection_stats()

    # 3-3. update data
    engine.delete_data(len(path_audios))
    engine.get_collection_stats()

    ##############################
    # Search Data
    ##############################
    
    # 4-1. search data by feature
    li_id, li_distance = engine.search_by_feature(feature, 5)
    result = [(idx, dis) for idx, dis in zip(li_id, li_distance)]
    print(result)

    # 4-2. search data by key
    li_id, li_distance = engine.search_by_key(len(path_audio) - 1, 5)    
    result = [(idx, dis) for idx, dis in zip(li_id, li_distance)]
    print(result)
