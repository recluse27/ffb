from FoodBot import app

app.run(debug=True,
        host="127.0.0.1",
        port=8000,
        use_reloader=True,
        threaded=True)
