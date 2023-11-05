from shiny import App, render, ui, reactive
import flag
from country_dict import countries
from exchange_rate import scrape_currency_conversion

all_countries = countries()

default_choices = {k: f"{flag.flag(v.code)} {v.name} {v.curr}" for (
    k, v) in all_countries.all.items() if "" in k}


app_ui = ui.page_sidebar(
    ui.sidebar(
        ui.div({"style": "font-weight: bold; margin-left: 2px;"},
               ui.input_numeric("am", "Amount", 1, min=0)),
        ui.div({"style": "font-weight: bold; margin-left: 2px;"},
               ui.input_text("z", "Filter", placeholder="Country Name"),
               ui.input_select("x", "Your Currency", default_choices, selected="United States")),
        ui.div({"style": "font-weight: bold; margin-left: 2px;"},
               ui.input_text("m", "Filter", placeholder="Country Name"),
               ui.input_select("y", "Convert to", default_choices, selected="Vietnam"))),
    ui.card(
        ui.div({"style": "text-align: center;"},
               ui.markdown("# Current¢")),
        ui.output_text_verbatim("txt")
    )

)


def server(input, output, session):
    @output
    @render.text
    async def txt():
        # calculate the currency conversion
        output = await scrape_currency_conversion(all_countries.all[input.x()].curr,
                                                  all_countries.all[input.y(
                                                  )].curr,
                                                  input.am())
        return f'x: "{output}"'

    # update the Your currency input options based on text
    @reactive.Calc
    def _():
        filter_str = input.z()
        filtered_input = {k: f"{flag.flag(v.code)} {v.name} {v.curr}" for (
            k, v) in all_countries.all.items() if filter_str.lower() in k.lower()}

        ui.update_select(
            "x",
            choices=filtered_input,
        )

    @reactive.Calc
    def _():

        filter_str = input.m()
        filtered_input = {k: f"{flag.flag(v.code)} {v.name} {v.curr}" for (
            k, v) in all_countries.all.items() if filter_str.lower() in k.lower()}

        ui.update_select(
            "y",
            choices=filtered_input,
        )


app = App(app_ui, server, debug=True)
