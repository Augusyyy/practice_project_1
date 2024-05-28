from data.file_storage import FileStorage

storage = FileStorage()

country_data = storage.load_model_data('data/country.json')

