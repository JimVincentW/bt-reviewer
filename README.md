## Setup

# 1. Clone the repository:

git clone https://github.com/your_username/your_repository.git


# 2. Install the required packages:

pip install -r requirements.txt

# 3. Export the OpenAI API key as an environment variable:

'''bash
export OPENAI_API_KEY=<key>  
'''

# 4. Run the script:

'''bash
python main.py
'''

Enter link of dip.bundestag.de process ("Vorgang")
e.g. https://dip.bundestag.de/vorgang/planungsstand-des-ausbaus-der-lehrter-bahn/302931?f.wahlperiode=20&f.typ=Vorgang&start=25&rows=25&pos=38



### With Docker:
Make sure to set the OPENAI_API_KEY environment variable in your shell before running docker-compose up --build, like this:

'''bash
export OPENAI_API_KEY=your-api-key
docker-compose up --build
'''

This way, the OpenAI API key will be set as an environment variable in the Docker container, and your Python script can use it to make requests to the OpenAI API.


Result in console and results.txt:

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)