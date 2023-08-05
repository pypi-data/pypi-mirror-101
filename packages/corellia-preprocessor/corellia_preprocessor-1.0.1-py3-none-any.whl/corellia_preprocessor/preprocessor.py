import pandas as pd
from ruamel.yaml import YAML

from corellia_preprocessor.operations import normalize, onehot_encode


class Preprocessor:

    def __init__(self, preprocess_file, data_file):
        """
        Instantiates a Preprocessor
        :param preprocess_file: Opened preprocess YAML file
        :param data_file: Opened data file
        """
        yaml = YAML()

        self.config = yaml.load(preprocess_file)

        self.label = self.config['label']
        self.features = self.config['features']

        self.data = pd.read_csv(data_file)

    def preprocess(self):
        """
        Preprocess test data according to Trainer requirements. By executing Trainer preprocess script
        :return: [Test data, Labels]
        """

        X = self.data[self.features]
        Y = self.data[[self.label]]

        for task in self.config['featureTasks']:
            if task['operation'] == 'normalize':
                X = normalize(X, **task.get('args', {}))

        for task in self.config['labelTasks']:
            if task['operation'] == 'onehot':
                Y = onehot_encode(Y, self.label, **task.get('args', {}))

        return X, Y
