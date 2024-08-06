#perfectoo
from flask import Flask, render_template_string, request, redirect, url_for, session
from pyngrok import ngrok
import secrets

# Generate a secure random SECRET_KEY
def generate_secret_key():
    return secrets.token_hex(16)

# Initialize Flask with a custom static folder
app = Flask(__name__, static_folder='/content/drive/MyDrive/ssf/static')
app.config['SECRET_KEY'] = generate_secret_key()

# Empathy scores for different options
empathy_scores = {
    'form_page_1': {'A': 1, 'B': 10, 'C': 5, 'D': 8},
    'form_page_2': {'A': 6, 'B': 10, 'C': 4, 'D': 1},
    'form_page_3': {'A': 2, 'B': 10, 'C': 3, 'D': 2},
    'form_page_4': {'A': 5, 'B': 8, 'C': 3, 'D': 1},
    'form_page_5': {'A': 7, 'B': 9, 'C': 4, 'D': 2}
}

# Evaluation metrics
# Evaluation metrics with more detailed categories
def evaluate_empathy(score):
    if score >= 31:
        return "Very High Empathy: You demonstrate an exceptional ability to understand and connect with others' emotions. Your empathy is deeply ingrained in your interactions and responses."
    elif score >= 26:
        return "High Empathy: You have a strong sense of empathy and are very attuned to the emotions and needs of others. You consistently show compassion and understanding."
    elif score >= 21:
        return "Moderate Empathy: You have a good level of empathy and usually respond well to others' emotions. You may occasionally miss some subtle cues but generally show understanding."
    elif score >= 16:
        return "Average Empathy: Your empathy is average. You are aware of others' feelings but may not always fully grasp their emotions or react as sensitively as possible."
    elif score >= 11:
        return "Low Empathy: You might find it challenging to understand and relate to others' feelings. There may be room for improvement in recognizing and responding to emotional cues."
    else:
        return "Very Low Empathy: You have significant difficulty in understanding and relating to others' emotions. Developing greater emotional awareness and sensitivity could benefit your relationships."

# HTML Templates
index_html = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Main Page</title>
    <style>
        body {
            background-image: url('{{ url_for("static", filename="1.png") }}');
            background-size: cover;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }
        .next-button {
            display: inline-block;
            padding: 10px 20px;
            font-size: 16px;
            color: white;
            background-color: #007BFF;
            text-align: center;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            text-decoration: none;
        }
        .next-button:hover {
            background-color: #0056b3;
        }
    </style>
</head>
<body>
    <a href="{{ url_for('form_page_1') }}" class="next-button">Next</a>
</body>
</html>
'''

form_html1 = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Form Page 1</title>
    <style>
        body {
            background-image: url('{{ url_for("static", filename="2.png") }}');
            background-size: cover;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
            flex-direction: column;
            overflow: hidden;
        }
        .form-container {
            background: rgba(255, 255, 255, 0.8);
            padding: 20px;
            border-radius: 8px;
            width: 80%;
            max-width: 500px;
            position: absolute;
            bottom: 20px;
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        .form-container div {
            margin-bottom: 15px;
            display: flex;
            align-items: center;
        }
        .form-container input[type="radio"] {
            margin-right: 10px;
            width: 20px;
            height: 20px;
            accent-color: #007BFF;
        }
        .form-container label {
            flex-grow: 1;
        }
        .form-container button {
            margin-top: 20px;
            padding: 10px 20px;
            font-size: 16px;
            color: white;
            background-color: #007BFF;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }
        .form-container button:hover {
            background-color: #0056b3;
        }
    </style>
</head>
<body>
    <div class="form-container">
        <form method="POST">
            <div>
                <input type="radio" id="option_a" name="response" value="A">
                <label for="option_a">A. Ignore them and continue with your work.</label>
            </div>
            <div>
                <input type="radio" id="option_b" name="response" value="B">
                <label for="option_b">B. Ask if everything is okay and offer to listen if they want to talk.</label>
            </div>
            <div>
                <input type="radio" id="option_c" name="response" value="C">
                <label for="option_c">C. Make a joke to lighten the mood.</label>
            </div>
            <div>
                <input type="radio" id="option_d" name="response" value="D">
                <label for="option_d">D. Offer them a drink and sit with them silently.</label>
            </div>
            <button type="submit">Submit</button>
        </form>
    </div>
</body>
</html>
'''

