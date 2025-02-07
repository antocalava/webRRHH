from flask import Flask
from flask_cors import CORS
from config.config import Config
from blueprints.access_blue_print import access_blue_print
from blueprints.home_office_blue_print import home_office_blue_print
from blueprints.travel_blue_print import travel_blue_print
from blueprints.festivity_blue_print import festivity_blue_print
from blueprints.hr_blue_print import hr_blue_print
from blueprints.user_blue_print import user_blue_print
from blueprints.holiday_blue_print import holiday_blue_print
from blueprints.home_page_blue_print import home_page_blue_print
import logging

""" 
import ssl
context = ssl.SSLContext()
context.load_cert_chain('fullchain.pem', 'privkey.pem')  """
#context=("cert.pem", "key.pem")

def update_blueprint(inc_app: Flask, blueprint_name, url_prefix_str, new_blueprint):
    inc_app.blueprints.pop(blueprint_name)
    rules_to_remove = [rule for rule in list(inc_app.url_map.iter_rules()) if rule.endpoint.startswith(blueprint_name)]
    for rule in rules_to_remove:
        # Remove the rule from the url_map
        inc_app.url_map._rules.remove(rule)
        inc_app.url_map._rules_by_endpoint[rule.endpoint].remove(rule)
        inc_app.view_functions.pop(rule.endpoint)
        
        # If there are no more rules under this endpoint, remove the endpoint as well
        if not inc_app.url_map._rules_by_endpoint[rule.endpoint]:
            del inc_app.url_map._rules_by_endpoint[rule.endpoint]
    inc_app.register_blueprint(new_blueprint, url_prefix=url_prefix_str)

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Register blueprints
    app.register_blueprint(access_blue_print, url_prefix='/access')
    app.register_blueprint(home_office_blue_print, url_prefix='/home-office')
    app.register_blueprint(travel_blue_print, url_prefix='/travel')
    app.register_blueprint(festivity_blue_print, url_prefix='/festivity')
    app.register_blueprint(hr_blue_print, url_prefix='/hr')
    app.register_blueprint(user_blue_print, url_prefix='/user')
    app.register_blueprint(holiday_blue_print, url_prefix='/holiday')
    app.register_blueprint(home_page_blue_print, url_prefix='/home')

    logging.basicConfig(level=logging.INFO)

    # Setup CORS
    CORS(app, resources={f"{app.config['API_PREFIX']}": {"origins": f"{app.config['FRONTEND_HOST']}"}})

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=8000, debug=True) #, ssl_context=context)
