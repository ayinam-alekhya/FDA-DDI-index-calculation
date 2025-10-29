from flask import Flask, render_template, request
import pandas as pd
import os
import re
import numpy as np
from itertools import permutations

app = Flask(__name__, static_folder='static')
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'xlsx', 'xls'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

df = pd.DataFrame()


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    return render_template('final.html')



@app.route('/', methods=['GET', 'POST'])
def upload_file():
    global df  # Use the global variable df
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'file' not in request.files:
            return redirect(request.url)

        file = request.files['file']
    
        if file.filename == '':
            return redirect(request.url)
    
        if file and allowed_file(file.filename):
            filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filename)
            
            # Process the Excel file
            df = pd.read_excel(filename, usecols=['Reactions', 'Suspect Product Active Ingredients', 'Suspect Product Names', 'Concomitant Product Names'])
    
            # Convert relevant columns to lowercase
            df['Reactions'] = df['Reactions'].str.lower()
            # Combine the three columns into a new column separated by semicolons, excluding columns with "-"
            df['Combined Column'] = np.where(
                df['Suspect Product Names'] == '-',
                df['Suspect Product Active Ingredients'],
                np.where(
                    df['Suspect Product Active Ingredients'] == '-',
                    df['Suspect Product Names'],
                    df['Suspect Product Names'] + ';' + df['Suspect Product Active Ingredients']
                )
            )
            
            df['Combined Column'] = np.where(
                df['Concomitant Product Names'] == '-',
                df['Combined Column'],
                np.where(
                    df['Combined Column'] == '-',
                    df['Concomitant Product Names'],
                    df['Combined Column'] + ';' + df['Concomitant Product Names']
                )
            )
            
            df['Combined Column'] = df['Combined Column'].str.lower()
            
            # # Create an XML string from the DataFrame
            # xml_content = df.to_xml(index=False)
            
            # # Specify the file path and name
            # upload_folder = app.config['UPLOAD_FOLDER']
            # xml_filename = os.path.join(upload_folder, 'combined_data.xml')
            
            # # Write the XML content to the file
            # with open(xml_filename, 'w') as xml_file:
            #     xml_file.write(xml_content)
            
            complete_string = ';'.join(df['Combined Column']).split(';')
    
            all_drugs = set(complete_string)
            sorted_drugs = sorted(list(all_drugs))

            return render_template('final.html', unique_drugs=sorted_drugs)

    return render_template('final.html', error=None)

@app.route('/select_drug', methods=['POST'])
def select_drug():
    global df  # Use the global variable df
    if request.method == 'POST':
        selected_drug1 = request.form.get('selected_drug1')
        selected_drug2 = request.form.get('selected_drug2')
        selected_drug3 = request.form.get('selected_drug3')
        selected_drugs = [selected_drug1, selected_drug2, selected_drug3]
        selected_drugs = [drug for drug in selected_drugs if drug]
        target_values = []
        for i, drug in enumerate(selected_drugs):
            target_values.append(drug.lower())  # Add lowercase individual drug
            for other_drug in selected_drugs[i + 1:]:
                # Add combinations of selected drugs
                target_values.append(drug.lower() + ";" + other_drug.lower())
                target_values.append(other_drug.lower() + ";" + drug.lower()) 
        
        for permuted_drugs in permutations(selected_drugs):
            target_values.append(";".join(permuted_drugs).lower())
        target_values = list(set(target_values))
            
        # target_values=['vancomycin']
        target_pattern = '|'.join(map(re.escape, target_values))
        # Filter the DataFrame based on lowercase columns for the specified values
        filtered_vancomycin_aki_df = df[
            (df['Reactions'].str.contains('acute kidney injury', na=False)) &
            (df['Combined Column'].str.fullmatch('|'.join(target_values), na=False))
        ]
        
        # filtered_vancomycin_df = df[
        #     (df['Reactions'].str.contains('acute kidney injury', na=False)) &
        #     (
        #         (df['Suspect Product Active Ingredients'].str.contains('vancomycin', na=False)) |
        #         (df['Suspect Product Active Ingredients'].str.contains('vancomycin hydrochloride', na=False))
        #     )
        # ]
        
        # # Remove rows where other drugs are mentioned
        # filtered_vancomycin_df = filtered_vancomycin_df[
        #     ~filtered_vancomycin_df['Suspect Product Active Ingredients'].str.contains(r'\b(?<!vancomycin)(?<!vancomycin hydrochloride)(?! hydrochloride)\b', na=False, regex=True)
        # ]

        
        # Count the number of cases
        count_acute_kidney_injury_vancomycin = filtered_vancomycin_aki_df.shape[0]
        n11 = count_acute_kidney_injury_vancomycin
        
        #Filter the DataFrame based on lowercase columns
        filtered_vancomycin_and_other_aki_df = df[
            (df['Reactions'].str.contains('acute kidney injury', na=False)) &
            (df['Combined Column'].str.contains(target_pattern, na=False, regex=True))
        ]
        
        
        count_acute_kidney_injury_vancomycin_and_others = filtered_vancomycin_and_other_aki_df.shape[0]-filtered_vancomycin_aki_df.shape[0]
        n21 = count_acute_kidney_injury_vancomycin_and_others
        
        # Filter the DataFrame based on lowercase columns for the specified values
        filtered_vancomycin_w_o_aki_df = df[
            ~df['Reactions'].str.contains('acute kidney injury', na=False) &
            (df['Combined Column'].str.fullmatch('|'.join(target_values), na=False))
        ]
        
        count_w_o_acute_kidney_injury_vancomycin = filtered_vancomycin_w_o_aki_df.shape[0]
        n12 = count_w_o_acute_kidney_injury_vancomycin
        
        filtered_vancomycin_and_other_w_o_aki_df = df[
            ~df['Reactions'].str.contains('acute kidney injury', na=False) &            
            (df['Combined Column'].str.contains(target_pattern, na=False, regex=True))
        ]
        
        count_w_o_acute_kidney_injury_vancomycin_and_others = filtered_vancomycin_and_other_w_o_aki_df.shape[0]-filtered_vancomycin_w_o_aki_df.shape[0]
        n22 = count_w_o_acute_kidney_injury_vancomycin_and_others
        
        # Filter the DataFrame based on the "Reactions" column
        filtered_df = df[df['Reactions'].str.contains('Acute Kidney Injury', case=False, na=False)]

        # Count the number of cases with "Acute Kidney Injury"
        count_acute_kidney_injury = filtered_df.shape[0]
        association_rules = os.path.join(app.config['UPLOAD_FOLDER'], 'arules.xlsx')
        dm = pd.read_excel(association_rules)

        table_html = dm.to_html(classes='table table-striped', index=False)

        
        
        #ROR= n12*n21/(n22*n11)
        if(n22 == 0 or n11 == 0):
            if(n11==0):
                reporting_odds_ratio = "There may be no value with the selected drug/drugs alone."
            elif(n22==0):
                reporting_odds_ratio = "There may be no value without acute kidney injury with selected drugs."
        else:
            reporting_odds_ratio = (n12*n21)/(n22*n11) 
        

        return render_template('final.html', message='File uploaded and processed successfully!', 
                               count_acute_kidney_injury=count_acute_kidney_injury,
                               count_acute_kidney_injury_vancomycin=count_acute_kidney_injury_vancomycin,
                               count_w_o_acute_kidney_injury_vancomycin=count_w_o_acute_kidney_injury_vancomycin,
                               count_acute_kidney_injury_vancomycin_and_others=count_acute_kidney_injury_vancomycin_and_others,
                               count_w_o_acute_kidney_injury_vancomycin_and_others=count_w_o_acute_kidney_injury_vancomycin_and_others,
                               reporting_odds_ratio=reporting_odds_ratio,s1=selected_drug1,s2=selected_drug2,s3=selected_drug3,
                               table=table_html)

    #return render_template('index.html', message='Invalid file format. Please upload an Excel file.')

            
        return render_template('result.html', selected_drug=selected_drug, ror=ror)


if __name__ == '__main__':
    #os.environ['FLASK_APP'] = 'main.py'
    #os.environ['FLASK_DEBUG'] = '0'  # Set to '0' if you don't want debug mode
    app.run(debug=True, port=5001)

