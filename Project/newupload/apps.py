from django.apps import AppConfig
from .service.file_service import *
import pandas as pd


class NewuploadConfig(AppConfig):
    name = 'newupload'
    def ready(self):
        cleanFolder("training")
        cleanFolder("up")
        cleanFolder("dataset")
        # cleanFolder("usermodels")
        df = pd.DataFrame(data = None, columns = ["filename", "seizurestart", "seizureEnd", "channels", "nSignal", "sampleFrequency"])
        fs = FileSystemStorage()
        dir = os.path.join(fs.base_location, "training", "file_list.csv")
        df.to_csv(dir, header=True, index=False)
        print("on startup")