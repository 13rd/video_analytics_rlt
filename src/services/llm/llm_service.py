from src.services.llm.llm_client import LLMClient
from src.services.llm.llm_config import SCHEMA_CONTEXT, SYSTEM_PROMPT
from settings import LLM_API_KEY, LLM_MODEL, SITE_URL, SITE_NAME


async def get_sql_request(user_request):
    """
    Response to LLMClient and generate sql request.
    :param user_request:
    :return:
    """
    llm_client = LLMClient(model=LLM_MODEL, api_key=LLM_API_KEY, site_url=SITE_URL, site_name=SITE_NAME)

    result = await llm_client.generate_sql(
        user_query=user_request,
        schema_context=SCHEMA_CONTEXT,
        system_prompt=SYSTEM_PROMPT,
        )

    if result["success"]:
        return result["sql"]
    else:
        return result['error']
