import queue

if __name__ == '__main__':
    q = queue.Queue()
    n = int(input())
    for i in range(n):
        temp = list(map(int, input().split()))
        if temp[0] == 1:
            q.put(temp[1])
        elif temp[0] == 2:
            if not q.empty():
                print(q.get())