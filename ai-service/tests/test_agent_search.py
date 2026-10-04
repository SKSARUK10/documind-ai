import asyncio

from app.services.agent_service import run_agent


async def main() -> None:

    result = await run_agent(
        question="What topics are covered in Module 7 about RAG?",
        document_ids=[
            "436e7a67-ff3a-4e10-9d76-de3ee94f2e15"
        ],
    )

    print("ANSWER:")
    print(result["answer"])

    print("\nTRACES:")
    print(result["traces"])

    print("\nSOURCES:")
    print(result["sources"])


if __name__ == "__main__":
    asyncio.run(main())
