from flask import json
import googlemaps
from com.models.crime.dataset import Dataset
import pandas as pd

class CrimeService:
    
    dataset = Dataset() #Dataset Instance 생성성

    def new_model(self, fname) -> object:

        this = self.dataset 
        this.context = "C:\\Users\\bitcamp\\Documents\\2025\\25ep_python(esg)\\Crimecity_250220\\com\\datas\\"
        this.fname = fname
        file_path = this.context + this.fname      

        if fname.endswith('.csv'):
                return pd.read_csv(file_path)
        elif fname.endswith('.xls') or fname.endswith('.xlsx'):
                return pd.read_excel(file_path)
        else:
                raise ValueError(f"지원하지 않는 파일 형식입니다 : {fname}. CSV 또는 Excel 파일만 사용 가능합니다.")
        

    def preprocess(self) -> Dataset:
        print("------------모델 전처리 시작-----------")
        this = self.dataset

        this.cctv_in_seoul = self.new_model("cctv_in_seoul.csv")
        this.crime_in_seoul = self.new_model("crime_in_seoul.csv")
        this.pop_in_seoul = self.new_model("pop_in_seoul.xls")
        print("데이터셋 로로딩 완료!")
    
        return this  
    


