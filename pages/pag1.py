import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('Student Mental health.csv')

st.title("""Dashboard de Insights
- Considerações Iniciais
         
        -Idade
        -Gênero
        -Situação Matrimonial""")

#criando graficos lado a lado
fig, axes = plt.subplots(1, 3, figsize=(24, 6))

#Histograma 'Age'"Student Mental health.csv"
sns.histplot(df['Age'], bins=7, kde=True, ax=axes[0], color='salmon')
axes[0].set_title('Distribuição da idade dos Entrevistados')
axes[0].set_xlabel('Idade')
axes[0].set_ylabel('Quantidade')


#Grafico de pizza idade
genero_counts = df['Choose your gender'].value_counts()
genero_counts.index = genero_counts.index.map({True:'Male' , False:'Female'})

axes[1].pie(
    genero_counts,
    labels=genero_counts.index,
    autopct='%1.1f%%',
    startangle=90,
    colors=['pink', 'skyblue', 'lightgray']
)
axes[1].set_title('Distribuição por genêro')
axes[1].axis('equal')

#Gráfico de Pizza matrimonio
matrimonio_counts = df['Marital status'].value_counts()
matrimonio_counts.index = matrimonio_counts.index.map({False:'No', True:'Yes'})

axes[2].pie(
    matrimonio_counts,
    labels=matrimonio_counts.index,
    autopct='%1.1f%%',
    startangle=90,
    colors=['lightgreen', 'lightyellow']
)
axes[2].set_title('Situação Matrimonial')
axes[2].axis('equal')


#sem sobreposição
plt.tight_layout()
st.pyplot(fig)

st.write("Gráfico: Doenças mentais por quantidade de pessoa")

colunas = ['Do you have Depression?', 'Do you have Anxiety?', 'Do you have Panic attack?']
contagens = df[colunas].sum()

fig, ax = plt.subplots(figsize=(8,6))
ax.bar(contagens.index, contagens.values, color='skyblue')  # ← CORRIGIDO AQUI

ax.set_title('Doenças Mentais')
ax.set_xlabel('Condição')
ax.set_ylabel('Quantidade de Pessoas')
plt.tight_layout()
st.pyplot(fig)

st.write('Pessoas que procuram ajuda por tipo de doença')
colunas = ['Do you have Depression?', 'Do you have Anxiety?', 'Do you have Panic attack?']

contagens = {}

for coluna in colunas:
    cont = 0
    for i in range(len(df)):
        if df[coluna].iloc[i] == 1 and df['Did you seek any specialist for a treatment?'].iloc[i] == 1:
            cont += 1
    contagens[coluna] = cont

#st.write(contagens)  # Opcional: mostra o dicionário na tela

fig, ax = plt.subplots(figsize=(8,6))
ax.bar(contagens.keys(), contagens.values(), color='orchid')
ax.set_title('Pessoas que Procuraram Ajuda por Tipo de Doença Mental')
ax.set_xlabel('Condição')
ax.set_ylabel('Quantidade de Pessoas')
plt.xticks(rotation=20)
plt.tight_layout()

st.pyplot(fig)


st.write("Relação entre casamento e doença mental")

# 1. Verifica se a pessoa tem pelo menos uma doença mental
df['Tem_alguma_doenca'] = (
    (df['Do you have Depression?'] == 1) |
    (df['Do you have Anxiety?'] == 1) |
    (df['Do you have Panic attack?'] == 1)
)

# 2. Cria categorias combinando estado civil e presença de doença
def classificar_pessoa(row):
    if row['Marital status'] == 1 and row['Tem_alguma_doenca']:
        return 'Casado e com Doença Mental'
    elif row['Marital status'] == 1:
        return 'Casado e Saudável'
    elif row['Marital status'] == 0 and row['Tem_alguma_doenca']:
        return 'Não Casado e com Doença'
    else:
        return 'Não Casado e Saudável'

df['Categoria_Mental_Marital'] = df.apply(classificar_pessoa, axis=1)

# 3. Conta as categorias
contagem = df['Categoria_Mental_Marital'].value_counts()

# 4. Cria o gráfico de pizza com Streamlit
fig, ax = plt.subplots(figsize=(6,6))
cores = ['green', 'lightgreen', 'red', 'lightcoral']
ax.pie(
    contagem,
    labels=contagem.index,
    autopct='%1.1f%%',
    startangle=90,
    colors=cores
)
ax.set_title('Relação entre Estado Civil e Doença Mental')
ax.axis('equal')
plt.tight_layout()

st.pyplot(fig)
