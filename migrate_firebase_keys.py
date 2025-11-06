"""
Migration script to normalize all Firebase document keys.

This script migrates existing Firebase documents from original usernames
to normalized keys. It:
1. Reads all documents from the quiz_progress collection
2. For each document, checks if the document ID needs normalization
3. Creates a new document with normalized key
4. Adds display_name field if missing
5. Deletes the old document

Run this script once to migrate all existing data.
"""

import os
import re
import sys
import unicodedata

try:
    import firebase_admin
    from firebase_admin import credentials, firestore
except ImportError:
    print(
        "❌ Firebase Admin SDK not installed. Install with: pip install firebase-admin"
    )
    sys.exit(1)


def normalize_username_key(name):
    """
    Normalize username to create a safe, consistent key for storage.
    Same implementation as in streamlit_app.py for consistency.
    """
    if not name:
        return ""

    # Normalize Unicode characters (e.g., "Maíra" -> "Maira")
    name = unicodedata.normalize("NFKD", name)

    # Convert to lowercase
    name = name.lower()

    # Replace spaces with underscores
    name = name.replace(" ", "_")

    # Remove or replace special characters, keep only alphanumeric and underscores
    name = re.sub(r"[^a-z0-9_-]", "", name)

    # Remove multiple consecutive underscores
    name = re.sub(r"_+", "_", name)

    # Remove leading/trailing underscores
    name = name.strip("_")

    # Ensure it's not empty (fallback to 'user' if somehow empty)
    if not name:
        name = "user"

    return name


def init_firebase():
    """Initialize Firebase connection."""
    try:
        # Check if Firebase is already initialized
        try:
            firebase_admin.get_app()
            # Already initialized, just get the client
            db = firestore.client()
            print("✅ Firebase already initialized, reusing connection")
            return db
        except ValueError:
            # Not initialized yet, proceed with initialization
            pass

        # Try to get credentials from serviceAccountKey.json
        if os.path.exists("serviceAccountKey.json"):
            cred = credentials.Certificate("serviceAccountKey.json")
            firebase_admin.initialize_app(cred)
            db = firestore.client()
            print("✅ Firebase initialized from serviceAccountKey.json")
            return db
        else:
            print("❌ serviceAccountKey.json not found")
            return None
    except Exception as e:
        print(f"❌ Firebase initialization failed: {e}")
        return None


def migrate_firebase_keys(dry_run=True):
    """
    Migrate all Firebase documents to use normalized keys.

    Args:
        dry_run: If True, only show what would be migrated without making changes
    """
    db = init_firebase()
    if not db:
        print("❌ Cannot proceed without Firebase connection")
        return

    print("\n" + "=" * 80)
    if dry_run:
        print("🔍 DRY RUN MODE - No changes will be made")
    else:
        print("🚀 MIGRATION MODE - Changes will be saved")
    print("=" * 80 + "\n")

    try:
        # Get all documents
        all_docs = list(db.collection("quiz_progress").stream())
        print(f"📊 Found {len(all_docs)} documents in Firebase\n")

        if len(all_docs) == 0:
            print("✅ No documents to migrate")
            return

        migrated_count = 0
        skipped_count = 0
        error_count = 0

        for doc in all_docs:
            old_key = doc.id
            normalized_key = normalize_username_key(old_key)

            # Check if migration is needed
            if old_key == normalized_key:
                print(f"⏭️  Skipping '{old_key}' (already normalized)")
                skipped_count += 1
                continue

            data = doc.to_dict()
            if not data:
                print(f"⚠️  Skipping '{old_key}' (empty document)")
                skipped_count += 1
                continue

            # Check if normalized key already exists
            new_doc = db.collection("quiz_progress").document(normalized_key).get()
            if new_doc.exists:
                print(
                    f"⚠️  Skipping '{old_key}' -> '{normalized_key}' (target already exists)"
                )
                skipped_count += 1
                continue

            # Prepare data for migration
            migrated_data = data.copy()
            # Add display_name if missing
            if "display_name" not in migrated_data:
                migrated_data["display_name"] = old_key

            print(f"🔄 Would migrate: '{old_key}' -> '{normalized_key}'")

            if not dry_run:
                try:
                    # Create new document with normalized key
                    db.collection("quiz_progress").document(normalized_key).set(
                        migrated_data
                    )
                    # Delete old document
                    db.collection("quiz_progress").document(old_key).delete()
                    print(f"   ✅ Migrated successfully")
                    migrated_count += 1
                except Exception as e:
                    print(f"   ❌ Error migrating: {e}")
                    error_count += 1
            else:
                migrated_count += 1

        print("\n" + "=" * 80)
        print("📊 MIGRATION SUMMARY")
        print("=" * 80)
        print(f"✅ Would migrate: {migrated_count}")
        print(f"⏭️  Skipped: {skipped_count}")
        print(f"❌ Errors: {error_count}")
        print(f"📝 Total processed: {len(all_docs)}")

        if dry_run:
            print("\n💡 To perform the actual migration, run:")
            print("   python migrate_firebase_keys.py --execute")
        else:
            print("\n✅ Migration completed!")

    except Exception as e:
        print(f"\n❌ Error during migration: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    # Check for --execute flag
    dry_run = "--execute" not in sys.argv

    if dry_run:
        print(
            "⚠️  Running in DRY RUN mode. Use --execute to perform actual migration.\n"
        )

    migrate_firebase_keys(dry_run=dry_run)
