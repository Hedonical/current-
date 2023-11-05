from shiny import App, render, ui, reactive
import flag
from country_dict import countries

all_countries = countries()

default_choices = {k: f"{flag.flag(v.code)} {v.name} {v.curr}" for (k,v) in all_countries.all.items() if "" in k}


app_ui = ui.page_fluid(
        ui.div({"style": "text-align: center;"},
               ui.markdown("# Current¢")),
        ui.div( {"style": "font-weight: bold; margin-left: 2px;"},
        ui.input_text("z", "Filter", placeholder="Country Name"),
        ui.input_select("x", "Your Currency", default_choices)),
        ui.div( {"style": "font-weight: bold; margin-left: 2px;"},
        ui.input_text("m", "Filter", placeholder="Country Name"),
        ui.input_select("y", "Convert to", default_choices)),
        ui.output_text_verbatim("txt")
)


def server(input, output, session):
    @output
    @render.text
    def txt():
        return f'x: "{input.x()}"'
    
    # update the Your currency input options based on text
    @reactive.Effect
    def _():
        filter_str = input.z()
        filtered_input = {k: f"{flag.flag(v.code)} {v.name} {v.curr}" for (k,v) in all_countries.all.items() if filter_str.lower() in k.lower()}

        ui.update_select(
            "x",
            choices=filtered_input,
        )
        
    @reactive.Effect
    def _():
        
        filter_str = input.m()
        filtered_input = {k: f"{flag.flag(v.code)} {v.name} {v.curr}" for (k,v) in all_countries.all.items() if filter_str.lower() in k.lower()}

        ui.update_select(
            "y",
            choices=filtered_input,
        )







app = App(app_ui, server, debug=True)
