import streamlit as st
import pandas as pd
from datetime import datetime

st.title("Formulário para Adicionar Novos Dados 📝")

# Verifica se o dataframe está no session_state
if 'df' not in st.session_state or st.session_state.df.empty:
    st.warning("Base de dados não carregada. Volte para a página principal.")
    st.stop()

# Exemplo prático do st.form da "Aula 2"
# O formulário agrupa os elementos e só envia os dados quando o botão é clicado.
with st.form(key="add_data_form"):
    st.subheader("Informações da Criança")

    # Usando colunas para melhor layout do formulário
    col1, col2 = st.columns(2)

    with col1:
        age = st.number_input("Idade", min_value=1, max_value=18, step=1)
        gender = st.selectbox("Gênero", options=["Male", "Female"])
        location = st.selectbox("Localização", options=["Urban", "Rural"])
        primary_device = st.selectbox("Dispositivo Principal", options=["Smartphone", "Tablet", "Laptop", "TV"])

    with col2:
        screen_time = st.slider("Tempo Médio de Tela (horas)", min_value=0.0, max_value=10.0, step=0.1)
        edu_ratio = st.slider("Proporção Educacional/Recreacional", min_value=0.0, max_value=1.0, step=0.01)
        exceeded_limit = st.checkbox("Excedeu o Limite Recomendado?")

    st.subheader("Observações de Saúde (Marque se aplicável)")
    col_health1, col_health2, col_health3, col_health4 = st.columns(4)
    with col_health1:
        anxiety = st.checkbox("Ansiedade")
    with col_health2:
        eye_strain = st.checkbox("Cansaço Visual")
    with col_health3:
        obesity_risk = st.checkbox("Risco de Obesidade")
    with col_health4:
        poor_sleep = st.checkbox("Sono Ruim")

    # Botão de envio do formulário
    submit_button = st.form_submit_button(label="Adicionar Registro")

# Lógica para processar os dados após o envio do formulário
if submit_button:
    # Cria um dicionário com os novos dados
    new_data = {
        'Age': age,
        'Gender': gender,
        'Avg_Daily_Screen_Time_hr': screen_time,
        'Primary_Device': primary_device,
        'Exceeded_Recommended_Limit': exceeded_limit,
        'Educational_to_Recreational_Ratio': edu_ratio,
        'Urban_or_Rural': location,
        'Anxiety': anxiety,
        'Eye Strain': eye_strain,
        'Obesity Risk': obesity_risk,
        'Poor Sleep': poor_sleep
    }

    # Converte o dicionário para um DataFrame
    new_df = pd.DataFrame([new_data])

    # Carrega o dataframe atual do estado da sessão
    current_df = st.session_state.df

    # Concatena o dataframe antigo com o novo
    updated_df = pd.concat([current_df, new_df], ignore_index=True)

    # Salva o dataframe atualizado de volta no arquivo Parquet
    try:
        updated_df.to_parquet("Indian_Kids_Screen_Time_Optimized.parquet", index=False)
        # Atualiza o dataframe no estado da sessão
        st.session_state.df = updated_df
        st.success("🎉 Dados adicionados com sucesso!")
        st.balloons()
    except Exception as e:
        st.error(f"Ocorreu um erro ao salvar os dados: {e}")