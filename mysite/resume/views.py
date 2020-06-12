import datetime
import folium
import json
import pandas as pd

from bokeh.embed import components
from bokeh.plotting import figure
from django.views import generic

from .models import Post, ProfileCard
from .forms import CountryForm


class PostList(generic.ListView):
    queryset = Post.objects.filter(status=1).order_by('-created_on')
    template_name = 'index.html'


class PostDetail(generic.DetailView):
    model = Post
    template_name = 'post_detail.html'


class Gallery(generic.TemplateView):
    template_name = 'gallery_home.html'


class Projects(generic.TemplateView):
    template_name = 'projects.html'


# Static Visualization Views
class CovidTimeSeries(generic.TemplateView):
    template_name = 'covid_bokeh.html'


class NotebooksHome(generic.TemplateView):
    template_name = 'notebooks_home.html'


class ProjectEuler11(generic.TemplateView):
    template_name = 'euler_11.html'

class ProjectEuler14(generic.TemplateView):
    template_name = 'euler_14.html'

class ComingSoonView(generic.TemplateView):
    template_name = "coming_soon.html"


# Dynamic Visualization Views
class CovidBokehView(generic.TemplateView):
    template_name = 'bokeh.html'
    form_class = CountryForm
    initial = {'input_country_1': 'United States', 'input_country_2': 'United Kingdom'}

    def form_valid(self, form):
        form.return_choices()

    def _create_bokeh_charts(self, df_grouped, dfc1, dfc2, country1, country2):
        new_cases_per_mill = df_grouped.new_cases_per_million
        avg, std = new_cases_per_mill.mean(), new_cases_per_mill.std()
        month_year = list(df_grouped.groups)

        p = figure(title=f"New Cases Per Million - OWID Data - {country1} vs {country2}",
                   x_axis_type='datetime')
        p.vbar(x=month_year, bottom=avg - std, top=avg + std, width=0.8,
               fill_alpha=0.2, line_color=None, legend_label="New Cases Per Million (1 StdDev)")
        p.circle(x=dfc1["date"], y=dfc1["new_cases_per_million"], size=10, alpha=0.5,
                 color="red", legend_label=f"{country1}")
        p.triangle(x=dfc2["date"], y=dfc2["new_cases_per_million"], size=10, alpha=0.3,
                   color="blue", legend_label=f"{country2}")
        p.legend.location = "top_left"

        script, div = components(p)

        return {'script':script, 'div': div}

    def get_context_data(self, **kwargs):

        # read our world in data covid data set
        df = pd.read_csv("../assets/resume/data/owid-covid-data.csv")
        df['date'] = df.date.map(lambda x: pd.to_datetime(x))
        df['month'] = df.date.map(lambda x: pd.to_datetime(x).month)
        df['year'] = df.date.map(lambda x: pd.to_datetime(x).year)
        df['month_year'] = df.date.map(lambda x: (x.month, x.year))

        country1 = ['United States']
        countries_compare_against = df.sort_values('total_deaths', ascending=False).location.unique()[2:10]
        country_comparisons = list(
            zip(['United States' for _ in range(len(countries_compare_against))], countries_compare_against))
        df.sort_values(['year', 'month', 'location'], inplace=True)
        html_figures = []
        df_grouped = df.groupby(['date'])
        for c1, c2 in country_comparisons:
            dfc1 = df[df.location == c1]
            dfc2 = df[df.location == c2]
            request = self._create_bokeh_charts(df_grouped, dfc1, dfc2, c1, c2)
            return request


class CovidFoliumView(generic.TemplateView):
    template_name = "folium.html"

    def get_context_data(self, **kwargs):
        figure = folium.Figure()

        m = folium.Map(location=[32.8304, -96.9238])
        m.add_to(figure)
        m.add_child(folium.LatLngPopup())

        # track timestamp for when data is pulled
        timestamp_ = datetime.datetime.now()
        timestamp_str = timestamp_.strftime(format="%m/%d/%y @ %H:%M UTC")
        print(f'Data pulled at {timestamp_str}')

        # read from url
        covid = pd.read_csv("https://coronadatascraper.com/data.csv", encoding='utf8')
        texas_covid_df = covid[(covid.country == 'United States') & (covid.state == 'Texas')]
        texas_covid_df = texas_covid_df[['cases', 'deaths', 'name', 'lat', 'long', 'url']]
        texas_covid_df = texas_covid_df[texas_covid_df.name != 'Texas, United States']
        texas_covid_df = texas_covid_df.sort_values(['cases', 'deaths'], ascending=False)
        texas_covid_df = texas_covid_df[texas_covid_df.cases > 100]

        # add markers to folium map
        for val in texas_covid_df.to_dict(orient='record'):
            # simple tooltip template for icon
            tooltip = f"""\
            <b>{val['name']} - Over 100 Cases Today</b>
            """

            # simple markdown templates for pop ups
            style = """\
            <style>
                table, th, td {
                  border: 1px solid black;
                  padding: 2px;
                }
            </style>"""

            popup = f"""\ 
            <table style="width:100%">
                <h3><b>{val['name']}</b></h3>
                <h5>At {timestamp_str}</h5>
                <h5>From https://coronadatascraper.com/ </h5>
              <tr>
                <th>Cases</th>
                <th>Deaths</th>
                <th>Data Source</th>
              </tr>
              <tr>
                <td>{val['cases']}</td>
                <td>{val['deaths']}</td>
                <td>{val['url']}</td>
              </tr>
            </table>
            """

            folium.Marker(
                [val['lat'], val['long']],
                popup=style + popup,
                tooltip=tooltip, ).add_to(m)

        figure.render()

        return {"map": figure}


class ProfileList(generic.ListView):
    """
    Class to define returning a list of profiles for our website
    Note:
        Django offers function based views (FBV) and class based views (CBV)
    """
    model = ProfileCard
    context_object_name = 'developers'   # your own name for the list as a template variable
    queryset = ProfileCard.objects.all()
    template_name = 'about.html'