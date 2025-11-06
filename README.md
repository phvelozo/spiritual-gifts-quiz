# 🎁 Teste de Dons Espirituais

Um questionário interativo para descobrir seus dons espirituais através de 45 perguntas.

## 🌟 Características

- ✅ 45 perguntas sobre 9 dons espirituais
- ✅ Salvamento automático de progresso
- ✅ Possibilidade de voltar e corrigir respostas
- ✅ Interface web com Streamlit
- ✅ Suporte para múltiplos usuários
- ✅ Retomar questionário de onde parou
- ✅ **Integração com Firebase** para persistência em nuvem (opcional)

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

4. **(Opcional)** Configure Firebase para persistência em nuvem:
   - Veja o guia completo em [`FIREBASE_SETUP.md`](FIREBASE_SETUP.md)
   - Sem Firebase, o app usará arquivos JSON locais

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
├── test.py                        # Versão CLI do questionário
├── streamlit_app.py               # Versão web com Streamlit
├── migrate_firebase_keys.py      # Script de migração de chaves Firebase
├── requirements.txt               # Dependências Python
├── quiz_progress.json             # Dados salvos (fallback local)
├── README.md                      # Este arquivo
├── FIREBASE_SETUP.md              # Guia de setup do Firebase
├── .streamlit/
│   └── secrets.toml.example       # Template de configuração Firebase
└── .gitignore                     # Arquivos ignorados pelo Git
```

## 💾 Dados Salvos

O progresso é salvo automaticamente com duas opções:

### 🔥 Firebase Firestore (Recomendado para produção)

- Dados persistem na nuvem
- Funciona em Streamlit Cloud
- Gratuito até 50K leituras/dia
- [Guia de setup completo](FIREBASE_SETUP.md)

### 📄 Arquivo JSON Local (Fallback automático)

- Usado quando Firebase não está configurado
- Ideal para testes locais
- Salvo em `quiz_progress.json`

Cada usuário pode:

- Pausar e continuar depois
- Voltar e corrigir respostas
- Ver seus resultados finais

## 🔑 Armazenamento de Dados por Nome de Usuário

O sistema usa **chaves normalizadas** para armazenar dados de usuários, garantindo:

- ✅ **Case-insensitive**: "Paulo", "paulo" e "PAULO" são tratados como o mesmo usuário
- ✅ **Caracteres especiais**: "Maíra" e "Maira" são normalizados corretamente
- ✅ **Espaços**: "João Silva" vira "joao_silva" internamente
- ✅ **Compatibilidade Firebase**: Chaves seguras para IDs de documentos
- ✅ **Preservação de nomes**: O nome original é salvo em `display_name` para exibição

### Migração de Dados Existentes

Se você já tem dados no Firebase com nomes originais, execute o script de migração:

```bash
# Primeiro, veja o que será migrado (modo dry-run)
python migrate_firebase_keys.py

# Depois, execute a migração real
python migrate_firebase_keys.py --execute
```

O script irá:

- Migrar documentos antigos para chaves normalizadas
- Adicionar o campo `display_name` para preservar nomes originais
- Manter todos os dados existentes
- Funcionar automaticamente durante o uso normal (migração sob demanda)

## 🔒 Privacidade

- Firebase: dados armazenados no Google Cloud (veja regras de segurança no setup)
- JSON local: dados salvos apenas no servidor
- Para produção: considere adicionar autenticação de usuários

## 📝 Licença

Livre para uso educacional e religioso.

## 🤝 Contribuindo

Sugestões e melhorias são bem-vindas!

---

Desenvolvido com ❤️ para ajudar pessoas a descobrir seus dons espirituais.
