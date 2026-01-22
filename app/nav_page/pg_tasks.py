import streamlit as st
from streamlit import session_state as ss
from my_task import MyTask
import db_utils

class PageTasks:
    def __init__(self):
        self.name = "Tasks"

    def create_task(self, crew=None):
        task = MyTask()   
        if 'tasks' not in ss:
            ss.tasks = [MyTask]
        ss.tasks.append(task)
        task.edit = True                
        db_utils.save_task(task)  # Save task to database

        if crew:
            crew.tasks.append(task)
            db_utils.save_crew(crew)

        return task

    def draw(self):
        with st.container():
            st.markdown(
                """
                <div style="margin-bottom: 20px;">
                    <h1 style="font-size:48px; margin-bottom:6px;">📝 Tasks</h1>
                    <p style="font-size:18px; opacity:0.75;">
                        A task is a specific assignment completed by an agent within the CrewAI framework.
                        Tasks define what needs to be done, who is responsible, and what tools or context
                        are required for execution.
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
                    font-size: 18px;
                    margin-bottom: 24px;
                ">
                    <strong>Task collaboration</strong>
                    <p style="margin-top:6px; opacity:0.9;">
                        Tasks can be collaborative and may involve multiple agents working together.
                        Collaboration is orchestrated by the crew’s execution process, enabling
                        efficient teamwork and complex workflows.
                    </p>
                </div>
                """,
                unsafe_allow_html=True,
            )

            st.markdown("---")
            editing = False
            if 'tasks' not in ss:
                ss.tasks = db_utils.load_tasks()  # Load tasks from database
            if 'crews' not in ss:
                ss.crews = db_utils.load_crews()  # Load crews from database

            # Dictionary to track task assignment
            task_assignment = {task.id: [] for task in ss.tasks}

            # Assign tasks to crews
            for crew in ss.crews:
                for task in crew.tasks:
                    task_assignment[task.id].append(crew.name)

            # Display tasks grouped by crew in tabs
            tabs = ["All Tasks"] + ["Unassigned Tasks"] + [crew.name for crew in ss.crews]
            tab_objects = st.tabs(tabs)

            # Display all tasks
            with tab_objects[0]:
                st.markdown("#### All Tasks")
                for task in ss.tasks:
                    task.draw()
                    if task.edit:
                        editing = True
                st.button('Create task', on_click=self.create_task, disabled=editing, key="create_task_all")

            # Display unassigned tasks
            with tab_objects[1]:
                st.markdown("#### Unassigned Tasks")
                unassigned_tasks = [task for task in ss.tasks if not task_assignment[task.id]]
                for task in unassigned_tasks:
                    unique_key = f"{task.id}_unasigned"
                    task.draw(key=unique_key)
                    if task.edit:
                        editing = True
                st.button('Create task', on_click=self.create_task, disabled=editing, key="create_task_unassigned")

            # Display tasks grouped by crew
            for i, crew in enumerate(ss.crews, 2):
                with tab_objects[i]:
                    st.markdown(f"#### {crew.name}")
                    assigned_tasks = [task for task in crew.tasks]
                    for task in assigned_tasks:
                        unique_key = f"{task.id}_{crew.name}"
                        task.draw(key=unique_key)
                        if task.edit:
                            editing = True
                    st.button('Create task', on_click=self.create_task, disabled=editing,kwargs={'crew': crew}, key=f"create_task_{crew.name}")


            if len(ss.tasks) == 0:
                st.write("No tasks defined yet.")
                st.button('Create task', on_click=self.create_task, disabled=editing)

