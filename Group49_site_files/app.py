from flask import Flask, render_template, json, request, redirect, url_for
import os
import database.db_connector as db
import database.db_credentials as crd

# Configuration

app = Flask(__name__)
db_connection = db.connect_to_database(crd.host, crd.user, crd.passwd, crd.db)

# Routes 

@app.route('/')
def reroute():
    return redirect(url_for('root'))

@app.route('/index')
def root():
    return render_template("main.j2")

@app.route('/games')
def games():
    query = "SELECT title, player_count, rating, online, publisher, genre, game_id FROM Games;"
    results = db.execute_query(db_connection=db_connection, query=query).fetchall()
    q2 = "SELECT item_ID, game_ID, title, name, quantity, (quantity - SUM(CASE WHEN paid = '0000-00-00' THEN '1' ELSE '0' END)) as available " \
         "FROM Console_Versions INNER JOIN Consoles ON console = console_ID INNER JOIN Games ON game = game_ID LEFT JOIN Game_Rentals " \
         "ON item_ID = game_version LEFT JOIN Rentals ON rental = rental_ID GROUP BY item_ID"
    r2 = db.execute_query(db_connection=db_connection, query=q2).fetchall()
    dropdown = "SELECT name, console_id FROM Consoles;"
    dd_results = db.execute_query(db_connection=db_connection, query=dropdown).fetchall()
    people = "SELECT first_name, last_name FROM Customers;"
    ppl_r = db.execute_query(db_connection=db_connection, query=people).fetchall()
    genres = ['2D Platformer', '3D Platformer', 'Action-Adventure', 'Action RPG', 'Arcade',
              'Battle Royale', 'Fighting', 'First-Person Shooter', 'Fitness', 'Japanese RPG', 'MOBA/MMORPG',
              'Open World', 'Party', 'Puzzle', 'Racing', 'Sports', 'Strategy', 'Survival Horror',
              'Third-Person Shooter', 'Visual Novel']
    return render_template("games.j2", games=results, versions=r2, dropdown=dd_results, genres=genres, people=ppl_r)

@app.route('/add_game', methods=["POST", "GET"])
def add_game():

    if request.method == "GET":
        return redirect(url_for('games'))
    
    elif request.method == "POST":
        print("Adding new game")
        # pull out the title from the form to check if the game has already been added
        title = request.form['title']

        # make sure the game isn't in the list first
        query = "SELECT title FROM Games WHERE title = '" + title + "';"
        check = db.execute_query(db_connection, query).fetchall();

        # in SQL/Flask, if a SELECT is returned with no values, fetchall returns () (not '' or None)
        if check == ():
            players = request.form['players']
            print(players)
            if players == "":
                players = 1
            rating = request.form['rating']
            if rating == "Choose...":
                rating = "?"
            online = request.form['online']
            if online == "Choose..." or online == "No":
                online = 0
            elif online == "Yes":
                online = 1
            publisher = request.form['publisher']
            if publisher == "":
                publisher = "Unknown"
            genre = request.form['genre']
            if genre == "Choose...":
                genre = "Unknown"
            query = "INSERT INTO Games (title, player_count, rating, online, publisher, genre) VALUES (%s,%s,%s,%s,%s,%s);"
            data = (title, players, rating, online, publisher, genre)

            db.execute_query(db_connection, query, data)

        return redirect(url_for('games'))

@app.route('/add_version', methods=["POST", "GET"])
def add_version():
    if request.method == "GET":
        return redirect(url_for('games'))

    elif request.method == "POST":
        game = request.form['cv_title']
        console = request.form['cv_name']
        quantity = request.form['quantity']
        gid = 'SELECT game_ID FROM Games WHERE title = "%s"' % (game)
        rg = db.execute_query(db_connection=db_connection,query=gid).fetchone()
        print(rg)
        cid = 'SELECT console_ID FROM Consoles WHERE name = "%s"' % (console)
        rc = db.execute_query(db_connection=db_connection,query=cid).fetchone()
        print(rc)
        query = 'INSERT INTO Console_Versions (game, console, quantity) VALUES (%s, %s, %s);'
        data = (rg['game_ID'], rc['console_ID'], quantity)
        db.execute_query(db_connection,query,data)
        return redirect(url_for('games'))


