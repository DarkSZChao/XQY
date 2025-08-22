import numpy as np
import pyreadr
import pandas as pd


def read_rds_file(file_path):
    result = pyreadr.read_r(file_path)
    data = result[None]
    return data


# 使用示例
if __name__ == "__main__":
    file_path = "mydata1.rds"  # 替换为你的文件路径
    df = read_rds_file(file_path)

    # NatIDWel = df.iloc[:, 1]
    # NatIDEng = df.iloc[:, 2]
    # NatIDScot = df.iloc[:, 3]
    # NatIDNI = df.iloc[:, 4]
    # NatIDBrit = df.iloc[:, 5]

    df['NatGroup'] = np.where(
        (df['NatIdBrit'] == 1) |
        (df['NatIdEng'] == 1) |
        (df['NatIdNI'] == 1) |
        (df['NatIdScot'] == 1) |
        (df['NatIdWel'] == 1),
        1, 0
    )
    df['NatGroup2'] = np.where(
        (df['NatIdOth'] == 1) |
        (df['NatIdPol'] == 1) |
        (df['NatIdDK'] == 1) |
        (df['NatIdRef'] == 1),
        1, 0
    )
    test = ((df['NatGroup'] == 1) & (df['NatGroup2'] == 1)).astype(int)

    df['WbSatLifeLevel'] = (df['WbSatLife'] >= 8).astype(int)
    df['WbLifeWrthLevel'] = (df['WbLifeWrth'] >= 8).astype(int)

    nan_stats_df = pd.DataFrame({
        'variable' : df.columns,
        'n_miss'   : df.isnull().sum().values,
        'prop_miss': df.isnull().mean().values,
        'pct_miss' : (df.isnull().mean() * 100).values
    })
    nan_stats_df = nan_stats_df.sort_values('n_miss', ascending=False)

    # pyreadr.write_rds('mydata1_miss.rds', nan_stats_df)

    # 补充nan
    # nan_mask = df['Gender'].isnull()
    # print(nan_mask[nan_mask].index.tolist())
    # df.loc[nan_mask, 'Gender'] = np.random.choice([1, 2], size=nan_mask.sum())

    columns_to_process = [
        'DvFGComm',  # 3.40%
        'LaDifBgrnd',  # 2.55%
        'DvHiQual2',  # 1.52%
        'LaRespCons',  # 1.07%
        'WbLifeWrth',  # 0.68%
        'Dvillness4',  # 0.60%
        'LaBelong',  # 0.49%
        'WbSatLife',  # 0.39%
        'LaOvSat',  # 0.22%
        'EconStat',  # 0.13%
        'Gender'  # 0.03%
    ]
    for column in columns_to_process:
        print(f'Working on: {column}')

        nan_mask = df[column].isnull()
        print('nan values:', nan_mask.sum(), nan_mask[nan_mask].index.tolist())

        mean_value = round(df[column].mean())
        print('mean values:', mean_value)

        df[column] = df[column].fillna(mean_value)

        pass










    pass
