#세 개의 자연수 A, B, C가 주어질 때 A × B × C를 계산한 결과에 0부터 9까지 
# 각각의 숫자가 몇 번씩 쓰였는지를 구하는 프로그램을 작성

a = 150
b = 266
c = 427

result = list((str(a*b*c)))
result
for i in range(10):
    if str(i) in result:
        print(result.count(str(i)))
    else:
        print(0)



