import DBcm

from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return render_template('base.html')

@app.route('/addPrompts', methods=['POST'])
def addPrompts():
    print('ADD PROMPTS')

    prompt = request.form['promptId']
    response = request.form['responseId']

    db_details = "GENAI.sqlite3"

    # create table
    SQL = """
        create table if not exists db_existing_prompts_tbl (
            id integer not null primary key autoincrement,
            prompt blob not null
        );
    """
    with DBcm.UseDatabase(db_details) as db:
        db.execute(SQL)
    
    # insert
    SQL = """
        INSERT INTO db_existing_prompts_tbl (prompt) 
            VALUES (?);
    """
    with DBcm.UseDatabase(db_details) as db:
        db.execute(SQL, ("Select Transaction Include Purchase Sale Include Realtime",))
        db.execute(SQL, ("Select Transaction Include Book Keeping Include Realtime",))
        db.execute(SQL, ("Select Transaction Include Dividend Include Realtime",))
        db.execute(SQL, ("Select Transaction Include Interest Include Realtime",))
        db.execute(SQL, ("Select Transaction Include Fees Include Realtime",))

    return render_template('toast.html', toast="Frequently Used Prompts Added Successfully")

@app.route('/search', methods=['GET'])
def search():
    print('SEARCH')

    db_details = "GENAI.sqlite3"

    # search
    SQL = """
        SELECT * FROM db_existing_prompts_tbl;
    """
    with DBcm.UseDatabase(db_details) as db:
        db.execute(SQL)
        results = db.fetchall()

    # shorten record output
    # cutoff = 80
    for i, record in enumerate(results):
        # prompt = record[1]
        # lengthRecord = len(prompt)
        # if lengthRecord > cutoff:
        #     results[i] = str(record)[5:cutoff] + "..."
        # else:
        #     results[i] = str(record)[5:-2] + "..."
        results[i] = str(record)[5:-2]
    
    return render_template('modalSearch.html', results=results)

@app.route('/search/<id>', methods=['GET'])
def searchItem(id):
    print('SEARCH ITEM')

    db_details = "GENAI.sqlite3"

    # search
    SQL = """
        SELECT prompt FROM db_existing_prompts_tbl
            WHERE id == ?;
    """
    with DBcm.UseDatabase(db_details) as db:
        db.execute(SQL, id)
        results = db.fetchall()
    
    searchedItem = str(results)[3:-4]
    print(searchedItem)

    return render_template('index.html', prompt=searchedItem, response="")

@app.route('/edit/<selection>', methods=['POST'])
def edit(selection):
    prompt = request.form['promptId']
    updatedPrompt = str(prompt) + " " + str(selection)
    return render_template('index.html', prompt=updatedPrompt)

@app.route('/getEnrichedPrompt', methods=['POST'])
def getEnrichedPrompt():
    print("GET ENRICHED PROMPT")

    prompt = request.form['promptId']
    print(prompt)

    if (prompt == None):
        return render_template('index.html', prompt=prompt, enrichedPrompt="Error: Invalid User Prompt Entered.", response="")
    elif (prompt == ''):
        return render_template('index.html', prompt=prompt, enrichedPrompt="Error: Invalid User Prompt Entered.", response="")
    else:
        enrichedPrompt = "Returned Enriched Prompt for " + str(prompt)
        return render_template('index.html', prompt=prompt, enrichedPrompt=enrichedPrompt, response="")
    
@app.route('/getResponse', methods=['POST'])
def getResponse():
    print("GET RESPONSE")

    prompt = request.form['promptId']
    enrichedPrompt = request.form['enrichedPromptId']

    if (enrichedPrompt == None):
        return render_template('index.html', response="Error: Invalid User Prompt Entered.")
    elif (enrichedPrompt == ''):
        return render_template('index.html', prompt=prompt, enrichedPrompt=enrichedPrompt, response="Error: Invalid User Prompt Entered.")
    else:
        response = "Returned AI Response for " + str(enrichedPrompt)
        return render_template('index.html', prompt=prompt, enrichedPrompt=enrichedPrompt, response=response)

@app.route('/save', methods=['POST'])
def save():
    print('SAVE')

    prompt = request.form['promptId']
    # response = "Returned Response for " + str(prompt)
    response = request.form['responseId']

    db_details = "GENAI.sqlite3"

    # create table
    SQL = """
        create table if not exists db_prompts_responses_tbl (
            id integer not null primary key autoincrement,
            prompt blob not null,
            response blob not null
        );
    """
    with DBcm.UseDatabase(db_details) as db:
        db.execute(SQL)
    
    # insert
    SQL = """
        INSERT INTO db_prompts_responses_tbl (prompt, response) 
            VALUES (?,?);
    """
    with DBcm.UseDatabase(db_details) as db:
        db.execute(SQL, (prompt,response,))

    return render_template('toast.html', toast="Prompt and Response Saved Successfully")

@app.route('/load', methods=['GET'])
def load():
    print('LOAD')

    db_details = "GENAI.sqlite3"

    # load
    SQL = """
        SELECT * FROM db_prompts_responses_tbl;
    """
    with DBcm.UseDatabase(db_details) as db:
        db.execute(SQL)
        results = db.fetchall()

    # shorten record output
    cutoff = 200
    for i, record in enumerate(results):
        prompt = record[1]
        response = record[2]
        lengthRecord = len(prompt) + len(response)
        if lengthRecord > cutoff:
            results[i] = str(record)[0:cutoff] + "..."
        else:
            results[i] = str(record)[0:-2] + "..."
        # results[i] = str(record)
    
    return render_template('modalLoad.html', results=results)

@app.route('/load/<id>', methods=['GET'])
def loadItem(id):
    print('LOAD ITEM')

    db_details = "GENAI.sqlite3"

    # load
    SQL = """
        SELECT * FROM db_prompts_responses_tbl 
            WHERE id == ?;
    """
    with DBcm.UseDatabase(db_details) as db:
        db.execute(SQL, id)
        results = db.fetchone()
    
    loadedItem = str(results)
    record=loadedItem.split(',')
    
    prompt=record[1][2:-1]
    response=record[2][2:-2]

    return render_template('index.html', prompt=prompt, response=response)

@app.route('/resetInput', methods=['GET'])
def resetInput():
    print('RESET Input')
    return render_template('index.html', prompt="", response="")

@app.route('/resetDB', methods=['POST'])
def reset():
    print('RESET DB')

    db_details = "GENAI.sqlite3"

    # delete from db_prompts_responses_tbl table
    SQL = """
        DROP TABLE IF EXISTS db_prompts_responses_tbl;
    """
    with DBcm.UseDatabase(db_details) as db:
        db.execute(SQL)

    # delete from db_existing_prompts_tbl table
    SQL = """
        DROP TABLE IF EXISTS db_existing_prompts_tbl;
    """
    with DBcm.UseDatabase(db_details) as db:
        db.execute(SQL)

    return render_template('toast.html', toast="DB RESET SUCCESSFULLY")

@app.route('/dbDetails', methods=['POST'])
def dbDetails():
    print('DB_DETAILS')

    db_details = "GENAI.sqlite3"

    # db details
    SQL = """
        PRAGMA TABLE_LIST;
    """
    with DBcm.UseDatabase(db_details) as db:
        db.execute(SQL)
        results = db.fetchall()
    
    output = ""
    for record in results:
        output += str(record) + "\n"
    
    return render_template('index.html', prompt="", response=output)

