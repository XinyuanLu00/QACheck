import os

CODE_DEMO_FIRST = '''Task: to verify a claim, we need to ask a series of simple questions. Here the task is given a claim, generate the first question to ask. This question should be simple enough with a single subject-verb-object structure.

Claim = Superdrag and Collective Soul are both rock bands.
To validate the above claim, the first simple question we need to ask is:
Question = Is Superdrag a rock band?

Claim = Jimmy Garcia lost by unanimous decision to a professional boxer that challenged for the WBO lightweight title in 1995. 
To validate the above claim, the first simple question we need to ask is: 
Question = Who is the professional boxer that challenged for the WBO lightweight title in 1995? 

Claim = The Swan of Catania was taught by the Italian composer Giovanni Furno.
To validate the above claim, the first simple question we need to ask is:
Question = What is the nationality of Giovanni Furno?

Claim = Smith worked on the series The Handmaid's Tale that is based on a novel by Margaret Atwood.
To validate the above claim, the first simple question we need to ask is:
Question = Which novel The Handmaid's Tale is based on?

Claim = The Potomac River runs along the neighborhood where Ashley Estates Kavanaugh's wedding was held.
To validate the above claim, the first simple question we need to ask is:
Question = Where was Ashley Estates Kavanaugh's wedding held?

Claim = Ulrich Walter's employer is headquartered in Cologne.
To validate the above claim, the first simple question we need to ask is:
Question = Who is Ulrich Walter's employer?

Claim = Lars Onsager won the Nobel prize when he was 30 years old.
To validate the above claim, the first simple question we need to ask is:
Question = When Lars Onsager won the Nobel prize?

Claim = [[CLAIM]]
To validate the above claim, the first simple question we need to ask is:
Question = '''

TEXT_DEMO_SUBSEQUENT = '''Claim = Superdrag and Collective Soul are both rock bands.
Here are what we already know:
Question 1 = Is Superdrag a rock band?
Answer 1 = Yes
To validate whether the Claim is true, what question do we still need to ask?
Question 2 = Is Collective Soul a rock band?

Claim = Jimmy Garcia lost by unanimous decision to a professional boxer that challenged for the WBO lightweight title in 1995. 
Here are what we already know:
Question 1 = Who is the professional boxer that challenged for the WBO lightweight title in 1995? 
Answer 1 = Orzubek Nazarov
To validate whether the Claim is true, what question do we still need to ask?
Question 2 = Did Jimmy Garcia lose by unanimous decision to Orzubek Nazarov?

Claim = The Swan of Catania was taught by the Italian composer Giovanni Furno.
Here are what we already know:
Question 1 = What is the nationality of Giovanni Furno?
Answer 1 = Italian
To validate whether the Claim is true, what question do we still need to ask?
Question 2 = Who was taught by Giovanni Furno?

Claim = Smith worked on the series The Handmaid's Tale that is based on a novel by Margaret Atwood.
Here are what we already know:
Question 1 = Which novel The Handmaid's Tale is based on?
Answer 1 = Margaret Atwood
To validate whether the Claim is true, what question do we still need to ask?
Question 2 = Who worked on the series The Handmaid's Tale?

Claim = The Potomac River runs along the neighborhood where Ashley Estates Kavanaugh's wedding was held.
Here are what we already know:
Question 1 = Where was Ashley Estates Kavanaugh's wedding held?
Answer 1 = Christ Church in Georgetown
To validate whether the Claim is true, what question do we still need to ask?
Question 2 = Which river runs along the Christ Church in Georgetown?

Claim = Ulrich Walter's employer is headquartered in Cologne.
Here are what we already know:
Question 1 = Who is Ulrich Walter's employer?
Answer 1 = University of Cologne
To validate whether the Claim is true, what question do we still need to ask?
Question 2 = Where is the University of Cologne headquartered?

Claim = Lars Onsager won the Nobel prize when he was 30 years old.
Here are what we already know:
Question 1 = When Lars Onsager won the Nobel prize?
Answer 1 = 1968
To validate whether the Claim is true, what question do we still need to ask?
Question 2 = When was Lars Onsager born?

Claim = [[CLAIM]]
Here are what we already know:
[[QA_CONTEXTS]]
To validate whether the Claim is true, what question do we still need to ask?
Question [[Q_INDEX]] = '''