@app.route('/filter_games', methods=["POST", "GET"])
def filter_games():
    query = 'SELECT game_id, title, player_count, rating, publisher, genre FROM Games LEFT JOIN Console_Versions ON ' \
            'game_ID = game LEFT JOIN Consoles ON console = console_ID '
    renter = request.form['frent']
    if renter != "Choose...":
        query += 'INNER JOIN Game_Rentals ON item_ID = game_version INNER JOIN Rentals ON rental = rental_ID INNER JOIN Customers ON customer = customer_ID WHERE'
    else:
        query += 'WHERE'
    game = request.form['ftitle']
    players = request.form['fplayers']
    rating = request.form['frating']
    online = request.form['fonline']
    pub = request.form['fpub']
    genre = request.form['fgenre']
    console = request.form['fcon']
    where = []
    if game != '':
        where.append(' title LIKE "%%' + game + '%%"')
    if players != 'Choose...':
        if players == 'Single-Player':
            where.append(' player_count = "1"')
        else:
            where.append(' player_count > "1"')
    if rating != 'Choose...':
        where.append(' rating = "' + rating +'"')
    if online != 'Choose...':
        if online == "Yes":
            where.append(' online = "1"')
        else:
            where.append(' online = "0"')
    if pub != 'Choose...':
        where.append(' publisher = "' + pub + '"')
    if genre != 'Choose...':
        where.append(' genre = "' + genre + '"')
    if console != 'Choose...':
        where.append(' name = "' + console + '"')
    if renter != 'Choose...':
        first, last = renter.split(' ', 1)
        where.append(' first_name = "' + first + '" AND last_name = "' + last + '"')
    if len(where) == 0:
        return redirect(url_for('games'))
    constraints = ''
    for i in range(len(where)):
        if i == 0:
            constraints += where[i]
        else:
            constraints += ' AND' + where[i]
    constraints += ' GROUP BY game_id;'
    print(constraints)
    query += constraints
    print(query)
    cursor = db.execute_query(db_connection=db_connection, query=query)
    results = cursor.fetchall()
    q2 = "SELECT item_ID, game_ID, title, name, quantity, (quantity - SUM(CASE WHEN paid = '0000-00-00' THEN '1' ELSE '0' END)) as available " \
         "FROM Console_Versions INNER JOIN Consoles ON console = console_ID INNER JOIN Games ON game = game_ID LEFT JOIN Game_Rentals " \
         "ON item_ID = game_version LEFT JOIN Rentals ON rental = rental_ID GROUP BY item_ID"
    r2 = db.execute_query(db_connection=db_connection, query=q2).fetchall()
    dropdown = "SELECT name, console_id FROM Consoles;"
    dd_results = db.execute_query(db_connection=db_connection, query=dropdown).fetchall()
    people = "SELECT first_name, last_name FROM Customers;"
    ppl_r = db.execute_query(db_connection=db_connection, query=people).fetchall()
    genres = ['2D Platformer', '3D Platformer', 'Action-Adventure', 'Action RPG', 'Arcade',
              'Battle Royale', 'Fighting', 'First-Person Shooter', 'Fitness', 'Japanese RPG', 'MOBA/MMORPG',
              'Open World', 'Party', 'Puzzle', 'Racing', 'Sports', 'Strategy', 'Survival Horror',
              'Third-Person Shooter', 'Visual Novel']
    return render_template("games.j2", games=results, versions=r2, dropdown=dd_results, genres=genres, people=ppl_r)

@app.route('/delete_game/<int:g_id>')
def delete_game(g_id):
    query = "DELETE FROM Games WHERE game_ID = %s"
    data = (g_id,)

    result = db.execute_query(db_connection, query, data)
    print("Row " + str(result.rowcount) + " deleted")
    return redirect(url_for('games'))

@app.route('/update_game/<int:g_id>', methods=['POST','GET'])
def update_game(g_id):
    if request.method == 'GET':
        g_query = 'SELECT * FROM Games WHERE game_id = %s' % (g_id)
        g_r = db.execute_query(db_connection=db_connection,query=g_query).fetchone()
        genres = ['2D Platformer', '3D Platformer', 'Action-Adventure', 'Action RPG', 'Arcade',
                  'Battle Royale', 'Fighting', 'First-Person Shooter', 'Fitness', 'Japanese RPG', 'MOBA/MMORPG',
                  'Open World', 'Party', 'Puzzle', 'Racing', 'Sports', 'Strategy', 'Survival Horror',
                  'Third-Person Shooter', 'Visual Novel']
        print(g_r)
        if g_r == None:
            return "No such game exists!"
        return render_template('update_game.j2', update=g_r, genres=genres)
    elif request.method == 'POST':
        print("Updated game!")
        game = g_id
        print(game)
        title = request.form['title']
        print(title)
        players = request.form['players']
        print(players)
        publisher = request.form['publisher']
        print(publisher)
        rating = request.form['rating']
        print(rating)
        if rating == "Choose...":
            rating = "TBD"
        online = 'online' in request.form
        print(online)
        genre = request.form['genre']
        print(genre)
        if genre == "Choose...":
            genre = "Unknown"
        print(request.form);
        query = 'UPDATE Games SET title = %s, player_count = %s, rating = %s, online = %s, publisher = %s, genre = %s WHERE game_id = %s'
        data = (title, players, rating, online, publisher, genre, game)
        db.execute_query(db_connection, query, data)
        return redirect(url_for('games'))

@app.route('/update_version/<int:cv_id>', methods=['POST','GET'])
def update_version(cv_id):
    if request.method == 'GET':
        cv_query = 'SELECT item_id, title, name, quantity FROM Games INNER JOIN Console_Versions ON game_id = game INNER ' \
                  'JOIN Consoles ON console = console_id WHERE item_id = %s' % (cv_id)
        cv_r = db.execute_query(db_connection=db_connection,query=cv_query).fetchone()
        gq = 'SELECT title FROM Games;'
        g_r = db.execute_query(db_connection=db_connection,query=gq).fetchall()
        cq = 'SELECT name FROM Consoles;'
        c_r = db.execute_query(db_connection=db_connection,query=cq).fetchall()
        print(cv_r)
        if cv_r == None:
            return "No such version exists!"
        return render_template('update_version.j2', update=cv_r, games=g_r,consoles=c_r)
    elif request.method == 'POST':
        print("Updated console version!")
        title = request.form['game']
        print(title)
        console = request.form['console']
        print(players)
        quantity = request.form['quantity']
        print(publisher)
        if quantity == 0:
            query = 'DELETE FROM Console_Versions WHERE item_ID = %s' % (cv_id)
            db.execute_query(db_connection, query)
            return redirect(url_for('games'))
        print(request.form)
        gid = 'SELECT game_ID FROM Games WHERE title = "%s"' % (title)
        rg = db.execute_query(db_connection=db_connection,query=gid).fetchone()
        cid = 'SELECT console_ID FROM Consoles WHERE name = "%s"' % (console)
        rc = db.execute_query(db_connection=db_connection,query=cid).fetchone()
        query = 'UPDATE Console_Versions SET game = %s, console = %s, quantity = %s WHERE item_ID = %s'
        data = (rg['game_ID'], rc['console_ID'], quantity)
        db.execute_query(db_connection, query, data)
        return redirect(url_for('games'))


