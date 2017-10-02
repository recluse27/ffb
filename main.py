from FoodBot import app

app.run(debug=True,
        host="10.0.0.4",
        port=443,
        use_reloader=True,
        threaded=True)