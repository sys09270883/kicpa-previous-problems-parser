from tika import parser
import re
import json


START_YEAR = 2016
END_YEAR = 2021


class ProblemParser:
    def __init__(self, answer):
        self.pid_list = []
        self.answer = answer
        self.datum = dict()


    def load(self, year):
        file = 'assets/' + str(year) + '_accounting_problems.pdf'
        return parser.from_file(file)


    def bind(self, year, problem):
        data = dict()

        pid_pos = problem.find('.')
        one_pos = problem.find('①')
        two_pos = problem.find('②')
        three_pos = problem.find('③')
        four_pos = problem.find('④')
        five_pos = problem.find('⑤')
        excep_pos = problem.find('※')
        pid = int(problem[0:pid_pos])

        data['pid'] = pid
        data['description'] = problem[pid_pos+1:one_pos].replace('\n\n', ' ').strip()
        data['p1'] = problem[one_pos+1:two_pos].replace('\n\n', ' ').strip()
        data['p2'] = problem[two_pos+1:three_pos].replace('\n\n', ' ').strip()
        data['p3'] = problem[three_pos+1:four_pos].replace('\n\n', ' ').strip()
        data['p4'] = problem[four_pos+1:five_pos].replace('\n\n', ' ').strip()
        data['p5'] = problem[five_pos+1:].replace('\n\n', ' ').strip()
        if excep_pos != -1:
            data['p5'] = problem[five_pos+1:excep_pos].replace('\n\n', ' ').strip()

        data['answer'] = self.answer[year][pid]

        self.pid_list.append(pid)

        return data


    def dump(self, year, problems):
        data_list = []

        for problem in problems:
            data = self.bind(year, problem)
            if data != None:
                data_list.append(data)

        self.datum[year] = data_list
        file = 'assets/accounting.json'

        with open(file, 'w', encoding='utf-8') as file:
            json.dump(self.datum, file, ensure_ascii=False, indent='\t')


    def cut(self, content):
        if re.search('옳', content) == None:
            return None
        if re.search('위 자료', content) != None:
            return None
        pos = content.find('회계학')
        content = content[0:pos].strip()
        pos = content.find('①')
        if pos == -1 or pos > 120:
            return None
        return content


    def make_json(self):
        for year in range(START_YEAR, END_YEAR):
            content = str(self.load(year)['content']).strip()
            pos_list = []

            for i in range(1, 51):
                pattern = '\n' + str(i) + '.'
                pos = content.find(pattern)
                pos_list.append(content.find(pattern))

            pos = pos_list[0]
            problems = []

            for i in pos_list:
                if pos == i:
                    continue
                sliced = content[pos:i]
                pos = i
                sliced = self.cut(sliced)

                if sliced != None:
                    problems.append(sliced)
            
            self.dump(year, problems)


class AnswerParser:
    def __init__(self):
        self.answer = dict()
        for i in range(2011, 2021):
            self.answer[i] = dict()


    def load(self, year):
        file = 'assets/' + str(year) + '_accounting_answer.pdf'
        return parser.from_file(file)


    def to_number(self, char_num):
        if char_num == '①':
            return 1
        elif char_num == '②':
            return 2
        elif char_num == '③':
            return 3
        elif char_num == '④':
            return 4
        elif char_num == '⑤':
            return 5
        return -1

    
    def cut(self, year, content):
        pos = content.find("회계학")
        content = content[pos:]

        pos = content.find('1')
        content = content[pos:]

        target_lines = content.split('\n')

        for target_line in target_lines:
            if target_line == "":
                continue
            content = target_line.split(' ')
            
            self.answer[year][int(content[0])] = self.to_number(content[1])
            self.answer[year][int(content[3])] = self.to_number(content[4])


    def get_answer(self):
        for year in range(START_YEAR, END_YEAR):
            content = str(self.load(year)['content']).strip()
            content = self.cut(year, content)

        return self.answer
