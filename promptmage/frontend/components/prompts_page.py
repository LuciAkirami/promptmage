from nicegui import ui
from collections import defaultdict
from typing import List

from promptmage.storage.prompt_store import PromptStore
from promptmage.prompt import Prompt


def create_prompts_view(prompt_store: PromptStore):
    side_panel = ui.element("div").style(
        "position: fixed; top: 0; right: 0; width: 50%; height: 100%; background-color: #f0f0f0; transform: translateX(100%); transition: transform 0.3s ease; z-index: 1000; overflow-y: auto;"
    )

    # Function to show the side panel with detailed information
    def show_side_panel(prompts: List[Prompt]):
        # get prompt with highest version
        side_panel.clear()
        with side_panel:
            ui.button(">>", on_click=hide_side_panel).style(
                "margin: 20px; margin-bottom: 0px; margin-top: 100px;"
            )
            for prompt in sorted(prompts, key=lambda p: p.version, reverse=True):
                with ui.card().style(
                    "padding: 20px; margin-right: 20px; margin-top: 10px; margin-bottom: 10px; margin-left: 20px"
                ):
                    # display run data
                    ui.label(f"Prompt ID: {prompt.id}")
                    ui.label(f"Name: {prompt.name}")
                    ui.label(f"Version: {prompt.version}")
                    ui.label(f"System prompt: {prompt.system}")
                    ui.label(f"User prompt: {prompt.user}")
                    with ui.row():
                        ui.button(
                            "Use Prompt",
                            on_click=lambda prompt_id=prompt.id: prompt_store.use_prompt(
                                prompt_id
                            ),
                        )
                        ui.button(
                            "Edit Prompt",
                            on_click=lambda prompt_id=prompt.id: prompt_store.edit_prompt(
                                prompt_id
                            ),
                        )
                        ui.button(
                            "Delete Prompt",
                            on_click=lambda prompt_id=prompt.id: delete_prompt(
                                prompt_id
                            ),
                        )
        side_panel.style("transform:translateX(0%);")
        side_panel.update()

    def delete_prompt(prompt_id):
        prompt_store.delete_prompt(prompt_id)

    # Function to hide the side panel
    def hide_side_panel():
        side_panel.clear()
        side_panel.style("transform:translateX(100%);")
        side_panel.update()

    def build_ui():
        ui.label("Prompts").classes("text-2xl")
        all_prompts = prompt_store.get_prompts()
        # group them by name
        prompts = defaultdict(list)
        for prompt in all_prompts:
            prompts[prompt.name].append(prompt)

        # Main UI setup
        with ui.card().style("padding: 20px"):
            # Create a table with clickable rows
            columns = [
                {"name": "name", "label": "name", "field": "name", "sortable": True},
                {
                    "name": "versions",
                    "label": "Number of versions",
                    "field": "versions",
                    "sortable": True,
                },
            ]

            rows = [
                {
                    "name": name,
                    "versions": len(prompts_for_name),
                }
                for name, prompts_for_name in prompts.items()
            ]

            table = ui.table(columns=columns, rows=rows)

            def on_row_click(event):
                selected_run_index = event.args[-2]["name"]
                show_side_panel(prompts=prompts[selected_run_index])

            table.on("rowClick", on_row_click)

    return build_ui
