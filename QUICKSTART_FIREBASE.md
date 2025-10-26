# 🚀 Quick Start: Firebase in 5 Minutes

Too long to read the full guide? Here's the fastest way to get Firebase working:

## ⚡ Super Quick Setup

### 1. Create Firebase Project (2 min)

1. Go to https://console.firebase.google.com/
2. Click "Add project" → Name it → Disable Analytics → Create
3. Click "Firestore Database" → "Create database" → "Production mode" → Choose region → Enable

### 2. Get Credentials (1 min)

1. Click ⚙️ → "Project settings" → "Service accounts" tab
2. Click "Generate new private key" → Confirm
3. A JSON file downloads - **keep it safe!**

### 3. Configure Streamlit (2 min)

Create `.streamlit/secrets.toml` in your project folder:

```bash
mkdir -p .streamlit
nano .streamlit/secrets.toml
```

Paste this format (fill with values from the downloaded JSON):

```toml
[firebase]
type = "service_account"
project_id = "your-project-id"
private_key_id = "abc123..."
private_key = "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n"
client_email = "firebase-adminsdk-xxx@your-project.iam.gserviceaccount.com"
client_id = "123456789"
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs/firebase-adminsdk..."
```

### 4. Run It!

```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```

That's it! Your app now saves to Firebase! 🎉

## 🔍 How to Verify It's Working

1. Start a quiz and answer a few questions
2. Click "💾 Salvar e Sair"
3. Go to Firebase Console → Firestore Database
4. You should see: `quiz_progress` → `[your-name]` → data

## 🌐 For Streamlit Cloud Deployment

1. Go to https://share.streamlit.io/
2. Deploy your app
3. Click ⋮ menu → Settings → Secrets
4. Paste the same TOML content from above
5. Save → Your app restarts with Firebase!

## ⚠️ Don't Forget!

- Add `.streamlit/secrets.toml` to `.gitignore` (already done!)
- Never commit Firebase credentials to Git
- Set proper security rules for production (see full guide)

## 🆘 Troubleshooting

**"Module not found: firebase-admin"**

```bash
pip install firebase-admin
```

**"Firebase not available" warning**

- Check that `.streamlit/secrets.toml` exists
- Verify the `[firebase]` section is present
- Restart Streamlit

**Still not working?**

- The app works fine without Firebase (uses JSON fallback)
- See detailed guide: [FIREBASE_SETUP.md](FIREBASE_SETUP.md)

## 📚 More Details?

See the complete setup guide: [`FIREBASE_SETUP.md`](FIREBASE_SETUP.md)