second_html = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Second Page</title>
    <style>
        body {
            background-image: url('{{ url_for("static", filename="3.png") }}');
            background-size: cover;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }
        .next-button {
            display: inline-block;
            padding: 10px 20px;
            font-size: 16px;
            color: white;
            background-color: #007BFF;
            text-align: center;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            text-decoration: none;
        }
        .next-button:hover {
            background-color: #0056b3;
        }
    </style>
</head>
<body>
    <a href="{{ url_for('form_page_2') }}" class="next-button">Next</a>
</body>
</html>
'''

form_html2 = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Form Page 2</title>
    <style>
        body {
            background-image: url('{{ url_for("static", filename="4.png") }}');
            background-size: cover;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
            flex-direction: column;
            overflow: hidden;
        }
        .form-container {
            background: rgba(255, 255, 255, 0.8);
            padding: 20px;
            border-radius: 8px;
            width: 80%;
            max-width: 500px;
            position: absolute;
            bottom: 20px;
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        .form-container div {
            margin-bottom: 15px;
            display: flex;
            align-items: center;
        }
        .form-container input[type="radio"] {
            margin-right: 10px;
            width: 20px;
            height: 20px;
            accent-color: #007BFF;
        }
        .form-container label {
            flex-grow: 1;
        }
        .form-container button {
            margin-top: 20px;
            padding: 10px 20px;
            font-size: 16px;
            color: white;
            background-color: #007BFF;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }
        .form-container button:hover {
            background-color: #0056b3;
        }
    </style>
</head>
<body>
    <div class="form-container">
        <form method="POST">
            <div>
                <input type="radio" id="option_a" name="response" value="A">
                <label for="option_a">A. Ignore the call because it's too late.</label>
            </div>
            <div>
                <input type="radio" id="option_b" name="response" value="B">
                <label for="option_b">B. Pick up the call and ask if everything is alright.</label>
            </div>
            <div>
                <input type="radio" id="option_c" name="response" value="C">
                <label for="option_c">C. Text them asking if they are okay.</label>
            </div>
            <div>
                <input type="radio" id="option_d" name="response" value="D">
                <label for="option_d">D. Wait until morning to return the call.</label>
            </div>
            <button type="submit">Submit</button>
        </form>
    </div>
</body>
</html>
'''

third_html = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Third Page</title>
    <style>
        body {
            background-image: url('{{ url_for("static", filename="5.png") }}');
            background-size: cover;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }
        .next-button {
            display: inline-block;
            padding: 10px 20px;
            font-size: 16px;
            color: white;
            background-color: #007BFF;
            text-align: center;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            text-decoration: none;
        }
        .next-button:hover {
            background-color: #0056b3;
        }
    </style>
</head>
<body>
    <a href="{{ url_for('form_page_3') }}" class="next-button">Next</a>
</body>
</html>
'''

form_html3 = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Form Page</title>
    <style>
        body {
            background-image: url('{{ url_for("static", filename="6.png") }}');
            background-size: cover;
            display: flex;
            justify-content: flex-end; /* Align to the right */
            align-items: flex-end; /* Align to the bottom */
            height: 100vh;
            margin: 0;
            overflow: hidden; /* Prevent scrolling */
        }
        .form-container {
            background: rgba(255, 255, 255, 0.8);
            padding: 20px;
            border-radius: 8px;
            max-width: 500px;
            width: 100%;
            margin: 20px; /* Add margin to position away from edges */
            display: flex;
            flex-direction: column;
        }
        .form-container div {
            margin-bottom: 15px;
            display: flex;
            align-items: center;
        }
        .form-container input[type="radio"] {
            margin-right: 10px;
            width: 20px;
            height: 20px;
            accent-color: #007BFF; /* Change to your preferred color */
        }
        .form-container label {
            flex-grow: 1;
        }
        .form-container button {
            margin-top: 20px;
            padding: 10px 20px;
            font-size: 16px;
            color: white;
            background-color: #007BFF; /* Change to your preferred color */
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }
        .form-container button:hover {
            background-color: #0056b3; /* Darker shade on hover */
        }
    </style>
</head>
<body>
    <div class="form-container">
        <form method="POST">
            <div>
                <input type="radio" id="option_a" name="response" value="A">
                <label for="option_a">A. Congratulate them warmly and ask them about their experience.</label>
            </div>
            <div>
                <input type="radio" id="option_b" name="response" value="B">
                <label for="option_b">B. Make a joke about how they finally achieved something.</label>
            </div>
            <div>
                <input type="radio" id="option_c" name="response" value="C">
                <label for="option_c">C. Tell them how you would have done it better.</label>
            </div>
            <div>
                <input type="radio" id="option_d" name="response" value="D">
                <label for="option_d">D. Nod and change the topic to something you find more interesting.</label>
            </div>
            <button type="submit">Submit</button>
        </form>
    </div>
</body>
</html>
'''

