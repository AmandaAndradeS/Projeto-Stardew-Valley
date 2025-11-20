# 🌾 Farm Planning Assistant

**Uma ferramenta inteligente, imersiva e estratégica para otimizar seus cultivos em Stardew Valley**

O **Farm Planning Assistant** é uma aplicação criada para ajudar jogadores de **Stardew Valley** a planejarem seus cultivos com eficiência, estratégia e visual atrativo.  
Ele combina **Ciência de Dados**, **análise de informações**, **lógica de otimização**, **design de interface** e **recursos multimídia** para gerar um plano completo de plantio — com culturas viáveis, ciclos possíveis, lucros projetados e eventos sazonais que podem afetar a fazenda.

Este projeto foi desenvolvido com foco em **aprendizado**, **experimentação prática** e **aperfeiçoamento contínuo**, utilizando várias bibliotecas do ecossistema Python, como `tkinter`, `pandas`, `reportlab`, `pygame` e `Pillow`.

<p align="center"> <img src="https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge" /> <img src="https://img.shields.io/badge/Tkinter-GUI-green?style=for-the-badge" /> <img src="https://img.shields.io/badge/Pandas-Data%20Analysis-orange?style=for-the-badge" /> <img src="https://img.shields.io/badge/ReportLab-PDF%20Generator-red?style=for-the-badge" /> <img src="https://img.shields.io/badge/Pillow-Image%20Processing-yellow?style=for-the-badge" /> <img src="https://img.shields.io/badge/Pygame-Audio%2FSound-purple?style=for-the-badge" /> <img src="https://img.shields.io/badge/Status-Em%20Desenvolvimento-9cf?style=for-the-badge" /> </p>

---

# ✨ Recursos Principais

## 🌱 Planejamento Inteligente de Cultivo

- **Cálculo de viabilidade:** identifica se uma cultura pode crescer e ser colhida no intervalo escolhido
    
- **Otimização de lucro:** calcula ciclos, custo total, lucro bruto e lucro líquido
    
- **Escolha da área plantável:**
    
    - Por **quadrados individuais**, ou
        
    - Pelo número de **Aspersores Nível II** (8 espaços por aspersor)
        

---

## 📅 Seleção Interativa de Datas e Eventos

Planeje suas plantações sem surpresas! 🎉

- Calendário customizado baseado nas quatro estações do jogo
    
- Análise automática de:
    
    - **Eventos sazonais**
        
    - **Festivais**
        
    - **Impacto no funcionamento das lojas e do gameplay**
        

_Assim você evita aquela frustração de uma loja fechada na hora da colheita._ 😉

---

## 📊 Geração Completa do Plano de Colheita

Tudo que você precisa para organizar sua fazenda de forma eficiente:

- Culturas recomendadas
    
- Número de colheitas possíveis
    
- Tempo de cultivo vs. intervalo selecionado
    
- Lucro estimado baseado nos preços oficiais da Wiki do jogo
    

_Planejar nunca foi tão fácil!_ 💡

---

## 🖼️ Experiência de Usuário Aprimorada

- Interface temática inspirada em Stardew Valley
    
- Botões arredondados e gradientes personalizados (via Pillow)
    
- Animações de hover (`animate_hover_color`)
    
- Sons integrados (hover, clique e música ambiente via pygame)
    
- Pop-ups elegantes, incluindo o calendário interativo
    

_Tudo pensado para que você se sinta dentro do jogo!_ 🎨

---

## 📄 Exportação em PDF

- Geração automática de relatório em PDF
    
- Visual limpo e organizado com todas as recomendações do período escolhido
    

_Perfeito para imprimir ou guardar suas estratégias!_ 📝

---

# ⚙️ Tecnologias e Dependências

|Categoria|Tecnologia|Uso|
|---|---|---|
|Interface|**tkinter / ttk**|Janela principal, pop-ups, calendário|
|Dados|**pandas, numpy**|Limpeza, transformação e cálculos|
|Imagens|**Pillow (PIL)**|Gradientes, ícones, arredondamento|
|Áudio|**pygame**|Música e efeitos|
|Relatórios|**ReportLab**|Exportação em PDF|
|Texto|**unidecode**|Normalização de strings|

