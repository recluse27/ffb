from FoodBot import app

app.run(debug=True,
        host="10.0.0.254",
        port=800,
        use_reloader=True,
        threaded=True)