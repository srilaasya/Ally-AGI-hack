from flask import Flask, render_template, request, jsonify, redirect

import os
import glob
import openai
import requests
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    input_url = request.json['input']
    print(f"Received input: {input_url}")

    input_url_css = "https://libreboot.org/news/libreboot20230423.html"
    input_url_html = "http://pnwx.com"

    # Process the input as needed
    if input_url == input_url_html:
        r = requests.get(input_url_html, allow_redirects=True)
        open('temp.html', 'wb').write(r.content)

        print(type(r.content), r.content.decode('utf-8'))
        string_content = r.content.decode('utf-8')

        initial_prompt = """
        You are an accessibility expert at Twitter where you work on making the website more accessible to people with visual disorders.
        I'm going to pass in an HTML file to you that is not optimised for people with visual disabilities and your job is to create an equivalent HTML file for people with the visual disorders.
        Create an alternate HTML file and include comments in the HTML file wherever you make changes. Make sure to preserve the original positioning of elements in the HTML page like whitespaces and tables.
        Definitely make the following changes - contrast ratio between text and its background should be at least 4.5:1 for normal text and 3:1 for large text (18pt or 14pt bold).
        Make sure to remove any background images, use a light background and a high contrast between text and background. Further, generic generic alt text fields for all images.
        """

        messages = [{"role": "system", "content": initial_prompt}, {"role": "user", "content": string_content}]
        print("api request sent to openai")
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages= messages,
            temperature=1,
            top_p=1,
            frequency_penalty=0.0,
            presence_penalty=0.0,
        )

        # Open the file in write mode and truncate its contents
        with open("temp.html", "w") as html_file:
            html_file.truncate()

        # Open the file in append mode
        with open("temp.html", "a") as html_file:
            # Write the new CSS code to the file
            html_file.write(response["choices"][0]["message"]["content"])

    if input_url == input_url_css:
        # get CSS files
        r = requests.get(input_url_css, allow_redirects=True)
        open('temp.css', 'wb').write(r.content)

        print(type(r.content), r.content.decode('utf-8'))
        string_content = r.content.decode('utf-8')

        css_files = glob.glob(os.path.join(input_url, "*.css"))
        # css_files

        with open(css_files[0], 'r') as file:
            # Read the contents of the file
            css_contents = file.read()

        initial_prompt = """
        You are an accessibility expert at Twitter where you work on making the website more accessible to people with visual disorders.
        I’m going to pass in an HTML file to you that is not optimised for people with visual disabilities and your job is to update the CSS file for people with the mentioned disabilities.
        Create an alternate CSS file and include comments in the CSS file wherever you make changes.
        """

        messages = [{"role": "system", "content": initial_prompt}, {"role": "user", "content": css_contents}]

        response = openai.ChatCompletion.create(
        model="gpt-4",
        messages= messages,
        temperature=1,
        top_p=1,
        frequency_penalty=0.0,
        presence_penalty=0.0,
        )

        # Open the file in write mode and truncate its contents
        with open(css_files[0], "w") as css_file:
            css_file.truncate()

        # Open the file in append mode
        with open(css_files[0], "a") as css_file:
            # Write the new CSS code to the file
            css_file.write(response["choices"][0]["message"]["content"])

    return redirect("/render")

@app.route('/render', methods=['GET'])
def render():
    return render_template('app/temp.html')

if __name__ == '__main__':
    app.run(debug=True)