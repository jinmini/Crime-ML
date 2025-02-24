from com.models.crime.data_reader import Datareader
from com.models.crime.dataset import Dataset
from com.models.crime.googlemap import GoogleMap
import pandas as pd
import os

class CrimeService:

    data_reader = Datareader()
    dataset = Dataset()
    gmaps = GoogleMap()

    def new_model(self, fname) -> pd.DataFrame:

        self.data_reader.fname = fname

        if fname.endswith('.csv'):
            return self.data_reader.csv_to_dframe() 
        elif fname.endswith('.xls') or fname.endswith('.xlsx'):
            return self.data_reader.xls_to_dframe(header=2, usecols='B,D,G,J,N') 
        else:
            raise ValueError(f"지원하지 않는 파일 형식입니다: {fname}. CSV 또는 Excel 파일만 사용 가능합니다.")
    
    def preprocess(self) -> Dataset:
        print("------------모델 전처리 시작-----------")
    
        cctv_data = self.new_model("cctv_in_seoul.csv")
        crime_data = self.new_model("crime_in_seoul.csv")
        pop_data = self.new_model("pop_in_seoul.xls")

        dataset = Dataset(cctv=cctv_data, crime=crime_data, pop=pop_data)
        
        dataset = self.cctv_ratio(dataset)
        dataset = self.crime_ordinal(dataset)
        dataset = self.pop_ratio(dataset)

        return dataset
    
    @staticmethod
    def cctv_ratio(dataset) -> object:
        cctv = dataset.cctv
        dataset.cctv = dataset.cctv.drop (['2013년도 이전', '2014년', '2015년', '2016년'], axis =1)
        print(f"✅ CCTV 데이터 Null 값 개수:\n, {dataset.cctv.isnull().sum()}")
        print(f'cctv 데이터 상위 5개 행:\n {cctv.head()}')
        return dataset
    
    @staticmethod
    def crime_ordinal(dataset) -> object:
    
        crime = dataset.crime
        print(f"\n✅ 범죄 데이터 Null 값 개수:\n, {dataset.crime.isnull().sum()}")
        print(f'crime 데이터 상위 5개 행:\n {crime.head()}')
        station_names = []
        for name in crime['관서명']:
            station_names.append('서울'+str(name[:-1]) + '경찰서')
        print(f"경찰서 관서명 리스트 : {station_names}")
        station_addrs = []
        station_lats = []
        station_lngs = []

        for name in station_names:
            tmp = CrimeService.gmaps.client.geocode(name, language = 'ko')
            if tmp:
                station_addrs.append(tmp[0].get("formatted_address")) 
                tmp_loc = tmp[0].get("geometry")
                station_lats.append(tmp_loc["location"]["lat"])
                station_lngs.append(tmp_loc["location"]["lng"])

        print(f"자치구 리스트 👇: {station_addrs}")
        gu_names = []
        for addr in station_addrs:
            tmp = addr.split()
            tmp_gu = [gu for gu in tmp if gu[-1] == '구'][0]
            gu_names.append(tmp_gu)
        print(f"자치구 리스트 2 👇: {gu_names}")

        crime['자치구'] = gu_names

        save_dir = r"C:\\Users\\bitcamp\\Documents\\2025\\25ep_python(esg)\\Crimecity_250220\\com\\saved_datas"
        os.makedirs(save_dir, exist_ok=True)  
        save_path = os.path.join(save_dir, 'police_position.csv')

        crime.to_csv(save_path, index=False, encoding='utf-8-sig')  
        print(f"✅ 변환된 데이터가 저장됨: {save_path}")

        # gmaps1 = CrimeService.gmaps
        # gmaps2 = CrimeService.gmaps
        
        # print("🅾️ ",gmaps1 is gmaps2)

        return dataset

    @staticmethod
    def pop_ratio(dataset) -> object:
        pop = dataset.pop
        pop.rename(columns = { # pop.columns[0] : '자치구', # 변경하지 않음.  
            pop.columns[1]: '인구수',
            pop.columns[2]: '한국인',
            pop.columns[3]: '외국인',
            pop.columns[4]: '고령자',}, inplace = True)
        print(f"\n✅ 인구 데이터 Null 값 개수:\n, {dataset.pop.isnull().sum()}")
        print(f'pop 데이터 상위 5개 행:\n {pop.head()}')
        return dataset