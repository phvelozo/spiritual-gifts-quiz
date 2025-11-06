# Firebase Setup for Spiritual Gifts Quiz

## 🔥 Firebase Integration

Your quiz application now supports Firebase Firestore for data storage! This allows reports to pull data from the cloud database instead of local JSON files.

## Setup Options

The application will automatically try these methods in order:

### Option 1: Streamlit Secrets (For Streamlit Cloud)

Already configured in your `streamlit_app.py`

### Option 2: Environment Variable (For Local Development)

```bash
export FIREBASE_CREDENTIALS="/path/to/your/serviceAccountKey.json"
```

### Option 3: Local JSON File (Easiest for Testing)

1. Download your Firebase service account key from Firebase Console
2. Save it as `serviceAccountKey.json` in the project root
3. **IMPORTANT**: Add it to `.gitignore` to avoid committing credentials!

```bash
# Add to .gitignore
echo "serviceAccountKey.json" >> .gitignore
```

## How to Get Firebase Credentials

1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Select your project
3. Go to **Project Settings** (gear icon)
4. Navigate to **Service Accounts** tab
5. Click **Generate New Private Key**
6. Save the downloaded JSON file as `serviceAccountKey.json`

## Usage

### Command Line Interface

```bash
# Run the application
python test.py

# The app will show Firebase status:
# ✅ Status: Conectado ao Firebase
# or
# 📄 Status: Modo local (JSON)
```

### Programmatic Usage

```python
from test import init_firebase, generate_gift_report, display_gift_report

# Initialize Firebase
init_firebase()

# Generate report from Firebase
report = generate_gift_report(use_firebase=True)

# Or use JSON fallback only
report = generate_gift_report(use_firebase=False)

# Display formatted report
display_gift_report()
```

## Data Structure in Firebase

**Collection**: `quiz_progress`

**Documents**: Each document ID is a **normalized username key** (e.g., `paulo`, `maira`, `joao_silva`)

**Document structure**:

```json
{
  "display_name": "Paulo",  // Original username for display
  "answers": {
    "1": 3,
    "2": 2,
    "3": 1,
    ...
  },
  "scores": {
    "A": 12,
    "B": 10,
    "C": 8,
    ...
  },
  "last_updated": "2025-11-03T10:30:00",
  "completed": true,
  "church_name": "Igreja Central"  // Optional
}
```

### Username Normalization

The system automatically normalizes usernames to create safe, consistent document IDs:

- **Case-insensitive**: "Paulo", "paulo", "PAULO" → all become `paulo`
- **Unicode handling**: "Maíra" → `maira` (accents removed)
- **Spaces**: "João Silva" → `joao_silva` (spaces become underscores)
- **Special characters**: Removed for Firebase compatibility
- **Display name preserved**: Original name stored in `display_name` field

**Examples**:
- Input: "Paulo" → Document ID: `paulo`
- Input: "Maíra" → Document ID: `maira`
- Input: "João Silva" → Document ID: `joao_silva`
- Input: "Tião" → Document ID: `tiao`

### Migrating Existing Data

If you have existing Firebase data with original usernames as document IDs, use the migration script:

```bash
# Preview what will be migrated (dry-run)
python migrate_firebase_keys.py

# Execute the migration
python migrate_firebase_keys.py --execute
```

The migration script will:
- ✅ Find all documents that need normalization
- ✅ Create new documents with normalized keys
- ✅ Add `display_name` field to preserve original names
- ✅ Delete old documents after migration
- ✅ Skip documents that are already normalized
- ✅ Handle conflicts gracefully

**Note**: The app also migrates data automatically when users save their progress, but running the script is recommended for bulk migration.

## Features

### 1. Gift Report (Ranking by Gift)

Shows all participants ranked by their score for each gift:

```
A: Profecia
────────────────────────────────────────────────────────────
  1. Paulo                 - 15 pontos
  2. Thomas                - 14 pontos
  3. test                  - 13 pontos

B: Serviço
────────────────────────────────────────────────────────────
  1. Nelson                - 14 pontos
  2. test                  - 12 pontos
```

### 2. Participant Summary

Shows all participants with their top gift and completion status:

```
Nome                 Dom Principal    Pontuação    Status
────────────────────────────────────────────────────────────
Paulo                Profecia         15           ✓ Completo
Nelson               Serviço          14           ✓ Completo
test                 Ensino           12           ⚠ Incompleto
```

## Automatic Fallback

The application automatically falls back to JSON files if:

- Firebase credentials are not found
- Firebase initialization fails
- Network connection is unavailable

This ensures the app works in all environments!

## Security Notes

⚠️ **Never commit your Firebase credentials to version control!**

Always add to `.gitignore`:

```
serviceAccountKey.json
.env
secrets.toml
```

## Dependencies

Make sure you have the Firebase Admin SDK installed:

```bash
pip install firebase-admin
```

If not already in `requirements.txt`, add it:

```
firebase-admin>=6.0.0
```
