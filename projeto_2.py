import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import streamlit as st

# Definindo o estilo do gráfico
sns.set_theme(context='talk', style='ticks')

# Configurando o título da página e ícone no Streamlit
st.set_page_config(
    page_title="CRISP-Seguros SA.",
    page_icon=":bar_chart:",  # Ícone de gráfico de barras
    layout="wide",
)

    # Definindo o limite de renda

LIMITE_RENDA = 16000
Min_renda = 2000
Min_veiculo = 4000
Min_imovel = 8000
Min_vida = 6000

def Potencial(param, renda, min, pessoas=0):
    if pessoas > 0 and renda > min:
        return "green"
    elif param and renda > min:
        return "green"
    else:
        return "red"

# Carregando os dados
renda = pd.read_csv('./input/previsao_de_renda.csv')

# Função da Tela 1
def Formulario():
    st.title("Formulário")
    with st.form("form_cliente"):
        data_ref = st.date_input("Data de Referência")
        id_cliente = st.text_input("ID do Cliente")
        sexo = st.selectbox("Sexo", ["Masculino", "Feminino"])
        posse_de_veiculo = st.selectbox("Posse de Veículo", [False, True])
        posse_de_imovel = st.selectbox("Posse de Imóvel", [False, True])
        qtd_filhos = st.number_input("Quantidade de Filhos", min_value=0, step=1)
        tipo_renda = st.selectbox("Tipo de Renda", ["Empresário", "Assalariado", "Servidor público", "Pensionista", "Bolsista"])
        educacao = st.selectbox("Educação", ["Secundário", "Superior completo", "Superior incompleto", "Primário", "Pós graduação"])
        estado_civil = st.selectbox("Estado Civil", ["Solteiro", "Casado", "Viúvo", "União", "Separado"])
        tipo_residencia = st.selectbox("Tipo de Residência", ["Casa", "Governamental", "Com os pais", "Aluguel", "Estúdio", "Comunitário"])
        idade = st.number_input("Idade", min_value=0, step=1)
        tempo_emprego = st.number_input("Tempo de Emprego (em anos)", min_value=0, step=1)
        qt_pessoas_residencia = st.number_input("Quantidade de Pessoas na Residência", min_value=0, step=1)
        renda = st.number_input("Renda (em R$)", min_value=0.0, step=0.01)

        submit_button = st.form_submit_button("Enviar")

        if submit_button:
            st.session_state.data_ref = data_ref
            st.session_state.id_cliente = id_cliente
            st.session_state.sexo = sexo
            st.session_state.posse_de_veiculo = posse_de_veiculo
            st.session_state.posse_de_imovel = posse_de_imovel
            st.session_state.qtd_filhos = qtd_filhos
            st.session_state.tipo_renda = tipo_renda
            st.session_state.educacao = educacao
            st.session_state.estado_civil = estado_civil
            st.session_state.tipo_residencia = tipo_residencia
            st.session_state.idade = idade
            st.session_state.tempo_emprego = tempo_emprego
            st.session_state.qt_pessoas_residencia = qt_pessoas_residencia
            st.session_state.renda = renda

            # Alterando a tela para Tela 2 após o envio do formulário
            st.session_state.tela_atual = "Cliente"
            st.rerun()

