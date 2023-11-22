import http.client
import json
import requests
import os
import csv
import time

# Lesson list JSON
lesson_list_json = {"lessonList": ["Adjectives|adjectives1", "Afrikaans days|daysinafrikaans", "Afrikaans months|monthsinafrikaans", "Basic phrases|basicafrikaansphrases", "Colours|colours1", "Communication problems|communicationproblems", "Countries|countries", "Drinks. At the bar ...|drinks1", "Family|family1", "Food words. Fruit|fruit", "Food words. Vegetables|vegetables", "Food words. General|foodwordsgeneral", "All food words|allfoodwords", "Food. General phrases|foodphrases1", "First words|firstwordsinafrikaans", "Future tense. 1|futuretense1", "Future tense. 2|futuretense2", "Introductions|introducingothers", "Modal Verbs|modalverbs", "Negation. 1|negation1", "Negation. 2|negation2", "Negation. 3|negation3", "Numbers. 1 to 10|numbers1to10", "Numbers. 11 to 20|numbers11to20", "Numbers. 1 to 20|numbers1to20", "Parts of the Body|partsofthebody", "Past tense|pasttense1", "Places and Buildings. 1|places1", "Plurals. Regular with E|afrikaanspluralswithe", "Plurals. Regular with S|afrikaanspluralswiths", "Irregular plurals|irregularplurals1", "Questions 1|questions1", "Questions 2|questions2 ", "Shopping|shoppingphrases", "Telling the time. On the hour|tellingthetime", "Telling the time. Half past the hour|tellingthetime1", "Time related phrases|timerelatedphrases", "Time related phrases. 1|timerelatedphrases1", "Travel phrases. General|travelgeneralphrases1", "Travel phrase. Taxi|traveltaxi", "Travel phrasse. Train and bus|traveltrainandbus", "The weather|weather1", "Personal Pronouns|personalpronouns1", "Useful phrases|usefulphrases1", "Word Order|wordorder1", "Vocabulary. Basic Vocab 1|basicvocab1", "Vocabulary. Basic Vocab 2|basicvocab2", "Vocabulary. Basic Vocab 3|basicvocab3", "Vocabulary. Basic Vocab 4|basicvocab4", "Vocabulary. Basic Vocab 5|basicvocab5", "Vocabulary. Basic Vocab 6|basicvocab6"]}

# Send a POST request to the website for each lesson
for lesson_item in lesson_list_json['lessonList']:
    lesson_name, lesson_payload = lesson_item.split('|')
    
    conn = http.client.HTTPSConnection("www.easyafrikaans.com")
    payload = f"lesson={lesson_payload}"
    headers = {
        'Accept': '*/*',
        'Accept-Language': 'en,en-US;q=0.9,en-DE;q=0.8,de-DE;q=0.7,de;q=0.6',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Origin': 'https://www.easyafrikaans.com',
        'Referer': 'https://www.easyafrikaans.com/easyafrikaans/learnmain.html?Lesson=usefulphrases1&?page=easyafrikaans/Useful_Phrases.html',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"'
    }
    conn.request("POST", "/php/getlessondata.php", payload, headers)
    res = conn.getresponse()
    data = res.read().decode("utf-8")

    # Parse the JSON response
    response_data = json.loads(data)

    # Extract the data you need from the JSON response
    lesson_title = response_data.get('lessonTitle', '')
    english_data = response_data.get('lessonEnglishList', [])
    afrikaans_data = response_data.get('lessonForeignList', [])
    sound_links = response_data.get('lessonSoundListSigned', [])

    # Create a folder with the lesson name
    folder_name = lesson_name
    os.makedirs(folder_name, exist_ok=True)

    # Create CSV files for English and Afrikaans phrases
    with open(os.path.join(folder_name, 'english.csv'), 'w', newline='', encoding='utf-8') as english_csv:
        english_writer = csv.writer(english_csv)
        english_writer.writerow(["English Phrase"])
        if isinstance(english_data, list):
            for sentence in english_data:
                english_writer.writerow([sentence.strip()])
        else:
            english_writer.writerow([english_data.strip()])

    with open(os.path.join(folder_name, 'afrikaans.csv'), 'w', newline='', encoding='utf-8') as afrikaans_csv:
        afrikaans_writer = csv.writer(afrikaans_csv)
        afrikaans_writer.writerow(["Afrikaans Phrase"])
        if isinstance(afrikaans_data, list):
            for sentence in afrikaans_data:
                afrikaans_writer.writerow([sentence.strip()])
        else:
            afrikaans_writer.writerow([afrikaans_data.strip()])

    # Download and save the audio files in the folder
    for i, sound_link in enumerate(sound_links, start=1):
        response = requests.get(sound_link)

        if response.status_code == 200:
            # Extract the file name from the URL or provide a custom name
            file_name = os.path.join(folder_name, f'sound_{i}.mp3')

            with open(file_name, 'wb') as sound_file:
                sound_file.write(response.content)
            print(f"Sound {i} saved as {file_name}")
        else:
            print(f"Failed to download Sound {i}")

    # Add a delay of 2 seconds before making the next request
    time.sleep(2)
