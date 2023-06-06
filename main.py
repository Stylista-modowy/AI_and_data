import os
import csv
from google.cloud import storage
import pandas as pd

def create_folder(bucket_name, folder_name, wagescsv_folder_name, useridclothes_folder_name, clothescsv_folder_name):
    # Path to your service account key file
    key_file_path = 'endless-codex-386021-d774fb36484c.json'

    # Create a client using the service account key file
    client = storage.Client.from_service_account_json(key_file_path)

    # Get the bucket
    bucket = client.bucket(bucket_name)

    # Create the user folder if it doesn't exist
    user_folder = bucket.blob(folder_name + '/')
    user_folder.upload_from_string('', content_type='application/x-www-form-urlencoded;charset=UTF-8')

    # Create the "wagescsv" folder inside the user folder
    wagescsv_folder = bucket.blob(folder_name + '/' + wagescsv_folder_name + '/')
    wagescsv_folder.upload_from_string('', content_type='application/x-www-form-urlencoded;charset=UTF-8')

    # Create the "useridclothes" folder inside the user folder
    useridclothes_folder = bucket.blob(folder_name + '/' + useridclothes_folder_name + '/')
    useridclothes_folder.upload_from_string('', content_type='application/x-www-form-urlencoded;charset=UTF-8')

    # Create the "clothescsv" folder inside the user folder
    clothescsv_folder = bucket.blob(folder_name + '/' + clothescsv_folder_name + '/')
    clothescsv_folder.upload_from_string('', content_type='application/x-www-form-urlencoded;charset=UTF-8')

    print(f'Folders created successfully for user "{folder_name}".')

def add_clothing_image(id, color, type, style, season, category, gender, image_path, image_folder_path, csv_folder_path):
    bucket_name = 'aiprojectusers'
    user_folder_name = 'Mateusz'

    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'endless-codex-386021-d774fb36484c.json'

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)

    image_blob = bucket.blob(f'{user_folder_name}/{image_folder_path}/{id}.jpg')
    image_blob.upload_from_filename(image_path)

    data = {
        'id': id.strip("[]"),
        'Color': color.strip("[]"),
        'Type': type.strip("[]"),
        'Style': style.strip("[]"),
        'Season': season.strip("[]"),
        'subCategory': category.strip("[]"),
        'Gender': gender.strip("[]"),
        'weight': 0
    }

    csv_folder = os.path.join(user_folder_name, csv_folder_path)
    os.makedirs(csv_folder, exist_ok=True)

    csv_file_path = os.path.join(csv_folder, f'{user_folder_name}clothes.csv')

    with open(csv_file_path, 'a', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=data.keys())

        if os.path.getsize(csv_file_path) == 0:
            writer.writeheader()

        # Write the data row
        writer.writerow(data)

    # Upload the CSV file to the specified CSV folder
    csv_blob = bucket.blob(f'{user_folder_name}/{csv_folder_path}/{user_folder_name}clothes.csv')
    csv_blob.upload_from_filename(csv_file_path)

    print(f'Successfully added clothing image {id}.jpg to folder "{user_folder_name}/{image_folder_path}"')
    print(f'Successfully added data to "{user_folder_name}/{csv_folder_path}/{user_folder_name}clothes.csv"')


##############
def generate_combinations(df):
    topwear_ids = df[df['subCategory'] == 'Topwear']['id'].unique()
    bottomwear_ids = df[df['subCategory'] == 'Bottomwear']['id'].unique()
    shoes_ids = df[df['subCategory'] == 'Shoes']['id'].unique()

    combinations = []

    for topwear_id in topwear_ids:
        topwear_gender = df.loc[df['id'] == topwear_id, 'Gender'].iloc[0]
        topwear_style = df.loc[df['id'] == topwear_id, 'Style'].iloc[0]
        topwear_season = df.loc[df['id'] == topwear_id, 'Season'].iloc[0]

        for bottomwear_id in bottomwear_ids:
            bottomwear_gender = df.loc[df['id'] == bottomwear_id, 'Gender'].iloc[0]
            bottomwear_style = df.loc[df['id'] == bottomwear_id, 'Style'].iloc[0]
            bottomwear_season = df.loc[df['id'] == bottomwear_id, 'Season'].iloc[0]

            if (bottomwear_gender == topwear_gender) and (bottomwear_style == topwear_style) and (bottomwear_season == topwear_season):
                for shoes_id in shoes_ids:
                    shoes_gender = df.loc[df['id'] == shoes_id, 'Gender'].iloc[0]
                    shoes_style = df.loc[df['id'] == shoes_id, 'Style'].iloc[0]
                    shoes_season = df.loc[df['id'] == shoes_id, 'Season'].iloc[0]

                    if (shoes_gender == topwear_gender) and (shoes_style == topwear_style) and (shoes_season == topwear_season):
                        combinations.append([topwear_id, bottomwear_id, shoes_id, topwear_gender, topwear_style, topwear_season, 0])

    return combinations

