import backoff  # for exponential backoff
import openai

from qafv_model.gpt3_template import GPT3_Template

@backoff.on_exception(backoff.expo, openai.error.RateLimitError)
def completions_with_backoff(**kwargs):
    return openai.Completion.create(**kwargs)

@backoff.on_exception(backoff.expo, openai.error.RateLimitError)
def chat_completions_with_backoff(**kwargs):
    return openai.ChatCompletion.create(**kwargs)

class GPT3_T5_Question_Answering:
    def __init__(self, API_KEY, model_name) -> None:
        self.API_KEY = API_KEY
        self.model_name = model_name
        openai.api_key = API_KEY
        self.gpt3_template = GPT3_Template()

    # used for chat-gpt and gpt-4
    def generate(self, input_string, max_token):
        response = chat_completions_with_backoff(
            model = self.model_name,
            messages=[
                    {"role": "user", "content": input_string}
                ],
            max_tokens = max_token,
            temperature = 0.01,
            top_p = 1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0
        )
        generated_text = response['choices'][0]['message']['content'].strip()
        return generated_text

    def retrieve_evidence(self, question):
        input_string = f'{question}\nRetrieve a Wikipedia article relevant to this question.'
        generated_text = self.generate(input_string, max_token = 512)
        return generated_text
    
    def answer_question(self, question):
        # retrieve evidence
        rationale = self.retrieve_evidence(question).strip()

        # answer question
        predict_answer = {}
        example = f'{rationale}\nQ: {question}\nThe answer is:'
        answer_text = self.generate(example, max_token = 32)
        
        predict_answer['rationale'] = rationale
        predict_answer['answer_text'] = answer_text
        return predict_answer


