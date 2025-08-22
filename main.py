import pandas as pd

# 读取 .dta 文件
df = pd.read_stata('national_survey_for_wales_2018-19.dta')  # 替换为你的文件路径

# 1. 定义要保留的列（根据需求修改此列表）
columns_to_keep = ['CaseNo', 'Dvillness4', 'NatIdPol', 'EconStat', 'NatIdOth', 'DvHiQual2', 'DvWIMDOvr5', 'DvFGComm', 'NatIdEng',
                   'NatIdBrit', 'NatIdNI', 'LaOvSat', 'NatIdWel', 'LaBelong', 'Garden', 'NatIdScot', 'WbSatLife', 'Gender', 'LaDifBgrnd',
                   'DvWEMWBS', 'VisitWhy14', 'WbLifeWrth', 'SampleNRWWeight', 'DvAgeGrp7', 'LaRespCons']

df = df[[col for col in columns_to_keep if col in df.columns]]

# 2. 筛选 gender 列，仅保留 'male' 或 'female'
valid_genders = ['male', 'female']
if 'gender' in df.columns:
    df = df[df['gender'].isin(valid_genders)].copy()  # 使用 .copy() 避免 SettingWithCopyWarning
    print("已筛选 gender 列，仅保留 'male' 和 'female'")
else:
    print("gender 列不存在")

# 可选：保存回 .dta 文件
df.to_stata('processed_file.dta', write_index=False)
