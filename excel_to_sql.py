import mysql.connector
import pandas as pd 

try:
    cnx = mysql.connector.connect(
        host='127.0.0.1',
        user='root',
        password='',
        database='py_connection'
    )
    print("Connection established successfully.")

    try:
        cursor = cnx.cursor()
        print("Cursor created successfully.")
        
    except mysql.connector.Error as err:
        print("Error creating cursor:", err)


except mysql.connector.Error as err:
    print("Error during connection:", err)

    
df = pd.read_excel('contact_result_table.xlsx')
column_names = df.columns.tolist()
# print(len(column_names))
# input('')

original_data_types = df.dtypes.tolist()



column_data_types = ['VARCHAR(255)' if dtype == 'object' else 'VARCHAR(255)' if dtype == 'int64' else 'VARCHAR(255)' if dtype=='datetime64[ns]' else 'VARCHAR(255)' if dtype=='float64' else 'VARCHAR(255)' if dtype=='bool' else dtype.name for dtype in original_data_types]

# column_definitions = ', '.join([f'{col} {data_type}' for col, data_type in zip(column_names, column_data_types)])
# column_definitions = '`nom_entreprise`, `siren`, `siret`, `date_creation`, `codeAPE`, `domaine_activite`, `activite`, `forme_juridique`, `tva_intra`, `capitalsocial`, `effectif`, `nic`, `numero_rcs`, `objet_social`, `filiale`, `diffusable`, `statut`, `addresse1`, `addresse2`, `ville`, `codePostal`, `pays`, `phone`, `fax`, `siteWeb`, `emailPrincipal`, `date_bilan`, `chiffre_affaires`, `annee_chiffre_affaires`, `dateCreditSafe`, `limit_csafe`, `score_csafe`, `score_intcsafe`, `FbAccount`, `LinkedIn`, `source` ,`departement`'
column_definitions = 'prenom,nom,email,emailPerso,linkedIn,phone,mobile,adresse1,adresse2,code_postal,ville,pays,job,dateAnnivairsaire,socialAccount,source'

# print(f'this is column def{column_definitions}')
# input('')
for row in df.itertuples(index=False):
    values = [str(value) if not pd.isna(value) else None for value in row]

    insert_query = f"""
    INSERT INTO contact ({column_definitions})
    VALUES ({', '.join(['%s'] * len(column_names))})
    """
    # values = row
    cursor.execute(insert_query, values)

cnx.commit()

print('done')
# for i in column_names:
#     print(i)

    



# print(df['nom_entreprise'])
