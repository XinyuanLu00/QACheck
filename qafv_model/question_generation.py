import backoff  # for exponential backoff
import openai

from .gpt3_template import GPT3_Template

@backoff.on_exception(backoff.expo, openai.error.RateLimitError)
def completions_with_backoff(**kwargs):
    return openai.Completion.create(**kwargs)

@backoff.on_exception(backoff.expo, openai.error.RateLimitError)
def chat_completions_with_backoff(**kwargs):
    return openai.ChatCompletion.create(**kwargs)

class GPT3_Question_Generator:
    def __init__(self, API_KEY, model_name) -> None:
        self.API_KEY = API_KEY
        self.model_name = model_name
        openai.api_key = API_KEY
        self.gpt3_template = GPT3_Template()

    # used for chat-gpt and gpt-4
    def generate(self, input_string):
        response = chat_completions_with_backoff(
            model = self.model_name,
            messages=[
                    {"role": "user", "content": input_string}
                ],
            max_tokens = 64,
            temperature = 0.01,
            top_p = 1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0
        )
        generated_text = response['choices'][0]['message']['content'].strip()
        return generated_text

    def generate_first_question(self, claim):
        example = self.gpt3_template.fill_QG_template_start(claim)
        generated_text = self.generate(example)
        return generated_text

    def generate_next_question(self, claim, qa_contexts):
        example = self.gpt3_template.fill_QG_template_followup(claim, qa_contexts)
        generated_text = self.generate(example)
        print(generated_text)
        return generated_text