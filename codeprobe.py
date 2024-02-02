import streamlit as st
from bs4 import BeautifulSoup
from Wappalyzer import Wappalyzer, WebPage
import requests
import jsbeautifier
import re

def scrape_website(url):
    # Function to scrape the website content
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    return str(soup)

def extract_css_from_html(html_code):
    # Function to extract CSS styles from HTML code
    styles = set()
    soup = BeautifulSoup(html_code, 'html.parser')
    style_tags = soup.find_all('style')

    for style_tag in style_tags:
        css_content = style_tag.get_text()
        extracted_styles = re.findall(r'{(.*?)}', css_content, re.DOTALL)
        styles.update(extracted_styles)

    return styles

def extract_js_from_html(html_code):
    # Function to extract JavaScript code from HTML
    scripts = set()
    soup = BeautifulSoup(html_code, 'html.parser')
    script_tags = soup.find_all('script')

    for script_tag in script_tags:
        js_content = script_tag.get_text()
        scripts.add(js_content)

    return scripts

def beautify_js(js_code):
    # Function to beautify JavaScript code
    beautified_code = jsbeautifier.beautify(js_code)
    return beautified_code

def extract_code_from_tag(html_code, tag_name, language):
    # Function to extract code snippets from HTML based on a given tag
    code_snippets = set()
    soup = BeautifulSoup(html_code, 'html.parser')
    code_tags = soup.find_all(tag_name)

    for code_tag in code_tags:
        code_content = code_tag.get_text()
        code_snippets.add((code_content, language))

    return code_snippets

def learn_links(technology):
    # Function to provide learning links for different technologies
    learning_links = {
        "HTML": "https://developer.mozilla.org/en-US/docs/Web/HTML",
        "CSS": "https://developer.mozilla.org/en-US/docs/Web/CSS",
        "JavaScript": "https://developer.mozilla.org/en-US/docs/Web/JavaScript",
        # Add more technologies and corresponding learning links as needed
    }

    return learning_links.get(technology, "No learning link available.")

def main():
    st.title("Website Analyzer")

    # Ask user for URL
    url = st.text_input("Enter website URL:")
    
    # Track whether the analysis has been performed
    analysis_performed = st.button("Analyze")

    if analysis_performed:
        try:
            # Scrape website
            html_code = scrape_website(url)

            # Display in expandable sections
            with st.expander("HTML Code", expanded=False):
                st.code(html_code[:5000], language='html')  # Truncate to first 5000 characters

            with st.expander("CSS Code", expanded=False):
                css_code = extract_css_from_html(html_code)
                for style in css_code:
                    st.code(style, language='css')

            with st.expander("JavaScript Code", expanded=False):
                js_code = extract_js_from_html(html_code)
                for js in js_code:
                    beautified_js = beautify_js(js)
                    st.code(beautified_js, language='javascript')

            # Display code for other languages
            with st.expander(get_code_expander_name(html_code), expanded=False):
                # Extract code from various HTML tags
                code_snippets = set()
                code_snippets.update(extract_code_from_tag(html_code, 'script', 'javascript'))
                code_snippets.update(extract_code_from_tag(html_code, 'style', 'css'))

                for code, language in code_snippets:
                    st.code(code, language=language)

            # Learn tab
            with st.expander("Learn"):
                st.write("Free Learning Resources:")
                for tech in ["HTML", "CSS", "JavaScript"]:
                    learn_link = learn_links(tech)
                    st.write(f"- Learn {tech}: {learn_link}")

                st.write("- Web Development: [MDN Web Docs](https://developer.mozilla.org/en-US/docs/Web)")
                st.write("- W3Schools: [W3Schools Online Web Tutorials](https://www.w3schools.com/)")
                st.write("- freeCodeCamp: [freeCodeCamp](https://www.freecodecamp.org/)")

        except Exception as e:
            st.error(f"An error occurred: {e}")

def get_code_expander_name(html_code):
    # Function to determine the name of the code expander based on the presence of 'script' or 'style' in HTML code
    if 'script' in html_code or 'style' in html_code:
        return "Function code"
    else:
        return "No Function code"

if __name__ == "__main__":
    main()
