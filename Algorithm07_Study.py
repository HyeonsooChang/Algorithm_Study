#!/usr/bin/env python
# coding: utf-8

# ##### 조건문과 반복문, break를 활용하여 다음 headlines 리스트의 요소들을 130자 크기의 하나의 문자열로 이어 붙이는 코드를 작성하세요.
# ```
# headlines = [
#   "Local Bear Eaten by Man",
#   "Legislature Announces New Laws",
#   "Peasant Discovers Violence Inherent in System",
#   "Cat Rescues Fireman Stuck in Tree",
#   "Brave Knight Runs Away",
#   "Papperbok Review: Totally Triffic"
# ]
# ```

# In[16]:


headlines = [
  "Local Bear Eaten by Man",
  "Legislature Announces New Laws",
  "Peasant Discovers Violence Inherent in System",
  "Cat Rescues Fireman Stuck in Tree",
  "Brave Knight Runs Away",
  "Papperbok Review: Totally Triffic"
]


headlines_v = ''

for i in headlines:
    if i not in headlines_v:
        headlines_v += i
        if len(headlines_v) == 130:
            break
        
headlines_v[:130]
        
    
        


# In[ ]:




