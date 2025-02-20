from com.models.crime.data_reader import Datareader
from com.models.crime.dataset import Dataset
import pandas as pd

class CrimeService:
    
    def __init__(self):
        self.data_reader = Datareader()  

    def new_model(self, fname) -> pd.DataFrame:

        self.data_reader.fname = fname

        if fname.endswith('.csv'):
            return self.data_reader.csv_to_dframe()  
        elif fname.endswith('.xls') or fname.endswith('.xlsx'):
            return self.data_reader.xls_to_dframe(header=0, usecols=None) 
        else:
            raise ValueError(f"지원하지 않는 파일 형식입니다: {fname}. CSV 또는 Excel 파일만 사용 가능합니다.")
    
    def preprocess(self) -> Dataset:
        print("------------모델 전처리 시작-----------")

        cctv_data = self.new_model("cctv_in_seoul.csv")
        crime_data = self.new_model("crime_in_seoul.csv")
        pop_data = self.new_model("pop_in_seoul.xls")

        print("데이터 로딩 완료!")

        dataset = Dataset(cctv=cctv_data, crime=crime_data, pop=pop_data)

        return dataset
