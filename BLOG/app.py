from flask import Flask, request, render_template, redirect, url_for
import sqlite3

app = Flask(__name__)

conn = sqlite3.connect('blog.db')  # Change database name to "blog"
us_name = []

@app.route('/')
def logreg():
    return render_template("login.html", alert="", pwalert="")

@app.route('/log', methods=['POST', 'GET'])
def home():
    conn = sqlite3.connect('blog.db')  # Change database name to "blog"
    a = request.form['em_log'].strip()
    b = request.form['pw_log'].strip()
    uname = []
    email = []
    pw = []

    cur = conn.cursor()
    cur.execute("SELECT * FROM users")
    li = cur.fetchall()
    for i in range(0, len(li)):
        uname.append(li[i][0])
        email.append(li[i][1])
        pw.append(li[i][2])

    if a not in email:
        return render_template("login.html", alert="\nUser not found!\n")
    else:
        n = email.index(a)
        if b != pw[n]:
            return render_template("login.html", pwalert="\nwrong password!\n")
        else:
            tmp = cur.execute("SELECT name FROM users WHERE email='{}'".format(a))
            tmp = tmp.fetchone()[0]
            us_name.append(tmp)
            cur.execute("UPDATE username SET uname_soln='{}'".format(tmp))
            conn.commit()
            return redirect(url_for('comm'))

@app.route('/reg', methods=['POST', 'GET'])
def reg():
    conn = sqlite3.connect('blog.db')  # Change database name to "blog"
    a = request.form['nm_reg'].strip()
    b = request.form['em_reg'].strip()
    c = request.form['pw_reg']
    
    cur = conn.cursor()
    cur.execute("INSERT INTO users VALUES('{}','{}','{}')".format(a, b, c))
    conn.commit()
    cur.execute("SELECT * FROM users")
    li = cur.fetchall()
    return render_template("login.html", alert="", pwalert="")

@app.route('/community')
def comm():
    conn = sqlite3.connect('blog.db')  # Change database name to "blog"
    cur = conn.cursor()
    li = cur.execute("SELECT * FROM community ORDER BY id DESC")
    return render_template("community.html", community=li, user_id=1)


@app.route('/sol/<int:id>')
def sol(id):
    return render_template("soln1.html",slid=id)

@app.route('/soladd/<int:sid>', methods=['POST','GET'])
def sol2(sid):
    slid = sid
    a = request.form['soln']
    conn = sqlite3.connect('blog.db')
    cur = conn.cursor()

    # Fetch the uname from the community table
    solli = cur.execute("SELECT uname FROM community WHERE id={}".format(slid))
    result = solli.fetchone()
    if result is not None:
        uname_from_community = result[0]
    else:
        uname_from_community = ""

    # Fetch the username from the username table
    res = cur.execute("SELECT uname_soln FROM username")
    result = res.fetchone()
    if result is not None:
        uname_soln = result[0]
    else:
        uname_soln = ""

    # Fetch the soln column from the community table
    unm = cur.execute("SELECT soln FROM community WHERE id={}".format(slid))
    result = unm.fetchone()
    if result is not None:
        current_soln = result[0]
    else:
        current_soln = ""

    new_soln = f"{current_soln}\n{uname_soln} : {a}"
    
    # Update the community table
    cur.execute("UPDATE community SET soln=? WHERE id=?", (new_soln, slid))
    conn.commit()

    # Fetch the updated community table
    li = cur.execute("SELECT * FROM community ORDER BY id DESC")
    li = li.fetchall()

    # Fetch the user ID
    id_con = cur.execute("SELECT * FROM users")
    id_con = id_con.fetchall()
    name = [i[0] for i in id_con]
    n_id = name.index("santhosh") + 1

    return render_template("community.html", community=li, sid=slid, user_id=n_id)

@app.route('/post2/<int:sid>', methods=['GET', 'POST'])
def topost2(sid):
    slid = sid
    a = request.form['post_sub']
    b = request.form['post_content']
    conn = sqlite3.connect('blog.db')  # Change database name to "blog"
    cur = conn.cursor()

    # Use parameterized query to avoid syntax errors and SQL injection
    query = "INSERT INTO community(uname, subject, content, soln) VALUES (?, ?, ?, '')"
    values = (us_name[0], a, b)
    cur.execute(query, values)
    
    conn.commit()
    
    li = cur.execute("SELECT * FROM community ORDER BY id DESC")
    li = li.fetchall()
    return render_template("community.html", community=li)


@app.route('/addprob/<int:id>', methods=['GET','POST'])
def topost(id):
    return render_template("post.html",sid=id)

if __name__ == "__main__":
    app.run()
