import plotly.express as px


def bar_chart(df, x, y, title):

    fig = px.bar(
        df,
        x=x,
        y=y,
        title=title,
        text_auto=True
    )

    fig.update_layout(
        template="plotly_white",
        height=400,
        title_x=0.5
    )

    return fig


def pie_chart(df, names, values, title):

    fig = px.pie(
        df,
        names=names,
        values=values,
        hole=0.5,
        title=title
    )

    fig.update_layout(
        height=400,
        title_x=0.5
    )

    return fig