from flask import Flask,render_template,request,url_for,redirect,flash,abort,session , jsonify
import json
import os.path
from werkzeug.utils import secure_filename

app = Flask(__name__) 
app.secret_key = 'this is a secret key hi hello bye'

@app.route('/') 
def home():        
    return render_template('home.html',codes = session.keys()) 
    

@app.route('/your-url', methods=['GET','POST'])
def your_url():
    if request.method == 'POST':
        urls = {}
        if os.path.exists('urls.json'):
            with open('urls.json') as urls_file:
                urls = json.load(urls_file)
        if request.form['code'] in urls.keys(): 
            flash('That short name has been taken .Pls select another ')
            return redirect(url_for('home'))
        
        if 'url' in request.form.keys():
             urls[request.form['code']] = {'url':request.form['url']}
        else:
            f = request.files['file']
            full_name = request.form['code'] + secure_filename(f.filename)
            f.save('C:/Users/sushr/OneDrive/Desktop/Projects/linkedin flask/static/user_files/'+ full_name)
            urls[request.form['code']] = {'file':full_name}

        with open('urls.json','w') as urls_file:
            json.dump(urls,urls_file)
            session[request.form['code']] = True
            
        return render_template('your_url.html',code = request.form  ['code'])
    else:
        return redirect(url_for('home'))
    
@app.route('/<string:code>')
def redirect_to_url(code):
    if os.path.exists('urls.json'):
        with open('urls.json') as urls_file:
            urls = json.load(urls_file)
            if code in urls.keys():
        
                if 'url' in urls[code].keys():
                    return  redirect(urls[code]['url'])
                else:
                    return redirect(url_for('static',filename = '/user_files/' + urls[code]['file']))
    return abort(404)     

@app.errorhandler(404)      
def page_not_found(error):
    return render_template('page_not_found.html'),404

@app.route('/api')
def session_api():
    return jsonify(list(session.keys()))

if __name__ == '__main__':
    app.run(debug=True)