import asyncio

from app.services.agent_service import run_agent


async def main() -> None:

    result = await run_agent(
        "What documents have I uploaded?"
    )

    print("ANSWER:")
    print(result["answer"])

    print("\nTRACES:")
    print(result["traces"])

    print("\nSOURCES:")
    print(result["sources"])


if __name__ == "__main__":
    asyncio.run(main())