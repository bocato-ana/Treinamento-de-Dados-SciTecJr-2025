import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.metrics import accuracy_score, confusion_matrix

st.set_page_config(page_title="Previsão de Depressão", layout="wide")

st.title("📊 Modelos de Machine Learning - Previsão de Depressão")

# --- Dados de exemplo ---
data = {
    'Choose your gender': [False, True, True, False, True, True, False, False, False, True, False, False, False, True, False, True],
    'Age': [18, 21, 19, 22, 23, 19, 23, 18, 19, 18, 20, 24, 18, 19, 18, 24],
    'What is your course?': ['Engineering', 'Islamic Education', 'Information Technology', 'Law', 'Mathematics', 'Engineering',
                             'Islamic Education', 'Information Technology', 'Human Resources', 'Human Sciences',
                             'Psychology', 'Engineering', 'Information Technology', 'Engineering', 'Business & Economics', 'Information Technology'],
    'Marital status': [False, False, False, True, False, False, True, False, False, False, False, True, False, False, False, False],
    'Do you have Depression?': [1, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0],
    'Do you have Anxiety?': [0, 1, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0],
    'Do you have Panic attack?': [1, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0],
    'Did you seek any specialist for a treatment?': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
}

df = pd.DataFrame(data)

# --- Tratamento dos dados ---
df['Age'].fillna(df['Age'].mean(), inplace=True)
df['Choose your gender'] = df['Choose your gender'].astype(int)
df['Marital status'] = df['Marital status'].astype(int)
df = pd.get_dummies(df, columns=['What is your course?'], drop_first=True)

# --- Separação de dados ---
X = df.drop(columns=['Do you have Depression?'])
y = df['Do you have Depression?']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# --- Modelos ---
model_log = LogisticRegression(max_iter=1000)
model_tree = DecisionTreeClassifier(max_depth=3, random_state=42)

model_log.fit(X_train, y_train)
model_tree.fit(X_train, y_train)

y_pred_log = model_log.predict(X_test)
y_pred_tree = model_tree.predict(X_test)

acc_log = accuracy_score(y_test, y_pred_log)
acc_tree = accuracy_score(y_test, y_pred_tree)

# --- Exibir resultados ---
st.subheader("✅ Acurácia dos Modelos")
col1, col2 = st.columns(2)
col1.metric("Regressão Logística", f"{acc_log*100:.2f}%")
col2.metric("Árvore de Decisão", f"{acc_tree*100:.2f}%")

# --- Matrizes de Confusão ---
st.subheader("📌 Matrizes de Confusão")

fig1, ax1 = plt.subplots()
sns.heatmap(confusion_matrix(y_test, y_pred_log), annot=True, cmap='Blues', fmt='d', ax=ax1)
ax1.set_title("Matriz - Regressão Logística")
ax1.set_xlabel("Previsto")
ax1.set_ylabel("Real")
st.pyplot(fig1)

fig2, ax2 = plt.subplots()
sns.heatmap(confusion_matrix(y_test, y_pred_tree), annot=True, cmap='Greens', fmt='d', ax=ax2)
ax2.set_title("Matriz - Árvore de Decisão")
ax2.set_xlabel("Previsto")
ax2.set_ylabel("Real")
st.pyplot(fig2)

# --- Árvore de Decisão ---
st.subheader("🌳 Visualização da Árvore de Decisão")

fig3, ax3 = plt.subplots(figsize=(12, 5))
plot_tree(model_tree, filled=True, feature_names=X.columns, class_names=['No', 'Yes'], rounded=True, ax=ax3)
st.pyplot(fig3)
