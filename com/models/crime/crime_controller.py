from com.models.crime.dataset import Dataset
from com.models.crime.crime_service import CrimeService

class CrimeController:
    dataset = Dataset()
    service = CrimeService()

    def modeling(self):
        print("데이터 로딩 및 전처리 진행 중중")
        this = self.service.preprocess()
        self.print_this(this)
        return this
    
    @staticmethod
    def print_this(this):
        print('*' * 100)
        print(f'1. CCTV 데이터 유형: \n {type(this.cctv_in_seoul)}')
        print(f'2. CCTV 데이터 컬럼: \n {this.cctv_in_seoul.columns}')
        print(f'3. CCTV 데이터 상위 5개 행:\n {this.cctv_in_seoul.head()}')
        print(f'4. CCTV 데이터 결측치 개수:\n {this.cctv_in_seoul.isnull().sum()}개')
        print(f'5. 범죄 데이터 유형: \n {type(this.crime_in_seoul)}')
        print(f'6. 범죄 데이터 컬럼: \n {this.crime_in_seoul.columns}')
        print(f'7. 범죄 데이터 상위 5개 행:\n {this.crime_in_seoul.head()}')
        print(f'8. 범죄 데이터 결측치 개수:\n {this.crime_in_seoul.isnull().sum()}개')
        print(f'9. 인구 데이터 유형: \n {type(this.pop_in_seoul)}')
        print(f'10. 인구 데이터 컬럼: \n {this.pop_in_seoul.columns}')
        print(f'11. 인구 데이터 상위 5개 행:\n {this.pop_in_seoul.head()}')
        print(f'12. 인구 데이터 결측치 개수:\n {this.pop_in_seoul.isnull().sum()}개')
        print('*' * 100)