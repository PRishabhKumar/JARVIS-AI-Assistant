import pymongo


client = pymongo.MongoClient("mongodb://localhost:27017/")

db = client['JARVIS']

collection = db['JARVISCollection']

# APPS

# calculator = {"name": "calculator", "path":"C:\\Windows\\System32\\calc.exe"}
# chrome = {"name": "chrome", "path": "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"}
# notepad = {"name": "notepad", "path": "C:\\Windows\\notepad.exe"}
# vs_code = {"name":"vs code", "path": "C:\\Users\\risha\\AppData\\Local\\Programs\\Microsoft VS Code\\bin\code"}
# file_explorer = {"name": "file explorer", "path": "C:\\Windows\\explorer.exe"}
# msWord = {"name": "ms word", "path": "C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\Word.lnk"}
# excel = {"name":"excel", "path":"C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\Excel.lnk"}
# powerpoint = {"name":"powerpoint", "path":"C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\PowerPoint.lnk"}
# onenote = {"name":"one note", "path":"C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\OneNote.lnk"}
# # WEBSITES

# google = {"name":"google", "path":"https://www.google.com/"}
# youtube = {"name":"youtube", "path":"https://www.youtube.com/"}
# vtop = {"name":"vtop", "path":"https://vtop.vit.ac.in/vtop/open/page"}
# ssst = {"name":"ssst", "path":"https://www.sai.org.in/"}
# irctc = {"name":"irctc", "path":"https://www.irctc.co.in/nget/train-search"}
# chatgpt = {"name":"chatgpt", "path":"https://chatgpt.com/"}
# linkedin = {"name":"linkedin", "path":"https://www.linkedin.com/feed/?trk=guest_homepage-basic_google-one-tap-submit"}
# instagram = {"name":"instagram", "path":"https://www.instagram.com/"}
# facebook = {"name":"facebook", "path":"https://www.facebook.com/"}


# #apps
# collection.insert_one(calculator)
# collection.insert_one(chrome)
# collection.insert_one(notepad)
# collection.insert_one(vs_code)
# collection.insert_one(file_explorer)
# collection.insert_one(msWord)
# collection.insert_one(excel)
# collection.insert_one(powerpoint)
# collection.insert_one(onenote)
# #websites
# collection.insert_one(google)
# collection.insert_one(youtube)
# collection.insert_one(vtop)
# collection.insert_one(ssst)
# collection.insert_one(irctc)
# collection.insert_one(chatgpt)
# collection.insert_one(linkedin)
# collection.insert_one(instagram)
# collection.insert_one(facebook)


contacts = {
    "Mummy": "9723466281",
    "Daddy": "9924942884",
    "Rajvi Didi": "7698931176",
    "Aastha Didi": "6352983352",
    "Pratham": "7284864096",
    "Harsita": "9265318783"
}

for name, number in contacts.items():
    collection.insert_one({"name":name, "number":number}) # add every item one by one in the database
    
    