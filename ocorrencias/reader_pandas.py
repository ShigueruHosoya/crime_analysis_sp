#%%
import os 
import pandas as pd 
import re
import time

start =time.perf_counter()

df_base = pd.DataFrame()
for idx,file in enumerate(os.listdir(os.path.join(os.getcwd(),'data'))):
    try:
        fname = ''.join(file.split('-')[1:])
        fname = fname.split('.csv')[0]
        fname = re.sub("\([^)]*\)", "", fname)
        fname = re.sub("  +"," ", fname).rstrip().lstrip()
        df = pd.read_csv(os.path.join(os.getcwd(),'data',file),
                    encoding='UTF-16-le',sep=';').columns.values[0]
        df_year = df 
        df = pd.read_csv(os.path.join(os.getcwd(),'data',file),
                        skiprows=1,encoding='UTF-16-le',sep=';')

        df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
        df['Ano'] = int(df_year)
        df['Delegacia'] = fname

        df_base = df_base.append(df)
    except Exception as e:
        print(e)
        pass
    
end = time.perf_counter()

print('Time elapsed: ', end-start)
    
# %%
df_base.head()
# %%
df_base['Ocorrencia'] = df_base['Ocorrencia'].str.replace(r"\(.*\)","", regex=True)
df_base['Ocorrencia'] = df_base['Ocorrencia'].str.replace(r"  +"," ", regex=True).str.rstrip().str.lstrip()
df_base = df_base.replace('...',0)
#%%
for idx,dtype in enumerate(df_base.dtypes):
    if idx ==0:
        pass
    elif idx >12:
        break
    else:
        df_base[df_base.columns[idx]] = df_base[df_base.columns[idx]].astype(float)
    
# %%
df_base_cp = df_base.groupby(['Ocorrencia', 'Ano', 'Delegacia']).sum().reset_index()

#%%
df_base_cp.drop(columns=['Os dados requisitados para o ano acima não estão disponíveis!'], axis=1,inplace=True)

#%%
df_base_cp.to_excel(r'C:\Users\Shigueru\Desktop\crime_analysis_sp\dados_compilados.xlsx',index=False)
# %%
