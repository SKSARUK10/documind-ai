import json
from typing import Any, cast, Sequence

from openai import AsyncOpenAI, OpenAI
from openai.types.chat import (
    ChatCompletionMessageParam,
    ChatCompletionToolUnionParam,
)

from langchain_core.messages import (
    AIMessage,
    AnyMessage,
    HumanMessage,
    SystemMessage,
    ToolMessage,
)

from app.core.config import get_settings


def _message_to_openai(
    message: AnyMessage,
) -> ChatCompletionMessageParam:

    if isinstance(message, HumanMessage):
        return cast(
            ChatCompletionMessageParam,
            {
                "role": "user",
                "content": str(message.content),
            },
        )

    if isinstance(message, SystemMessage):
        return cast(
            ChatCompletionMessageParam,
            {
                "role": "system",
                "content": str(message.content),
            },
        )

    if isinstance(message, ToolMessage):
        return cast(
            ChatCompletionMessageParam,
            {
                "role": "tool",
                "content": str(message.content),
                "tool_call_id": message.tool_call_id,
            },
        )

    if isinstance(message, AIMessage):

        result: dict[str, Any] = {
            "role": "assistant",
            "content": (
                str(message.content)
                if message.content
                else None
            ),
        }

        if message.tool_calls:
            result["tool_calls"] = [
                {
                    "id": tool_call["id"],
                    "type": "function",
                    "function": {
                        "name": tool_call["name"],
                        "arguments": json.dumps(
                            tool_call["args"]
                        ),
                    },
                }
                for tool_call in message.tool_calls
            ]

        return cast(
            ChatCompletionMessageParam,
            result,
        )

    raise TypeError(
        f"Unsupported message type: {type(message).__name__}"
    )


def _openai_to_ai_message(response: Any) -> AIMessage:

    message = response.choices[0].message

    tool_calls = []

    if message.tool_calls:

        for tool_call in message.tool_calls:

            arguments = json.loads(
                tool_call.function.arguments
            )

            tool_calls.append(
                {
                    "name": tool_call.function.name,
                    "args": arguments,
                    "id": tool_call.id,
                    "type": "tool_call",
                }
            )

    return AIMessage(
        content=message.content or "",
        tool_calls=tool_calls,
    )


def _convert_tools(
    tools: Sequence[Any],
) -> list[ChatCompletionToolUnionParam]:

    converted: list[ChatCompletionToolUnionParam] = []

    for tool in tools:

        converted.append(
            cast(
                ChatCompletionToolUnionParam,
                {
                    "type": "function",
                    "function": {
                        "name": tool.name,
                        "description": tool.description or "",
                        "parameters": tool.args_schema.model_json_schema(),
                    },
                },
            )
        )

    return converted


class OpenAIChatModel:

    def __init__(self):

        settings = get_settings()

        api_key = settings.llm_api_key.get_secret_value()

        self.model = settings.llm_model

        self.client = OpenAI(
            api_key=api_key,
            base_url=settings.llm_base_url,
        )

        self.async_client = AsyncOpenAI(
            api_key=api_key,
            base_url=settings.llm_base_url,
        )

    def bind_tools(
        self,
        tools: Sequence[Any],
    ):

        return BoundOpenAIChatModel(
            model=self,
            tools=_convert_tools(tools),
        )

    def invoke(
        self,
        prompt: str,
    ) -> AIMessage:

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        )

        return _openai_to_ai_message(response)

    async def ainvoke(
        self,
        messages: list[AnyMessage],
    ) -> AIMessage:

        openai_messages: list[ChatCompletionMessageParam] = [
            _message_to_openai(message)
            for message in messages
        ]

        response = await self.async_client.chat.completions.create(
            model=self.model,
            messages=openai_messages,
        )

        return _openai_to_ai_message(response)


class BoundOpenAIChatModel:

    def __init__(
        self,
        model: OpenAIChatModel,
        tools: list[ChatCompletionToolUnionParam],
    ):

        self.model = model
        self.tools = tools

    async def ainvoke(
        self,
        messages: list[AnyMessage],
    ) -> AIMessage:

        openai_messages: list[ChatCompletionMessageParam] = [
            _message_to_openai(message)
            for message in messages
        ]

        response = await self.model.async_client.chat.completions.create(
            model=self.model.model,
            messages=openai_messages,
            tools=self.tools,
            tool_choice="auto",
        )

        return _openai_to_ai_message(response)


def create_llm() -> OpenAIChatModel:

    return OpenAIChatModel()


def generate_answer(
    question: str,
    context: str,
) -> str:

    llm = create_llm()

    prompt = f"""
Answer the question using only the provided context.

Context:
{context}

Question:
{question}

If the answer is not available in the context, say:
"I don't know based on the provided document."
"""

    response = llm.invoke(prompt)

    return str(response.content)
