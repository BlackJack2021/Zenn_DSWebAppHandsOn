import numpy as np
import pandas as pd
from pathlib import Path
import lightgbm
from lightgbm import LGBMClassifier
import pickle
import warnings
warnings.simplefilter('ignore', pd.core.common.SettingWithCopyWarning)


class GenerateModel:

    base_dir = Path(__file__).resolve().parent

    def __init__(self):
        pass

    @classmethod
    def __read_data(cls) -> pd.DataFrame:
        path_to_data = cls.base_dir / 'data' / 'train.csv'
        return pd.read_csv(path_to_data)

    @staticmethod
    def __extract_required_columns(df: pd.DataFrame):
        required_columns = ['Survived','Sex','Pclass','Age','Parch','SibSp']
        return df[required_columns]
    
    @staticmethod
    def encode_sex(x: str):
        if x in ('male', '男性'):
            return 1
        elif x in ('female', '女性'):
            return 0
        else:
            return np.nan

    @classmethod
    def __preprocess_df(cls, df: pd.DataFrame) -> pd.DataFrame:
        tmp_df = cls.__extract_required_columns(df)
        tmp_df['Sex'] = tmp_df['Sex'].apply(lambda x: cls.encode_sex(x))
        return tmp_df

    @staticmethod
    def __train_model(df: pd.DataFrame) -> lightgbm.sklearn.LGBMModel:
        '''
        目的変数を Survived とし、LightGBMによる学習を行います。
        '''
        y = df['Survived']
        X = df.drop(['Survived'], axis=1)
        
        model = LGBMClassifier()
        model.fit(X.values, y.values)

        return model

    @classmethod
    def __save_model(cls, model: lightgbm.sklearn.LGBMModel):
        '''
        pickle 形式で作成した lightGBM モデルを保存します。
        '''
        path_to_model = cls.base_dir / 'model' / 'model.pkl'
        with open(path_to_model, "wb") as f:
            pickle.dump(model, f)

    @classmethod
    def generate_model(cls):
        '''
        モデルの学習から保存まで一貫して行います。
        '''
        df = cls.__read_data()
        preprocessed_df = cls.__preprocess_df(df)
        lgbm_model = cls.__train_model(preprocessed_df)
        cls.__save_model(lgbm_model)


class PredictOnAPI(GenerateModel):

    def __init__(self):
        pass

    @classmethod
    def __load_model(cls):
        '''
        pickle 形式で作成されたモデルを読み込みます。
        存在しない場合は作成を行います。
        '''

        path_to_model = cls.base_dir / 'model' / 'model.pkl'
        if path_to_model.exists() == False:
            print('modelが存在しないので作成します。')
            cls.generate_model()

        with open(path_to_model, "rb") as f:
            model = pickle.load(f)

        return model

    @staticmethod
    def __encode_pclass(x: str):
        if x == '上層クラス（お金持ち）':
            return 1
        elif x == '中級クラス（一般階級）':
            return 2
        elif x == '下層クラス（労働階級）':
            return 3
        else:
            return np.nan

    @classmethod
    def derive_survival_probability(
        cls,
        Sex: str,
        Pclass: str,
        Age: int,
        Parch: int,
        SibSp: int
    ) -> float:

        '''
        与えられた特徴量について、
        事前に学習済みのモデルを用いてタイタニック生存確率を算出します。
        '''
        model = cls.__load_model()

        encoded_sex = cls.encode_sex(Sex)
        encoded_pclass = cls.__encode_pclass(Pclass)

        features = np.array([[
            encoded_sex, encoded_pclass, Age, Parch, SibSp
        ]])

        survival_probability = model.predict_proba(features)[0][1]

        return round(survival_probability,3)

