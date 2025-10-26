# 🚀 Guia de Deploy - Teste de Dons Espirituais

## 📱 Deploy Gratuito com Streamlit Cloud (Recomendado)

### Passo 1: Preparar o Repositório

1. Crie um repositório no GitHub
2. Faça upload dos arquivos:
   ```bash
   cd spiritual-gifts-quiz
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/seu-usuario/spiritual-gifts-quiz.git
   git push -u origin main
   ```

### Passo 2: Deploy no Streamlit Cloud

1. Acesse: https://share.streamlit.io
2. Clique em "New app"
3. Conecte sua conta GitHub
4. Selecione:
   - Repository: `seu-usuario/spiritual-gifts-quiz`
   - Branch: `main`
   - Main file path: `streamlit_app.py`
5. Clique em "Deploy!"

🎉 **Pronto!** Seu app estará online em minutos em uma URL como:
`https://seu-usuario-spiritual-gifts-quiz.streamlit.app`

---

## 🌐 Outras Opções de Deploy

### Opção 2: Railway.app

1. Acesse: https://railway.app
2. Clique em "Start a New Project"
3. Selecione "Deploy from GitHub repo"
4. Conecte seu repositório
5. Railway detecta automaticamente o Streamlit
6. Deploy automático!

**Custo:** Gratuito com $5/mês de crédito

### Opção 3: Heroku

```bash
# 1. Criar Procfile
echo "web: streamlit run streamlit_app.py --server.port=\$PORT --server.address=0.0.0.0" > Procfile

# 2. Instalar Heroku CLI e fazer deploy
heroku login
heroku create seu-app-name
git push heroku main
```

**Custo:** ~$7/mês (Eco Dynos)

### Opção 4: DigitalOcean App Platform

1. Acesse: https://cloud.digitalocean.com/apps
2. Clique em "Create App"
3. Conecte seu repositório GitHub
4. Configure:
   - Run Command: `streamlit run streamlit_app.py`
   - HTTP Port: 8501
5. Deploy!

**Custo:** A partir de $5/mês

---

## 🖥️ Deploy em Servidor Próprio (VPS)

### Usando Docker

```dockerfile
# Criar Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "streamlit_app.py"]
```

```bash
# Build e Run
docker build -t spiritual-gifts-quiz .
docker run -p 8501:8501 spiritual-gifts-quiz
```

### Usando Nginx + Supervisor (Ubuntu/Debian)

```bash
# 1. Instalar dependências
sudo apt update
sudo apt install python3-pip nginx supervisor

# 2. Instalar pacotes Python
pip3 install -r requirements.txt

# 3. Criar arquivo supervisor
sudo nano /etc/supervisor/conf.d/spiritual-quiz.conf
```

Conteúdo do arquivo:

```ini
[program:spiritual-quiz]
command=/usr/bin/streamlit run /path/to/streamlit_app.py
directory=/path/to/spiritual-gifts-quiz
autostart=true
autorestart=true
user=www-data
redirect_stderr=true
stdout_logfile=/var/log/spiritual-quiz.log
```

```bash
# 4. Configurar Nginx
sudo nano /etc/nginx/sites-available/spiritual-quiz
```

Conteúdo:

```nginx
server {
    listen 80;
    server_name seu-dominio.com;

    location / {
        proxy_pass http://localhost:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
    }
}
```

```bash
# 5. Ativar e iniciar
sudo ln -s /etc/nginx/sites-available/spiritual-quiz /etc/nginx/sites-enabled/
sudo supervisorctl reread
sudo supervisorctl update
sudo systemctl restart nginx
```

---

## 🔧 Configurações de Produção

### Variáveis de Ambiente (opcional)

Crie `.streamlit/secrets.toml` (não versione este arquivo):

```toml
[database]
# Se quiser usar banco de dados no futuro
# connection_string = "postgresql://user:pass@host/db"
```

### Backup Automático dos Dados

```bash
# Criar script de backup (backup.sh)
#!/bin/bash
cp quiz_progress.json "backups/quiz_progress_$(date +%Y%m%d_%H%M%S).json"
```

```bash
# Adicionar ao crontab (rodar todo dia às 2h)
crontab -e
# Adicionar linha:
0 2 * * * /path/to/backup.sh
```

---

## 📊 Monitoramento

### Streamlit Cloud

- Logs automáticos no dashboard
- Métricas de uso gratuitas

### Self-hosted

```bash
# Ver logs
tail -f /var/log/spiritual-quiz.log

# Monitorar uso
htop
```

---

## 🔐 Segurança (Recomendações)

1. **HTTPS**: Use Let's Encrypt para certificado SSL

   ```bash
   sudo apt install certbot python3-certbot-nginx
   sudo certbot --nginx -d seu-dominio.com
   ```

2. **Firewall**: Abra apenas portas necessárias

   ```bash
   sudo ufw allow 80
   sudo ufw allow 443
   sudo ufw enable
   ```

3. **Backups**: Configure backups automáticos
4. **Atualizações**: Mantenha sistema e pacotes atualizados

---

## 🆘 Troubleshooting

### App não inicia

```bash
# Verificar logs do Streamlit
streamlit run streamlit_app.py --logger.level=debug
```

### Erro de importação

```bash
# Reinstalar dependências
pip install -r requirements.txt --force-reinstall
```

### Dados não salvam

- Verificar permissões do arquivo `quiz_progress.json`
- Garantir que o diretório é gravável

---

## 📞 Suporte

Para problemas específicos de deploy:

- Streamlit: https://docs.streamlit.io
- Railway: https://docs.railway.app
- Heroku: https://devcenter.heroku.com

---

**Recomendação:** Para facilidade e custo zero, use **Streamlit Cloud** 🚀
