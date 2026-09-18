from __future__ import annotations

from .rag import build_pipeline


def main() -> None:
    pipeline = build_pipeline()

    print("CampusCare AI")
    print("Ask a campus-support question. Type 'exit' to quit.\n")

    while True:
        try:
            question = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        if question.lower() in {"exit", "quit"}:
            print("CampusCare AI: Goodbye!")
            break

        if not question:
            print("CampusCare AI: Please enter a question.\n")
            continue

        response = pipeline.answer(question)

        print(f"\nCampusCare AI: {response.answer}")

        if response.sources:
            print("\nSources:")
            for source in response.sources:
                print(
                    f"- {source['title']} "
                    f"(similarity={source['score']})"
                )

        print()


if __name__ == "__main__":
    main()
