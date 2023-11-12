import backoff  # for exponential backoff
import openai
import random

from .gpt3_template import GPT3_Template

@backoff.on_exception(backoff.expo, openai.error.RateLimitError)
def completions_with_backoff(**kwargs):
    return openai.Completion.create(**kwargs)

@backoff.on_exception(backoff.expo, openai.error.RateLimitError)
def chat_completions_with_backoff(**kwargs):
    return openai.ChatCompletion.create(**kwargs)

class Fact_Reasoner:
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

    def claim_verification(self, claim, qa_contexts):
        qa_contexts_txt = ''
        for ques, ans in qa_contexts:
            qa_contexts_txt += f'Q: {ques}\nA: {ans}\n'
        
        # template = f'''Based on the above information, is it true that {claim[:-1]}? \n Options: (A) True (B) False (C) Impossible to tell \n A: Let's think step by step.'''
        template = f'''Based on the above information, is it true that {claim[:-1]}? True, false, or neither? \n A: Let's think step by step.'''
        example = f'{qa_contexts_txt}\n{template}'.strip()
        
        out = self.generate(example, max_token = 256)
        return out

    def map_prediction(self, prediction):
        prediction = prediction.lower().strip()
        refutes_indicator = ["no", "false"]
        supports_indicator = ["yes", "true"]
        
        for indicator in refutes_indicator:
            if prediction.find(indicator) >= 0:
                return 'refutes'
        
        for indicator in supports_indicator:
            if prediction.find(indicator) >= 0:
                return 'supports'
        
        return random.sample(['supports', 'refutes'], 1)[0]

    # A more stable claim verification that first list all evidence gathered and then do chain-of-thoughts
    def CoT_claim_verification(self, claim, qa_contexts):
        # convert each q-a pair into a statement
        statements = []
        for ques, ans in qa_contexts:
            example = f'''Question = {ques}\nAnswer = {ans}\nConvert the above question-answer pair into a statement.'''
            statement = self.generate(example, max_token = 64)
            statements.append(statement)
        evidence = ' '.join(statements)
        
        # verify the claim with CoT
        template = f'''{claim} Is this claim true or false? \n\n Answer: {evidence} Therefore, the final answer is: '''
        prediction = self.generate(template, max_token = 8)
        
        # get the final label
        label = self.map_prediction(prediction)
        label_map = {'supports': 'True', 'refutes': 'False'}
        label_str = label_map[label]
        explanation = f'{evidence} Therefore, the final answer is: {label_str}.'
        return explanation

    def is_information_sufficient(self, claim, qa_contexts):
        def map_text_to_label(raw_text):
            indicators = ['yes, we can know']
            for indicator in indicators:
                if raw_text.lower().find(indicator) >= 0:
                    return True
            return False

        example = self.gpt3_template.fill_can_we_step_question(claim, qa_contexts)
        raw_output = self.generate(example, max_token = 32)
        prediction = map_text_to_label(raw_output)
        return prediction