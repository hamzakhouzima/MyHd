# import pandas as pd
# import requests
# import json 



# def fetch_siren_code(departement_code):
#     url =  'https://api.pappers.fr/v2/recherche'
#     sirens = []
#     departement_code = departement_code
#     params = {
#         'api_token'  : '8e1208fbdf2ceac4824859264e3f4c9c3cad69062dfc3484',
#         'departement' : departement_code
         
#     }
#     response = requests.get(url, params=params)
#     response_json = response.json()
#     response_data = response_json['resultats'] 
#     print(response_json)
    
#     for i in response_data:
#         siren = i.get('siren','None')
#         sirens.append(siren)
        
    
#     return sirens
    
    
    
# #########################################


# def fetch_data(siren):
    
    
#     url = 'https://api.pappers.fr/v2/entreprise'

#     siren = siren
#     params = {
    
#     'api_token' : '8e1208fbdf2ceac4824859264e3f4c9c3cad69062dfc3484',
#     # 'q' : 'ENGIE'
#     'siren' : siren,
   

    
#     }

    
#     response = requests.get(url, params=params)
#     # print(response.status_code)
#     # input('')
#     response_json = response.json()
#     print(response_json)
#     print('####')
#     # print(response_json['resultats'])
#     # input('')
#     # response_data = response_json['resultats']
#     data = response_json
#     return data
# ###############################################################

# def define_schema(siren):
#     data = fetch_data(siren)
#     entry = {
#         'nom_entreprise': data.get('nom_entreprise', "None"),
#         'siren': data.get('siren', "None"),
#         'siret': data['siege'].get('siret', "None"),
#         'date_creation': data.get('date_creation', "None"),
#         'codeAPE': data.get('code_naf', "None"),
#         'domaine_activite': data.get('domaine_activite', "None"),
#         'activite': data.get('activite', "None"),
#         'forme_juridique': data.get('forme_juridique', "None"),
#         'tva_intra': data.get('numero_tva_intracommunautaire', "None"),
#         'capitalsocial': data.get('capital', "None"),
#         'effectif': data.get('effectif', "None"),
#         'nic': data['siege'].get('nic', "None"),
#         'numero_rcs' : data.get('numero_rcs', "None"),  
#         'objet_social': data.get('objet_social', "None"),
#         'filiale': data['siege'].get('siege', "None"), #fillial
#         'diffusable': data.get('diffusable', "None"),
#         'statut': "None",
#         'addresse1': data['siege'].get('adresse_ligne_1', "None"),
#         'addresse2': data['siege'].get('adresse_ligne_2', "None"),
#         'ville': data['siege'].get('ville', "None"),
#         'codePostal': data['siege'].get('code_postal', "None"),
#         'pays': data['siege'].get('pays', "None"),
#         # 'phone':data['association'].get('telephone', "None"),
#         'phone':"None",
#         'fax': "None",
#         'siteWeb': "None",
#         # 'emailPrincipal': data['association'].get('email', "None"),
#         'emailPrincipal': "None",
#         # 'date_bilan': data.get('date_debut_activite'),
#         'date_bilan': "None",
#         # 'chiffre_affaires': data.get('chiffre_affaires', "None"),
#         'chiffre_affaires': "None",
#         'annee_chiffre_affaires': "None",
#         'dateCreditSafe': "None",
#         'limit_csafe': "None",
#         'score_csafe': "None",
#         'score_intcsafe': "None",
#         'FbAccount': "None",
#         'LinkedIn': "None",
#         'source': "None",
#     }
#     return entry

# departements = ['65']
# departement_sirens=[]
# #this function must take an argument of departement 
# for num,i in enumerate(departements):
#     single_departement = fetch_siren_code(i)
#     departement_sirens.append(single_departement)
#     big_array = [define_schema(siren) for siren in departement_sirens]
#     df = pd.DataFrame(big_array)
#     df.to_excel(f'departement_num_{num}-B2B.xlsx', index=False)
#     print(f'departement  num {num} is fetched')
#     departement_sirens.clear()  
    
        


import pandas as pd
import requests

def fetch_siren_code(departement_code):
    url = 'https://api.pappers.fr/v2/recherche'
    sirens = []
    params = {
        'api_token': '8e1208fbdf2ceac4824859264e3f4c9c3cad69062dfc3484',
        'departement': departement_code,
        'tranche_effectif_min':'10'
    }
    response = requests.get(url, params=params)
    response_json = response.json()
    response_data = response_json.get('resultats', [])
    
    for item in response_data:
        siren = item.get('siren', 'None')
        sirens.append(siren)
    
    return sirens

def fetch_data(siren):
    url = 'https://api.pappers.fr/v2/entreprise'
    params = {
        'api_token': '8e1208fbdf2ceac4824859264e3f4c9c3cad69062dfc3484',
        'siren': siren
    }
    response = requests.get(url, params=params)
    response_json = response.json()
    
    return response_json

def define_schema(data,dep):
    entry = {
        'nom_entreprise': data.get('nom_entreprise', 'None'),
        'siren': data.get('siren', 'None'),
        'siret': data['siege'].get('siret', 'None'),
        'date_creation': data.get('date_creation', 'None'),
        'codeAPE': data.get('code_naf', 'None'),
        'domaine_activite': data.get('domaine_activite', 'None'),
        'activite': data.get('activite', 'None'),
        'forme_juridique': data.get('forme_juridique', 'None'),
        'tva_intra': data.get('numero_tva_intracommunautaire', 'None'),
        'capitalsocial': data.get('capital', 'None'),
        'effectif': data.get('effectif', 'None'),
        'nic': data['siege'].get('nic', 'None'),
        'numero_rcs': data.get('numero_rcs', 'None'),  
        'objet_social': data.get('objet_social', 'None'),
        'filiale': data['siege'].get('siege', 'None'), #fillial
        'diffusable': data.get('diffusable', 'None'),
        'statut': 'None',
        'adresse1': data['siege'].get('adresse_ligne_1', 'None'),
        'adresse2': data['siege'].get('adresse_ligne_2', 'None'),
        'ville': data['siege'].get('ville', 'None'),
        'codePostal': data['siege'].get('code_postal', 'None'),
        'pays': data['siege'].get('pays', 'None'),
        'phone': 'None',
        'fax': 'None',
        'siteWeb': 'None',
        'emailPrincipal': 'None',
        'date_bilan': 'None',
        'chiffre_affaires': 'None',
        'annee_chiffre_affaires': 'None',
        'dateCreditSafe': 'None',
        'limit_csafe': 'None',
        'score_csafe': 'None',
        'score_intcsafe': 'None',
        'FbAccount': 'None',
        'LinkedIn': 'None',
        'source': 'None',
        'departement' : dep,
    }
    return entry

departements = ['62']
departement_sirens = []

for num, departement in enumerate(departements):
    single_departement = fetch_siren_code(departement)
    departement_sirens.extend(single_departement)
    
    big_array = [define_schema(fetch_data(siren),departement) for siren in departement_sirens]
    df = pd.DataFrame(big_array)
    df.to_excel(f'departement_num_{departement}-B2B.xlsx', index=False)
    print(f'Departement num {departement} is fetched successfully')
    
    departement_sirens.clear()
