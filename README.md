# 🎁 Teste de Dons Espirituais

Um questionário interativo para descobrir seus dons espirituais através de 45 perguntas.

## 🌟 Características

- ✅ 45 perguntas sobre 9 dons espirituais
- ✅ Salvamento automático de progresso
- ✅ Possibilidade de voltar e corrigir respostas
- ✅ Interface web com Streamlit
- ✅ Suporte para múltiplos usuários
- ✅ Retomar questionário de onde parou

## 📦 Dons Espirituais Avaliados

- **A - Profecia**: Comunicar verdades de Deus
- **B - Serviço**: Ajudar nas necessidades práticas
- **C - Ensino**: Explicar conceitos bíblicos
- **D - Exortação**: Encorajar e aconselhar
- **E - Contribuição**: Doar recursos generosamente
- **F - Liderança**: Organizar e supervisionar
- **G - Misericórdia**: Cuidar dos que sofrem
- **H - Evangelista**: Compartilhar o evangelho
- **I - Pastor**: Acompanhar e cuidar de cristãos

## 🚀 Como Usar

### Versão Terminal (CLI)

```bash
python3 test.py
```

### Versão Web (Streamlit)

```bash
streamlit run streamlit_app.py
```

## 📋 Instalação

1. Clone o repositório ou baixe os arquivos

2. Instale as dependências:

```bash
pip install -r requirements.txt
```

3. Execute o aplicativo:

```bash
# Terminal
python3 test.py

# Web
streamlit run streamlit_app.py
```

## 🌐 Deploy Online

### Opção 1: Streamlit Cloud (Gratuito)

1. Faça push do código para GitHub
2. Acesse [share.streamlit.io](https://share.streamlit.io)
3. Conecte seu repositório GitHub
4. Deploy automático!

### Opção 2: Heroku

```bash
# Adicione Procfile
echo "web: streamlit run streamlit_app.py --server.port=$PORT" > Procfile

# Deploy
heroku create seu-app-name
git push heroku main
```

### Opção 3: Railway

1. Acesse [railway.app](https://railway.app)
2. Conecte seu repositório
3. Deploy automático!

## 📁 Estrutura de Arquivos

```
spiritual-gifts-quiz/
├── test.py              # Versão CLI do questionário
├── streamlit_app.py     # Versão web com Streamlit
├── requirements.txt     # Dependências Python
├── quiz_progress.json   # Dados salvos dos usuários
└── README.md           # Este arquivo
```

## 💾 Dados Salvos

O progresso é salvo automaticamente em `quiz_progress.json`. Cada usuário pode:

- Pausar e continuar depois
- Voltar e corrigir respostas
- Ver seus resultados finais

## 🔒 Privacidade

Os dados são salvos localmente no arquivo JSON. Para uso em produção, considere:

- Usar banco de dados (PostgreSQL, MongoDB)
- Adicionar autenticação
- Implementar backups regulares

## 📝 Licença

Livre para uso educacional e religioso.

## 🤝 Contribuindo

Sugestões e melhorias são bem-vindas!

---

Desenvolvido com ❤️ para ajudar pessoas a descobrir seus dons espirituais.
