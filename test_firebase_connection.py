#!/usr/bin/env python3
"""
Test Firebase connection - improved version.
"""

import os
import sys

print("=" * 80)
print("FIREBASE CONNECTION TEST")
print("=" * 80)

# Step 1: Check if serviceAccountKey.json exists
print("\n1️⃣  Checking for serviceAccountKey.json...")
if os.path.exists("serviceAccountKey.json"):
    print("✅ serviceAccountKey.json found")
else:
    print("❌ serviceAccountKey.json NOT found")

# Step 2: Check if firebase-admin is installed
print("\n2️⃣  Checking firebase-admin package...")
try:
    import firebase_admin

    print(f"✅ firebase-admin installed (version: {firebase_admin.__version__})")
except ImportError:
    print("❌ firebase-admin not installed")
    sys.exit(1)

# Step 3: Try to initialize Firebase
print("\n3️⃣  Attempting to initialize Firebase...")
try:
    import test

    print("   Calling init_firebase()...")
    result = test.init_firebase()

    print(f"\n   Result: {result}")
    print(f"   test.FIREBASE_ENABLED: {test.FIREBASE_ENABLED}")
    print(f"   test.db object: {test.db}")

    if result and test.FIREBASE_ENABLED and test.db:
        print("\n✅ Firebase initialized successfully!")

        # Step 4: Try to read from Firestore
        print("\n4️⃣  Testing Firestore connection...")
        try:
            # Try to get collection
            all_docs = list(test.db.collection("quiz_progress").stream())
            print(f"✅ Successfully connected to Firestore")
            print(f"   Total participants in database: {len(all_docs)}")

            if len(all_docs) > 0:
                print(f"\n   Sample participants:")
                for doc in all_docs[:5]:
                    print(f"   - {doc.id}")

        except Exception as e:
            print(f"❌ Firestore connection failed: {e}")
            import traceback

            traceback.print_exc()
    else:
        print("\n❌ Firebase initialization failed")
        print("   Check that your credentials are correct")

except Exception as e:
    print(f"❌ Error during initialization: {e}")
    import traceback

    traceback.print_exc()

print("\n" + "=" * 80)
print("Test complete!")
print("=" * 80 + "\n")