fourth_html = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Fourth Page</title>
    <style>
        body {
            background-image: url('{{ url_for("static", filename="7.png") }}');
            background-size: cover;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }
        .next-button {
            display: inline-block;
            padding: 10px 20px;
            font-size: 16px;
            color: white;
            background-color: #007BFF;
            text-align: center;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            text-decoration: none;
        }
        .next-button:hover {
            background-color: #0056b3;
        }
    </style>
</head>
<body>
    <a href="{{ url_for('form_page_4') }}" class="next-button">Next</a>
</body>
</html>
'''

form_html4 = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Form Page</title>
    <style>
        body {
            background-image: url('{{ url_for("static", filename="8.png") }}');
            background-size: cover;
            display: flex;
            justify-content: flex-end; /* Align to the right */
            align-items: flex-end; /* Align to the bottom */
            height: 100vh;
            margin: 0;
            overflow: hidden; /* Prevent scrolling */
        }
        .form-container {
            background: rgba(255, 255, 255, 0.8);
            padding: 20px;
            border-radius: 8px;
            max-width: 500px;
            width: 100%;
            margin: 20px; /* Add margin to position away from edges */
            display: flex;
            flex-direction: column;
        }
        .form-container div {
            margin-bottom: 15px;
            display: flex;
            align-items: center;
        }
        .form-container input[type="radio"] {
            margin-right: 10px;
            width: 20px;
            height: 20px;
            accent-color: #007BFF; /* Change to your preferred color */
        }
        .form-container label {
            flex-grow: 1;
        }
        .form-container button {
            margin-top: 20px;
            padding: 10px 20px;
            font-size: 16px;
            color: white;
            background-color: #007BFF; /* Change to your preferred color */
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }
        .form-container button:hover {
            background-color: #0056b3; /* Darker shade on hover */
        }
    </style>
</head>
<body>
    <div class="form-container">
        <form method="POST">
            <div>
                <input type="radio" id="option_a" name="response" value="A">
                <label for="option_a">A. Tell them you don't have time to help.</label>
            </div>
            <div>
                <input type="radio" id="option_b" name="response" value="B">
                <label for="option_b">B. Help them immediately, even if it disrupts your own plans.</label>
            </div>
            <div>
                <input type="radio" id="option_c" name="response" value="C">
                <label for="option_c">C. Offer to help after finishing your current task.</label>
            </div>
            <div>
                <input type="radio" id="option_d" name="response" value="D">
                <label for="option_d">D. Suggest they ask someone else for help.</label>
            </div>
            <button type="submit">Submit</button>
        </form>
    </div>
</body>
</html>
'''

five_html = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Fifth Page</title>
    <style>
        body {
            background-image: url('{{ url_for("static", filename="9.png") }}');
            background-size: cover;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }
        .next-button {
            display: inline-block;
            padding: 10px 20px;
            font-size: 16px;
            color: white;
            background-color: #007BFF;
            text-align: center;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            text-decoration: none;
        }
        .next-button:hover {
            background-color: #0056b3;
        }
    </style>
</head>
<body>
    <a href="{{ url_for('form_page_5') }}" class="next-button">Next</a>
