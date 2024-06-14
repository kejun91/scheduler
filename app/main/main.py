from app.main.cli.parser import parse
from app.main.web.server import start_server


def execute(argv):
    is_web = False
    web_port = 8666
    argv_length = len(argv)
    if argv_length > 1:
        if argv_length > 2:
            if argv[1] == '-p' or argv[1] == '--port':
                try:
                    web_port = int(argv[2])
                    is_web = True
                except ValueError as ve:
                    print(f'{argv[2]} is not a valid port')
    else:
        is_web = True

    if is_web:
        start_server(web_port)
    else:
        parse(argv, argv_length)