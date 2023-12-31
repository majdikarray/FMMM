from flask import Flask, render_template, request,redirect,url_for,Response
import sqlite3
import csv
app = Flask(__name__)


# Créer une connexion à la base de données
conn = sqlite3.connect('formation.db')


# Créer un curseur pour exécuter des requêtes SQL tathbit les rq sql
c = conn.cursor()


# Vérifier que la table "personnes" existe
table_exists = c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='personnes'").fetchone()

# Si la table n'existe pas, la créer
if table_exists is None:
    c.execute('''CREATE TABLE personnes
                 (nom text, prenom text, age int,sexe text,nommaladie text, duree text, types int)''')
    
#alter_table = c.execute('''ALTER TABLE personnes ADD COLUMN hopital text ''')  

# Enregistrer les changements et fermer la connexion
conn.commit()
conn.close()

#nhadhro formulaire
@app.route('/')
#1ere page formulaire
def formulaire():
    return render_template('formulaire.html')

#fonction submit insersion des données   
@app.route('/ajouter', methods=['POST'])
def ajouter():
    nom = request.form['nom']
    prenom = request.form['prenom']
    age = request.form['age']
    sexe = request.form['sexe']
    nommaladie = request.form['nommaladie']
    duree = request.form['duree']
    types = request.form['types']
    pays = request.form['pays']
    hopital=request.form['hopital']
    conn = sqlite3.connect('formation.db')
    c = conn.cursor()
    c.execute('INSERT INTO personnes VALUES (?, ?, ?,?,?,?,?,?,?)', (nom, prenom, age,sexe,nommaladie,duree,types,pays,hopital))
    conn.commit()
    conn.close()
    return redirect(url_for('afficher'))

#naffichiw les donnees li amelnelhom insertion 
"""affiicher donnees """
@app.route('/afficher')
def afficher():
    conn = sqlite3.connect('formation.db')
    c = conn.cursor()
    personnes = c.execute("SELECT * FROM personnes").fetchall()
    conn.close()
    return render_template('acceuil.html', personnes=personnes)

@app.route('/export_personne')
def export_personne():
    conn = sqlite3.connect('formation.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM personnes")

    # Write data to CSV file
    with open('personne.csv', 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow([i[0] for i in cursor.description]) # write headers
        csvwriter.writerows(cursor)

    conn.close()

    # Return CSV file as a response
    with open('personne.csv', 'r') as f:
        csv_data = f.read()

    return Response(
        csv_data,
        mimetype="text/csv",
        headers={"Content-disposition":
                 "attachment; filename=personne.csv"})
   
if __name__ == '__main__':
    app.run(debug=True)
