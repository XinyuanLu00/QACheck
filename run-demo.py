import argparse
from flask import (Flask, flash, jsonify, make_response, redirect, render_template, request, url_for)

app = Flask(__name__)
debug = True
dataset = None

from qafv_model.fact_checker import QAFV_Fact_Checker
##########################################################################
FLAGS = 0

parser = argparse.ArgumentParser()
parser.add_argument("--model_name", default = 'gpt-4', type=str)
parser.add_argument("--API_KEY", required=True, type=str, help="API key for GPT3")
args = parser.parse_args()

fact_checker = QAFV_Fact_Checker(args)

contexts_history = []
prediction_with_rationale = ""
current_claims = []
##########################################################################

def get_fresh_data(number=5):
    output_list = ["Ulrich Walter's employer is headquartered in Cologne.",
                   "Winter's Tale was the creation of a French poet.", 
                   "Donald Trump and Joe Biden were born in the same state.",
                   "Lars Onsager won the Nobel prize when he was 30 years old."]
    return output_list

@app.route('/')
def index():
    return redirect(url_for('home'))

@app.route('/home')
def home():
    global FLAGS
    global contexts_history
    global prediction_with_rationale
    global current_claims
    current_claims = get_fresh_data(5)
    contexts_history = []
    prediction_with_rationale = ""
    FLAGS = 0
    return render_template('index.html', claims=current_claims,
                            selected_claim = "",
                            contexts_history = contexts_history, 
                            prediction_with_rationale = prediction_with_rationale, 
                            flags = FLAGS)

def show_results():
    global FLAGS
    global contexts_history
    global prediction_with_rationale
    global current_claims
    group_choice = request.form.getlist('group-choice')
    # no selection for user
    if len(group_choice) == 0:
        return render_template('index.html', claims = current_claims,
                            selected_claim = "",
                            contexts_history = contexts_history, 
                            prediction_with_rationale = prediction_with_rationale, 
                            flags = FLAGS)
    
    claim_text = ""
    # when user selected a question
    if group_choice[0] == 'select_question':
        question_index = int(request.form['question-choices'])
        claim_text = current_claims[question_index]
    # when user inputed a question
    elif group_choice[0] == 'custom_question':
        claim_text = request.form.get('self-input', '')
    else:
        raise NotImplementedError
    
    print('Generating outputs from model ...')
    prediction_with_rationale, contexts_history = fact_checker.verify_single_claim_GPT3(claim_text)
    print(prediction_with_rationale, contexts_history)
    return claim_text

def clear_results():
    global FLAGS
    global contexts_history
    global prediction_with_rationale
    global current_claims
    contexts_history = []
    prediction_with_rationale = ""
    FLAGS = 0
    current_claims = get_fresh_data(5)

@app.route('/submit', methods=['POST'])
def submit():
    global FLAGS
    selected_claim = ""
    if FLAGS == 0:
        selected_claim = show_results()
        FLAGS = 1 # change flag
    elif FLAGS == 1:
        clear_results()
        FLAGS = 0 # change flag

    # return redirect(url_for('home_with_output', model_output=model_output))
    return render_template('index.html', claims = current_claims,
                            selected_claim = selected_claim, 
                            contexts_history = contexts_history, 
                            prediction_with_rationale = prediction_with_rationale, 
                            flags = FLAGS)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)