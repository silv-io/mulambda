from dynaconf import Dynaconf

settings = Dynaconf(
    envvar_prefix="MULAMBDA",
    settings_files=["settings.toml", ".secrets.toml"],
)