CODE_DEMO_SUBSEQUENT = '''Claim = Superdrag and Collective Soul are both rock bands.
To validate the above claim, we need to ask the following simple questions sequentially: 
Question 1 = Is Superdrag a rock band?
Answer 1 = Yes
Question 2 = Is Collective Soul a rock band?

Claim = Jimmy Garcia lost by unanimous decision to a professional boxer that challenged for the WBO lightweight title in 1995. 
To validate the above claim, we need to ask the following simple questions sequentially: 
Question 1 = Who is the professional boxer that challenged for the WBO lightweight title in 1995? 
Answer 1 = Orzubek Nazarov
Question 2 = Did Jimmy Garcia lose by unanimous decision to Orzubek Nazarov?

Claim = The Swan of Catania was taught by the Italian composer Giovanni Furno.
To validate the above claim, we need to ask the following simple questions sequentially: 
Question 1 = What is the nationality of Giovanni Furno?
Answer 1 = Italian
Question 2 = Who was taught by Giovanni Furno?

Claim = Smith worked on the series The Handmaid's Tale that is based on a novel by Margaret Atwood.
To validate the above claim, we need to ask the following simple questions sequentially:
Question 1 = Which novel The Handmaid's Tale is based on?
Answer 1 = Margaret Atwood
Question 2 = Who worked on the series The Handmaid's Tale?

Claim = The Potomac River runs along the neighborhood where Ashley Estates Kavanaugh's wedding was held.
To validate the above claim, we need to ask the following simple questions sequentially:
Question 1 = Where was Ashley Estates Kavanaugh's wedding held?
Answer 1 = Christ Church in Georgetown
Question 2 = Which river runs along the Christ Church in Georgetown?

Claim = Ulrich Walter's employer is headquartered in Cologne.
To validate the above claim, we need to ask the following simple questions sequentially:
Question 1 = Who is Ulrich Walter's employer?
Answer 1 = University of Cologne
Question 2 = Where is the University of Cologne headquartered?

Claim = Lars Onsager won the Nobel prize when he was 30 years old.
To validate the above claim, we need to ask the following simple questions sequentially: 
Question 1 = When Lars Onsager won the Nobel prize?
Answer 1 = 1968
Question 2 = When was Lars Onsager born?

Claim = [[CLAIM]]
To validate the above claim, we need to ask the following simple questions sequentially: 
[[QA_CONTEXTS]]'''

TEXT_ZEROSHOT_SUBSEQUENT = '''Claim = [[CLAIM]]
Here are what we already know:
[[QA_CONTEXTS]]
To validate whether the Claim is true, what question do we still need to ask?
Question [[Q_INDEX]] = '''

# based on the information given
CODE_ZEROSHOT_STOP = '''Claim = [[CLAIM]]
To validate the above claim, we have asked the following questions:
[[QA_CONTEXTS]]
Can we know whether the claim is true or false now?
Answer = '''