@app.route('/consoles')
def consoles():
    query = "SELECT name, company, portable, vr, backwards_comp, max_resolution, console_id FROM Consoles;"
    cursor = db.execute_query(db_connection=db_connection, query=query)
    results = cursor.fetchall()
    q2 = "SELECT item_ID, console_id, title, name, quantity, (quantity - SUM(CASE WHEN paid = '0000-00-00' THEN '1' ELSE '0' END)) as available " \
         "FROM Console_Versions INNER JOIN Consoles ON console = console_ID INNER JOIN Games ON game = game_ID LEFT JOIN Game_Rentals " \
         "ON item_ID = game_version LEFT JOIN Rentals ON rental = rental_ID GROUP BY item_ID"
    c2 = db.execute_query(db_connection=db_connection, query=q2)
    r2 = c2.fetchall()
    return render_template("consoles.j2", consoles=results, versions=r2)

@app.route('/add_console', methods=["POST", "GET"])
def add_console():

    if request.method == "GET":
        query = 'SELECT name, company, portable, vr, backwards_comp, max_resolution FROM Consoles;'
        result = db.execute_query(db_connection, query).fetchall();
        print(result)
        q2 = "SELECT item_ID, console_id, title, name, quantity, (quantity - SUM(CASE WHEN paid = '0000-00-00' THEN '1' ELSE '0' END)) as available " \
             "FROM Console_Versions INNER JOIN Consoles ON console = console_ID INNER JOIN Games ON game = game_ID LEFT JOIN Game_Rentals " \
             "ON item_ID = game_version LEFT JOIN Rentals ON rental = rental_ID GROUP BY item_ID"
        c2 = db.execute_query(db_connection=db_connection, query=q2)
        r2 = c2.fetchall()
        return render_template('consoles.j2', consoles=result, versions=r2)

    elif request.method == "POST":
        print("Adding new console")
        # pull out the title from the form to check if the game has already been added
        name = request.form['name']
        # while you're at it, pull out the console versions values so we don't get a pre-reference error
        comp = request.form['company']
        portable = 'portable' in request.form
        vr = 'vr' in request.form
        bc = 'bc' in request.form
        max_res = request.form['maxres']

        # make sure the game isn't in the list first
        query = "SELECT name FROM Consoles WHERE name = '" + name + "';"
        check = db.execute_query(db_connection, query).fetchall();

        # in SQL/Flask, if a SELECT is returned with no values, fetchall returns () (not '' or None)
        if check == ():
            if comp == 'Choose...':
                comp = 0
            if max_res == 'Choose...':
                max_res = 720
            if portable:
                portable = 1
            else:
                portable = 0
            if vr:
                vr = 1
            else:
                vr = 0
            if bc:
                bc = 1
            else:
                bc = 0
            print(name, comp, portable, vr, bc, max_res)
            query = "INSERT INTO Consoles (name, company, portable, vr, backwards_comp, max_resolution) VALUES (%s,%s,%s,%s,%s,%s);"
            data = (name, comp, portable, vr, bc, max_res)
            db.execute_query(db_connection, query, data)

        return redirect(url_for('consoles'))

@app.route('/filter_consoles', methods=["POST", "GET"])
def filter_consoles():
    game = request.form['game']
    # while you're at it, pull out the console versions values so we don't get a pre-reference error
    comp = request.form['fcompany']
    portable = 'fportable' in request.form
    vr = 'fvr' in request.form
    bc = 'fbc' in request.form
    max_res = request.form['fmaxres']
    if game == '' and comp == 'Choose...' and not portable and not vr and not bc and max_res == 'Choose...':
        return redirect(url_for('consoles'))
    query = 'SELECT c.name, c.company, c.portable, c.vr, c.backwards_comp, c.max_resolution FROM Consoles c INNER JOIN Console_Versions cv ON c.console_ID = cv.console INNER JOIN Games g ON cv.console = c.console_ID WHERE'
    where = []
    if game != '':
        where.append(' c.name LIKE "%%' + str(game) + '%%"')
    if comp != 'Choose...':
        where.append(' c.company = "' + str(comp) + '"')
    if portable:
        where.append(' c.portable = "1"')
    if vr:
        where.append(' c.vr = "1"')
    if bc:
        where.append(' c.backwards_comp = "1"')
    if max_res != 'Choose...':
        where.append(' max_resolution = "' + str(max_res) + '"')
    print(where)
    constraints = ''
    for i in range(len(where)):
        if i == len(where) - 1:
            constraints += where[i] + ' GROUP BY console_ID;'
        else:
            constraints += where[i] + ' AND'
    print(constraints)
    query += constraints
    print(query)
    cursor = db.execute_query(db_connection=db_connection, query=query)
    results = cursor.fetchall()
    q2 = "SELECT item_ID, console_id, title, name, quantity, (quantity - SUM(CASE WHEN paid = '0000-00-00' THEN '1' ELSE '0' END)) as available " \
         "FROM Console_Versions INNER JOIN Consoles ON console = console_ID INNER JOIN Games ON game = game_ID LEFT JOIN Game_Rentals " \
         "ON item_ID = game_version LEFT JOIN Rentals ON rental = rental_ID GROUP BY item_ID"
    c2 = db.execute_query(db_connection=db_connection, query=q2)
    r2 = c2.fetchall()
    return render_template("consoles.j2", consoles=results, versions=r2)

@app.route('/delete_console/<int:c_id>')
def delete_console(c_id):
    query = "DELETE FROM Consoles WHERE console_ID = %s"
    data = (c_id,)

    result = db.execute_query(db_connection, query, data)
    print("Row " + str(result.rowcount) + " deleted")
    return redirect(url_for('consoles'))

