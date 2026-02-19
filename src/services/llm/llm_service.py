from src.services.llm.llm_client import LLMClient
from src.services.llm.llm_config import SCHEMA_CONTEXT, SYSTEM_PROMPT


async def get_sql_request(user_request):
    llm_client = LLMClient(model="openrouter/aurora-alpha")

    result = await llm_client.generate_sql(
        user_query=user_request,
        schema_context=SCHEMA_CONTEXT,
        system_prompt=SYSTEM_PROMPT,
        )

    if result["success"]:
        return result["sql"]
    else:
        return result['error']
