import pickle


class FileStorage:
    def load_model_data(self,filename):
        with open(filename, 'rb') as f:
           contents = f.read()
           data = pickle.loads(contents)
           return data
