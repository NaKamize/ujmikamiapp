from storages.backends.azure_storage import AzureStorage

class MediaStorage(AzureStorage):
    azure_container = 'media'
    expiration_secs = None

class StaticStorage(AzureStorage):
    azure_container = 'static'
    expiration_secs = None
