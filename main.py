from FoodBot import app

app.run(debug=True,
        host="127.0.0.1", #""10.0.0.4",
        port=8000, #443,
        use_reloader=True,
        threaded=True)
