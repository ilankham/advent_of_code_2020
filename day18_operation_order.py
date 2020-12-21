""" Solutions for https://adventofcode.com/2020/day/18 """

# import modules used below.
from collections import UserString
from itertools import chain


# Part 1: After evaluating each arithmetic expression in the provided data
# file, with + and * having the same level of operator precedence, what is the
# sum of the resulting values?


# Create data model for arithmetic expressions.
class ArithmeticExpression(UserString):
    """ Data Model for arithmetic expressions """

    @property
    def tokenized(self):
        """ Return fully tokenized self, delimited by spaces and parentheses"""
        split_by_dlm = self.split(' ')

        tokenized_values = []
        for token in split_by_dlm:
            if token[0] == '(':
                for position, _ in enumerate(token):
                    if token[position] == '(':
                        tokenized_values.append('(')
                    else:
                        tokenized_values.append(token[position:])
                        break
            elif token[-1] == ')':
                for position, _ in enumerate(token):
                    if token[-1*(position+1)] != ')':
                        tokenized_values.append(token[:-1*position])
                        tokenized_values.extend(
                            list(')'*position)
                        )
                        break
            else:
                tokenized_values.append(token)
        return tokenized_values

    def evaluate_using_precedence(self, precedence=None):
        """ Evaluate self as arithmetic expression with given precedence """

        if precedence is None:
            precedence = {1: {'*', '/'}, 2: {'+', '-'}}

        def evaluate(expression):
            all_operators = set(
                chain.from_iterable(v for v in precedence.values())
            )
            subexpressions = []
            expression_position = 0
            expression_length = len(expression)
            while expression_position < expression_length:
                token = expression[expression_position]
                if token.isdigit():
                    subexpressions.append(int(token))
                elif token in all_operators:
                    subexpressions.append(token)
                elif token == '(':
                    delimit_start = expression_position + 1
                    delimiter_count = 1
                    while delimiter_count != 0:
                        expression_position += 1
                        token = expression[expression_position]
                        if token == '(':
                            delimiter_count += 1
                        elif token == ')':
                            delimiter_count -= 1
                    subexpressions.append(
                        evaluate(expression[delimit_start:expression_position])
                    )
                expression_position += 1

            evaluations = []
            for level in precedence:
                evaluations.append(subexpressions[0])
                current_operator = ''
                for token in subexpressions[1:]:
                    if token in precedence[level]:
                        current_operator = token
                    elif isinstance(token, int) and current_operator != '':
                        evaluations[-1] = eval(
                            f'{evaluations[-1]}'
                            f'{current_operator}'
                            f'{token}'
                        )
                        current_operator = ''
                    else:
                        evaluations.append(token)
                subexpressions = evaluations
                evaluations = []

            return subexpressions[0]

        return evaluate(self.tokenized)

# Read and evaluate arithmetic expressions from data file for Part 1.
expressions = []
evaluations1 = []
with open('data/day18_operation_order-data.txt') as fp:
    for line in fp:
        expressions.append(
            ArithmeticExpression(line.rstrip())
        )
        evaluations1.append(
            ArithmeticExpression(line.rstrip()).evaluate_using_precedence(
                {1: {'+', '*'}}
            )
        )

# Find sum of evaluated arithmetic expressions for Part 1.
print(
    f'Number of arithmetic expressions in data file: '
    f'{len(expressions)}'
)
print(
    f'Sum of evaluated arithmetic expressions for Part 1: '
    f'{sum(evaluations1)}'
)


# Part 2: After evaluating each arithmetic expression in the provided data
# file, with + having higher precedence than *, what is the sum of the
# resulting values?


# Read arithmetic expressions from data file for Part 2.
evaluations2 = []
for exp in expressions:
    evaluations2.append(exp.evaluate_using_precedence({1: {'+'}, 2: {'*'}}))

# Find sum of evaluated arithmetic expressions for Part 2.
print(
    f'Sum of evaluated arithmetic expressions for Part 2: '
    f'{sum(evaluations2)}'
)
