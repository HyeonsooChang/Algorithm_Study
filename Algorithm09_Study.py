#나누어 떨어지는 숫자 배열 (프로그래머스)

def solution(arr, divisor):
    answer = []
    for i in range(len(arr)):
        if arr[i] % divisor == 0:
            answer.append(arr[i])
    if len(answer) == 0:
        answer.append(-1)
    else:
        answer.sort()
    return answer


#두 정수 사이의 합 (프로그래머스)

def solution(a, b):
    answer = 0
    if a<b:
        for i in range(a,b+1):
            answer += i
    else:
        for i in range(b, a+1):
            answer += i
    return answer