from FoodBot import app


def get_app():
    return app


if __name__ == "main":
    app.run(debug=True,
            host="127.0.0.1",
            port=8000,
            use_reloader=True,
            threaded=True)