---

# 🧠 Destaques Técnicos e Funcionalidades Avançadas

- Determinação automática da viabilidade de cada cultura
    
- Cálculo completo de ciclos possíveis e lucros
    
- Interpretação e tratamento do intervalo de datas
    
- Suporte à escolha dinâmica da área de plantio
    
- Funções avançadas para gradientes, arredondamento de cantos e animações
    
- Carregamento inteligente de recursos (imagens, sons, cursores)
    

_Um verdadeiro assistente de fazenda ao seu alcance!_ 🌟

---

# 🏗️ Arquitetura do Projeto

|Arquivo|Descrição|
|---|---|
|**`main_app.py`**|Interface gráfica e inicialização|
|**`logica.py`**|Núcleo da lógica de otimização e cálculos|
|**`tratamento_dados.py`**|Processamento de entrada e chamadas da lógica|
|**`tratamento_menssagem.py`**|Formatação narrativa do plano final|
|**`calendario.py`**|Widget customizado de calendário|
|**`config.py`**|Configurações gerais do projeto|
|**`utils.py`**|Funções auxiliares (UI, animações, imagens)|

---
---

# 📂 Estrutura de Diretórios

```bash
Farm Planning Assistant/
├── assets/
│   ├── images/              # Ícones, fundos, sprites
│   ├── sounds/              # Música e efeitos sonoros
│   └── cursors/             # Cursores personalizados
│
├── data/
│   ├── Cultivos.csv         # Dados dos cultivos
│   └── Estações.csv         # Eventos e festivais
│
├── build/                   # Arquivos gerados durante a build
├── dist/                    # Executáveis finais
│
├── src/
│   ├── __init__.py
│   ├── calendario.py        # Lógica do calendário e cálculo de dias
│   ├── config.py            # Configurações gerais do app
│   ├── logica.py            # Regras centrais de funcionamento
│   ├── main_app.py          # Arquivo principal da interface
│   ├── tratamento_dados.py  # Limpeza e processamento dos dados CSV
│   ├── tratamento_menssagem.py # Padronização de textos e mensagens
│   └── utils.py             # Funções auxiliares
│
├── .gitignore
├── farm planning assistant.spec
├── main_app.spec
└── README.md
```
---

# 🌟 Nota Importante

_Olá, fazendeiro! 🌾 Antes de continuar, algumas informações importantes sobre este projeto:_

- O **Farm Planning Assistant** é um projeto **não oficial**, criado exclusivamente para fins educativos e de aprendizado.
    
- Ele utiliza **imagens, personagens, músicas, cursores e outros elementos visuais de Stardew Valley**, todos de propriedade do criador do jogo, **ConcernedApe**.
    
- Este projeto **não possui vínculo** com o criador do jogo ou distribuidores oficiais, e **não tem fins lucrativos**.
    
- Todos os recursos do jogo são utilizados apenas como referência para estudo e desenvolvimento da aplicação.
    
- Os créditos aos elementos originais e ao criador são devidamente mencionados e respeitados.
    

_✨ Em resumo: estamos aqui para aprender, experimentar e nos divertir, respeitando integralmente os direitos autorais de Stardew Valley! 🎮_

---

# 🙌 Sobre o Desenvolvimento

_✨ Este projeto não é perfeito — e está tudo bem!_  
Estamos aprendendo, testando, pesquisando, errando e ajustando passo a passo.

Mesmo sem sermos especialistas, colocamos **dedicação e cuidado** em cada detalhe.

### Objetivos principais:

- Desafiar nossas habilidades
    
- Criar algo funcional e bonito
    
- Evoluir tecnicamente
    
- E nos divertir no processo
    

---

# 👩‍💻 Criadores

[https://github.com/AmandaAndradeS](https://github.com/AmandaAndradeS)  
[https://github.com/IguinN01](https://github.com/IguinN01)
    
---


🌾 Obrigada por conferir o **Farm Planning Assistant**! Esperamos que ele torne suas plantações mais estratégicas, seu dia mais divertido e sua experiência com Stardew Valley ainda mais imersiva. Boa colheita! 🍓🎮✨