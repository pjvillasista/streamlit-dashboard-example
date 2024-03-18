import altair as alt
import plotly.express as px
import pandas as pd


# Heatmap
def make_heatmap(input_df, input_y, input_x, input_color, input_color_theme):
    heatmap = (
        alt.Chart(input_df)
        .mark_rect()
        .encode(
            y=alt.Y(
                f"{input_y}:O",
                axis=alt.Axis(
                    title="Year",
                    titleFontSize=18,
                    titlePadding=15,
                    titleFontWeight=900,
                    labelAngle=0,
                ),
            ),
            x=alt.X(
                f"{input_x}:O",
                axis=alt.Axis(
                    title="", titleFontSize=18, titlePadding=15, titleFontWeight=900
                ),
            ),
            color=alt.Color(
                f"max({input_color}):Q",
                legend=None,
                scale=alt.Scale(scheme=input_color_theme),
            ),
            stroke=alt.value("black"),
            strokeWidth=alt.value(0.25),
        )
        .properties(width=900)
        .configure_axis(labelFontSize=12, titleFontSize=12)
    )
    # height=300
    return heatmap


# Choropleth map
def make_choropleth(input_df, input_id, input_column, input_color_theme):
    # Calculate the range for the color scale based on the input column
    max_population = input_df[input_column].max()

    choropleth = px.choropleth(
        input_df,
        locations=input_id,  # This expects state codes in the DataFrame
        color=input_column,  # This is the column in input_df that dictates the color scale
        locationmode="USA-states",
        color_continuous_scale=input_color_theme,
        range_color=(0, max_population),  # Updated to use max_population
        scope="usa",
        labels={input_column: "Population"},  # Updated label to use input_column key
    )
    choropleth.update_layout(
        template="plotly_dark",
        plot_bgcolor="rgba(0, 0, 0, 0)",
        paper_bgcolor="rgba(0, 0, 0, 0)",
        margin=dict(l=0, r=0, t=0, b=0),
        height=350,
    )
    return choropleth


# Donut chart
def make_donut(input_response, input_text, input_color):
    if input_color == "blue":
        chart_color = ["#29b5e8", "#155F7A"]
    if input_color == "green":
        chart_color = ["#27AE60", "#12783D"]
    if input_color == "orange":
        chart_color = ["#F39C12", "#875A12"]
    if input_color == "red":
        chart_color = ["#E74C3C", "#781F16"]

    source = pd.DataFrame(
        {"Topic": ["", input_text], "% value": [100 - input_response, input_response]}
    )
    source_bg = pd.DataFrame({"Topic": ["", input_text], "% value": [100, 0]})

    plot = (
        alt.Chart(source)
        .mark_arc(innerRadius=45, cornerRadius=25)
        .encode(
            theta="% value",
            color=alt.Color(
                "Topic:N",
                scale=alt.Scale(
                    # domain=['A', 'B'],
                    domain=[input_text, ""],
                    # range=['#29b5e8', '#155F7A']),  # 31333F
                    range=chart_color,
                ),
                legend=None,
            ),
        )
        .properties(width=130, height=130)
    )

    text = plot.mark_text(
        align="center",
        color="#29b5e8",
        font="Lato",
        fontSize=32,
        fontWeight=700,
        fontStyle="italic",
    ).encode(text=alt.value(f"{input_response} %"))
    plot_bg = (
        alt.Chart(source_bg)
        .mark_arc(innerRadius=45, cornerRadius=20)
        .encode(
            theta="% value",
            color=alt.Color(
                "Topic:N",
                scale=alt.Scale(
                    # domain=['A', 'B'],
                    domain=[input_text, ""],
                    range=chart_color,
                ),  # 31333F
                legend=None,
            ),
        )
        .properties(width=130, height=130)
    )
    return plot_bg + plot + text
