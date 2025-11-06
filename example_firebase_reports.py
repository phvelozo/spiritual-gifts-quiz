#!/usr/bin/env python3
"""
Example script demonstrating Firebase report functionality.
Run this to see how to use the Firebase-enabled reporting features.
"""

from test import (
    FIREBASE_ENABLED,
    display_gift_report,
    display_participant_summary,
    generate_gift_report,
    get_top_performers_by_gift,
    init_firebase,
)


def main():
    print("=" * 80)
    print("FIREBASE REPORTS - EXAMPLE SCRIPT")
    print("=" * 80)

    # Initialize Firebase
    print("\n1️⃣  Initializing Firebase...")
    init_firebase()

    if FIREBASE_ENABLED:
        print("✅ Firebase is enabled and ready!")
    else:
        print("📄 Firebase not available, using JSON fallback")

    print("\n" + "-" * 80)

    # Example 1: Display full gift report
    print("\n2️⃣  Displaying full gift report (from Firebase if available):")
    display_gift_report()

    print("-" * 80)

    # Example 2: Display participant summary
    print("\n3️⃣  Displaying participant summary:")
    display_participant_summary()

    print("-" * 80)

    # Example 3: Get top performers programmatically
    print("\n4️⃣  Getting top 3 performers for each gift (programmatic access):")
    top_performers = get_top_performers_by_gift(top_n=3)

    for gift, rankings in sorted(top_performers.items()):
        if rankings:
            print(f"\n{gift}:")
            for rank, (name, score) in enumerate(rankings, 1):
                print(f"  {rank}. {name} - {score} pontos")

    print("\n" + "-" * 80)

    # Example 4: Get raw report data
    print("\n5️⃣  Getting raw report data for custom processing:")
    report = generate_gift_report()

    # Count total participants
    all_participants = set()
    for gift, rankings in report.items():
        for name, score in rankings:
            all_participants.add(name)

    print(f"\nTotal unique participants: {len(all_participants)}")
    print(f"Total gifts tracked: {len(report)}")

    # Find highest scores across all gifts
    if report:
        all_scores = []
        for gift, rankings in report.items():
            for name, score in rankings:
                all_scores.append((name, gift, score))

        all_scores.sort(key=lambda x: x[2], reverse=True)

        print("\n🏆 Highest individual gift scores across all participants:")
        for i, (name, gift, score) in enumerate(all_scores[:5], 1):
            print(f"  {i}. {name} - Gift {gift}: {score} pontos")

    print("\n" + "=" * 80)
    print("Example completed!")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    main()
