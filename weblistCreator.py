import pickle

dic = {"facebook": "https://www.facebook.com", "youtube": "https://www.youtube.com",
       "gmail": "https://www.gmail.com", 'bu': "https://bux.bracu.ac.bd/dashboard"}

with open("./DataBase/Other/webList.p", "wb") as f:
    pickle.dump(dic, f)

print(dic)