CODE_DEMO_STOP = '''Claim = Superdrag and Collective Soul are both rock bands.
To validate the above claim, we have asked the following questions: 
Question 1 = Is Superdrag a rock band?
Answer 1 = Yes
Can we know whether the claim is true or false now?
Prediction = No, we cannot know. 

Claim = Superdrag and Collective Soul are both rock bands.
To validate the above claim, we have asked the following questions: 
Question 1 = Is Superdrag a rock band?
Answer 1 = Yes
Question 2 = Is Collective Soul a rock band?
Answer 2 = Yes
Can we know whether the claim is true or false now?
Prediction = Yes, we can know.

Claim = Jimmy Garcia lost by unanimous decision to a professional boxer that challenged for the WBO lightweight title in 1995. 
To validate the above claim, we have asked the following questions:
Question 1 = Who is the professional boxer that challenged for the WBO lightweight title in 1995? 
Answer 1 = Orzubek Nazarov
Can we know whether the claim is true or false now?
Prediction = No, we cannot know.

Claim = Jimmy Garcia lost by unanimous decision to a professional boxer that challenged for the WBO lightweight title in 1995. 
To validate the above claim, we have asked the following questions:
Question 1 = Who is the professional boxer that challenged for the WBO lightweight title in 1995? 
Answer 1 = Orzubek Nazarov
Question 2 = Did Jimmy Garcia lose by unanimous decision to Orzubek Nazarov?
Can we know whether the claim is true or false now?
Prediction = Yes, we can know.

Claim = The Swan of Catania was taught by the Italian composer Giovanni Furno.
To validate the above claim, we have asked the following questions: 
Question 1 = What is the nationality of Giovanni Furno?
Answer 1 = Italian
Can we know whether the claim is true or false now?
Prediction = No, we cannot know.

Claim = Lars Onsager won the Nobel prize when he was 30 years old.
To validate the above claim, we have asked the following questions:  
Question 1 = When Lars Onsager won the Nobel prize?
Answer 1 = 1968
Can we know whether the claim is true or false now?
Prediction = No, we cannot know.

Claim = Smith worked on the series The Handmaid's Tale that is based on a novel by Margaret Atwood. 
To validate the above claim, we have asked the following questions:
Question 1 = Which novel The Handmaid's Tale is based on?
Answer 1 = Margaret Atwood
Can we know whether the claim is true or false now?
Prediction = No, we cannot know.

Claim = Smith worked on the series The Handmaid's Tale that is based on a novel by Margaret Atwood. 
To validate the above claim, we have asked the following questions:
Question 1 = Which novel The Handmaid's Tale is based on?
Answer 1 = Margaret Atwood
Question 2 = Did Smith work on the series The Handmaid's Tale?
Answer 2 = Yes
Can we know whether the claim is true or false now?
Prediction = Yes, we can know.

Claim = The first season of the series The Handmaid's Tale was released in 2017.
To validate the above claim, we have asked the following questions:
Question 1 = When was the first season of the series The Handmaid's Tale released?
Answer 1 = 2017
Can we know whether the claim is true or false now?
Prediction = Yes, we can know.

Claim = [[CLAIM]]
To validate the above claim, we have asked the following questions:
[[QA_CONTEXTS]]
Can we know whether the claim is true or false now?
Prediction = '''

class GPT3_Template:
    def __init__(self) -> None:
        self.QG_template_start = CODE_DEMO_FIRST
        self.QG_template_followup = CODE_DEMO_SUBSEQUENT
        self.can_we_stop = CODE_DEMO_STOP

    def fill_can_we_step_question(self, claim, qa_contexts):
        example = self.can_we_stop.replace('[[CLAIM]]', claim.strip())
        qa_contexts_txt = ''
        for idx, (ques, ans) in enumerate(qa_contexts):
            qa_contexts_txt += f'Question {idx+1} = {ques}\nAnswer {idx+1} = {ans}\n'
        example = example.replace('[[QA_CONTEXTS]]', qa_contexts_txt.strip())
        return example

    def fill_QG_template_start(self, claim):
        example = self.QG_template_start.replace('[[CLAIM]]', claim.strip())
        return example

    def fill_QG_template_followup(self, claim, qa_contexts):
        example = self.QG_template_followup.replace('[[CLAIM]]', claim.strip())
        
        qa_contexts_txt = ''
        for idx, (ques, ans) in enumerate(qa_contexts):
            qa_contexts_txt += f'Question {idx+1} = {ques}\nAnswer {idx+1} = {ans}\n'

        ## for CODE_DEMO_SUBSEQUENT
        Q_index = str(len(qa_contexts)+1)
        qa_contexts_txt += f'Question {Q_index} ='
        example = example.replace('[[QA_CONTEXTS]]', qa_contexts_txt.strip())

        return example

