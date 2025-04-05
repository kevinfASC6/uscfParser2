from flask import Flask, render_template, request, jsonify
import requests
from bs4 import BeautifulSoup
from tabulate import tabulate
from flask_httpauth import HTTPBasicAuth

app = Flask(__name__)

custom_headers = {
    'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8"
}


def view_players(ids):
    base_url = "https://www.uschess.org/msa/MbrDtlTnmtHst.php?"
    all_player_data = []  # To store information for all players

    for player_id in ids:
        url = base_url + str(player_id)
        html = requests.get(url, headers=custom_headers)
        soup = BeautifulSoup(html.text, "html.parser")

        # Extract required data from the HTML
        liverating0 = soup.find_all('td')
        lix = liverating0[5].text.replace("\n", "")
        liverating = soup.findChildren('table')
        li1 = liverating[6]
        rows = li1.findChildren(['th', 'tr'])[:6]
        all_player_data.append([lix])
        for row in rows:
            cells = row.findChildren('td')
            row_data = [cell.text for cell in cells]
            all_player_data.append(row_data)
    all_player_data = tabulate(all_player_data, tablefmt="html")
    return all_player_data 


@auth.verify_password
def verify_password(username, password):
    return username == USER and password == PASSWORD


@app.route("/", methods=['GET', 'POST'])
@auth.login_required
def home():
    if request.method == 'POST':
        player_ids = request.form.get('player_ids')
        player_ids = [int(id.strip()) for id in player_ids.split(",")]
        if player_ids:
            posts = view_players(player_ids)
            return render_template("home.html", posts=posts)
    return render_template("home.html", posts="")


if __name__ == "__main__":
    app.run(debug=True)


