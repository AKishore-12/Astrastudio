import streamlit as st
from streamlit import session_state as ss
from my_knowledge_source import MyKnowledgeSource
import db_utils
import os
import shutil
from pathlib import Path

class PageKnowledge:
    def __init__(self):
        self.name = "Knowledge"

    def create_knowledge_source(self):
        knowledge_source = MyKnowledgeSource()
        if 'knowledge_sources' not in ss:
            ss.knowledge_sources = []
        ss.knowledge_sources.append(knowledge_source)
        knowledge_source.edit = True
        db_utils.save_knowledge_source(knowledge_source)
        return knowledge_source

    def clear_knowledge(self):
        # This will clear knowledge stores in CrewAI
        # Get CrewAI home directory
        home_dir = Path.home()
        crewai_dir = home_dir / ".crewai"
        
        # Remove knowledge folder
        knowledge_dir = crewai_dir / "knowledge"
        if knowledge_dir.exists():
            shutil.rmtree(knowledge_dir)
            st.success("Knowledge stores cleared successfully!")
        else:
            st.info("No knowledge stores found to clear.")

    def draw(self):
        st.markdown(
            """
            <div style="margin-bottom: 20px;">
                <h1 style="font-size:48px; margin-bottom:6px;">📚 Knowledge</h1>
                <p style="font-size:18px; opacity:0.75;">
                    Knowledge allows agents to access and use external information sources during
                    their tasks. It acts as a reference library that agents can consult while working,
                    helping them make informed and grounded decisions.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # ---- Documentation summary ----
        st.markdown(
            """
            <div style="
                border-radius: 12px;
                padding: 14px 16px;
                border: 1px solid rgba(255,255,255,0.08);
                background: rgba(255,255,255,0.02);
                max-width: 500px;
                margin-bottom: 24px;
                font-size: 18px;
            ">
                <strong>Why use Knowledge?</strong>
                <ul style="margin-top:8px; padding-left:18px; opacity:0.9;">
                    <li>Enhance agents with domain-specific information</li>
                    <li>Support decisions with real-world data</li>
                    <li>Maintain context across conversations</li>
                    <li>Ground responses in factual information</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("---")
        
        # Create knowledge directory if it doesn't exist
        os.makedirs("knowledge", exist_ok=True)
        
        
        # Display existing knowledge sources
        editing = False
        if 'knowledge_sources' not in ss:
            ss.knowledge_sources = db_utils.load_knowledge_sources()
            
        for knowledge_source in ss.knowledge_sources:
            knowledge_source.draw()
            if knowledge_source.edit:
                editing = True
                
        if len(ss.knowledge_sources) == 0:
            st.write("No knowledge sources defined yet.")
            
        st.button('Create Knowledge Source', on_click=self.create_knowledge_source, disabled=editing)

        # Clear knowledge button
        st.button("Clear All Knowledge Stores", on_click=self.clear_knowledge, 
                  help="This will clear all knowledge stores in CrewAI, removing cached embeddings")