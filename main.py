import mysql.connector
import pandas as pd
import os
def upload_data_to_sql(item_id, color, category, style, season, subCategory, gender, item_image):
    connection = mysql.connector.connect(
        host='stylistadb.mysql.database.azure.com',
        port=3306,
        user='stylista',
        password='modowy1!',
        database='stylista'
    )

    cursor = connection.cursor()

    sql = "INSERT INTO wardrobe_test (item_id, color, category, style, season, subCategory, gender, item_image) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    values = (item_id, color, category, style, season, subCategory, gender, item_image)

    cursor.execute(sql, values)

    connection.commit()
    connection.close()
def delete_data_from_sql(item_id):
    connection = mysql.connector.connect(
        host='stylistadb.mysql.database.azure.com',
        port=3306,
        user='stylista',
        password='modowy1!',
        database='stylista'
    )

    cursor = connection.cursor()

    sql = "DELETE FROM wardrobe_test WHERE item_id = %s"
    value = (item_id,)

    cursor.execute(sql, value)

    connection.commit()
    connection.close()



def generate_combinations(df):
    topwear_ids = df[df['subCategory'] == 'Topwear']['item_id'].unique()
    bottomwear_ids = df[df['subCategory'] == 'Bottomwear']['item_id'].unique()
    shoes_ids = df[df['subCategory'] == 'Shoes']['item_id'].unique()

    combinations = []

    for topwear_id in topwear_ids:
        topwear_gender = df.loc[df['item_id'] == topwear_id, 'gender'].iloc[0]
        topwear_style = df.loc[df['item_id'] == topwear_id, 'style'].iloc[0]
        topwear_season = df.loc[df['item_id'] == topwear_id, 'season'].iloc[0]

        for bottomwear_id in bottomwear_ids:
            bottomwear_gender = df.loc[df['item_id'] == bottomwear_id, 'gender'].iloc[0]
            bottomwear_style = df.loc[df['item_id'] == bottomwear_id, 'style'].iloc[0]
            bottomwear_season = df.loc[df['item_id'] == bottomwear_id, 'season'].iloc[0]

            if (bottomwear_gender == topwear_gender) and (bottomwear_style == topwear_style) and (bottomwear_season == topwear_season):
                for shoes_id in shoes_ids:
                    shoes_gender = df.loc[df['item_id'] == shoes_id, 'gender'].iloc[0]
                    shoes_style = df.loc[df['item_id'] == shoes_id, 'style'].iloc[0]
                    shoes_season = df.loc[df['item_id'] == shoes_id, 'season'].iloc[0]

                    if (shoes_gender == topwear_gender) and (shoes_style == topwear_style) and (shoes_season == topwear_season):
                        combinations.append([topwear_id, bottomwear_id, shoes_id, topwear_gender, topwear_style, topwear_season, 0])

    return combinations

def generate_and_save_combinations(host, port, username, password, database, table_name, output_csv_path):
    connection = mysql.connector.connect(
        host=host,
        port=port,
        user=username,
        password=password,
        database=database
    )

    query = f"SELECT * FROM {table_name}"
    df = pd.read_sql(query, connection)

    combinations = generate_combinations(df)

    columns = ['topwear_id', 'bottomwear_id', 'shoes_id', 'gender', 'style', 'season', 'weight']
    data = pd.DataFrame(combinations, columns=columns)

    data.to_csv(output_csv_path, index=False)
    print(f'Combinations CSV file saved to {output_csv_path}')

    connection.close()
def load_combinations_from_csv_to_sql(host, port, username, password, database, table_name, combinations_csv_path):
    connection = mysql.connector.connect(
        host=host,
        port=port,
        user=username,
        password=password,
        database=database
    )

    create_table_query = f"""
    CREATE TABLE IF NOT EXISTS {table_name} (
        topwear_id VARCHAR(255),
        bottomwear_id VARCHAR(255),
        shoes_id VARCHAR(255),
        gender VARCHAR(255),
        style VARCHAR(255),
        season VARCHAR(255),
        weight INT
    )
    """
    cursor = connection.cursor()
    cursor.execute(create_table_query)
    connection.commit()

    combinations_df = pd.read_csv(combinations_csv_path)

    insert_query = f"INSERT INTO {table_name} (topwear_id, bottomwear_id, shoes_id, gender, style, season, weight) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    cursor = connection.cursor()
    for _, row in combinations_df.iterrows():
        values = (row['topwear_id'], row['bottomwear_id'], row['shoes_id'], row['gender'], row['style'], row['season'], row['weight'])
        cursor.execute(insert_query, values)
    connection.commit()

    cursor.close()
    connection.close()

def update_weight_in_sql(host, port, username, password, database, table_name, row_id, new_weight):
    connection = mysql.connector.connect(
        host=host,
        port=port,
        user=username,
        password=password,
        database=database
    )

    update_query = f"UPDATE {table_name} SET weight = %s WHERE idwages = %s"
    cursor = connection.cursor()
    cursor.execute(update_query, (new_weight, row_id))
    connection.commit()

    cursor.close()
    connection.close()

item_id = '1529'
color = 'Red'
category = 'T-shirt'
style = 'Casual'
season = 'Summer'
subCategory = 'Topwear'
gender = 'Male'
item_image = '1529.jpg'

#upload_data_to_sql(item_id, color, category, style, season, subCategory, gender, item_image)
#delete_data_from_sql(item_id)
"""
upload_data_to_sql('1529', 'Red', 'T-Shirt', 'Casual', 'Summer', 'Topwear', 'Male', '1529.jpg')
upload_data_to_sql('1531', 'Grey', 'T-Shirt', 'Casual', 'Summer', 'Topwear', 'Male', '1531.jpg')
upload_data_to_sql('1533', 'Red', 'T-Shirt', 'Casual', 'Summer', 'Topwear', 'Male', '1533.jpg')
upload_data_to_sql('1534', 'Black', 'T-Shirt', 'Casual', 'Summer', 'Topwear', 'Male', '1534.jpg')
upload_data_to_sql('8779', 'Blue', 'T-Shirt', 'Formal', 'Summer', 'Topwear', 'Male', '8779.jpg')
upload_data_to_sql('1541', 'Red', 'Shoes', 'Casual', 'Summer', 'Shoes', 'Male', '1541.jpg')
upload_data_to_sql('1543', 'Black', 'Shoes', 'Casual', 'Summer', 'Shoes', 'Male', '1543.jpg')
upload_data_to_sql('1567', 'Red', 'Trousers', 'Casual', 'Summer', 'Bottomwear', 'Male', '1567.jpg')
upload_data_to_sql('1569', 'Red', 'Trousers', 'Casual', 'Summer', 'Bottomwear', 'Male', '1569.jpg')
upload_data_to_sql('1572', 'Red', 'Trousers', 'Casual', 'Summer', 'Bottomwear', 'Male', '1572.jpg')
"""
# Example usage
host = 'stylistadb.mysql.database.azure.com'
port = 3306
username = 'stylista'
password = 'modowy1!'
database = 'stylista'
table_name = 'wardrobe_test'
output_csv_path = 'combinations.csv'
#generate_and_save_combinations('stylistadb.mysql.database.azure.com', 3306, 'stylista', 'modowy1!', 'stylista', 'combinations.csv')
#generate_and_save_combinations(host, port, username, password, database, "wardrobe_test", "wages.csv")
#generate_and_save_combinations(host, port, username, password, database, table_name, output_csv_path)
#load_combinations_from_csv_to_sql(host, port, username, password, database, "wages", output_csv_path)
#update_weight_in_sql(host, port, username, password, database, "wages", "1", 1)