@app.route('/update_console/<int:c_id>', methods=['POST','GET'])
def update_console(c_id):
    if request.method == 'GET':
        c_query = 'SELECT * FROM Consoles WHERE console_id = %s' % (c_id)
        c_r = db.execute_query(db_connection=db_connection,query=c_query).fetchone()
        print(c_r)
        if c_r == None:
            return "No such console exists!"
        return render_template('update_console.j2', update=c_r)
    elif request.method == 'POST':
        print("Updated console!")
        name = request.form['name']
        print(name)
        company = request.form['company']
        print(company)
        portable = 'portable' in request.form
        print(portable)
        vr = 'vr' in request.form
        print(vr)
        bc = 'bc' in request.form
        print(bc)
        max_res = request.form['maxres']
        print(max_res)
        print(request.form);
        query = 'UPDATE Consoles SET name = %s, company = %s, portable = %s, vr = %s, backwards_comp = %s, max_resolution = %s WHERE console_id = %s'
        data = (name, company, portable, vr, bc, max_res, c_id)
        db.execute_query(db_connection, query, data)
        return redirect(url_for('consoles'))


@app.route('/rentals')
def rentals():
    query = "SELECT rental_ID, first_name, last_name, DATE_FORMAT(rent_date, '%%b %%e %%Y') as date, DATE_FORMAT(paid, '%%b %%e %%Y') as paid, " \
            "COUNT(game_version) as rentals, COUNT(game_version) * '4.99' as cost, DATE_FORMAT(DATE_ADD(rent_date, INTERVAL 3 DAY), '%%b %%e %%Y') as due, " \
            "CASE WHEN DATEDIFF(CURRENT_DATE, rent_date) <= 3 THEN '0.00' WHEN DATE_FORMAT(paid, '%%b %%e %%Y') IS NULL THEN DATEDIFF(CURRENT_DATE, DATE_ADD(rent_date, INTERVAL 3 DAY)) WHEN DATE_ADD(rent_date, INTERVAL 3 DAY) > paid " \
            "THEN '0.00' ELSE DATEDIFF(paid, DATE_ADD(rent_date, INTERVAL 3 DAY)) END AS days_late, CASE WHEN DATEDIFF(CURRENT_DATE, rent_date) <= 3 THEN '0.00' WHEN COUNT(game_version) = '0' THEN '0.00' WHEN DATE_FORMAT(paid, '%%b %%e %%Y') IS NULL " \
            "THEN DATEDIFF(CURRENT_DATE, DATE_ADD(rent_date, INTERVAL 3 DAY)) * 1.99 WHEN DATE_ADD(rent_date, INTERVAL 3 DAY) > paid THEN '0.00' " \
            "ELSE DATEDIFF(paid, DATE_ADD(rent_date, INTERVAL 3 DAY)) * 1.99 END AS late_fee, ((COUNT(game_version) * '4.99') + (CASE WHEN DATEDIFF(CURRENT_DATE, rent_date) <= 3 THEN '0.00' WHEN COUNT(game_version) = '0' THEN '0.00' " \
            "WHEN DATE_FORMAT(paid, '%%b %%e %%Y') IS NULL THEN DATEDIFF(CURRENT_DATE, DATE_ADD(rent_date, INTERVAL 3 DAY)) * 1.99 WHEN DATE_ADD(rent_date, INTERVAL 3 DAY) > paid " \
            "THEN '0.00' ELSE DATEDIFF(paid, DATE_ADD(rent_date, INTERVAL 3 DAY)) * 1.99 END)) as total FROM Rentals INNER JOIN Customers ON customer = customer_ID " \
            "LEFT JOIN Game_Rentals ON rental_ID = rental GROUP BY rental_ID;"
    cursor = db.execute_query(db_connection=db_connection, query=query)
    results = cursor.fetchall()
    q2 = "SELECT game_version, rental, title, name FROM Game_Rentals INNER JOIN Console_Versions on game_version = item_ID " \
         "INNER JOIN Games ON game = game_ID INNER JOIN Consoles ON console = console_ID;"
    r2 = db.execute_query(db_connection=db_connection, query=q2).fetchall()
    q3 = "SELECT title, name FROM Games INNER JOIN Console_Versions ON game_ID = game INNER JOIN Consoles ON console = console_ID;"
    r3 = db.execute_query(db_connection=db_connection, query=q3).fetchall()
    q4 = "SELECT first_name, last_name, rent_date FROM Customers INNER JOIN Rentals ON customer_ID = customer;"
    r4 = db.execute_query(db_connection=db_connection, query=q4).fetchall()
    q5 = "SELECT first_name, last_name FROM Customers;"
    r5 = db.execute_query(db_connection=db_connection, query=q5).fetchall()
    return render_template("rentals.j2", rentals=results, items=r2, g_versions=r3, people=r4, customers=r5)

