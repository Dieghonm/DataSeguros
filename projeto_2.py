import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import streamlit as st

import random 
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score

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

# Carregando e limpa os dados, procedimentos copiados do arquivo projeto-2.jpynb
rendaDF = pd.read_csv('./input/previsao_de_renda.csv')
rendaDF = rendaDF.drop(columns=['data_ref', 'Unnamed: 0'])
rendaDF = rendaDF.drop_duplicates()

ids_duplicados = rendaDF[rendaDF.duplicated(subset='id_cliente', keep=False)]['id_cliente']
registros_a_remover = rendaDF[(rendaDF['id_cliente'].isin(ids_duplicados)) & (rendaDF['educacao'] == 'Secundário')]
rendaDF = rendaDF.drop(index=registros_a_remover.index)
rendaDF['tempo_emprego'] = rendaDF['tempo_emprego'].fillna(0)

rendaDF['sexo'] = rendaDF['sexo'].map({'M': True, 'F': False})
rendaDF.rename(columns={'sexo': 'masculino'}, inplace=True)


# Função da Tela 1
def Formulario():
    st.title("Formulário")
    
    if 'erro' not in st.session_state:
        st.session_state.erro = ""

    with st.form("form_cliente"):
        data_ref = st.date_input("Data de Referência")
        id_cliente = int(st.text_input("ID do Cliente", value=str(random.randint(1000, 9999))))
        sexo = st.selectbox("Sexo", ["Unknown", "Masculino", "Feminino"])
        posse_de_veiculo = st.selectbox("Posse de Veículo", ["Unknown", False, True])
        posse_de_imovel = st.selectbox("Posse de Imóvel", ["Unknown", False, True])
        qtd_filhos = st.number_input("Quantidade de Filhos", min_value=0, step=1)
        tipo_renda = st.selectbox("Tipo de Renda", ["Unknown", "Empresário", "Assalariado", "Servidor público", "Pensionista", "Bolsista"])
        educacao = st.selectbox("Educação", ["Unknown", "Secundário", "Superior completo", "Superior incompleto", "Primário", "Pós graduação"])
        estado_civil = st.selectbox("Estado Civil", ["Unknown", "Solteiro", "Casado", "Viúvo", "União", "Separado"])
        tipo_residencia = st.selectbox("Tipo de Residência", ["Unknown", "Casa", "Governamental", "Com os pais", "Aluguel", "Estúdio", "Comunitário"])
        idade = st.number_input("Idade", min_value=0, step=1)
        tempo_emprego = float(st.number_input("Tempo de Emprego (em anos)", min_value=0, step=1))
        qt_pessoas_residencia = float(st.number_input("Quantidade de Pessoas na Residência", min_value=0, step=1))
        renda = st.number_input("Renda (em R$)", min_value=0.0, step=0.01)
        
        submit_button = st.form_submit_button("Enviar")
        
        if submit_button:
            campos_nao_preenchidos = []

            if sexo == "Unknown":
                campos_nao_preenchidos.append("sexo")
            if posse_de_veiculo == "Unknown":
                campos_nao_preenchidos.append("posse_de_veiculo")
            if posse_de_imovel == "Unknown":
                campos_nao_preenchidos.append("posse_de_imovel")
            if tipo_renda == "Unknown":
                campos_nao_preenchidos.append("tipo_renda")
            if educacao == "Unknown":
                campos_nao_preenchidos.append("educacao")
            if estado_civil == "Unknown":
                campos_nao_preenchidos.append("estado_civil")
            if tipo_residencia == "Unknown":
                campos_nao_preenchidos.append("tipo_residencia")
            if idade == 0:
                campos_nao_preenchidos.append("idade")
            if tempo_emprego == 0:
                campos_nao_preenchidos.append("tempo_emprego")
            if qt_pessoas_residencia == 0:
                campos_nao_preenchidos.append("qt_pessoas_residencia")
            if renda == 0:
                campos_nao_preenchidos.append("renda")

            if len(campos_nao_preenchidos) > 1:
                st.session_state.erro = (
                    f"Por favor, preencha todos os campos corretamente. Campos inválidos: "
                    f"{', '.join(campos_nao_preenchidos)}"
                )

            elif campos_nao_preenchidos[0] in ["renda", "qt_pessoas_residencia", "posse_de_imovel", "posse_de_veiculo"]:
                campo_faltante = campos_nao_preenchidos[0]

                dados_formulario = {
                    "id_cliente": id_cliente,
                    "masculino": sexo == 'Masculino',
                    "posse_de_veiculo":  None if posse_de_veiculo == "Unknown" else posse_de_veiculo,
                    "posse_de_imovel": None if posse_de_imovel == "Unknown" else posse_de_imovel,
                    "qtd_filhos": qtd_filhos,
                    "tipo_renda": tipo_renda,
                    "educacao": educacao,
                    "estado_civil": estado_civil,
                    "tipo_residencia": tipo_residencia,
                    "idade": idade,
                    "tempo_emprego": tempo_emprego,
                    "qt_pessoas_residencia": qt_pessoas_residencia,
                    "renda": renda,
                }

                novo_cliente_df = pd.DataFrame([dados_formulario])
                novoDF = pd.concat([rendaDF, novo_cliente_df], ignore_index=True)

                DFdummies = pd.get_dummies(novoDF, columns=['tipo_renda', 'educacao', 'estado_civil', 'tipo_residencia'])
                novo_cliente_dummies = DFdummies.iloc[-len(novo_cliente_df):]
                DFdummies_restante = DFdummies.iloc[:-len(novo_cliente_df)]

                y = DFdummies_restante[campo_faltante]
                X = DFdummies_restante.drop(columns=[campo_faltante])
                X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
                
                model = RandomForestRegressor(n_estimators=100, random_state=42)
                model.fit(X_train, y_train)

                previsao_teste = model.predict(X_test)

                # Avaliação do desempenho
                r2 = r2_score(y_test, previsao_teste)
                st.write(f"A precisão do modelo (R²) nos dados de teste é: {r2 * 100:.2f}%")
                
                # # Previsão para o campo faltante
                novo_cliente_dummies_ = novo_cliente_dummies.drop(columns=[campo_faltante])
                campo_faltante_pred = model.predict(novo_cliente_dummies_)

                if campo_faltante in ["posse_de_imovel", "posse_de_veiculo"]:
                    campo_faltante_pred_percent = campo_faltante_pred
                    campo_faltante_pred = campo_faltante_pred > 0.5

                    st.write(f"A previsão para o campo {campo_faltante} é: {campo_faltante_pred_percent*100}%, provavelmente {campo_faltante_pred}")
                else:
                    st.write(f"A previsão para o campo {campo_faltante} é: {campo_faltante_pred}")     
                st.session_state[campo_faltante] = campo_faltante_pred

            if len(campos_nao_preenchidos) < 2:
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
                st.session_state.tela_atual = "Cliente"
                st.session_state.erro = ""
                st.markdown("")

    if st.session_state.erro:
        st.markdown(f"<p style='color:red;'>{st.session_state.erro}</p>", unsafe_allow_html=True)


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
    sns.histplot(rendaDF['renda'], kde=True, bins=100, color='skyblue', ax=ax[0], edgecolor='black')
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
    rendaDF['faixa_salarial'] = pd.cut(rendaDF['renda'], bins=bins, labels=labels, right=False)

    # ---------- Gráfico 2: Renda por Faixa Salarial e Posse de Veículo
    sns.countplot(x='faixa_salarial', hue='posse_de_veiculo', data=rendaDF, ax=ax[1])
    ax[1].set_title("Distribuição de Renda por Faixa Salarial e Posse de Veículo")
    ax[1].set_xlabel("Faixa Salarial")
    ax[1].set_ylabel("Quantidade de Clientes")
    ax[1].set_xticklabels(ax[1].get_xticklabels(), rotation=45)
    ax[1].grid(axis='y', linestyle='--', alpha=0.7)
    if 'renda' in st.session_state:
        color = Potencial(st.session_state.posse_de_veiculo, st.session_state.renda, Min_veiculo)
        ax[1].scatter(min(st.session_state.renda // 2000, 7), 150, color=color, s=100, label="Cliente", zorder=5)

    # ---------- Gráfico 3: Renda por Faixa Salarial e Posse de Imóvel
    sns.countplot(x='faixa_salarial', hue='posse_de_imovel', data=rendaDF, ax=ax[2])
    ax[2].set_title("Distribuição de Renda por Faixa Salarial e Posse de Imóvel")
    ax[2].set_xlabel("Faixa Salarial")
    ax[2].set_ylabel("Quantidade de Clientes")
    ax[2].set_xticklabels(ax[2].get_xticklabels(), rotation=45)
    ax[2].grid(axis='y', linestyle='--', alpha=0.7)
    if 'renda' in st.session_state:
        color = Potencial(st.session_state.posse_de_imovel, st.session_state.renda, Min_imovel)
        ax[2].scatter(min(st.session_state.renda // 2000, 7), 150, color=color, s=100, label="Cliente", zorder=5)

    # Gráfico 3: Comparação de Renda com a Quantidade de Filhos
    sns.countplot(x='faixa_salarial', hue='qtd_filhos', data=rendaDF, ax=ax[3])
    ax[3].set_title("Distribuição de Renda por Faixa Salarial e Quantidade de Filhos")
    ax[3].set_xlabel("Faixa Salarial")
    ax[3].set_ylabel("Quantidade de Clientes")
    ax[3].set_xticklabels(ax[3].get_xticklabels(), rotation=45)
    ax[3].grid(axis='y', linestyle='--', alpha=0.7)
    if 'renda' in st.session_state:
        color = Potencial(st.session_state.qtd_filhos, st.session_state.renda, Min_vida, st.session_state.qtd_filhos)
        ax[3].scatter(min(st.session_state.renda // 2000, 7), 150, color=color, s=100, label="Cliente", zorder=5)

    # Gráfico 4: Comparação de Renda com Estado Civil
    sns.countplot(x='faixa_salarial', hue='estado_civil', data=rendaDF, ax=ax[4])
    ax[4].set_title("Distribuição de Renda por Faixa Salarial e Estado Civil")
    ax[4].set_xlabel("Faixa Salarial")
    ax[4].set_ylabel("Quantidade de Clientes")
    ax[4].set_xticklabels(ax[4].get_xticklabels(), rotation=45)
    ax[4].grid(axis='y', linestyle='--', alpha=0.7)
    if 'renda' in st.session_state:
        color = "green" if st.session_state.estado_civil == "Casado" and st.session_state.renda > Min_vida else "red"
        ax[3].scatter(min(st.session_state.renda // 2000, 7), 150, color=color, s=100, label="Cliente", zorder=5)

    # Filtrando os dados para clientes casados ou com mais de 0 filhos
    dados_filtrados = rendaDF.query("estado_civil == 'casado' or qtd_filhos > 0")
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
