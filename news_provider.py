from flask import Flask
from flask_restful import Resource, Api
from flasgger import Swagger, LazyJSONEncoder
from webargs import fields
from webargs.flaskparser import use_args
from newsapi import NewsApiClient

app = Flask(__name__)
api = Api(app)
app.json_encoder = LazyJSONEncoder

swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": '/',
            "route": '/news_provider_schema.json',
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/apidocs/"
}

app.config['SWAGGER'] = {
    "openapi": "3.0.2"
}

swagger = Swagger(app, template_file="news_provider_schema.json", config=swagger_config)


class News(Resource):
    # add you api key before using
    # '''https://newsapi.org/v2/everything?q={}&sortBy=publishedAt&apiKey='''

    @use_args(
        {
            'term': fields.Str(required=False, missing='Python'),
            'page': fields.Int(required=False, missing=1)
        },
        location='querystring'
    )
    def get(self, args):
        if args['term'] == '_exit':
            exit()
        return self._get_news(search_term=args['term'], page=args['page'])

    @staticmethod
    def _get_news(search_term='nasa', page=1, page_size=10):
        # add you api key before using
        newsapi = NewsApiClient(api_key='')
        news = newsapi.get_everything(q=search_term,
                                      language='en',
                                      page=page,
                                      page_size=page_size)
        return news.get('articles') if news.get('totalResults') > 0 else []


api.add_resource(News, '/news')

if __name__ == '__main__':
    app.run(host='localhost', port=5008, debug=True)
