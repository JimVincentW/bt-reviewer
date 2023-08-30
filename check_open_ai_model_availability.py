import openai
import pprint

openai.organization = "org-MCbDxK9vjStYvGK3l9vZnNao"
openai.api_key = "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"

GPT4 = 'gpt-4-0314'
MODEL_NAME = GPT4
model = openai.Model(MODEL_NAME)

def list_all_models():
    model_list = openai.Model.list()['data']
    model_ids = [x['id'] for x in model_list]
    model_ids.sort()
    pprint.pprint(model_ids)

if __name__ == '__main__':
    list_all_models()