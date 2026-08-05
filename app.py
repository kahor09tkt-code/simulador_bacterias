import streamlit as st
import pandas as pd


st.set_page_config(
    page_title="Simulador de Bacterias",
    page_icon="🦠",
    layout="wide"
)


def crescimento_exponencial(populacao, taxa):
    crescimento = taxa * populacao
    nova_populacao = populacao + crescimento

    if nova_populacao < 0:
        nova_populacao = 0

    return nova_populacao


def crescimento_logistico(populacao, taxa, capacidade):
    crescimento = taxa * populacao * (1 - populacao / capacidade)
    nova_populacao = populacao + crescimento

    if nova_populacao < 0:
        nova_populacao = 0

    if nova_populacao > capacidade:
        nova_populacao = capacidade

    return nova_populacao


def aplicar_antibiotico(populacao, reducao):
    fator_sobrevivencia = 1 - reducao / 100
    nova_populacao = populacao * fator_sobrevivencia

    if nova_populacao < 0:
        nova_populacao = 0

    return nova_populacao


def calcular_taxa_escassez(taxa, reducao):
    fator = 1 - reducao / 100
    nova_taxa = taxa * fator

    if nova_taxa < 0:
        nova_taxa = 0

    return nova_taxa


st.title("Simulador de Crescimento de Colonias de Bacterias")

st.write(
    "Este programa simula o crescimento de uma colonia bacteriana "
    "ao longo do tempo usando diferentes modelos matematicos."
)


st.sidebar.header("Configuracoes da simulacao")


modelo = st.sidebar.selectbox(
    "Modelo de crescimento",
    ["Exponencial", "Logistico"]
)


populacao_inicial = st.sidebar.number_input(
    "Populacao inicial",
    min_value=1.0,
    value=100.0,
    step=10.0
)


taxa_crescimento = st.sidebar.number_input(
    "Taxa de crescimento",
    min_value=0.0,
    max_value=1.0,
    value=0.3,
    step=0.05
)


numero_passos = st.sidebar.number_input(
    "Numero de passos",
    min_value=1,
    max_value=10000,
    value=48,
    step=1
)


capacidade = None


if modelo == "Logistico":

    capacidade = st.sidebar.number_input(
        "Capacidade de suporte",
        min_value=float(populacao_inicial),
        value=max(10000.0, float(populacao_inicial)),
        step=100.0
    )


st.sidebar.header("Antibiotico")


usar_antibiotico = st.sidebar.checkbox(
    "Aplicar antibiotico"
)


tempo_antibiotico = 20
reducao_antibiotico = 90


if usar_antibiotico:

    tempo_antibiotico = st.sidebar.number_input(
        "Passo do antibiotico",
        min_value=1,
        max_value=int(numero_passos),
        value=min(20, int(numero_passos))
    )


    reducao_antibiotico = st.sidebar.slider(
        "Reducao da populacao (%)",
        min_value=0,
        max_value=100,
        value=90
    )


st.sidebar.header("Escassez de nutrientes")


usar_escassez = st.sidebar.checkbox(
    "Aplicar escassez de nutrientes"
)


inicio_escassez = 10
duracao_escassez = 5
reducao_escassez = 50


if usar_escassez:

    inicio_escassez = st.sidebar.number_input(
        "Inicio da escassez",
        min_value=1,
        max_value=int(numero_passos),
        value=min(10, int(numero_passos))
    )


    duracao_escassez = st.sidebar.number_input(
        "Duracao da escassez",
        min_value=1,
        max_value=int(numero_passos),
        value=min(5, int(numero_passos))
    )


    reducao_escassez = st.sidebar.slider(
        "Reducao da taxa de crescimento (%)",
        min_value=0,
        max_value=100,
        value=50
    )


rodar = st.sidebar.button(
    "Rodar simulacao",
    type="primary",
    use_container_width=True
)


if rodar:

    populacao = float(populacao_inicial)

    tempos = [0]
    populacoes = [populacao]
    eventos = []


    for tempo in range(1, int(numero_passos) + 1):

        taxa_atual = taxa_crescimento


        if usar_escassez:

            fim_escassez = inicio_escassez + duracao_escassez


            if inicio_escassez <= tempo < fim_escassez:

                taxa_atual = calcular_taxa_escassez(
                    taxa_crescimento,
                    reducao_escassez
                )


            if tempo == inicio_escassez:

                eventos.append(
                    f"Passo {tempo}: inicio da escassez de nutrientes. "
                    f"A taxa de crescimento foi reduzida em "
                    f"{reducao_escassez}%."
                )


            if tempo == fim_escassez:

                eventos.append(
                    f"Passo {tempo}: fim da escassez de nutrientes. "
                    f"A taxa de crescimento voltou ao valor original."
                )


        if usar_antibiotico and tempo == tempo_antibiotico:

            populacao_antes = populacao

            populacao = aplicar_antibiotico(
                populacao,
                reducao_antibiotico
            )


            eventos.append(
                f"Passo {tempo}: antibiotico aplicado. "
                f"A populacao passou de "
                f"{populacao_antes:.2f} para "
                f"{populacao:.2f}."
            )


        if modelo == "Exponencial":

            populacao = crescimento_exponencial(
                populacao,
                taxa_atual
            )


        else:

            populacao = crescimento_logistico(
                populacao,
                taxa_atual,
                capacidade
            )


        populacao = max(0, populacao)

        tempos.append(tempo)
        populacoes.append(populacao)


    dados = pd.DataFrame(
        {
            "Tempo": tempos,
            "Populacao": populacoes
        }
    )


    st.subheader("Resultados")


    coluna1, coluna2, coluna3 = st.columns(3)


    coluna1.metric(
        "Populacao inicial",
        f"{populacao_inicial:.0f}"
    )


    coluna2.metric(
        "Populacao final",
        f"{populacao:.0f}"
    )


    coluna3.metric(
        "Modelo",
        modelo
    )


    st.subheader("Crescimento da populacao")


    st.line_chart(
        dados,
        x="Tempo",
        y="Populacao"
    )


    st.subheader("Dados da simulacao")


    st.dataframe(
        dados,
        use_container_width=True,
        hide_index=True
    )


    st.subheader("Log de eventos")


    if eventos:

        for evento in eventos:

            st.write(evento)

    else:

        st.info(
            "Nenhum evento foi aplicado nesta simulacao."
        )


else:

    st.info(
        "Configure os parametros na barra lateral "
        "e clique em Rodar simulacao."
    )