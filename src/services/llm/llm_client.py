import httpx
import json
from typing import Optional, Dict, Any


class LLMClient:
    def __init__(self,
                 api_key: Optional[str] = None,
                 model: str = "x-ai/grok-code-fast-1",
                 site_url: Optional[str] = None,
                 site_name: Optional[str] = None,):
        self.api_key = api_key
        if not self.api_key:
            raise ValueError("API ключ не найден. Проверьте .env файл или передайте api_key.")

        self.base_url = "https://openrouter.ai/api/v1"
        self.model = model
        self.timeout = 30.0
        self.site_url = site_url
        self.site_name = site_name

    async def generate_sql(self, user_query: str, schema_context: str, system_prompt: str) -> Dict[str, Any]:
        """
        Отправляет запрос к LLM и возвращает парсеный JSON с SQL запросом.
        """
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": self.site_url,
                "X-Title": self.site_name,
            }

            # Формируем сообщение системы с контекстом схемы
            full_system_prompt = (f"{system_prompt}\n\n### ТЕКУЩАЯ СХЕМА БД \n"
                                  f"Используй ТОЛЬКО эти таблицы и колонки. Не выдумывай другие.:\n{schema_context}")

            payload = {
                "model": self.model,
                "messages": [
                    {"role": "system", "content": full_system_prompt},
                    {"role": "user", "content": user_query}
                ],
                "temperature": 0.0,  # Важно для детерминированного SQL
                "response_format": {"type": "json_object"}
            }

            try:
                response = await client.post(
                    f"{self.base_url}/chat/completions",
                    json=payload,
                    headers=headers
                )
                response.raise_for_status()
                data = response.json()

                content = data['choices'][0]['message']['content']
                parsed_content = json.loads(content)

                return {
                    "success": True,
                    "sql": parsed_content.get("sql"),
                    "raw_response": content,
                    "model_used": data.get("model"),
                    "usage": data.get("usage")
                }


            except httpx.HTTPStatusError as e:
                error_detail = e.response.text
                return {"success": False, "error": f"HTTP Error {e.response.status_code}: {error_detail}"}
            except json.JSONDecodeError as e:
                return {"success": False, "error": f"JSON Parse Error: {str(e)}"}
            except Exception as e:
                return {"success": False, "error": f"Unexpected Error: {str(e)}"}
