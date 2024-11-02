from shiny import App, render, ui, reactive
import flag
from country_dict import countries
from exchange_rate import scrape_currency_conversion
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import plotly.express as px

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
        ui.output_plot("historic"),
    ),
)


def server(input, output, session):

    @output
    @render.plot
    # async def historic():

    #     # calculate the currency conversion
    #     output = await scrape_currency_conversion(all_countries.all[input.x()].curr,
    #                                               all_countries.all[input.y(
    #                                               )].curr,
    #                                               input.am())

    #     output = output.sort_values(by='Date')

    #     fig, ax = plt.subplots()
    #     ax.plot(output["Date"], output["Price"])
    #     ax.xaxis.set_major_locator(mdates.DayLocator(interval=2))
    #     plt.xticks(rotation=40)

    #     plt.xlabel('Date')
    #     plt.ylabel(all_countries.all[input.y(
    #     )].curr)

    #     return fig
    async def historic():
        # calculate the currency conversion
        output_data = await scrape_currency_conversion(all_countries.all[input.x()].curr,
                                                      all_countries.all[input.y()].curr,
                                                      input.am())

        output_data = output_data.sort_values(by='Date')

        fig = px.line(output_data, x="Date", y="Price", labels={'Price': all_countries.all[input.y()].curr})
        fig.update_layout(xaxis_title='Date', yaxis_title=all_countries.all[input.y()].curr)

        return fig

    # update the Your currency input options based on text
    @reactive.Effect
    @reactive.event(input.z)
    def _():
        filter_str = input.z()
        if filter_str == "":
            return
        filtered_input = {k: f"{flag.flag(v.code)} {v.name} {v.curr}" for (
            k, v) in all_countries.all.items() if filter_str.lower() in k.lower()}

        ui.update_select(
            "x",
            choices=filtered_input,
        )

    @reactive.Effect
    @reactive.event(input.m)
    def _():
        filter_str = input.m()
        if filter_str == "":
            return

        filtered_input = {k: f"{flag.flag(v.code)} {v.name} {v.curr}" for (
            k, v) in all_countries.all.items() if filter_str.lower() in k.lower()}

        ui.update_select(
            "y",
            choices=filtered_input,
        )

    @reactive.Effect
    @reactive.event(input.advice)
    async def _():
        output = await scrape_currency_conversion(all_countries.all[input.x()].curr,
                                                  all_countries.all[input.y(
                                                  )].curr,
                                                  input.am())
        std_div = output["Price"].std()

        out_mean = output["Price"].mean()

        current_price = output["Price"][output["Date"].idxmax()]

        if current_price > out_mean + std_div:
            m = ui.modal(
                "🟢 Conversion rates are above average, you will be receiving more resulting currency",
                title="Should you purchase?",
                easy_close=True,
                footer=(ui.modal_button("Close")),
            )
        elif current_price < out_mean - std_div:
            m = ui.modal(
                "🔴 Conversion rates are below average, you will be receiving less resulting currency",
                title="Should you purchase?",
                easy_close=True,
                footer=(ui.modal_button("Close")),
            )
        else:
            m = ui.modal(
                "🟡 Conversion rates are about average, you will be receiving average resulting currency",
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
