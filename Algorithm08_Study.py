#!/usr/bin/env python
# coding: utf-8

# ##### 장바구니에 아래와 같은 과일이 들어있고 과일 판별 리스트가 있습니다. 현재 장바구니에는 과일이 몇개이고 과일이 아닌 것은 몇개인지 출력하세요.
# 
# ```
# basket_items = {'apples': 4, 'oranges': 19, 'kites': 3, 'sandwiches': 8}
# fruits = ['apples', 'oranges', 'pears', 'peaches', 'grapes', 'bananas']
# ```

# In[18]:


'''
예시 출력)
과일은 23개이고, 11개는 과일이 아닙니다..
'''

basket_items = {'apples': 4, 'oranges': 19, 'kites': 3, 'sandwiches': 8}
fruits = ['apples', 'oranges', 'pears', 'peaches', 'grapes', 'bananas']

sum1 = 0
sum2 = 0

for i in basket_items:
    if i in fruits:
        sum1 += basket_items.get(i)
    else:
        sum2 += basket_items.get(i)
        
print(sum1)
print(sum2)

