from flask import Flask, render_template, url_for, request, redirect
import pandas as pd
import os
import sys
import logging
import logging.handlers

logger = logging.getLogger('kumologging')
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
logger.addHandler(ch)

def create_json(state):
    # Load the dataframe
    target = os.path.join(app.static_folder, 'cleaned_campaign_finance.csv')
    df = pd.read_csv(target)

    # Filter the df by state
    filtered_by_state = df[df['candidate_state'] == state]

    # Create nodes
    committees = pd.DataFrame({'id': filtered_by_state['comittee_name'].unique(), 'group': 1})
    candidates = pd.DataFrame({'id': filtered_by_state['candidate_name'].unique(), 'group': 2})
    nodes = pd.concat([committees,candidates], axis=0, join='outer', ignore_index=True)

    # Create links
    links = pd.DataFrame(filtered_by_state.groupby(['comittee_name','candidate_name'], as_index=False)['transaction_amount'].sum())
    links.columns = ['source','target','value']

    # Create json
    links_list = links.to_dict(orient='records')
    nodes_list = nodes.to_dict(orient='records')
    state_dict = {'links': links_list}
    state_dict['nodes'] = nodes_list

    return state_dict

states = {
    'AL': 'Alabama',
    'AK': 'Alaska',
    'AZ': 'Arizona',
    'AR': 'Arkansas',
    'CA': 'California',
    'CO': 'Colorado',
    'CT': 'Connecticut',
    'DE': 'Delaware',
    'FL': 'Florida',
    'GA': 'Georgia',
    'HI': 'Hawaii',
    'ID': 'Idaho',
    'IL': 'Illinois',
    'IN': 'Indiana',
    'IA': 'Iowa',
    'KS': 'Kansas',
    'KY': 'Kentucky',
    'LA': 'Louisiana',
    'ME': 'Maine',
    'MD': 'Maryland',
    'MA': 'Massachusetts',
    'MI': 'Michigan',
    'MN': 'Minnesota',
    'MS': 'Mississippi',
    'MO': 'Missouri',
    'MT': 'Montana',
    'NE': 'Nebraska',
    'NV': 'Nevada',
    'NH': 'New Hampshire',
    'NJ': 'New Jersey',
    'NM': 'New Mexico',
    'NY': 'New York',
    'NC': 'North Carolina',
    'ND': 'North Dakota',
    'OH': 'Ohio',
    'OK': 'Oklahoma',
    'OR': 'Oregon',
    'PA': 'Pennsylvania',
    'RI': 'Rhode Island',
    'SC': 'South Carolina',
    'SD': 'South Dakota',
    'TN': 'Tennessee',
    'TX': 'Texas',
    'UT': 'Utah',
    'VT': 'Vermont',
    'VA': 'Virginia',
    'WA': 'Washington',
    'WV': 'West Virginia',
    'WI': 'Wisconsin',
    'WY': 'Wyoming',
    'DC': 'District of Columbia',
    'AS': 'American Samoa',
    'GU': 'Guam',
    'MP': 'Northern Mariana Islands',
    'PR': 'Puerto Rico',
    'UM': 'United States Minor Outlying Islands',
    'VI': 'U.S. Virgin Islands'
    }

app = Flask(__name__)

@app.route("/")
def flaskapp():
    return render_template("index.html")

@app.route('/network/<selected_state>', methods=['GET', 'POST'])
def network(selected_state):
    state_network = create_json(selected_state)
    selected_state_long = states.get(selected_state)

    return render_template('network.html',
        len = len(states),
        states = states,
        data = state_network,
        selected_state = selected_state,
        selected_state_long = selected_state_long)

@app.route('/candidates')
def candidates():
    return render_template('candidates.html')

@app.route('/committees')
def committees():
    return render_template('committees.html')

if __name__ == "__main__":
    app.run(debug = True, use_reloader=True)


