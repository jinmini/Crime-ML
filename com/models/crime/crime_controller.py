from com.models.crime.dataset import Dataset
from com.models.crime.crime_service import CrimeService

class CrimeController:

    def __init__(self):
        self.service = CrimeService() 

    def modeling(self):

        print("데이터 로딩 및 전처리 진행 중중")
        dataset = self.service.preprocess()  # ✅ Dataset 객체 반환
        self.print_this(dataset)  # ✅ Dataset 정보 출력
        return dataset
    
    @staticmethod
    def print_this(this):
        print('*' * 100)
        print(f'1. CCTV 데이터 유형: \n {type(this.cctv)}')
        print(f'2. CCTV 데이터 컬럼: \n {this.cctv.columns}')
        print(f'3. CCTV 데이터 상위 5개 행:\n {this.cctv.head()}')
        print(f'4. CCTV 데이터 결측치 개수:\n {this.cctv.isnull().sum()}개')
        print(f'5. 범죄 데이터 유형: \n {type(this.crime)}')
        print(f'6. 범죄 데이터 컬럼: \n {this.crime.columns}')
        print(f'7. 범죄 데이터 상위 5개 행:\n {this.crime.head()}')
        print(f'8. 범죄 데이터 결측치 개수:\n {this.crime.isnull().sum()}개')
        print(f'9. 인구 데이터 유형: \n {type(this.pop)}')
        print(f'10. 인구 데이터 컬럼: \n {this.pop.columns}')
        print(f'11. 인구 데이터 상위 5개 행:\n {this.pop.head()}')
        print(f'12. 인구 데이터 결측치 개수:\n {this.pop.isnull().sum()}개')
        print('*' * 100)