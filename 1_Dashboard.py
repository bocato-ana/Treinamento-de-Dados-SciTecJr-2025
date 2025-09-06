import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

st.title("Dashboard de Insights 📈")

# Verifica se o dataframe está no session_state (carregado pela app.py)
if 'df' not in st.session_state or st.session_state.df.empty:
    st.warning("Por favor, carregue os dados na página principal primeiro.")
    st.stop()

df = st.session_state.df

# --- Métricas Principais (KPIs) ---
# Usando colunas para organizar as métricas, um conceito de layout da "Aula 2".
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="Total de Registros", value=df.shape[0])
with col2:
    st.metric(label="Média de Idade", value=f"{df['Age'].mean():.1f} anos")
with col3:
    st.metric(label="Média de Tempo de Tela", value=f"{df['Avg_Daily_Screen_Time_hr'].mean():.2f} horas")

st.markdown("---")

# --- Gráficos Interativos ---
# Usando colunas novamente para colocar os gráficos lado a lado.
col1, col2 = st.columns(2)

with col1:
    # Gráfico 1: Distribuição do Tempo de Tela
    st.subheader("Distribuição do Tempo de Tela Diário")
    fig_hist = px.histogram(
        df,
        x='Avg_Daily_Screen_Time_hr',
        nbins=30,
        title="Frequência do Tempo de Tela (em horas)",
        labels={'Avg_Daily_Screen_Time_hr': 'Horas Diárias de Tela'},
        color_discrete_sequence=['#6a1b9a']
    )
    st.plotly_chart(fig_hist, use_container_width=True)

    # Gráfico 2: Tempo de Tela por Gênero
    st.subheader("Tempo de Tela por Gênero")
    fig_box = px.box(
        df,
        x='Gender',
        y='Avg_Daily_Screen_Time_hr',
        title="Comparativo de Tempo de Tela entre Gêneros",
        labels={'Gender': 'Gênero', 'Avg_Daily_Screen_Time_hr': 'Horas Diárias de Tela'},
        color='Gender',
        color_discrete_map={'Male': '#1e88e5', 'Female': '#d81b60'}
    )
    st.plotly_chart(fig_box, use_container_width=True)


with col2:
    # Gráfico 3: Dispositivos Mais Usados
    st.subheader("Dispositivos Principais Mais Utilizados")
    device_counts = df['Primary_Device'].value_counts().reset_index()
    device_counts.columns = ['Primary_Device', 'count']
    fig_pie = px.pie(
        device_counts,
        names='Primary_Device',
        values='count',
        title="Proporção de Uso por Dispositivo",
        hole=0.3,
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    st.plotly_chart(fig_pie, use_container_width=True)

    # Gráfico 4: Relação Idade vs Tempo de Tela
    st.subheader("Relação: Idade vs. Tempo de Tela")
    fig_scatter = px.scatter(
        df,
        x='Age',
        y='Avg_Daily_Screen_Time_hr',
        title="Idade vs. Horas de Tela",
        labels={'Age': 'Idade', 'Avg_Daily_Screen_Time_hr': 'Horas Diárias de Tela'},
        color='Urban_or_Rural',
        color_discrete_map={'Urban': '#6a1b9a', 'Rural': '#f9a825'},
        hover_data=['Gender', 'Primary_Device'] # Adiciona contexto ao passar o mouse
    )
    st.plotly_chart(fig_scatter, use_container_width=True)