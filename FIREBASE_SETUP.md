# 🔥 Firebase Setup Guide

This guide will help you set up Firebase Firestore for persistent quiz data storage.

## Why Firebase?

- ✅ Free tier (50K reads/20K writes per day)
- ✅ No server management needed
- ✅ Data persists across app restarts
- ✅ Perfect for Streamlit Cloud deployment

## Step-by-Step Setup

### 1. Create a Firebase Project

1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Click **"Add project"** or **"Create a project"**
3. Enter project name (e.g., `spiritual-gifts-quiz`)
4. Disable Google Analytics (optional)
5. Click **"Create project"**

### 2. Create Firestore Database

1. In your Firebase project, click **"Firestore Database"** in the left menu
2. Click **"Create database"**
3. Choose **"Start in production mode"** (we'll set rules next)
4. Select your region (choose closest to your users)
5. Click **"Enable"**

### 3. Set Firestore Security Rules

1. In Firestore Database, go to the **"Rules"** tab
2. Replace the rules with:

```
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /quiz_progress/{document=**} {
      allow read, write: if true;
    }
  }
}
```

3. Click **"Publish"**

> ⚠️ **Note**: These rules allow public read/write. For production, you should add authentication or more restrictive rules.

### 4. Get Service Account Credentials

1. Click the **⚙️ gear icon** (Settings) → **"Project settings"**
2. Go to the **"Service accounts"** tab
3. Click **"Generate new private key"**
4. Click **"Generate key"** (a JSON file will download)
5. **Keep this file secure!** It contains sensitive credentials

### 5. Configure Streamlit Secrets

#### For Local Development:

Create a `.streamlit/secrets.toml` file in your project:

```toml
[firebase]
type = "service_account"
project_id = "your-project-id"
private_key_id = "your-private-key-id"
private_key = "-----BEGIN PRIVATE KEY-----\nYour-Private-Key-Here\n-----END PRIVATE KEY-----\n"
client_email = "your-service-account@your-project.iam.gserviceaccount.com"
client_id = "your-client-id"
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "your-cert-url"
```

Copy the values from the downloaded JSON file.

> ⚠️ **Important**: Add `.streamlit/` to your `.gitignore` file!

#### For Streamlit Cloud Deployment:

1. Go to your app on [Streamlit Cloud](https://share.streamlit.io/)
2. Click the **⋮** menu → **"Settings"**
3. Go to the **"Secrets"** section
4. Paste the same TOML configuration above
5. Click **"Save"**

### 6. Test the Setup

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Run your app:

```bash
streamlit run streamlit_app.py
```

3. Complete a few quiz questions and click **"💾 Salvar e Sair"**
4. Check Firebase Console → Firestore Database
5. You should see a new collection called `quiz_progress` with your data!

## Troubleshooting

### "Firebase not available" message

- Check that `firebase-admin` is installed: `pip install firebase-admin`
- Verify your `secrets.toml` file is in the `.streamlit/` folder
- Check that the `[firebase]` section is properly formatted

### "Permission denied" errors

- Make sure Firestore security rules allow read/write
- Verify your service account has the correct permissions

### Data not saving

- Check Streamlit logs for error messages
- Verify Firebase credentials are correct
- Try the fallback JSON mode first (remove secrets temporarily)

## Fallback Mode

The app automatically falls back to local JSON file storage if:

- Firebase credentials are not configured
- Firebase connection fails
- You're testing locally

This means the app will work even without Firebase setup!

## Security Best Practices

For production apps:

1. **Enable Authentication**: Use Firebase Authentication or Streamlit auth
2. **Update Security Rules**: Restrict access to authenticated users only
3. **Use Environment Variables**: For sensitive credentials
4. **Monitor Usage**: Check Firebase Console for quota usage
5. **Add Data Validation**: Validate user input before saving

## Support

If you need help:

- [Firebase Documentation](https://firebase.google.com/docs/firestore)
- [Streamlit Secrets Management](https://docs.streamlit.io/streamlit-community-cloud/deploy-your-app/secrets-management)
