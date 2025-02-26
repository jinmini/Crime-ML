import numpy as np
from com.models.data_reader import Datareader
from com.models.dataset import Dataset
from com.models.googlemap import GoogleMap
import pandas as pd
import os
from com.models import save_dir

class CrimeService:

    data_reader = Datareader()
    dataset = Dataset()

    def preprocess(self, *args) -> Dataset:
        """파일 로드 및 전처리 함수"""
        print(f"------------모델 전처리 시작-----------")

        this = self.dataset
        for i in list(args):
            # print(f"args 값 출력: {i}")
            self.save_object_to_csv(this, i)
        return this
    
    def create_matrix(self, fname) -> object:
        reader = self.data_reader
        reader.fname = fname

        if fname.endswith('.csv'):
            return reader.csv_to_dframe()
        elif fname.endswith('.xls') or fname.endswith('.xlsx'):
            return reader.xls_to_dframe(header=2, usecols='B,D,G,J,N')
        else:
            raise ValueError(f"❌ 지원하지 않는 파일 형식: {fname}")

    def save_object_to_csv(self, this, fname) -> object:

        full_name = os.path.join(save_dir, fname)

        print(f"⛔save_csv 처음 : {fname}")
    
        if not os.path.exists(full_name) and  fname == "cctv_in_seoul.csv":
            this.cctv = self.create_matrix(fname)
            this = self.update_cctv(this)
            this.cctv.to_csv(full_name, index=False)
            
        elif not os.path.exists(full_name) and  fname == "crime_in_seoul.csv":
            this.crime = self.create_matrix(fname)
            this = self.update_crime(this) 
            this.crime.to_csv(full_name, index=False)

        elif not os.path.exists(full_name) and  fname == "pop_in_seoul.xls":
            this.pop = self.create_matrix(fname)
            this = self.update_pop(this)
            this.pop.to_csv(os.path.join(save_dir, "pop_in_seoul.csv"), index=False)

        else:
            print(f"파일이 이미 존재합니다. {fname}")

        return this
    
    @staticmethod
    def update_cctv(this) -> object:
        this.cctv = this.cctv.drop(['2013년도 이전', '2014년', '2015년', '2016년'], axis = 1)
        print(f"CCTV 데이터 헤드: {this.cctv.head()}")
        cctv = this.cctv
        cctv = cctv.rename(columns = {'기관명' : '자치구'})
        this.cctv = cctv
        return this
  
    @staticmethod
    def update_crime(this) -> object:

        gmaps = GoogleMap()

        print(f"CRIME 데이터 헤드: {this.crime.head()}")
        crime = this.crime
        station_names = [] # 경찰서 관서명 리스트
        for name in crime['관서명']:
            station_names.append('서울' + str(name[:-1]) + '경찰서')
        print(f"🔥💧경찰서 관서명 리스트: {station_names}")
        station_addrs = []
        station_lats = []
        station_lngs = []

        for name in station_names:
            tmp = gmaps.geocode(name, language = 'ko')
            print(f"""{name}의 검색 결과: {tmp[0].get("formatted_address")}""")
            station_addrs.append(tmp[0].get("formatted_address"))
            tmp_loc = tmp[0].get("geometry")
            station_lats.append(tmp_loc['location']['lat'])
            station_lngs.append(tmp_loc['location']['lng'])
            
        print(f"🔥💧자치구 리스트: {station_addrs}")
        gu_names = []
        for addr in station_addrs:
            tmp = addr.split()
            tmp_gu = [gu for gu in tmp if gu[-1] == '구'][0]
            gu_names.append(tmp_gu)
        [print(f"🔥💧자치구 리스트 2: {gu_names}")]
        crime['자치구'] = gu_names
      
        cols = ['살인 검거', '강도 검거', '강간 검거', '절도 검거', '폭력 검거']
        temp = crime[cols] / crime[cols].max()
        crime['검거율'] = np.sum(temp, axis=1)

        crime = crime[['자치구', '검거율']].round({'검거율': 1})

        this.crime = crime
        return this

    @staticmethod
    def update_pop(this) -> object:
        pop = this.pop
        pop = pop.rename(columns = {
            # pop.columns[0] : '자치구',  # 변경하지 않음
            pop.columns[1]: '인구수',   
            pop.columns[2]: '한국인',
            pop.columns[3]: '외국인',
            pop.columns[4]: '고령자',})
        this.pop = pop
        return this
    
    # @staticmethod
    # def merge_datasets():
    #     saved_dir = r"C:\\Users\\bitcamp\\Documents\\2025\\25ep_python(esg)\\Crimecity_250220\\com\saved_datas"

    #     cctv_file = os.path.join(saved_dir, "cctv_in_seoul_processed.csv")
    #     crime_file = os.path.join(saved_dir, "police_position.csv")
    #     pop_file = os.path.join(saved_dir, "pop_in_seoul_preprocess.csv")

    #     cctv_df = pd.read_csv(cctv_file, encoding='utf-8-sig')
    #     crime_df = pd.read_csv(crime_file, encoding='utf-8-sig')
    #     pop_df = pd.read_csv(pop_file, encoding='utf-8-sig')

    #     print("✅ CCTV 데이터 로드 완료:", cctv_df.shape)
    #     print("✅ 범죄 데이터 로드 완료:", crime_df.shape)
    #     print("✅ 인구 데이터 로드 완료:", pop_df.shape)

    #     merged_df = pd.merge(cctv_df, crime_df, on="자치구", how="inner")
    #     merged_df = pd.merge(merged_df, pop_df, on="자치구", how="inner")

    #     print("✅ 최종 데이터 병합 완료:", merged_df.shape)
    #     print("✅ 최종 데이터 상위 5개 행:\n", merged_df.head())

    #     final_save_path = os.path.join(saved_dir, "seoul_final_dataset.csv")
    #     merged_df.to_csv(final_save_path, index=False, encoding='utf-8-sig')
    #     print(f"✅ 최종 데이터 저장 완료: {final_save_path}")

    #     pass
