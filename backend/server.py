from waitress import serve

from temat.wsgi import application


def main():
    serve(application, host="0.0.0.0", port="8000", threads=6)


if __name__ == "__main__":
    main()
