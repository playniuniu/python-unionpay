from app import create_app
import meinheld

app = create_app()

if __name__ == '__main__':
    meinheld.listen(("0.0.0.0", 5000))
    meinheld.run(app)