# Função da Tela 2
def Cliente():
    st.title("Cliente - Dados Preenchidos")

    st.write("Data de Referência:", st.session_state.data_ref)
    st.write("ID do Cliente:", st.session_state.id_cliente)
    st.write("Sexo:", st.session_state.sexo)
    st.write("Posse de Veículo:", st.session_state.posse_de_veiculo)
    st.write("Posse de Imóvel:", st.session_state.posse_de_imovel)
    st.write("Quantidade de Filhos:", st.session_state.qtd_filhos)
    st.write("Tipo de Renda:", st.session_state.tipo_renda)
    st.write("Educação:", st.session_state.educacao)
    st.write("Estado Civil:", st.session_state.estado_civil)
    st.write("Tipo de Residência:", st.session_state.tipo_residencia)
    st.write("Idade:", st.session_state.idade)
    st.write("Tempo de Emprego:", st.session_state.tempo_emprego, "anos")
    st.write("Quantidade de Pessoas na Residência:", st.session_state.qt_pessoas_residencia)
    st.write("Renda: R$", st.session_state.renda)

    # Cálculo e destaque para o potencial
    potencial_cor = "Cliente com potencial" if st.session_state.renda > Min_renda else "- **Nenhum seguro recomendado no momento**"

    st.markdown(f"### **Potencial do Cliente: {potencial_cor.upper()}**")

    # Determinar quais seguros são recomendados
    seguros_recomendados = []
    if st.session_state.posse_de_veiculo and st.session_state.renda > Min_veiculo :
        seguros_recomendados.append("Seguro de Veículo")
    if st.session_state.posse_de_imovel and st.session_state.renda > Min_imovel :
        seguros_recomendados.append("Seguro Residencial")
    if st.session_state.qtd_filhos > 0 and st.session_state.renda > Min_vida:
        seguros_recomendados.append("Seguro de Vida")
    if st.session_state.estado_civil == "Casado" and st.session_state.renda > Min_vida:
        seguros_recomendados.append("Seguro de Vida")

    st.markdown("### **Seguros Recomendados:**")
    if seguros_recomendados:
        for seguro in seguros_recomendados:
            st.markdown(f"- **{seguro}**")
    else:
        st.markdown("- **Nenhum seguro recomendado no momento**")


