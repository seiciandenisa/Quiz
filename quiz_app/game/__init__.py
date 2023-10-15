from dataclasses import field, dataclass
from random import shuffle
from typing import List

from quiz_app.api import ApiClient


@dataclass
class Question():
    category: str
    type: str
    difficulty: str
    question: str
    correct_answer: str
    incorrect_answers: List[str]
    answers: List[str] = field(default_factory=list, init=False)

    def check_answer(self, answer: str):
        return answer == self.correct_answer

    def __post_init__(self):
        self.answers.extend(self.incorrect_answers)
        self.answers.append(self.correct_answer)
        shuffle(self.answers)


@dataclass
class Quiz:
    number_of_questions: int
    difficulty: str
    questions: list[Question]
    current_question: int
    number_of_correct_answers: int

    @classmethod
    def create_game(cls, number_of_questions, difficulty, category):
        raw_questions: dict = ApiClient.get_questions(difficulty, number_of_questions, category)
        questions = [Question(**raw_question) for raw_question in raw_questions]
        return Quiz(number_of_questions, difficulty, questions, 0, 0)

    def save(self, request):
        request.session['saved_quiz'] = self

    def stop(self, request):
        del request.session['saved_quiz']

    @classmethod
    def restore(cls, request):
        return request.session.get('saved_quiz')

    def get_question(self):
        question = self.questions[self.current_question]
        self.current_question += 1
        return question

    def check_answer(self, answer):
        if self.questions[self.current_question - 1].correct_answer == answer:
            self.number_of_correct_answers += 1

    def get_result(self):
        return {
            'correct_answers': self.number_of_correct_answers,
            'all_questions': self.number_of_questions
        }
