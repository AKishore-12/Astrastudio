import streamlit as st
from streamlit import session_state as ss
import db_utils
from nav_page.pg_home import PageHome
from nav_page.pg_agents import PageAgents
from nav_page.pg_tasks import PageTasks
from nav_page.pg_crews import PageCrews
from nav_page.pg_tools import PageTools
from nav_page.pg_mcp import PageMCP
from nav_page.pg_crew_run import PageCrewRun
from nav_page.pg_export_crew import PageExportCrew
from nav_page.pg_results import PageResults
from nav_page.pg_knowledge import PageKnowledge
from nav_page.pg_credentials import PageCredentials
from dotenv import load_dotenv
from llms import load_secrets_fron_env
import os


def pages():
    return {
        'Home': PageHome(),
        'Crews': PageCrews(),
        'Tools': PageTools(),
        'Agents': PageAgents(),
        'Tasks': PageTasks(),
        'MCP': PageMCP(),
        'Knowledge': PageKnowledge(),  # Add this line
        'Kickoff!': PageCrewRun(),
        'Results': PageResults(),
        'Import/export': PageExportCrew(),
        'Credentials': PageCredentials(),
    }

PAGE_ICONS = {
    "Home": "🏠",
    "Crews": "🧠",
    "Tools": "🛠️",
    "Agents": "🤖",
    "Tasks": "📝",
    "MCP": "🔗",
    "Knowledge": "📚",
    "Kickoff!": "🚀",
    "Results": "📊",
    "Import/export": "📦",
    "Credentials": "🔐",
}


def load_data():
    ss.agents = db_utils.load_agents()
    ss.tasks = db_utils.load_tasks()
    ss.crews = db_utils.load_crews()
    ss.tools = db_utils.load_tools()
    ss.enabled_tools = db_utils.load_tools_state()
    ss.knowledge_sources = db_utils.load_knowledge_sources()
    ss.mcps = db_utils.load_mcps()


def draw_sidebar():
    with st.sidebar:
        st.image("img/logo.png", use_container_width=True)
        st.markdown("---")

        if "page" not in ss:
            ss.page = "Home"

        for page_name in pages().keys():
            icon = PAGE_ICONS.get(page_name, "•")
            is_active = ss.page == page_name

            if st.button(
                f"{icon}  {page_name}",
                key=f"nav-{page_name}",
                width="stretch",
                type="primary" if is_active else "secondary",
            ):
                ss.page = page_name
                st.rerun()
            
def main():
    st.set_page_config(page_title="Astrastudio", page_icon="img/icon.png", layout="wide")
    load_dotenv()
    load_secrets_fron_env()
    if (str(os.getenv('AGENTOPS_ENABLED')).lower() in ['true', '1']) and not ss.get('agentops_failed', False):
        try:
            import agentops
            agentops.init(api_key=os.getenv('AGENTOPS_API_KEY'),auto_start_session=False)    
        except ModuleNotFoundError as e:
            ss.agentops_failed = True
            print(f"Error initializing AgentOps: {str(e)}")            
        
    db_utils.initialize_db()
    load_data()
    draw_sidebar()
    PageCrewRun.maintain_session_state() #this will persist the session state for the crew run page so crew run can be run in a separate thread
    pages()[ss.page].draw()
    
if __name__ == '__main__':
    main()
