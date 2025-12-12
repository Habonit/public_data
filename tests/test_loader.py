"""
Tests for data loading utilities.

대상: utils/loader.py
TDD approach: Tests written before implementation per Constitution XII.
"""
import io
import os
import tempfile
import pytest
import pandas as pd
from utils.loader import read_csv_safe, read_uploaded_csv, get_dataset_info


class TestReadCsvSafe:
    """
    대상: utils/loader.py - read_csv_safe()
    의도: 다양한 인코딩의 CSV 파일 읽기 기능 검증
    """

    def test_read_utf8_csv(self, tmp_path):
        """
        대상: utils/loader.py:12 - read_csv_safe()
        의도: UTF-8 인코딩 CSV 파일 정상 읽기 검증
        """
        # Arrange
        csv_content = "name,age\n홍길동,30\n김철수,25"
        csv_file = tmp_path / "utf8.csv"
        csv_file.write_text(csv_content, encoding='utf-8')

        # Act
        df = read_csv_safe(str(csv_file))

        # Assert
        assert len(df) == 2
        assert list(df.columns) == ['name', 'age']
        assert df.iloc[0]['name'] == '홍길동'

    def test_read_cp949_csv(self, tmp_path):
        """
        대상: utils/loader.py:12 - read_csv_safe()
        의도: CP949 인코딩 CSV 파일 정상 읽기 검증
        """
        # Arrange
        csv_content = "이름,나이\n홍길동,30\n김철수,25"
        csv_file = tmp_path / "cp949.csv"
        csv_file.write_text(csv_content, encoding='cp949')

        # Act
        df = read_csv_safe(str(csv_file))

        # Assert
        assert len(df) == 2
        assert '이름' in df.columns
        assert df.iloc[0]['이름'] == '홍길동'

    def test_read_utf8_sig_csv(self, tmp_path):
        """
        대상: utils/loader.py:12 - read_csv_safe()
        의도: UTF-8 BOM 인코딩 CSV 파일 정상 읽기 검증
        """
        # Arrange
        csv_content = "name,value\ntest,100"
        csv_file = tmp_path / "utf8_sig.csv"
        csv_file.write_text(csv_content, encoding='utf-8-sig')

        # Act
        df = read_csv_safe(str(csv_file))

        # Assert
        assert len(df) == 1
        assert 'name' in df.columns

    def test_file_not_found_raises_error(self):
        """
        대상: utils/loader.py:12 - read_csv_safe()
        의도: 존재하지 않는 파일 경로 시 FileNotFoundError 발생 검증
        """
        # Act & Assert
        with pytest.raises(FileNotFoundError):
            read_csv_safe('/nonexistent/path/file.csv')

    def test_empty_csv_file_raises_error(self, tmp_path):
        """
        대상: utils/loader.py:12 - read_csv_safe()
        의도: 완전히 빈 CSV 파일 읽기 시 EmptyDataError 발생 검증

        Note: pandas.read_csv()는 컬럼조차 없는 빈 파일에서 EmptyDataError를 발생시킴.
              이는 소스 코드의 버그가 아니라 pandas의 정상 동작임.
        """
        # Arrange
        csv_file = tmp_path / "empty.csv"
        csv_file.write_text("", encoding='utf-8')

        # Act & Assert
        with pytest.raises(Exception):  # pandas.errors.EmptyDataError
            read_csv_safe(str(csv_file))

    def test_csv_with_header_only(self, tmp_path):
        """
        대상: utils/loader.py:12 - read_csv_safe()
        의도: 헤더만 있고 데이터가 없는 CSV 파일은 빈 DataFrame 반환 검증
        """
        # Arrange
        csv_file = tmp_path / "header_only.csv"
        csv_file.write_text("col1,col2,col3\n", encoding='utf-8')

        # Act
        df = read_csv_safe(str(csv_file))

        # Assert
        assert len(df) == 0
        assert list(df.columns) == ['col1', 'col2', 'col3']


class TestReadUploadedCsv:
    """
    대상: utils/loader.py - read_uploaded_csv()
    의도: 업로드된 파일 객체 읽기 기능 검증
    """

    def test_read_uploaded_utf8_csv(self):
        """
        대상: utils/loader.py:46 - read_uploaded_csv()
        의도: UTF-8 인코딩 업로드 파일 정상 읽기 검증
        """
        # Arrange
        csv_content = b"name,age\nAlice,30\nBob,25"
        uploaded_file = io.BytesIO(csv_content)

        # Act
        df = read_uploaded_csv(uploaded_file)

        # Assert
        assert len(df) == 2
        assert 'name' in df.columns
        assert df.iloc[0]['name'] == 'Alice'

    def test_read_uploaded_utf8_sig_csv(self):
        """
        대상: utils/loader.py:46 - read_uploaded_csv()
        의도: UTF-8 BOM 인코딩 업로드 파일 정상 읽기 검증
        """
        # Arrange
        csv_content = '\ufeffname,value\ntest,100'.encode('utf-8')
        uploaded_file = io.BytesIO(csv_content)

        # Act
        df = read_uploaded_csv(uploaded_file)

        # Assert
        assert len(df) == 1
        assert 'name' in df.columns

    def test_read_uploaded_cp949_csv(self):
        """
        대상: utils/loader.py:46 - read_uploaded_csv()
        의도: CP949 인코딩 업로드 파일 정상 읽기 검증
        """
        # Arrange
        csv_content = "이름,나이\n홍길동,30".encode('cp949')
        uploaded_file = io.BytesIO(csv_content)

        # Act
        df = read_uploaded_csv(uploaded_file)

        # Assert
        assert len(df) == 1
        assert '이름' in df.columns

    def test_uploaded_file_with_accident_datetime_preprocessed(self):
        """
        대상: utils/loader.py:46 - read_uploaded_csv()
        의도: 사고일시 컬럼 포함 시 전처리 자동 적용 검증
        """
        # Arrange
        csv_content = "사고일시,기상상태\n2022-01-01 08,맑음\n2022-06-15 18,흐림".encode('utf-8')
        uploaded_file = io.BytesIO(csv_content)

        # Act
        df = read_uploaded_csv(uploaded_file)

        # Assert
        assert '시간대' in df.columns
        assert '사고연' in df.columns
        assert df.iloc[0]['시간대'] == '출근시간대'

    def test_uploaded_file_seek_reset(self):
        """
        대상: utils/loader.py:46 - read_uploaded_csv()
        의도: 파일 포인터가 리셋되어 재읽기 가능 검증
        """
        # Arrange
        csv_content = b"col1,col2\na,1\nb,2"
        uploaded_file = io.BytesIO(csv_content)
        # 파일 포인터를 끝으로 이동
        uploaded_file.seek(0, 2)

        # Act
        df = read_uploaded_csv(uploaded_file)

        # Assert
        assert len(df) == 2


