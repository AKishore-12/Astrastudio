import streamlit as st
from streamlit import session_state as ss
import os

CREDENTIAL_FIELDS = {
    "OPENAI_API_KEY": {"secret": True},
    "OPENAI_API_BASE": {"secret": False, "default": "https://api.openai.com/v1/"},
    "GROQ_API_KEY": {"secret": True},
    "GEMINI_API_KEY": {"secret": True},
    "ANTHROPIC_API_KEY": {"secret": True},
    "XAI_API_KEY": {"secret": True},
    "LMSTUDIO_API_BASE": {"secret": False},
    "OLLAMA_HOST": {"secret": False},
}


class PageCredentials:
    def __init__(self):
        self.name = "Credentials"

    def init_session_state(self):
        if "env_vars" not in ss:
            ss.env_vars = {
                key: os.getenv(key, cfg.get("default", ""))
                for key, cfg in CREDENTIAL_FIELDS.items()
            }


    def apply_credentials(self):
        for key, value in ss.env_vars.items():
            if value:
                os.environ[key] = value
            else:
                os.environ.pop(key, None)

        st.success("Credentials applied for this session.")

    def draw(self):
        self.init_session_state()

        # ---- Page header ----
        st.markdown(
            """
            <div style="margin-bottom: 20px;">
                <h1 style="font-size:48px; margin-bottom:6px;">🔐 Credentials</h1>
                <p style="font-size:18px; opacity:0.8; max-width:900px;">
                    Store API keys for the current session. Values are cleared on page refresh
                    and are not persisted.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.info(
            "Credentials are stored only in memory and will be cleared when the page is refreshed."
        )

        st.markdown("---")

        # ---- Credential inputs ----
        for key, cfg in CREDENTIAL_FIELDS.items():
            ss.env_vars[key] = st.text_input(
                label=key,
                value=ss.env_vars.get(key, ""),
                type="password" if cfg.get("secret") else "default",
                placeholder="Not set",
            )

        st.markdown("<br>", unsafe_allow_html=True)

        st.button("Apply credentials", on_click=self.apply_credentials)

        if st.button("Clear credentials"):
            st.session_state.env_vars = {
                "OPENAI_API_KEY": None,
                "OPENAI_API_BASE": "https://api.openai.com/v1/",
                "GROQ_API_KEY": None,
                "GEMINI_API_KEY": None,
                "LMSTUDIO_API_BASE": None,
                "ANTHROPIC_API_KEY": None,
                "OLLAMA_HOST": None,
                "XAI_API_KEY": None,
            }
            st.session_state.credentials_initialized = True
            st.rerun()

