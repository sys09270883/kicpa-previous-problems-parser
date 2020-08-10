from parsers import ProblemParser, AnswerParser

answer_parser = AnswerParser()
answer = answer_parser.get_answer()

problem_parser = ProblemParser(answer)
problem_parser.make_json()
