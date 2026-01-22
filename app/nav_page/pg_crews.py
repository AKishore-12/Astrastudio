import streamlit as st
from streamlit import session_state as ss
from my_crew import MyCrew
import db_utils

class PageCrews:
    def __init__(self):
        self.name = "Crews"

    def create_crew(self):
        crew = MyCrew()
        if 'crews' not in ss:
            ss.crews = [MyCrew]
        ss.crews.append(crew)
        crew.edit = True
        db_utils.save_crew(crew)  # Save crew to database
        return crew

    def draw(self):
        with st.container():

            # ---- Page header ----
            st.markdown(
                """
                <div style="margin-bottom: 16px;">
                    <h1 style="margin-bottom: 4px; font-size:48px;">🧠 Crews</h1>
                    <p style="opacity: 0.75; font-size:18px;">
                        A crew represents a collaborative group of agents working together to achieve a set of tasks.
                        In CrewAI, a crew defines how agents collaborate, how tasks are executed, and how the overall
                        workflow is coordinated.
                    </p>
                </div>
                """,
                unsafe_allow_html=True,
            )

            st.markdown("---")

            # ---- Load crews ----
            editing = False
            if 'crews' not in ss:
                ss.crews = db_utils.load_crews()

            # ---- Render crews ----
            for crew in ss.crews:
                crew.draw()
                if crew.edit:
                    editing = True

            if len(ss.crews) == 0:
                st.info("No crews defined yet.")

            st.markdown("<br>", unsafe_allow_html=True)

            # ---- Create crew action ----
            st.button(
                "➕ Create crew",
                on_click=self.create_crew,
                disabled=editing,
                use_container_width=False,
            )
