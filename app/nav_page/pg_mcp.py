import streamlit as st
from streamlit import session_state as ss
from utils import rnd_id
import db_utils


class PageMCP:
    def __init__(self):
        self.name = "MCP"

    def init_state(self):
        if "mcps" not in ss:
            ss.mcps = []

    def add_mcp(self, name, mcp_type, endpoint, command):
        mcp = {
            "id": f"mcp_{rnd_id()}",
            "name": name,
            "type": mcp_type,
            "endpoint": endpoint,
            "command": command,
            "enabled": True,
        }
        ss.mcps.append(mcp)
        db_utils.save_mcp(mcp)

    def remove_mcp(self, mcp_id):
        ss.mcps = [m for m in ss.mcps if m["id"] != mcp_id]
        db_utils.delete_mcp(mcp_id)
        st.rerun()

    def draw(self):
        self.init_state()

        # ---- Page header ----
        st.markdown(
            """
            <div style="margin-bottom:20px;">
                <h1 style="font-size:48px; margin-bottom:6px;">MCP</h1>
                <p style="font-size:18px; opacity:0.75;">
                    Connect agents to external Model Context Protocol (MCP) servers.
                    MCP servers provide tools, resources, and prompts beyond local capabilities.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            <div style="
                border-radius:12px;
                padding:14px 16px;
                border:1px solid rgba(255,255,255,0.08);
                background:rgba(255,255,255,0.02);
                max-width:500px;
                margin-bottom:24px;
                font-size:18px;
            ">
                <strong>What MCP provides</strong>
                <ul style="margin-top:8px; padding-left:18px;">
                    <li>Remote tools and actions</li>
                    <li>External data sources</li>
                    <li>Shared context across agents</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("---")

        # ---- Add MCP ----
        st.markdown("### Add MCP server")

        name = st.text_input("Name")
        mcp_type = st.selectbox("Transport", ["http", "stdio"])

        endpoint = None
        command = None

        if mcp_type == "http":
            endpoint = st.text_input("Server URL", placeholder="http://localhost:3000")
        else:
            command = st.text_input("Command", placeholder="node server.js")

        if st.button("➕ Add MCP server", disabled=not name):
            self.add_mcp(name, mcp_type, endpoint, command)
            st.rerun()

        st.markdown("---")

        # ---- Enabled MCPs ----
        st.markdown("### Enabled MCP servers")

        if not ss.mcps:
            st.info("No MCP servers configured.")
            return

        for mcp in ss.mcps:
            with st.expander(mcp["name"], expanded=not mcp["enabled"]):
                st.write(f"**Type:** {mcp['type']}")
                if mcp["endpoint"]:
                    st.code(mcp["endpoint"])
                if mcp["command"]:
                    st.code(mcp["command"])

                mcp["enabled"] = st.checkbox(
                    "Enabled",
                    value=mcp["enabled"],
                    key=f"enabled_{mcp['id']}",
                )

                if st.button("🗑 Remove MCP", key=f"remove_{mcp['id']}"):
                    self.remove_mcp(mcp["id"])
