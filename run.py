from src.contacts.entrypoints.app.application import create_app

app = create_app()

if __name__ == '__main__':
    app.run()