# Função da Tela 3
def Estatistica():    
    # Configurando o tamanho padrão das fontes
    plt.rcParams.update({
        'font.size': 14,           # Tamanho geral das fontes
        'axes.titlesize': 16,      # Tamanho do título do gráfico
        'axes.labelsize': 14,      # Tamanho dos rótulos dos eixos
        'xtick.labelsize': 8,     # Tamanho dos rótulos do eixo X
        'ytick.labelsize': 8,     # Tamanho dos rótulos do eixo Y
        'legend.fontsize': 12      # Tamanho da fonte da legenda
    })

    # Criando a figura e os eixos para os gráficos
    fig, ax = plt.subplots(6, 1, figsize=(10, 30))

    # ---------- Gráfico 1: Distribuição de Renda (Histograma + KDE)
    sns.histplot(renda['renda'], kde=True, bins=100, color='skyblue', ax=ax[0], edgecolor='black')
    ax[0].set_title("Distribuição de Renda (Histograma + KDE)")
    ax[0].set_xlabel("Renda")
    ax[0].set_ylabel("Frequência / Densidade")
    ax[0].grid(axis='y', linestyle='--', alpha=0.7)
    ax[0].set_xlim(0, LIMITE_RENDA)

    # Ajustando os ticks do eixo X
    def custom_ticks(x, pos):
        if x < LIMITE_RENDA:
            return str(int(x / 1000) * 1000)  # Exibe o valor em mil (ex: 0, 5000, 10000...)
        else:
            return f'{LIMITE_RENDA}+'  # Exibe 'limite de renda +' quando atingir o limite

    ax[0].xaxis.set_major_formatter(FuncFormatter(custom_ticks))
    if 'renda' in st.session_state:
        color='green' if st.session_state.renda > Min_renda else 'red', 
        ax[0].scatter(st.session_state.renda, 100, color=color, s=250, label="Cliente", zorder=5)


    # ---------- Definindo as faixas salariais
    bins = range(0, LIMITE_RENDA + 1, Min_renda)  # Faixas de 0 a 15.000 com intervalos de 2.000
    labels = [f'{i}-{i+Min_renda}' for i in bins[:-1]]  # Labels como '0-2000', '2000-4000', etc.
    renda['faixa_salarial'] = pd.cut(renda['renda'], bins=bins, labels=labels, right=False)

    # ---------- Gráfico 2: Renda por Faixa Salarial e Posse de Veículo
    sns.countplot(x='faixa_salarial', hue='posse_de_veiculo', data=renda, ax=ax[1])
    ax[1].set_title("Distribuição de Renda por Faixa Salarial e Posse de Veículo")
    ax[1].set_xlabel("Faixa Salarial")
    ax[1].set_ylabel("Quantidade de Clientes")
    ax[1].set_xticklabels(ax[1].get_xticklabels(), rotation=45)
    ax[1].grid(axis='y', linestyle='--', alpha=0.7)
    if 'renda' in st.session_state:
        color = Potencial(st.session_state.posse_de_veiculo, st.session_state.renda, Min_veiculo)
        ax[1].scatter(min(st.session_state.renda // 2000, 7), 150, color=color, s=100, label="Cliente", zorder=5)

    # ---------- Gráfico 3: Renda por Faixa Salarial e Posse de Imóvel
    sns.countplot(x='faixa_salarial', hue='posse_de_imovel', data=renda, ax=ax[2])
    ax[2].set_title("Distribuição de Renda por Faixa Salarial e Posse de Imóvel")
    ax[2].set_xlabel("Faixa Salarial")
    ax[2].set_ylabel("Quantidade de Clientes")
    ax[2].set_xticklabels(ax[2].get_xticklabels(), rotation=45)
    ax[2].grid(axis='y', linestyle='--', alpha=0.7)
    if 'renda' in st.session_state:
        color = Potencial(st.session_state.posse_de_imovel, st.session_state.renda, Min_imovel)
        ax[2].scatter(min(st.session_state.renda // 2000, 7), 150, color=color, s=100, label="Cliente", zorder=5)

    # Gráfico 3: Comparação de Renda com a Quantidade de Filhos
    sns.countplot(x='faixa_salarial', hue='qtd_filhos', data=renda, ax=ax[3])
    ax[3].set_title("Distribuição de Renda por Faixa Salarial e Quantidade de Filhos")
    ax[3].set_xlabel("Faixa Salarial")
    ax[3].set_ylabel("Quantidade de Clientes")
    ax[3].set_xticklabels(ax[3].get_xticklabels(), rotation=45)
    ax[3].grid(axis='y', linestyle='--', alpha=0.7)
    if 'renda' in st.session_state:
        color = Potencial(st.session_state.qtd_filhos, st.session_state.renda, Min_vida, st.session_state.qtd_filhos)
        ax[3].scatter(min(st.session_state.renda // 2000, 7), 150, color=color, s=100, label="Cliente", zorder=5)

    # Gráfico 4: Comparação de Renda com Estado Civil
    sns.countplot(x='faixa_salarial', hue='estado_civil', data=renda, ax=ax[4])
    ax[4].set_title("Distribuição de Renda por Faixa Salarial e Estado Civil")
    ax[4].set_xlabel("Faixa Salarial")
    ax[4].set_ylabel("Quantidade de Clientes")
    ax[4].set_xticklabels(ax[4].get_xticklabels(), rotation=45)
    ax[4].grid(axis='y', linestyle='--', alpha=0.7)
    if 'renda' in st.session_state:
        color = "green" if st.session_state.estado_civil == "Casado" and st.session_state.renda > Min_vida else "red"
        ax[3].scatter(min(st.session_state.renda // 2000, 7), 150, color=color, s=100, label="Cliente", zorder=5)

    # Filtrando os dados para clientes casados ou com mais de 0 filhos
    dados_filtrados = renda.query("estado_civil == 'casado' or qtd_filhos > 0")
    dados_filtrados['qt_pessoas_residencia_agrupado'] = dados_filtrados['qt_pessoas_residencia'].apply(
        lambda x: '0' if x == 0 else 
                    '5 ou mais' if x >= 5 else 
                    str(x)
    )

    sns.countplot(
        x='faixa_salarial', 
        hue='qt_pessoas_residencia_agrupado', 
        data=dados_filtrados, 
        ax=ax[5], 
        palette=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd'],
    )
    ax[5].set_title("Distribuição de Renda (Apenas Casados ou com Filhos)")
    ax[5].set_xlabel("Faixa Salarial")
    ax[5].set_ylabel("Quantidade de Clientes")
    ax[5].set_xticklabels(ax[5].get_xticklabels(), rotation=45)
    ax[5].grid(axis='y', linestyle='--', alpha=0.7)
    ax[5].legend(title="Pessoas na Residência")


    st.title("Estatisticas dos clientes")

    st.write('# Análise exploratória da previsão de renda')

    # # Ajustando o espaçamento entre os gráficos
    plt.subplots_adjust(hspace=1)

    # # Removendo bordas extras
    sns.despine()

    # Exibindo os gráficos no Streamlit
    st.pyplot(fig)



# Criando a barra lateral
st.sidebar.title("Navegação")
escolha = st.sidebar.radio(
    "Escolha uma tela:",
    ("Formulario", "Cliente", "Estatistica")
)

# Exibindo o conteúdo com base na escolha do usuário
if escolha == "Formulario":
    Formulario()
elif escolha == "Cliente":
    Cliente()
elif escolha == "Estatistica":
    Estatistica()