@app.route('/add_rental', methods=["POST", "GET"])
def add_rental():

    if request.method == "GET":
        print("The method is wrong. Change this in the HTML.")
        query = "SELECT rental_ID, first_name, last_name, DATE_FORMAT(rent_date, '%%b %%e %%Y') as date, DATE_FORMAT(paid, '%%b %%e %%Y') as paid, " \
                "COUNT(game_version) as rentals, COUNT(game_version) * '4.99' as cost, DATE_FORMAT(DATE_ADD(rent_date, INTERVAL 3 DAY), '%%b %%e %%Y') as due, " \
                "CASE WHEN DATEDIFF(CURRENT_DATE, rent_date) <= 3 THEN '0.00' WHEN DATE_FORMAT(paid, '%%b %%e %%Y') IS NULL THEN DATEDIFF(CURRENT_DATE, DATE_ADD(rent_date, INTERVAL 3 DAY)) WHEN DATE_ADD(rent_date, INTERVAL 3 DAY) > paid " \
                "THEN '0.00' ELSE DATEDIFF(paid, DATE_ADD(rent_date, INTERVAL 3 DAY)) END AS days_late, CASE WHEN DATEDIFF(CURRENT_DATE, rent_date) <= 3 THEN '0.00' WHEN COUNT(game_version) = '0' THEN '0.00' WHEN DATE_FORMAT(paid, '%%b %%e %%Y') IS NULL " \
                "THEN DATEDIFF(CURRENT_DATE, DATE_ADD(rent_date, INTERVAL 3 DAY)) * 1.99 WHEN DATE_ADD(rent_date, INTERVAL 3 DAY) > paid THEN '0.00' " \
                "ELSE DATEDIFF(paid, DATE_ADD(rent_date, INTERVAL 3 DAY)) * 1.99 END AS late_fee, ((COUNT(game_version) * '4.99') + (CASE WHEN DATEDIFF(CURRENT_DATE, rent_date) <= 3 THEN '0.00' WHEN COUNT(game_version) = '0' THEN '0.00' " \
                "WHEN DATE_FORMAT(paid, '%%b %%e %%Y') IS NULL THEN DATEDIFF(CURRENT_DATE, DATE_ADD(rent_date, INTERVAL 3 DAY)) * 1.99 WHEN DATE_ADD(rent_date, INTERVAL 3 DAY) > paid " \
                "THEN '0.00' ELSE DATEDIFF(paid, DATE_ADD(rent_date, INTERVAL 3 DAY)) * 1.99 END)) as total FROM Rentals INNER JOIN Customers ON customer = customer_ID " \
                "LEFT JOIN Game_Rentals ON rental_ID = rental GROUP BY rental_ID;"
        cursor = db.execute_query(db_connection=db_connection, query=query)
        results = cursor.fetchall()
        q2 = "SELECT game_version, rental, title, name FROM Game_Rentals INNER JOIN Console_Versions on game_version = item_ID " \
             "INNER JOIN Games ON game = game_ID INNER JOIN Consoles ON console = console_ID;"
        r2 = db.execute_query(db_connection=db_connection, query=q2).fetchall()
        q3 = "SELECT title, name FROM Games INNER JOIN Console_Versions ON game_ID = game INNER JOIN Consoles ON console = console_ID;"
        r3 = db.execute_query(db_connection=db_connection, query=q3).fetchall()
        q4 = "SELECT first_name, last_name, rent_date FROM Customers INNER JOIN Rentals ON customer_ID = customer;"
        r4 = db.execute_query(db_connection=db_connection, query=q4).fetchall()
        q5 = "SELECT first_name, last_name FROM Customers;"
        r5 = db.execute_query(db_connection=db_connection, query=q5).fetchall()
        return render_template("rentals.j2", rentals=results, items=r2, g_versions=r3, people=r4, customers=r5)

    elif request.method == "POST":
        print("Adding new rental")
        # pull out the title from the form to check if the game has already been added
        customer = request.form['customer']
        first, last = customer.split(' ', 1)
        # pull out rent_date and paid
        rent_date = request.form['rent_date']
        paid = request.form['paid']

        # make sure the customer isn't in the list first
        query = "SELECT customer_id FROM Customers WHERE first_name = '" + first + "' AND last_name = '" + last + "';"
        check = db.execute_query(db_connection, query).fetchall();

        # in SQL/Flask, if a SELECT is returned with no values, fetchall returns () (not '' or None)
        if check != ():
            query = "INSERT INTO Rentals (customer, rent_date, paid) VALUES (%s,%s,%s);"
            data = (check[0]['customer_id'], rent_date, paid)
            db.execute_query(db_connection, query, data)
        else: print("Customer does not exist.")

        return redirect(url_for('rentals'))

@app.route('/add_item', methods=["POST", "GET"])
def add_item():
    g_version = request.form['copies']
    title, name = g_version.split("--", 1)
    customer = request.form['person']
    name_date = customer.split()
    first_name = name_date[0]
    last_name = name_date[1]
    date = name_date[3]
    item_ID = "SELECT item_ID, quantity, rating FROM Console_Versions INNER JOIN Games ON game = game_ID INNER JOIN Consoles ON console = console_ID WHERE title = '%s' AND name = '%s'" % (title, name)
    c_ID = "SELECT rental_ID, DATEDIFF(CURRENT_DATE, birthday) DIV 365 AS age FROM Rentals INNER JOIN Customers ON customer = customer_ID WHERE first_name = '%s' AND last_name = '%s' AND rent_date = '%s'" % (first_name, last_name, date)
    r1 = db.execute_query(db_connection=db_connection, query=item_ID).fetchone()
    r2 = db.execute_query(db_connection=db_connection, query=c_ID).fetchone()
    if r2['age'] < 17 and (r1['rating'] == 'M' or r1['rating'] == 'AO'):
        return redirect(url_for('rentals'))
    rent_count = "SELECT (quantity - SUM(CASE WHEN paid = '0000-00-00' THEN '1' ELSE '0' END)) as available FROM Console_Versions " \
                 "INNER JOIN Consoles ON console = console_ID INNER JOIN Games ON game = game_ID LEFT JOIN Game_Rentals ON " \
                 "item_ID = game_version LEFT JOIN Rentals ON rental = rental_ID WHERE item_ID = %s" % (r1['item_ID'])
    rent_count += " GROUP BY item_ID"
    r3 = db.execute_query(db_connection=db_connection, query=rent_count).fetchone()
    if int(r3['available']) == 0:
        return redirect(url_for('rentals'))
    query = "INSERT INTO Game_Rentals (game_version, rental) VALUES (%s, %s)"
    data = (r1['item_ID'], r2['rental_ID'])
    db.execute_query(db_connection, query, data)
    return redirect(url_for('rentals'))

@app.route('/delete_item/<int:gv_id>/<int:re_id>')
def delete_item(gv_id, re_id):
    query = "DELETE FROM Game_Rentals WHERE game_version = %s AND rental = %s" % (gv_id, re_id)
    result = db.execute_query(db_connection, query=query)
    print("Row " + str(result.rowcount) + " deleted.")
    return redirect(url_for('rentals'))

