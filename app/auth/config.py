from pydantic_settings import BaseSettings, SettingsConfigDict


class AuthConfig(BaseSettings):
    """Settings owned by the auth domain."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_ignore_empty=True,
        extra="ignore",
    )

    SECRET_KEY: str
    JWT_ALG: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 8

    # The single credential pair the API accepts at the login endpoint.
    API_USERNAME: str
    API_PASSWORD: str


auth_settings = AuthConfig()  # type: ignore # ty: ignore[unused-ignore-comment]
