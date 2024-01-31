from lib.calc import reduced_fraction, plus, multiply, divide, reversed_text

ops = ['+', '*', '/']
vrs = ['a', 'c', 'g', 't']

store = {}


def is_op(c: str) -> bool:
  return ops.count(c) > 0

def is_vr(c: str) -> bool:
  return vrs.count(c) > 0

def parse_case(text: str) -> bool | int:
  if (text.startswith('case ')):
    return int(text[5:])
  return False

def parse_fraction(text: str) -> str | bool:
  if ((parse_case(text) != False) or is_op(text[len(text)-1])):
    return False
  texts = text.split('=')
  [N, D] = texts[1].split('/')
  store[texts[0]] = reduced_fraction(int(N), int(D))

def parse_onp(text: str) -> str | bool:
  if (not is_op(text[len(text)-1])):
    return False
  texts = text.split('=')
  store[texts[0]] = parse_expression(reversed_text(texts[1]))


def parse_expression(exp: str):
  left = None
  right = None
  op = None
  in_right = False
  in_left = False
  left_name = ''
  right_name = ''
  
  for i in range(len(exp)):
    c = exp[i]

    if (op == None and is_op(c)):
      op = c
      in_right = True
      continue

    if (op == None and not in_right and c == '_'):
      in_right = True
      continue

    if (op != None and is_op(c)):
      if (in_left):
        right = store[right_name]
        left = parse_expression(exp[i:])
      else:
        right = parse_expression(exp[i:])

        dash_count = 0
        j = i + 1
        while j < len(exp) and not is_op(exp[j]):
          if (exp[j] == '_' and dash_count > 0):
            break
          if (exp[j] == '_'):
            dash_count += 1
          j = j + 1

        left = parse_expression(exp[j:])

      return calc(left, right, op)
    
    if (in_right and c == '_'):
      if (i == len(exp) - 1):
        return store[right_name]
      
      in_right = False
      in_left = True
      continue
    
    if (in_left and c == '_'):
      in_left = False
      return calc(store[left_name], store[right_name], op)

    if (in_right and is_vr(c)):
      right_name = c + right_name
      continue
    
    if (in_left and is_vr(c)):
      left_name = c + left_name
      continue
    

def calc(left: tuple, right: tuple, op: str):
  if (op == '+'):
    return plus(left, right)
  if (op == '*'):
    return multiply(left, right)
  if (op == '/'):
    return divide(left, right)
  return (-1, -1)



if __name__ == "__main__":
  with open('./input.txt') as f:
    content = f.read()

  words = content.split('\n')
  words.reverse()

  results = []
  for word in words:
    parse_fraction(word)
    parse_onp(word)
    case_number = parse_case(word)

    if case_number != False:
      results.append({"case": case_number, "answer": store})
      store = {}

  results.reverse()
  for res in results:
    print(f'case {res['case']} Y')
    answer =  sorted(res['answer'].items())
    
    for ans in answer:
      print(f'{ans[0]} {ans[1][0]} {ans[1][1]}')