def create_combinations_csv(input_csv_path, output_csv_path):
    df = pd.read_csv(input_csv_path)
    combinations = generate_combinations(df)

    columns = ['topwear_id', 'bottomwear_id', 'shoes_id', 'gender', 'style', 'season', 'weight']
    data = pd.DataFrame(combinations, columns=columns)

    data.to_csv(output_csv_path, index=False)
    print(f'Combinations CSV file saved to {output_csv_path}')

def upload_csv_to_gcs(bucket_name, folder_name, csv_file_path):
    # Set your Google Cloud Storage bucket name
    bucket_name = 'aiprojectusers'

    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'endless-codex-386021-d774fb36484c.json'

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)

    blob = bucket.blob(f'{folder_name}/{csv_file_path}')
    blob.upload_from_filename(csv_file_path)

    print(f'CSV file "{csv_file_path}" uploaded to folder "{folder_name}" in bucket "{bucket_name}"')

if __name__ == '__main__':
    user_name = 'Mateusz'
    bucket_name = 'aiprojectusers' #zasobnik
    folder_name = user_name    #folder dla uzytkownika
    wagescsv_folder_name = user_name+ 'wagescsv'  #folder dla wag
    useridclothes_folder_name = user_name+ 'useridclothes'  #folder dla obrazkow ubran
    clothescsv_folder_name = user_name+ 'clothescsv'  #csv ubran

    create_folder(bucket_name, folder_name, wagescsv_folder_name, useridclothes_folder_name,clothescsv_folder_name)
    # dodawania ubrania do folderu oraz specyfikajci co csv
    add_clothing_image('1529', 'Red', 'T-Shirt', 'Casual', 'Summer', 'Topwear', 'Male', '1529.jpg', useridclothes_folder_name, clothescsv_folder_name)
    #  1529  1531   1533    1534    # shoes 1541 1542 1543   #bottomwear 1567 1569   1572
    add_clothing_image('1531', 'Grey', 'T-Shirt', 'Casual', 'Summer', 'Topwear', 'Male', '1531.jpg',useridclothes_folder_name, clothescsv_folder_name)
    add_clothing_image('1533', 'Red', 'T-Shirt', 'Casual', 'Summer', 'Topwear', 'Male', '1533.jpg',useridclothes_folder_name, clothescsv_folder_name)
    add_clothing_image('1534', 'Black', 'T-Shirt', 'Casual', 'Summer', 'Topwear', 'Male', '1534.jpg',useridclothes_folder_name, clothescsv_folder_name)
    add_clothing_image('8779', 'Blue', 'T-Shirt', 'Formal', 'Summer', 'Topwear', 'Male', '8779.jpg',useridclothes_folder_name, clothescsv_folder_name)
    ####
    add_clothing_image('1541', 'Red', 'Shoes', 'Casual', 'Summer', 'Shoes', 'Male', '1541.jpg', useridclothes_folder_name, clothescsv_folder_name)
    add_clothing_image('1543', 'Black', 'Shoes', 'Casual', 'Summer', 'Shoes', 'Male', '1529.jpg',useridclothes_folder_name, clothescsv_folder_name)
    ###
    add_clothing_image('1567', 'Red', 'Trousers', 'Casual', 'Summer', 'Bottomwear', 'Male', '1567.jpg',useridclothes_folder_name, clothescsv_folder_name)
    add_clothing_image('1569', 'Red', 'Trousers', 'Casual', 'Summer', 'Bottomwear', 'Male', '1569.jpg',useridclothes_folder_name, clothescsv_folder_name)
    add_clothing_image('1572', 'Red', 'Trousers', 'Casual', 'Summer', 'Bottomwear', 'Male', '1572.jpg',useridclothes_folder_name, clothescsv_folder_name)

    input_csv_path = 'Mateusz/Mateuszclothescsv/Mateuszclothes.csv'
    output_csv_path = 'output.csv'
    create_combinations_csv(input_csv_path, output_csv_path)
    csv_file_path = 'output.csv'
    upload_csv_to_gcs(bucket_name, 'Mateusz/Mateuszwagescsv', csv_file_path)