</body>
</html>
'''

form_html5 = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Form Page 5</title>
    <style>
        body {
            background-image: url('{{ url_for("static", filename="10.png") }}');
            background-size: cover;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
            flex-direction: column;
            overflow: hidden;
        }
        .form-container {
            background: rgba(255, 255, 255, 0.8);
            padding: 20px;
            border-radius: 8px;
            width: 80%;
            max-width: 500px;
            position: absolute;
            bottom: 20px;
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        .form-container div {
            margin-bottom: 15px;
            display: flex;
            align-items: center;
        }
        .form-container input[type="radio"] {
            margin-right: 10px;
            width: 20px;
            height: 20px;
            accent-color: #007BFF;
        }
        .form-container label {
            flex-grow: 1;
        }
        .form-container button {
            margin-top: 20px;
            padding: 10px 20px;
            font-size: 16px;
            color: white;
            background-color: #007BFF;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }
        .form-container button:hover {
            background-color: #0056b3;
        }
    </style>
</head>
<body>
    <div class="form-container">
        <form method="POST">
            <div>
                <input type="radio" id="option_a" name="response" value="A">
                <label for="option_a">A. Share your own experiences and how you overcame them.</label>
            </div>
            <div>
                <input type="radio" id="option_b" name="response" value="B">
                <label for="option_b">B. Listen carefully and offer emotional support.</label>
            </div>
            <div>
                <input type="radio" id="option_c" name="response" value="C">
                <label for="option_c">C. Tell them not to worry and everything will be fine.</label>
            </div>
            <div>
                <input type="radio" id="option_d" name="response" value="D">
                <label for="option_d">D. Suggest they distract themselves with a hobby.</label>
            </div>
            <button type="submit">Submit</button>
        </form>
    </div>
</body>
</html>
'''

result_html_template = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Result Page</title>
    <style>
        body {
            background-image: url('{{ url_for("static", filename="bg_result.png") }}');
            background-size: cover;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
            text-align: center;
        }
        .result-container {
            background: rgba(255, 255, 255, 0.8);
            padding: 20px;
            border-radius: 8px;
            width: 80%;
            max-width: 600px;
        }
    </style>
</head>
<body>
    <div class="result-container">
        <h1>Empathy Assessment Result</h1>
        <p>Total Score: {{ total_score }}</p>
        <p>{{ result_text }}</p>
    </div>
</body>
</html>
'''

# Routes for each page
@app.route('/')
def index():
    return render_template_string(index_html)

@app.route('/form_page_1', methods=['GET', 'POST'])
def form_page_1():
    if request.method == 'POST':
        selected_option = request.form.get('response')
        score = empathy_scores['form_page_1'].get(selected_option, 0)
        session['total_score'] = score
        return redirect(url_for('second_page'))
    return render_template_string(form_html1)

@app.route('/second_page')
def second_page():
    return render_template_string(second_html)

@app.route('/form_page_2', methods=['GET', 'POST'])
def form_page_2():
    if request.method == 'POST':
        selected_option = request.form.get('response')
        score = empathy_scores['form_page_2'].get(selected_option, 0)
        session['total_score'] += score
        return redirect(url_for('third_page'))
    return render_template_string(form_html2)

@app.route('/third_page')
def third_page():
    return render_template_string(third_html)

@app.route('/form_page_3', methods=['GET', 'POST'])
def form_page_3():
    if request.method == 'POST':
        selected_option = request.form.get('response')
        score = empathy_scores['form_page_3'].get(selected_option, 0)
        session['total_score'] += score
        return redirect(url_for('fourth_page'))
    return render_template_string(form_html3)

@app.route('/fourth_page')
def fourth_page():
    return render_template_string(fourth_html)

@app.route('/form_page_4', methods=['GET', 'POST'])
def form_page_4():
    if request.method == 'POST':
        selected_option = request.form.get('response')
        score = empathy_scores['form_page_4'].get(selected_option, 0)
        session['total_score'] += score
        return redirect(url_for('fifth_page'))
    return render_template_string(form_html4)

@app.route('/fifth_page')
def fifth_page():
    return render_template_string(five_html)

@app.route('/form_page_5', methods=['GET', 'POST'])
def form_page_5():
    if request.method == 'POST':
        selected_option = request.form.get('response')
        score = empathy_scores['form_page_5'].get(selected_option, 0)
        session['total_score'] += score
        return redirect(url_for('result_page'))
    return render_template_string(form_html5)

@app.route('/result_page')
def result_page():
    total_score = session.get('total_score', 0)
    result_text = evaluate_empathy(total_score)
    return render_template_string(result_html_template, total_score=total_score, result_text=result_text)

if __name__ == '__main__':
    ngrok.set_auth_token('2jvMhQfiX7gvbcpkL8pv3Jbsgzg_2uzw5qZS9FXXcUgvLdjfN')
    public_url = ngrok.connect(5000)
    print(" * ngrok tunnel \"{}\" -> \"http://127.0.0.1:5000\"".format(public_url))
    app.run()
