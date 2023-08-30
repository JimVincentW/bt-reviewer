import os
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
import PyPDF2
import openai
import json
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import ChatPromptTemplate
from langchain.callbacks import StdOutCallbackHandler

# Set your OpenAI API key and organization ID
openai.organization = "org-MCbDxK9vjStYvGK3l9vZnNao"
openai.api_key = os.getenv("OPENAI_API_KEY")
GPT4 = 'gpt-4-0314'
MODEL_NAME = GPT4

# Check OpenAI model availability
def check_model_availability():
    model_list = openai.Model.list()['data']
    model_ids = [x['id'] for x in model_list]
    if MODEL_NAME not in model_ids:
        print(f'Model {MODEL_NAME} is not available.')
        exit()

# Scrape and download documents
def extract_info(driver):
    # Extract information from the Übersicht section
    uebersicht = driver.find_element(By.ID, 'content-übersicht')
    initiative = uebersicht.find_element(By.XPATH, '//label[text()="Initiative:"]/following-sibling::span').text
    beratungsstand = uebersicht.find_element(By.XPATH, '//label[text()="Beratungsstand:"]/following-sibling::span').text
    
    # Extract information from the Wichtige Drucksachen and Plenum sections
    wichtige_drucksachen = []
    plenum = []
    documents = driver.find_elements(By.XPATH, '//label[text()="Wichtige Drucksachen"]/following-sibling::ul/li')

    for doc in documents:
        date = doc.find_element(By.XPATH,'./div/div').text
        title = doc.find_element(By.XPATH,'./div/div/a').text
        link = doc.find_element(By.XPATH,'./div/div/a').get_attribute('href')
        if 'BT-Drucksache' in title:
            wichtige_drucksachen.append({'date': date, 'title': title, 'link': link})
        elif 'BT-Plenarprotokoll' in title:
            plenum.append({'date': date, 'title': title, 'link': link})
    
    return {
        'initiative': initiative,
        'beratungsstand': beratungsstand,
        'wichtige_drucksachen': wichtige_drucksachen,
        'plenum': plenum
    }

def download_file(url, date):
    doc_type = date.split('(')[1].split()[0]
    local_filename = f'Drucksachen/{doc_type}.pdf'
    
    # Create the Drucksachen folder if it doesn't exist
    if not os.path.exists('Drucksachen'):
        os.makedirs('Drucksachen')
    
    try:
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(local_filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
    except requests.exceptions.RequestException as e:
        print(f"Error downloading file: {e}")
        return None
    
    return local_filename

# Process each document file
def process_documents():
    with open('fragenkatalog.json', 'r', encoding='utf-8') as file:
        fragenkatalog = json.load(file)

    document_files = [f for f in os.listdir('Drucksachen') if f.endswith('.pdf')]

    handler = StdOutCallbackHandler()
    llm = ChatOpenAI(temperature=0, model='gpt-4-0314', streaming=True)

    template = ChatPromptTemplate.from_messages([
        ("system", "Du bist juristischer Referent des Bundestages."),
        ("human", "Bitte beantworte diesen Fragenkatalog zu dem angehängten Dokument in angemessener Knappheit. Um die Fragen zu beantworten arbeite bitte in Stichpunkten."),
        ("ai", "Alles klar, was sind die Fragen?"),
        ("human", "Die Fragen: {questions}. \n\nSei bitte so konkret wie möglich."),
        ("ai", "Okay, was ist das Dokument?"),
        ("human", "Das Dokument: {document}")
        ,
    ])

    chain = LLMChain(llm=llm, prompt=template, callbacks=[handler])

    for document_file in document_files:
        document_type, _ = os.path.splitext(document_file)
        questions = fragenkatalog['DokumentTypen'].get(document_type)
        if questions is None:
            print(f'No questions found for document type: {document_type}')
            continue
        questions_str = '\n'.join(questions)

        document_path = os.path.join('Drucksachen', document_file)
        with open(document_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            document_text = ''
            for page_num in range(len(list(reader.pages))):
                page = reader.pages[page_num]
                document_text += page.extract_text()

        result = chain.run({
            'document': document_text,
            'questions': questions_str
        })
        print(result)
        print("**********************")

        with open('results.txt', 'a') as f:
            f.write('******NEUES DOKUMENT*******************************************************+\n')
            f.write(f'Document: {document_file}\n')
            f.write(f'Fragenkatalog für: {document_type}\n')
            f.write('Fragen:\n')
            f.write(questions_str)
            f.write('\n\LLM:\n')
            f.write(str(result))

        # Delete the document file
        os.remove(document_path)

# Main function
if __name__ == '__main__':
    check_model_availability()
    
    url = input("Bundestag Vorganslink:")
    driver = webdriver.Firefox()

    try:
        # Navigate to the page
        driver.get(url)
        # Wait for the page to load completely
        driver.implicitly_wait(10)
        # Extract the information
        info = extract_info(driver)
        # Download wichtige_drucksachen documents
        for doc in info['wichtige_drucksachen']:
            url = doc['link']
            date = doc['date']
            local_filename = download_file(url, date)
            if local_filename:
                print(f'Downloaded {local_filename}')
            else:
                print(f'Failed to download document: {url}')

    finally:
        # Close the browser window
        driver.quit()
    
    process_documents()
