from FoodBot import app

if __name__ == "main":
    app.run(debug=True,
            host="10.0.0.4",
            port=8080,
            use_reloader=True,
            threaded=True)