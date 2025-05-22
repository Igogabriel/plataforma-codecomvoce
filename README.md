# 🧠 Plataforma Educacional - CodeComVocê (Modo Console)

Esta é uma **plataforma de ensino interativa** desenvolvida em **Python via console**, com foco em **educação digital, lógica de programação e segurança online**.

Ela permite ao usuário acessar conteúdos em PDF, responder quizzes de múltipla escolha e visualizar seu desempenho com estatísticas como média, moda e mediana.

---

## 🎯 Objetivos

- Promover a **inclusão digital** e a **alfabetização tecnológica**.
- Ensinar programação de forma didática e acessível via terminal.
- Armazenar e analisar o desempenho do aluno de forma automatizada.

---

## ⚙️ Funcionalidades

### 📘 Acesso a Conteúdo
- A leitura do conteúdo ocorre por meio de arquivos PDF.
- Os tópicos incluem:
  - Pensamento Computacional
  - Programação em Python
  - Segurança Digital

### ❓ Quiz Interativo no Console
- Quizzes de 10 perguntas com alternativas.
- Interface 100% em modo texto, sem janelas gráficas.
- O sistema corrige automaticamente as respostas e armazena os resultados.

### 📊 Relatórios de Desempenho
- Exibe ao final de cada quiz:
  - Média
  - Moda
  - Mediana
- Os dados são armazenados em `performance.json`.

### 💾 Armazenamento de Dados
- Usa arquivos JSON para guardar:
  - Perguntas e respostas dos quizzes
  - Resultados dos usuários
  - Controle simples de usuários

---

## 🛠️ Tecnologias Utilizadas

- **Python 3 (modo console)**
- **JSON** para persistência dos dados
- **PyPDF2** para leitura de PDFs
- **Biblioteca `statistics`** para cálculos estatísticos

---

## 🚀 Como Executar o Projeto

### 1. Clone o repositório:

```bash
git clone https://github.com/Igogabriel/plataforma-codecomvoce
cd plataformaeducacional
