import pandas as pd
import csv

def categorize_grammy_awards(input_data):
    categories = set([row['category'] for row in input_data])
    
    macro_categories = {
        'OfTheYear': [],
        'PopDanceElectronic': [],
        'RockMetalAlternative': [],
        'RnBRapSpokenWordPoetry': [],
        'JazzTraditionalPopContemporaryInstrumentalMusicalTheater': [],
        'CountryAmericanRoots': [],
        'GospelContemporaryChristian': [],
        'LatinGlobalReggaeNewAgeAmbientChant': [],
        'ChildrensComedyAudioBooksVisualMediaMusicVideoFilm': [],
        'PackageNotesHistorical': [],
        'ProductionEngineeringCompositionArrangement': [],
        'Classical': [],
        'Other': []
    }
    
    for category in categories:
        category_lower = category.lower()

        if 'OfTheYear' in category or category.endswith('OfTheYear') or 'bestnewartist' in category_lower:
            macro_categories['OfTheYear'].append(category)
        
        elif ('pop' in category_lower or 'dance' in category_lower or 
            'electronic' in category_lower):
            macro_categories['PopDanceElectronic'].append(category)
            
        elif ('rock' in category_lower or 'metal' in category_lower or 
              'alternative' in category_lower):
            macro_categories['RockMetalAlternative'].append(category)
            
        elif ('r&b' in category_lower or 'randb' in category_lower or 
              'rap' in category_lower or 'hip hop' in category_lower or 
              'spoken word' in category_lower or 'poetry' in category_lower):
            macro_categories['RnBRapSpokenWordPoetry'].append(category)
            
        elif ('jazz' in category_lower or 'traditional pop' in category_lower or 
              'contemporary instrumental' in category_lower or 
              'musical theater' in category_lower or 'theatre' in category_lower):
            macro_categories['JazzTraditionalPopContemporaryInstrumentalMusicalTheater'].append(category)
            
        elif ('country' in category_lower or 'americana' in category_lower or 
              'bluegrass' in category_lower or 'folk' in category_lower or 
              'american roots' in category_lower):
            macro_categories['CountryAmericanRoots'].append(category)
            
        elif ('gospel' in category_lower or 'christian' in category_lower or 
              'religious' in category_lower):
            macro_categories['GospelContemporaryChristian'].append(category)
            
        elif ('latin' in category_lower or 'global' in category_lower or 
              'world' in category_lower or 'reggae' in category_lower or 
              'new age' in category_lower or 'ambient' in category_lower or 
              'chant' in category_lower):
            macro_categories['LatinGlobalReggaeNewAgeAmbientChant'].append(category)
            
        elif ('children' in category_lower or 'comedy' in category_lower or 
              'audio book' in category_lower or 'audiobook' in category_lower or 
              'visual media' in category_lower or 'music video' in category_lower or 
              'film' in category_lower):
            macro_categories['ChildrensComedyAudioBooksVisualMediaMusicVideoFilm'].append(category)
            
        elif ('package' in category_lower or 'notes' in category_lower or 
              'historical' in category_lower or 'history' in category_lower):
            macro_categories['PackageNotesHistorical'].append(category)
            
        elif ('production' in category_lower or 'engineering' in category_lower or 
              'engineered' in category_lower or 'composition' in category_lower or 
              'arrangement' in category_lower or 'arranging' in category_lower):
            macro_categories['ProductionEngineeringCompositionArrangement'].append(category)
            
        elif 'classical' in category_lower or 'opera' in category_lower or 'orchestra' in category_lower:
            macro_categories['Classical'].append(category)
            
        else:
            macro_categories['Other'].append(category)
    
    macro_categories = {k: v for k, v in macro_categories.items() if v}
    
    with open('C:\\Users\\fgall\\Desktop\\MELODY\\csv\\GrammyCategoriesUppercase.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Macro Genre', 'Sub Genres'])
        for macro, categories in macro_categories.items():
            writer.writerow([macro, str(categories)])
    
    return macro_categories



df = pd.read_csv('C:\\Users\\fgall\\Desktop\\MELODY\\csv\\the_grammy_awards_mapped_uppercase.csv')
data = df.to_dict('records')

result = categorize_grammy_awards(data)

print("\nRisultato della categorizzazione:")
for macro, categories in result.items():
    print(f"\n{macro}:")
    for category in categories:
        print(f"  - {category}")