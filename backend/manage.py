from flask.cli import FlaskGroup
from casestudy.app import start_app

app = start_app()

cli = FlaskGroup(create_app=start_app)

if __name__ == '__main__':
    cli()
