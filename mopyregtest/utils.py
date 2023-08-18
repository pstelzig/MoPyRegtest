"""
MoPyRegtest: A Python enabled simple regression testing framework for Modelica models.

Copyright (c) Dr. Philipp Emanuel Stelzig, 2019--2023.

MIT License. See the project's LICENSE file.
"""

def ask_confirmation(question, max_asks=5):
    answer = None

    for q in range(0, max_asks):
        print("{} [yes|no] ".format(question), end="")
        answer_as_str = input()

        if answer_as_str.strip().lower() == "yes":
            answer = True
            break
        elif answer_as_str.strip().lower() == "no":
            answer = False
            break

    if answer is None:
        raise ValueError("Answer to question \"{}\" not understood. ".format(question))

    return answer


def replace_in_str(repl_str, repl_dict):
    for k, v in repl_dict.items():
        repl_str = repl_str.replace(k, v)

    return repl_str


def replace_in_file(filename, repl_dict):
    fhandle = open(str(filename), 'r')
    contents = fhandle.read()
    fhandle.close()

    contents = replace_in_str(contents, repl_dict)

    fhandle = open(str(filename), 'w')
    fhandle.truncate()
    fhandle.write(contents)
    fhandle.close()

    return