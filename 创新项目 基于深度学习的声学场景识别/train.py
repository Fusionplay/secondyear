from .cnn import SceneNetwork
from .loader import FeaturesLoader

if __name__ == '__main__':
    train_dir      = r'F:\projectdata\train'
    validation_dir = r'F:\projectdata\valid'
    evaluation_dir = r'F:\projectdata\eval'

    # labels = ['bus', 'cafe_restaurant', 'beach', 'city_center', 'forest_path', 'car', 'grocery_store', 'home',
    #          'library', 'metro_station', 'office', 'park', 'residential_area', 'train', 'tram']
    labels = ['airport-barcelona', 'bus-london', 'metro-barcelona', 'metro_station-barcelona', 'park-barcelona',
              'public_square-barcelona',
              'shopping_mall-barcelona', 'street_pedestrian-barcelona', 'street_traffic-barcelona', 'tram-barcelona']
    # labels=['war','veh','str','rai','pla','for','bea','bar','the','tra']
    batch_size = 32

    # sampling_rate = 48000.0
    sampling_rate = 48000.0
    hop_size = 512.0
    time_duration = 10.0
    t_dim = (int(time_duration * sampling_rate / hop_size) + 1) * 2  # *2 for both *1 for MFCCs = (937 + 1) * 2

    n_features = 20

    input_shape = (n_features, t_dim, 1)

    # 获取特征
    train_loader = FeaturesLoader(train_dir, labels, n_features=n_features)
    validation_loader = FeaturesLoader(validation_dir, labels, n_features=n_features)
    evaluation_loader = FeaturesLoader(evaluation_dir, labels, n_features=n_features)

    x_train, y_train = train_loader.get_data()
    x_val, y_val = validation_loader.get_data()

    scene_network = SceneNetwork()
    scene_network.build_model(input_shape)

    scene_network.train_model(x_train, y_train, x_val, y_val, batch_size=batch_size, epochs=50)
    # scene_network.save_model('./etc/models/model.h5')
    scene_network.save_model(r'F:\projectdata\models\model.h5')
    # Clear dataset from memory
    del x_train
    del y_train
    del x_val
    del y_val

    x_eval, y_eval = evaluation_loader.get_data()
    scene_network.evaluate_model(x_eval, y_eval)
