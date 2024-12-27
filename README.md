# **Análise de Cliente em Potencial**

Este projeto tem como objetivo identificar clientes em potencial para diferentes tipos de seguros com base em critérios como renda, posse de bens (imóveis e veículos), e perfil demográfico. A aplicação utiliza Python e Streamlit para criar uma interface interativa que permite a visualização dos dados e a análise de seguros recomendados.

---

## **Descrição do Projeto**

A análise é baseada em dados de clientes, e o sistema classifica clientes de acordo com seu potencial para adquirir seguros como:
- **Seguro de Veículo**  
- **Seguro Residencial**  
- **Seguro de Vida**

### **Funcionalidades Principais**
1. **Formulário de entrada de dados**: Permite ao usuário inserir informações do cliente.
2. **Classificação do cliente**: Destaca o potencial do cliente para diferentes seguros com base na renda e nos critérios de posse.
3. **Visualização estatística**: Gráficos que mostram a distribuição dos clientes por faixa salarial, posse de bens e outros aspectos demográficos.

---

## **Tecnologias Utilizadas**
- **Python**: Linguagem principal para processamento de dados e lógica do sistema.
- **Streamlit**: Para criar a interface interativa do usuário.
- **Seaborn** e **Matplotlib**: Para a geração de gráficos e visualizações estatísticas.
- **Pandas**: Para manipulação e análise de dados.

---

## **Pré-requisitos**
Certifique-se de que os seguintes itens estão instalados no seu ambiente:
- Python 3.8 ou superior
- As bibliotecas listadas no arquivo `requirements.txt`.

### **Instalação**
1. Clone o repositório:
   ```bash
   git clone https://github.com/seu_usuario/analise-cliente-potencial.git
   cd analise-cliente-potencial
   ```
2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

---

## **Como Executar**
1. Certifique-se de que os dados estão no diretório `./input` (exemplo: `previsao_de_renda.csv`).
2. Execute o arquivo principal do Streamlit:
   ```bash
   streamlit run main.py
   ```
3. Acesse a aplicação no navegador pelo endereço fornecido no terminal (geralmente `http://localhost:8501`).

---

## **Estrutura do Projeto**
- **`main.py`**: Arquivo principal da aplicação Streamlit.
- **`input/`**: Diretório para arquivos de entrada (dados CSV).
- **`output/`**: Diretório para salvar resultados e gráficos gerados.
- **`requirements.txt`**: Lista de dependências do projeto.

---

## **Detalhes Técnicos**
### **Parâmetros e Critérios de Classificação**
Os clientes são avaliados com base nos seguintes critérios:
- **Renda mínima para seguros**:
  - Seguro de Veículo: R$ 4.000
  - Seguro Residencial: R$ 8.000
  - Seguro de Vida: R$ 6.000
- Clientes casados ou com filhos têm maior potencial para seguro de vida.

### **Visualizações Incluídas**
1. **Distribuição de renda (Histograma + KDE)**: Identifica padrões de renda entre os clientes.
2. **Faixas salariais por posse de bens**: Mostra a relação entre renda, posse de veículos e imóveis.
3. **Análise por quantidade de filhos**: Avalia a relação entre renda e dependentes.

---

## **Contribuindo**
Contribuições são bem-vindas! Siga os passos abaixo:
1. Faça um fork do repositório.
2. Crie um branch para sua feature:
   ```bash
   git checkout -b minha-feature
   ```
3. Submeta um pull request para revisão.

---

## **Licença**
Este projeto está licenciado sob a [MIT License](LICENSE).