@app.route('/filter_rentals', methods=["POST", "GET"])
def filter_rentals():
    first_name = request.form['ffirst']
    last_name = request.form['flast']
    date = request.form['fdate']
    unpaid = 'unpaid' in request.form
    if first_name == '' and last_name == '' and date == '' and not unpaid:
        return redirect(url_for('rentals'))
    query = "SELECT rental_ID, first_name, last_name, DATE_FORMAT(rent_date, '%%b %%e %%Y') as date, DATE_FORMAT(paid, '%%b %%e %%Y') as paid, " \
            "COUNT(game_version) as rentals, COUNT(game_version) * '4.99' as cost, DATE_FORMAT(DATE_ADD(rent_date, INTERVAL 3 DAY), '%%b %%e %%Y') as due, " \
            "CASE WHEN DATEDIFF(CURRENT_DATE, rent_date) <= 3 THEN '0.00' WHEN DATE_FORMAT(paid, '%%b %%e %%Y') IS NULL THEN DATEDIFF(CURRENT_DATE, DATE_ADD(rent_date, INTERVAL 3 DAY)) WHEN DATE_ADD(rent_date, INTERVAL 3 DAY) > paid " \
            "THEN '0.00' ELSE DATEDIFF(paid, DATE_ADD(rent_date, INTERVAL 3 DAY)) END AS days_late, CASE WHEN DATEDIFF(CURRENT_DATE, rent_date) <= 3 THEN '0.00' WHEN COUNT(game_version) = '0' THEN '0.00' WHEN DATE_FORMAT(paid, '%%b %%e %%Y') IS NULL " \
            "THEN DATEDIFF(CURRENT_DATE, DATE_ADD(rent_date, INTERVAL 3 DAY)) * 1.99 WHEN DATE_ADD(rent_date, INTERVAL 3 DAY) > paid THEN '0.00' " \
            "ELSE DATEDIFF(paid, DATE_ADD(rent_date, INTERVAL 3 DAY)) * 1.99 END AS late_fee, ((COUNT(game_version) * '4.99') + (CASE WHEN DATEDIFF(CURRENT_DATE, rent_date) <= 3 THEN '0.00' WHEN COUNT(game_version) = '0' THEN '0.00' " \
            "WHEN DATE_FORMAT(paid, '%%b %%e %%Y') IS NULL THEN DATEDIFF(CURRENT_DATE, DATE_ADD(rent_date, INTERVAL 3 DAY)) * 1.99 WHEN DATE_ADD(rent_date, INTERVAL 3 DAY) > paid " \
            "THEN '0.00' ELSE DATEDIFF(paid, DATE_ADD(rent_date, INTERVAL 3 DAY)) * 1.99 END)) as total FROM Rentals INNER JOIN Customers ON customer = customer_ID " \
            "LEFT JOIN Game_Rentals ON rental_ID = rental WHERE"
    where = []
    if first_name != '':
        where.append(' first_name LIKE "%%' + str(first_name) + '%%"')
    if last_name != '':
        where.append(' last_name LIKE "%%' + str(last_name) + '%%"')
    if date != '':
        where.append(' rent_date = "' + str(date) + '"')
    if unpaid:
        where.append(' paid = "0000-00-00" OR paid IS NULL')
    print(where)
    constraints = ''
    for i in range(len(where)):
        if i == len(where) - 1:
            constraints += where[i] + ' GROUP BY rental_ID;'
        else:
            constraints += where[i] + ' AND'
    print(constraints)
    query += constraints
    print(query)
    cursor = db.execute_query(db_connection=db_connection, query=query)
    results = cursor.fetchall()
    q2 = "SELECT game_version, rental, title, name FROM Game_Rentals INNER JOIN Console_Versions on game_version = item_ID " \
         "INNER JOIN Games ON game = game_ID INNER JOIN Consoles ON console = console_ID;"
    r2 = db.execute_query(db_connection=db_connection, query=q2).fetchall()
    q3 = "SELECT title, name FROM Games INNER JOIN Console_Versions ON game_ID = game INNER JOIN Consoles ON console = console_ID;"
    r3 = db.execute_query(db_connection=db_connection, query=q3).fetchall()
    q4 = "SELECT first_name, last_name FROM Customers INNER JOIN Rentals ON customer_ID = customer;"
    r4 = db.execute_query(db_connection=db_connection, query=q4).fetchall()
    q5 = "SELECT first_name, last_name FROM Customers;"
    r5 = db.execute_query(db_connection=db_connection, query=q5).fetchall()
    return render_template("rentals.j2", rentals=results, items=r2, g_versions=r3, people=r4, customers=r5)

@app.route('/delete_rental/<int:r_id>')
def delete_rental(r_id):
    query = "DELETE FROM Rentals WHERE rental_ID = %s"
    data = (r_id,)

    result = db.execute_query(db_connection, query, data)
    print("Row " + str(result.rowcount) + " deleted")
    return redirect(url_for('rentals'))

@app.route('/update_rental/<int:r_id>', methods=['POST','GET'])
def update_rental(r_id):
    if request.method == 'GET':
        r_query = 'SELECT first_name, last_name, rental_ID, rent_date, paid FROM Rentals INNER JOIN Customers ON customer = customer_ID WHERE rental_id = %s' % (r_id)
        r_r = db.execute_query(db_connection=db_connection,query=r_query).fetchone()
        cu_query = 'SELECT first_name, last_name FROM Customers;'
        cu_r = db.execute_query(db_connection=db_connection,query=cu_query).fetchall()
        print(r_r)
        print(cu_r)
        if r_r == None:
            return "No such rental exists!"
        return render_template('update_rental.j2', update=r_r, people=cu_r)
    elif request.method == 'POST':
        print("Updated rental!")
        customer = request.form['customer']
        print(customer)
        first, last = customer.split(" ", 1)
        print(first)
        print(last)
        r_date = request.form['rent_date']
        print(r_date)
        paid = request.form['paid']
        print(paid)
        print(request.form);
        c_search = 'SELECT customer_ID FROM Customers WHERE first_name = "%s" AND last_name = "%s"' % (first, last)
        cs_id = db.execute_query(db_connection=db_connection, query=c_search).fetchone()
        print(cs_id)
        query = 'UPDATE Rentals SET customer = %s, rent_date = %s, paid = %s WHERE rental_id = %s'
        data = (cs_id['customer_ID'], r_date, paid, r_id)
        db.execute_query(db_connection, query, data)
        return redirect(url_for('rentals'))

