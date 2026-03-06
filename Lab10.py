#name: Reece Dickerson
# date: 3/5/2026
# description: Implementation of CRUD operations with DynamoDB — CS178 Lab 10
# proposed score: 5 (out of 5) -- if I don't change this, I agree to get 0 points.

import boto3

# boto3 uses the credentials configured via `aws configure` on EC2
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('Video_Games')

def get_table():
    """Return a reference to the DynamoDB Video_Games table."""
    dynamodb = boto3.resource("dynamodb", region_name='us-east-1')
    return dynamodb.Table('Video_Games')

def create_game():
    title = input("What is the title of the new video game? ")
    table.update_item(
        Key={"Title": title},
        UpdateExpression="SET Ratings = :r",
        ExpressionAttributeValues={':r': []}
    )
    print("creating a video game")

def print_game(game):
    title = game.get("Title", "Unknown Title")
    year = game.get("Year", "Unknown Year")
    ratings = game.get("Ratings", "No ratings")
    developer = game.get("Developer", "Unknown Developer")
    genres = game.get("Genres", "Unknown Genre")

    print(f"  Title  : {title}")
    print(f"  Year   : {year}")
    print(f"  Ratings: {ratings}")
    print(f"  Developer: {developer}")
    print(f"  Genres  : {genres}")
    print()


def print_all_games():
    """Scan the entire Video_Games table and print each item."""
    table = get_table()
    
    # scan() retrieves ALL items in the table.
    # For large tables you'd use query() instead — but for our small
    # dataset, scan() is fine.
    response = table.scan()
    items = response.get("Items", [])
    
    if not items:
        print("No video games found. Make sure your DynamoDB table has data.")
        return
    
    print(f"Found {len(items)} video game(s):\n")
    for game in items:
        print_game(game)

def update_rating():
    try:
        title = input("What is the video game title? ")
        rating = int(input("What is the rating (integer): "))
        table.update_item(
            Key={"Title": title},
            UpdateExpression="SET Ratings = list_append(Ratings, :r)",
            ExpressionAttributeValues={':r': [rating]}
        )
    except Exception:
        print("Error in updating video game rating")

    print("updating rating")

def delete_game():
    title = input("What video game would you like to delete? ")
    table.delete_item(Key={"Title": title})
    print("deleting video game")

def query_game():
    title = input("What video game would you like to see the average ratings of? ")
    if table.get_item(Key={"Title": title}).get("Item") is None:
        print(f"Video game not found")
        return
    response = table.get_item(Key={"Title": title})
    game = response.get("Item")
    ratings_list = game["Ratings"]
    if ratings_list:
        average_rating = sum(ratings_list) / len(ratings_list)
        print(f"Average rating for '{title}': {average_rating}")
    else:
        print(f"Video game has no ratings")
    print("query video game")

def print_menu():
    print("----------------------------")
    print("Press C: to CREATE a new video game")
    print("Press R: to READ all video games")
    print("Press U: to UPDATE a video game (add a review)")
    print("Press D: to DELETE a video game")
    print("Press Q: to QUERY a video game's average rating")
    print("Press X: to EXIT application")
    print("----------------------------")

def main():
    input_char = ""
    while input_char.upper() != "X":
        print_menu()
        input_char = input("Choice: ")
        if input_char.upper() == "C":
            create_game()
        elif input_char.upper() == "R":
            print_all_games()
        elif input_char.upper() == "U":
            update_rating()
        elif input_char.upper() == "D":
            delete_game()
        elif input_char.upper() == "Q":
            query_game()
        elif input_char.upper() == "X":
            print("exiting...")
        else:
            print("Not a valid option. Try again.")

main()
