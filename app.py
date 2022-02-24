import streamlit as st
import pandas as pd
from collections import defaultdict

st.title("Hospital Demo")

@st.cache
def read_files(paths, sheet_name):
    return pd.concat([pd.read_excel(path, sheet_name=sheet_name) for path in paths])


def strip(x):
    try:
        if type(x) == str:
            x = x.strip()
            if x == "":
                return None
            return x.strip()
        else:
            return None
    except:
        pass


files = st.file_uploader('上传数据（请一次性上传所有excel）:', type=['xls', 'xlsx'], accept_multiple_files=True)
sheet_name = st.text_input('Excel表名', value='手术')
if files:
    c2i = defaultdict(int)
    with st.sidebar:
        st.header('手术价值设置')
        c2i['四级'] = st.number_input('四级手术价值：', value=4)
        c2i['三级'] = st.number_input('三级手术价值：', value=3)
        c2i['二级'] = st.number_input('二级手术价值：', value=2)
        c2i['一级'] = st.number_input('一级手术价值：', value=1)
        st.header('助手折减系数设置')
        factor1 = st.number_input('一助折减系数：', value=0.7, step=0.1)
        factor2 = st.number_input('二助折减系数：', value=0.6, step=0.1)
    df = read_files(files, sheet_name)
    df = df[~df['手术医生'].isna()]
    use_col = ['手术项目1', '分级1', '手术项目2', '分级2', '手术项目3', '分级3', '手术项目4', '分级4',
               '手术项目5', '分级5', '手术项目6', '分级6', '手术项目7', '分级7', '手术医生', '一助', '二助']
    df = df[use_col]
    df = df.applymap(strip).reset_index(drop=True)
    ans = {}
    for ind, row in df.iterrows():
        score = 0
        for i in range(1, 8):
            score += c2i[row["分级" + str(i)]]
        if row.手术医生 is not None:
            if ans.get(row.手术医生):
                ans[row.手术医生] += score
            else:
                ans[row.手术医生] = score
        if row.一助 is not None:
            if ans.get(row.一助):
                ans[row.一助] += score * factor1
            else:
                ans[row.一助] = score * factor1
        if row.二助 is not None:
            if ans.get(row.二助):
                ans[row.二助] += score * factor2
            else:
                ans[row.二助] = score * factor2
    ans = pd.Series(ans, name='分数').to_frame().reset_index().sort_values('分数', ascending=False).reset_index(drop=True)
    st.table(ans)