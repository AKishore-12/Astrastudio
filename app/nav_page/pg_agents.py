import streamlit as st
from streamlit import session_state as ss
from my_agent import MyAgent
import db_utils

class PageAgents:
    def __init__(self):
        self.name = "Agents"

    def create_agent(self, crew=None):
        agent = MyAgent()
        if 'agents' not in ss:
            ss.agents = [MyAgent]
        ss.agents.append(agent)
        agent.edit = True
        db_utils.save_agent(agent)  # Save agent to database

        if crew:
            crew.agents.append(agent)
            db_utils.save_crew(crew)

        return agent

    def draw(self):
        with st.container():

            # ---- Page header (COMMON STYLE) ----
            st.markdown(
                """
                <div style="margin-bottom: 20px;">
                    <h1 style="font-size:48px; margin-bottom:6px;">🤖 Agents</h1>
                    <p style="font-size:18px; opacity:0.75;">
                        An agent is an autonomous unit within the CrewAI framework.
                        Agents execute tasks, make decisions based on their role and goal,
                        and collaborate with other agents to achieve objectives.
                    </p>
                </div>
                """,
                unsafe_allow_html=True,
            )

            # ---- Agent capabilities (documentation summary) ----
            st.markdown(
                """
                <div style="
                    border-radius: 12px;
                    padding: 14px 16px;
                    border: 1px solid rgba(255,255,255,0.08);
                    background: rgba(255,255,255,0.02);
                    max-width: 500px;
                    margin-bottom: 24px;
                    font-size:18px;
                ">
                    <strong>Agent capabilities</strong>
                    <ul style="margin-top:8px; padding-left:18px; opacity:0.9;">
                        <li>Perform specific tasks</li>
                        <li>Make decisions based on role and goal</li>
                        <li>Use tools to accomplish objectives</li>
                        <li>Communicate and collaborate with other agents</li>
                        <li>Maintain memory of interactions</li>
                        <li>Delegate tasks when allowed</li>
                    </ul>
                </div>
                """,
                unsafe_allow_html=True,
            )

            st.markdown("---")

            # ---- Existing logic BELOW (UNCHANGED) ----
            editing = False

            if 'agents' not in ss:
                ss.agents = db_utils.load_agents()

            if 'crews' not in ss:
                ss.crews = db_utils.load_crews()

            # Dictionary to track agent assignment
            agent_assignment = {agent.id: [] for agent in ss.agents}

            # Assign agents to crews
            for crew in ss.crews:
                for agent in crew.agents:
                    agent_assignment[agent.id].append(crew.name)

            # Display agents grouped by crew in tabs
            tabs = ["All Agents", "Unassigned Agents"] + [crew.name for crew in ss.crews]
            tab_objects = st.tabs(tabs)

            # ---- All Agents ----
            with tab_objects[0]:
                st.markdown("#### All Agents")
                for agent in ss.agents:
                    agent.draw()
                    if agent.edit:
                        editing = True
                st.button(
                    "➕ Create agent",
                    on_click=self.create_agent,
                    disabled=editing,
                    key="create_agent_all",
                )

            # ---- Unassigned Agents ----
            with tab_objects[1]:
                st.markdown("#### Unassigned Agents")
                unassigned_agents = [
                    agent for agent in ss.agents if not agent_assignment[agent.id]
                ]
                for agent in unassigned_agents:
                    unique_key = f"{agent.id}_unassigned"
                    agent.draw(key=unique_key)
                    if agent.edit:
                        editing = True
                st.button(
                    "➕ Create agent",
                    on_click=self.create_agent,
                    disabled=editing,
                    key="create_agent_unassigned",
                )

            # ---- Agents by Crew ----
            for i, crew in enumerate(ss.crews, 2):
                with tab_objects[i]:
                    st.markdown(f"#### {crew.name}")
                    for agent in crew.agents:
                        unique_key = f"{agent.id}_{crew.name}"
                        agent.draw(key=unique_key)
                        if agent.edit:
                            editing = True
                    st.button(
                        "➕ Create agent",
                        on_click=self.create_agent,
                        disabled=editing,
                        kwargs={"crew": crew},
                        key=f"create_agent_{crew.name}",
                    )

            if len(ss.agents) == 0:
                st.info("No agents defined yet.")
                st.button("➕ Create agent", on_click=self.create_agent, disabled=editing)


