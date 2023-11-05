from shiny import App, render, ui, reactive, Inputs, Outputs, Session
import flag
from country_dict import countries
from exchange_rate import scrape_currency_conversion
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from forex_python.converter import CurrencyCodes

c = CurrencyCodes()

all_countries = countries()

default_choices = {
    k: f"{flag.flag(v.code)} {v.name} {v.curr}"
    for (k, v) in all_countries.all.items()
    if "" in k
}


app_ui = ui.page_sidebar(
    ui.sidebar(
        ui.div(
            {"style": "font-weight: bold; margin-left: 2px;"},
            ui.input_numeric("am", "Amount", 1, min=0),
        ),
        ui.div(
            {"style": "font-weight: bold; margin-left: 2px;"},
            ui.input_text("z", "Filter", placeholder="Country Name"),
            ui.input_select(
                "x", "Your Currency", default_choices, selected="United States"
            ),
        ),
        ui.div(
            {"style": "font-weight: bold; margin-left: 2px;"},
            ui.input_text("m", "Filter", placeholder="Country Name"),
            ui.input_select("y", "Convert to", default_choices, selected="Vietnam"),
        ),
    ),
    ui.card(
<<<<<<< HEAD
        ui.div(
            {"style": "text-align: center; background-color:#458f69; color:#FFFFFF"},
            ui.markdown("# Current¢"),
        ),
        ui.column(
            12,
            ui.div(
                {"style": "text-align:center"},
                ui.input_action_button("advice", "Advice"),
                ui.input_action_button("alert", "Alert Me"),
            ),
        ),
        ui.output_text_verbatim("txt"),
    ),
=======
        ui.div({"style": "text-align: center; background-color:#458f69; color:#FFFFFF"},
               ui.markdown("# Current¢")),
        ui.output_plot("historic")
    )

>>>>>>> 433eaf2698d52641e7db625e8943474875342838
)


def server(input, output, session):

    @output
    @render.plot
    async def historic():

        # calculate the currency conversion
<<<<<<< HEAD
        output = await scrape_currency_conversion(
            all_countries.all[input.x()].curr,
            all_countries.all[input.y()].curr,
            input.am(),
        )
        return f'x: "{output}"'
=======
        output = await scrape_currency_conversion(all_countries.all[input.x()].curr,
                                                  all_countries.all[input.y(
                                                  )].curr,
                                                  input.am())

        output = output.sort_values(by='Date')

        fig, ax = plt.subplots()
        ax.plot(output["Date"], output["Price"])
        ax.xaxis.set_major_locator(mdates.DayLocator(interval=2))
        plt.xticks(rotation=40)

        plt.xlabel('Date')
        plt.ylabel(c.get_symbol(all_countries.all[input.y(
        )].curr))  # NEED TO ADD CURRENCY SYMBOL

        plt.tight_layout()
        plt.show()
        return fig
>>>>>>> 433eaf2698d52641e7db625e8943474875342838

    # update the Your currency input options based on text
    @reactive.Effect
    @reactive.event(input.z)
    def _():
        filter_str = input.z()
<<<<<<< HEAD
        filtered_input = {
            k: f"{flag.flag(v.code)} {v.name} {v.curr}"
            for (k, v) in all_countries.all.items()
            if filter_str.lower() in k.lower()
        }
=======
        if filter_str == "":
            return
        filtered_input = {k: f"{flag.flag(v.code)} {v.name} {v.curr}" for (
            k, v) in all_countries.all.items() if filter_str.lower() in k.lower()}
>>>>>>> 433eaf2698d52641e7db625e8943474875342838

        ui.update_select(
            "x",
            choices=filtered_input,
        )

    @reactive.Effect
    @reactive.event(input.m)
    def _():
        filter_str = input.m()
<<<<<<< HEAD
        filtered_input = {
            k: f"{flag.flag(v.code)} {v.name} {v.curr}"
            for (k, v) in all_countries.all.items()
            if filter_str.lower() in k.lower()
        }
=======
        if filter_str == "":
            return

        filtered_input = {k: f"{flag.flag(v.code)} {v.name} {v.curr}" for (
            k, v) in all_countries.all.items() if filter_str.lower() in k.lower()}
>>>>>>> 433eaf2698d52641e7db625e8943474875342838

        ui.update_select(
            "y",
            choices=filtered_input,
        )

    @reactive.Effect
    @reactive.event(input.advice)
    def _():
        m = ui.modal(
            "Right now is a BAD TIME to buy.",
            title="Should you purchase?",
            easy_close=True,
            footer=(ui.modal_button("Close")),
        )
        ui.modal_show(m)

    @reactive.Effect
    @reactive.event(input.alert)
    def _():
        m = ui.modal(
            ui.input_text("number", "Phone Number"),
            title="Enter your phone number for text alerts: ",
            easy_close=True,
            footer=(ui.modal_button("Submit"), ui.modal_button("Close")),
        )
        ui.modal_show(m)


app = App(app_ui, server, debug=True)