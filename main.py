def main():
    import os

    from src.backend.config.settings import settings

    llm = settings.get_llm()

    res = llm.invoke("Hello")

    print(res.content)
    print(
        f"open ai api key from global: {os.getenv('OPENAI_API_KEY')}"
    )  # ✅ safe : revoked  # noqa: E501
    print(
        f"open ai api key from class: {settings.openai_api_key}"
    )  # ✅ safe : can't be printed as pydantic SecretStr  # noqa: E501


if __name__ == "__main__":
    main()