@app.route('/customers')
def customers():
    query = "SELECT customer_ID, first_name, last_name, street, city, state, zip, phone, email, DATE_FORMAT(birthday, '%%b %%e %%Y') as birthday FROM Customers;"
    cursor = db.execute_query(db_connection=db_connection, query=query)
    results = cursor.fetchall()
    q2 = "SELECT customer, rental, game_version, title, name, DATE_FORMAT(rent_date, '%%b %%e %%Y') AS rent_date, DATE_FORMAT(DATE_ADD(rent_date, INTERVAL 3 DAY), '%%b %%e %%Y') AS due, " \
         "DATE_FORMAT(paid, '%%b %%e %%Y') AS paid, first_name, last_name FROM Games INNER JOIN Console_Versions ON game_ID = game " \
         "INNER JOIN Consoles ON console = console_ID INNER JOIN Game_Rentals ON item_ID = game_version " \
         "INNER JOIN Rentals ON rental = rental_ID INNER JOIN Customers ON customer = customer_ID;"
    r2 = db.execute_query(db_connection=db_connection, query=q2).fetchall()
    states = ['AL', 'AK', 'AS', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'DC', 'FL', 'GA', 'GU', 'HI', 'ID', 'IL', 'IN',
              'IA',
              'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY',
              'NC',
              'ND', 'MP', 'OH', 'OK', 'OR', 'PA', 'PR', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'VI', 'WA',
              'WV', 'WI', 'WY']
    gq = 'SELECT title FROM Games;'
    g_r = db.execute_query(db_connection=db_connection, query=gq).fetchall()
    cq = 'SELECT name FROM Consoles;'
    c_r = db.execute_query(db_connection=db_connection, query=cq).fetchall()
    return render_template("customers.j2", customers=results, states=states, items=r2, games=g_r, consoles=c_r)

@app.route('/add_customer', methods=["POST", "GET"])
def add_customer():

    if request.method == "GET":
        query = "SELECT customer_ID, first_name, last_name, street, city, state, zip, phone, email, DATE_FORMAT(birthday, '%%b %%e %%Y') as birthday FROM Customers;"
        cursor = db.execute_query(db_connection=db_connection, query=query)
        results = cursor.fetchall()
        q2 = "SELECT customer, rental, game_version, title, name, DATE_FORMAT(rent_date, '%%b %%e %%Y') AS rent_date, DATE_FORMAT(DATE_ADD(rent_date, INTERVAL 3 DAY), '%%b %%e %%Y') AS due, " \
             "DATE_FORMAT(paid, '%%b %%e %%Y') AS paid, first_name, last_name FROM Games INNER JOIN Console_Versions ON game_ID = game " \
             "INNER JOIN Consoles ON console = console_ID INNER JOIN Game_Rentals ON item_ID = game_version " \
             "INNER JOIN Rentals ON rental = rental_ID INNER JOIN Customers ON customer = customer_ID;"
        r2 = db.execute_query(db_connection=db_connection, query=q2).fetchall()
        states = ['AL', 'AK', 'AS', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'DC', 'FL', 'GA', 'GU', 'HI', 'ID', 'IL', 'IN',
                  'IA',
                  'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY',
                  'NC',
                  'ND', 'MP', 'OH', 'OK', 'OR', 'PA', 'PR', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'VI', 'WA',
                  'WV', 'WI', 'WY']
        gq = 'SELECT title FROM Games;'
        g_r = db.execute_query(db_connection=db_connection, query=gq).fetchall()
        cq = 'SELECT name FROM Consoles;'
        c_r = db.execute_query(db_connection=db_connection, query=cq).fetchall()
        return render_template("customers.j2", customers=results, states=states, items=r2, games=g_r, consoles=c_r)

    elif request.method == "POST":
        print("Adding new customer")
        # pull out attributes
        first_name = request.form['first_name']
        if " " in first_name:
            first_name = first_name.replace(" ", "-")
        last_name = request.form['last_name']
        if " " in last_name:
            last_name = last_name.replace(" ", "-")
        street = request.form['street']
        city = request.form['city']
        state = request.form['state']
        zip_code = request.form['zip_code']
        phone = request.form['phone']
        email = request.form['email']
        birthday = request.form['birthday']

        # make sure the customer isn't in the list first
        query = "SELECT first_name FROM Customers WHERE first_name = '" + first_name + "' AND last_name = '" + last_name + "';"
        check = db.execute_query(db_connection, query).fetchall();

        # in SQL/Flask, if a SELECT is returned with no values, fetchall returns () (not '' or None)
        if check == ():
            query = "INSERT INTO Customers (first_name, last_name, street, city, state, zip, phone, email, birthday) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s);"
            data = (first_name, last_name, street, city, state, zip_code, phone, email, birthday)
            db.execute_query(db_connection, query, data)

        return redirect(url_for('customers'))

