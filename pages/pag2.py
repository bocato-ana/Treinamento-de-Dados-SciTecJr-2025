import streamlit as st
import pandas as pd

st.title("Formulário para Adicionar Novos Dados 📝")

# Verifica se o dataframe está no session_state
if 'df' not in st.session_state or st.session_state.df.empty:
    st.warning("Base de dados não carregada. Volte para a página principal.")
    st.stop()

with st.form(key="add_data_form"):
    st.subheader("Informações do Participante")

    col1, col2 = st.columns(2)

    with col1:
        age = st.number_input("Idade", min_value=10, max_value=80, step=1)
        gender = st.selectbox("Gênero", options=["Male", "Female"])
        marital_status = st.selectbox("Estado Civil", options=["No", "Yes"])

    with col2:
        sought_specialist = st.selectbox("Procurou Especialista para Tratamento?", options=["No", "Yes"])
    
    st.subheader("Doenças Mentais (Marque se aplicável)")
    col_dep, col_anx, col_panic = st.columns(3)
    with col_dep:
        depression = st.checkbox("Depressão")
    with col_anx:
        anxiety = st.checkbox("Ansiedade")
    with col_panic:
        panic_attack = st.checkbox("Pânico")

    submit_button = st.form_submit_button(label="Enviar")

if submit_button:
    # Mapear respostas para True/False ou valores corretos
    new_data = {
        'Age': age,
        'Choose your gender': True if gender == "Male" else False,
        'Marital status': True if marital_status == "Yes" else False,
        'Do you have Depression?': int(depression),
        'Do you have Anxiety?': int(anxiety),
        'Do you have Panic attack?': int(panic_attack),
        'Did you seek any specialist for a treatment?': 1 if sought_specialist == "Yes" else 0,
    }

    new_df = pd.DataFrame([new_data])

    # Converte para os tipos corretos
    new_df['Choose your gender'] = new_df['Choose your gender'].astype(bool)
    new_df['Marital status'] = new_df['Marital status'].astype(bool)
    
    for col in ['Do you have Depression?', 'Do you have Anxiety?', 'Do you have Panic attack?', 'Did you seek any specialist for a treatment?']:
        new_df[col] = new_df[col].astype('Int8')

    current_df = st.session_state.df

    updated_df = pd.concat([current_df, new_df], ignore_index=True)

    try:
        updated_df.to_parquet("Student Mental health.parquet", index=False)
        st.session_state.df = updated_df
        st.success("🎉 Dados adicionados com sucesso!")
        st.balloons()
    except Exception as e:
        st.error(f"Ocorreu um erro ao salvar os dados: {e}")


