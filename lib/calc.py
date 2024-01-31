def gcd(x: int, y: int):
  while y != 0:
    (x, y) = (y, x % y)
  return x

def lcm(x: int, y: int):
  return (x * y) / gcd(x, y)

def reduced_fraction(N: int, D: int):
  c = gcd(N, D)
  return (int(N/c), int(D/c))

def plus(A: tuple, B: tuple):
  common_denominator = lcm(A[1], B[1])
  AN = A[0] * common_denominator / A[1]
  BN = B[0] * common_denominator / B[1]
  return reduced_fraction(AN + BN, common_denominator)

def multiply(A: tuple, B: tuple):
  return reduced_fraction(A[0] * B[0], A[1] * B[1])

def divide(A: tuple, B: tuple):
  return multiply(A, (B[1], B[0]))

def reversed_text(text: str):
  return text[::-1]