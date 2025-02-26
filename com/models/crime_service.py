import numpy as np
from sklearn import preprocessing
from com.models.data_reader import Datareader
from com.models.dataset import Dataset
from com.models.googlemap import GoogleMap
import pandas as pd
import os
from com.models import save_dir

class CrimeService:

    data_reader = Datareader()
    dataset = Dataset()

    def __init__(self):
        self.crime_rate_columns = ['살인검거율', '강도검거율', '강간검거율', '절도검거율', '폭력검거율']
        self.crime_columns = ['살인', '강도', '강간', '절도', '폭력']

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

        print(f"🌱save_csv 실행 : {fname}")
        full_name = os.path.join(save_dir, fname)

        if not os.path.exists(full_name) and  fname == "cctv_in_seoul.csv":
            this.cctv = self.create_matrix(fname)
            this = self.update_cctv(this)
            
        elif not os.path.exists(full_name) and  fname == "crime_in_seoul.csv":
            this.crime = self.create_matrix(fname)
            this = self.update_crime(this) 
            this = self.update_police(this) 

        elif not os.path.exists(full_name) and  fname == "pop_in_seoul.xls":
            this.pop = self.create_matrix(fname)
            this = self.update_pop(this)

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
    
        crime['자치구'] = gu_names

        crime.to_csv(os.path.join(save_dir, 'crime_in_seoul.csv'), index=False)
        this.crime = crime
        return this
    
    @staticmethod
    def update_police(this) -> object:

        crime = this.crime

        police = pd.pivot_table(crime, index='자치구', aggfunc=np.sum)

        # ✅ 검거율 계산
        for crime_type in ['살인', '강도', '강간', '절도', '폭력']:
            police[f'{crime_type}검거율'] = (police[f'{crime_type} 검거'] / police[f'{crime_type} 발생']) * 100

        # ✅ 검거율 100% 초과값 조정
        for col in ['살인검거율', '강도검거율', '강간검거율', '절도검거율', '폭력검거율']:
            police[col] = police[col].apply(lambda x: min(x, 100))

        police.reset_index(inplace=True)  # ✅ `자치구`를 컬럼으로 변환
        police = police[['자치구', '살인검거율', '강도검거율', '강간검거율', '절도검거율', '폭력검거율']]  # ✅ 컬럼 정리
        police = police.round(1)  # ✅ 소수점 첫째 자리 반올림

        police.to_csv(os.path.join(save_dir, 'police_in_seoul.csv'), index=False) 

        crime_rate_columns = ['살인검거율', '강도검거율', '강간검거율', '절도검거율', '폭력검거율']
        crime_columns = ['살인', '강도', '강간', '절도', '폭력']

        x = police[crime_rate_columns].values
        min_max_scalar = preprocessing.MinMaxScaler()
        """
          스케일링은 선형변환을 적용하여
          전체 자료의 분포를 평균 0, 분산 1이 되도록 만드는 과정
          """
        x_scaled = min_max_scalar.fit_transform(x.astype(float))
        """
         정규화 normalization
         많은 양의 데이터를 처리함에 있어 데이터의 범위(도메인)를 일치시키거나
         분포(스케일)를 유사하게 만드는 작업
         """
        police_norm = pd.DataFrame(x_scaled, columns=crime_columns, index=police.index)
        police_norm[crime_rate_columns] = police[crime_rate_columns]
        police_norm['범죄'] = np.sum(police_norm[crime_rate_columns], axis=1)
        police_norm['검거'] = np.sum(police_norm[crime_columns], axis=1)
        police_norm.to_csv(os.path.join(save_dir, 'police_norm_in_seoul.csv'))

        this.police = police

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
