from promptmage.storage.data_store import DataStore

from nicegui import ui


def create_runs_view(data_store: DataStore):

    side_panel = ui.element("div").style(
        "position: fixed; top: 0; right: 0; width: 50%; height: 100%; background-color: #f0f0f0; transform: translateX(100%); transition: transform 0.3s ease; z-index: 1000"
    )

    # Function to show the side panel with detailed information
    def show_side_panel(run_data):
        side_panel.clear()
        with side_panel:
            with ui.card().style(
                "padding: 20px; margin-right: 20px; margin-top: 100px; margin-bottom: 20px; margin-left: 20px"
            ):
                ui.button("Hide", on_click=hide_side_panel)
                # display run data
                ui.label(f"Run ID: {run_data['run_id']}")
                ui.label(f"Step Name: {run_data['step_name']}")
                ui.label(f"Run Time: {run_data['run_time']}")
                ui.label(f"Prompt: {run_data['prompt']}")
                ui.label(f"Input Data: {run_data['input_data']}")
                ui.label(f"Output Data: {run_data['output_data']}")
        side_panel.style("transform:translateX(0%);")
        side_panel.update()

    # Function to hide the side panel
    def hide_side_panel():
        side_panel.clear()
        side_panel.style("transform:translateX(100%);")
        side_panel.update()

    def build_ui():
        ui.label("Runs").classes("text-2xl")
        runs = data_store.get_all_data()
        # Main UI setup
        with ui.card().style("padding: 20px"):
            # Create a table with clickable rows
            columns = [
                {"name": "run_id", "label": "run_id", "field": "run_id"},
                {"name": "name", "label": "name", "field": "name", "sortable": True},
                {
                    "name": "run_time",
                    "label": "run_time",
                    "field": "run_time",
                    "sortable": True,
                },
            ]

            rows = [
                {
                    "run_id": run_data["run_id"],
                    "name": run_data["step_name"],
                    "run_time": run_data["run_time"],
                }
                for _, run_data in runs.items()
            ]

            table = ui.table(columns=columns, rows=rows)

            def on_row_click(event):
                selected_run_index = event.args[-2]["run_id"]
                show_side_panel(run_data=runs[selected_run_index])

            table.on("rowClick", on_row_click)

        # with ui.column():
        #     ui.label("Runs")
        #     runs = data_store.get_all_data()
        #     for run_id, run_data in runs.items():
        #         with ui.card():
        #             with ui.expansion(
        #                 f"Run {run_id} of step \"{run_data['step_name']}\""
        #             ).classes("w-full"):
        #                 ui.label(f"Run time: {run_data['run_time']}")
        #                 ui.label(f"Prompt: {run_data['prompt']}")
        #                 ui.label(f"Input data: {run_data['input_data']}")
        #                 ui.label(f"Output data: {run_data['output_data']}")
        #             ui.update()

    return build_ui