@app.route('/filter_customers', methods=["POST", "GET"])
def filter_customers():
    first_name = request.form['ffname']
    last_name = request.form['flname']
    street = request.form['fstreet']
    city = request.form['fcity']
    state = request.form['fstate']
    zip_code = request.form['fzip']
    phone = request.form['fphone']
    email = request.form['femail']
    age = request.form['fage']
    game = request.form['game']
    console = request.form['console']
    if first_name == '' and last_name == '' and street == '' and city == '' and state == 'Choose...' and zip_code == '' \
            and phone == '' and email == '' and age == 'Choose...' and game == 'Choose...' and console == 'Choose...':
        return redirect(url_for('customers'))
    query = 'SELECT first_name, last_name, street, city, state, zip, phone, email, birthday, customer_id FROM Customers ' \
            'LEFT JOIN Rentals ON customer_ID = customer LEFT JOIN Game_Rentals ON rental_ID = rental LEFT JOIN Console_Versions ' \
            'ON game_version = item_ID LEFT JOIN Games ON game = game_ID LEFT JOIN Consoles ON console = console_ID WHERE'
    where = []
    if first_name != '':
        where.append(' first_name LIKE "%%' + str(first_name) + '%%"')
    if last_name != '':
        where.append(' last_name LIKE "%%' + str(last_name) + '%%"')
    if street != '':
        where.append(' street = "' + str(street) + '"')
    if city != '':
        where.append(' city LIKE "%%' + str(city) + '%%"')
    if state != 'Choose...':
        where.append(' state = "' + str(state) + '"')
    if zip_code != '':
        where.append(' zip = "' + str(zip_code) + '"')
    if phone != '':
        where.append(' phone = "' + str(phone) + '"')
    if email != '':
        where.append(' email LIKE "%%' + str(email) + '%%"')
    if age != 'Choose...':
        if age == '16 & Under':
            where.append(' birthday > DATE_SUB(CURRENT_DATE, INTERVAL 17 YEAR)')
        elif age == '17-34':
            where.append(' birthday > DATE_SUB(CURRENT_DATE, INTERVAL 35 YEAR) AND birthday <= DATE_SUB(CURRENT_DATE, INTERVAL 17 YEAR)')
        elif age == '35-49':
            where.append(' birthday > DATE_SUB(CURRENT_DATE, INTERVAL 50 YEAR) AND birthday <= DATE_SUB(CURRENT_DATE, INTERVAL 35 YEAR)')
        elif age == '50-64':
            where.append(' birthday > DATE_SUB(CURRENT_DATE, INTERVAL 64 YEAR) AND birthday <= DATE_SUB(CURRENT_DATE, INTERVAL 50 YEAR)')
        else:
            where.append(' birthday <= DATE_SUB(CURRENT_DATE, INTERVAL 65 YEAR)')
    if game != 'Choose...':
        where.append(' title = "' + str(game) + '"')
    if console != 'Choose...':
        where.append(' name = "' + str(console) + '"')
    print(where)
    constraints = ''
    for i in range(len(where)):
        if i == len(where) - 1:
            constraints += where[i] + ' GROUP BY customer_ID;'
        else:
            constraints += where[i] + ' AND'
    print(constraints)
    query += constraints
    print(query)
    cursor = db.execute_query(db_connection=db_connection, query=query)
    results = cursor.fetchall()
    q2 = "SELECT customer, rental, game_version, title, name, DATE_FORMAT(rent_date, '%%b %%e %%Y') AS rent_date, DATE_FORMAT(DATE_ADD(rent_date, INTERVAL 3 DAY), '%%b %%e %%Y') AS due, " \
         "DATE_FORMAT(paid, '%%b %%e %%Y') AS paid, first_name, last_name FROM Games INNER JOIN Console_Versions ON game_ID = game " \
         "INNER JOIN Consoles ON console = console_ID INNER JOIN Game_Rentals ON item_ID = game_version " \
         "INNER JOIN Rentals ON rental = rental_ID INNER JOIN Customers ON customer = customer_ID;"
    r2 = db.execute_query(db_connection=db_connection, query=q2).fetchall()
    states = ['AL', 'AK', 'AS', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'DC', 'FL', 'GA', 'GU', 'HI', 'ID', 'IL', 'IN',
              'IA',
              'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY',
              'NC',
              'ND', 'MP', 'OH', 'OK', 'OR', 'PA', 'PR', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'VI', 'WA',
              'WV', 'WI', 'WY']
    gq = 'SELECT title FROM Games;'
    g_r = db.execute_query(db_connection=db_connection, query=gq).fetchall()
    cq = 'SELECT name FROM Consoles;'
    c_r = db.execute_query(db_connection=db_connection, query=cq).fetchall()
    return render_template("customers.j2", customers=results, states=states, items=r2, games=g_r, consoles=c_r)

@app.route('/delete_customer/<int:cu_id>')
def delete_customer(cu_id):
    query = "DELETE FROM Customers WHERE customer_ID = %s"
    data = (cu_id,)

    result = db.execute_query(db_connection, query, data)
    print("Row " + str(result.rowcount) + " deleted")
    return redirect(url_for('customers'))

@app.route('/update_customer/<int:cu_id>', methods=['POST','GET'])
def update_customer(cu_id):
    if request.method == 'GET':
        cu_query = "SELECT * FROM Customers WHERE customer_ID = %s" % (cu_id)
        cu_r = db.execute_query(db_connection=db_connection,query=cu_query).fetchone()
        states = ['AL', 'AK', 'AS', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'DC', 'FL', 'GA', 'GU', 'HI', 'ID', 'IL', 'IN',
                  'IA',
                  'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY',
                  'NC',
                  'ND', 'MP', 'OH', 'OK', 'OR', 'PA', 'PR', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'VI', 'WA',
                  'WV', 'WI', 'WY']
        if cu_r == None:
            return "No such customer exists!"
        return render_template('update_customer.j2', update=cu_r, states=states)
    elif request.method == 'POST':
        print("Updated customer!")
        first = request.form['f_name']
        print(first)
        last = request.form['l_name']
        print(last)
        street = request.form['street']
        print(street)
        city = request.form['city']
        print(city)
        state = request.form['state']
        print(state)
        zip = request.form['zip']
        print(zip)
        phone = request.form['phone']
        print(phone)
        email = request.form['email']
        print(email)
        bday = request.form['birthday']
        print(bday)
        query = 'UPDATE Customers SET first_name = %s, last_name = %s, street = %s, city = %s, state = %s, zip = %s, phone = %s, email = %s, birthday = %s WHERE customer_ID = %s'
        data = (first, last, street, city, state, zip, phone, email, bday, cu_id)
        db.execute_query(db_connection, query, data)
        return redirect(url_for('customers'))

# Listener

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 7673))
    app.run(port=port, debug=True)