class TestGetDatasetInfo:
    """
    대상: utils/loader.py - get_dataset_info()
    의도: DataFrame 메타정보 반환 기능 검증
    """

    def test_normal_dataframe_info(self):
        """
        대상: utils/loader.py:173 - get_dataset_info()
        의도: 정상 DataFrame의 메타정보 반환 검증
        """
        # Arrange
        df = pd.DataFrame({
            'name': ['Alice', 'Bob', 'Charlie'],
            'age': [25, 30, 35],
            'score': [90.5, 85.0, 92.3]
        })

        # Act
        info = get_dataset_info(df)

        # Assert
        assert info['row_count'] == 3
        assert info['column_count'] == 3
        assert 'name' in info['dtypes']
        assert 'age' in info['dtypes']
        assert info['missing_ratios']['name'] == 0.0

    def test_empty_dataframe_info(self):
        """
        대상: utils/loader.py:173 - get_dataset_info()
        의도: 빈 DataFrame의 메타정보 반환 검증
        """
        # Arrange
        df = pd.DataFrame()

        # Act
        info = get_dataset_info(df)

        # Assert
        assert info['row_count'] == 0
        assert info['column_count'] == 0
        assert info['dtypes'] == {}
        assert info['missing_ratios'] == {}
        assert info['numeric_summary'].empty

    def test_dataframe_with_missing_values(self):
        """
        대상: utils/loader.py:173 - get_dataset_info()
        의도: 결측값 포함 DataFrame의 missing_ratios 계산 검증
        """
        # Arrange
        df = pd.DataFrame({
            'col1': [1, 2, None, 4],
            'col2': [None, None, 'c', 'd']
        })

        # Act
        info = get_dataset_info(df)

        # Assert
        assert info['missing_ratios']['col1'] == 0.25  # 1/4
        assert info['missing_ratios']['col2'] == 0.5   # 2/4

    def test_numeric_summary_generated(self):
        """
        대상: utils/loader.py:173 - get_dataset_info()
        의도: 숫자형 컬럼 통계(describe) 생성 검증
        """
        # Arrange
        df = pd.DataFrame({
            'numeric': [10, 20, 30, 40, 50],
            'text': ['a', 'b', 'c', 'd', 'e']
        })

        # Act
        info = get_dataset_info(df)

        # Assert
        assert not info['numeric_summary'].empty
        assert 'numeric' in info['numeric_summary'].columns
        assert 'mean' in info['numeric_summary'].index

    def test_categorical_summary_generated(self):
        """
        대상: utils/loader.py:173 - get_dataset_info()
        의도: 범주형 컬럼 value_counts 생성 검증
        """
        # Arrange
        df = pd.DataFrame({
            'category': ['A', 'B', 'A', 'A', 'C'],
            'value': [1, 2, 3, 4, 5]
        })

        # Act
        info = get_dataset_info(df)

        # Assert
        assert 'category' in info['categorical_summary']
        assert info['categorical_summary']['category']['A'] == 3
        assert info['categorical_summary']['category']['B'] == 1

    def test_categorical_summary_limited_to_top_20(self):
        """
        대상: utils/loader.py:173 - get_dataset_info()
        의도: 범주형 컬럼 value_counts가 상위 20개로 제한되는지 검증
        """
        # Arrange
        df = pd.DataFrame({
            'category': [f'cat_{i}' for i in range(30)]
        })

        # Act
        info = get_dataset_info(df)

        # Assert
        assert len(info['categorical_summary']['category']) <= 20

    def test_dtypes_correctly_captured(self):
        """
        대상: utils/loader.py:173 - get_dataset_info()
        의도: 다양한 데이터 타입이 올바르게 캡처되는지 검증
        """
        # Arrange
        df = pd.DataFrame({
            'int_col': [1, 2, 3],
            'float_col': [1.1, 2.2, 3.3],
            'str_col': ['a', 'b', 'c'],
            'bool_col': [True, False, True]
        })

        # Act
        info = get_dataset_info(df)

        # Assert
        assert 'int' in info['dtypes']['int_col']
        assert 'float' in info['dtypes']['float_col']
        assert info['dtypes']['str_col'] == 'object'
        assert 'bool' in info['dtypes']['bool_col']
