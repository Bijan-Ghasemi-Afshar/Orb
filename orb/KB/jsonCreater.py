import json

data = {}  
data['trainingData'] = []
data['trainingData'].append({  
    "class":"General", 
    "sentence":"how are you?"

})
data['trainingData'].append({
    "class":"General", 
    "sentence":"how is your day?"
})
data['trainingData'].append({
    "class":"General", 
    "sentence":"good day"
})
data['trainingData'].append({
    "class":"General", 
    "sentence":"how is it going today?"
})
data['trainingData'].append({
    "class":"General", 
    "sentence":"what day is it?"
})
data['trainingData'].append({
    "class":"General",
     "sentence":"hello"
})
data['trainingData'].append({
    "class":"General",
     "sentence":"i'm hungry"
})
data['trainingData'].append({
    "class":"General", 
    "sentence":"what time is it?"
})

with open('trainingData.json', 'w') as outfile:  
    json.dump(data, outfile)