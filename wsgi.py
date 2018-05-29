from FoodBot import app, testing

print(testing)

app.run(debug=True,
        host="10.0.0.4",
        port=80,
        use_reloader=True,
        threaded=True)
