from .user_manager import UserManager
from .score import Score
from .user import User
from datetime import datetime
from random import randint

class DiceGame:
  def __init__(self):
    self.user_manager = UserManager()
    self.scores = []
    self.recent_User = None
    self.load_scores()

  def load_scores(self):
    try:
      with open("data/history.txt", "r") as file:
        for line in file:
          username, game_id, points, wins = line.strip().split("|")
          score = Score(username, game_id)
          score.points = int(points)
          score.wins = int(wins)
          self.scores.append(score)
    except FileNotFoundError:
      pass
    except ValueError:
      print("Error: Invalid data in history file")
    
  def save_scores(self):
    with open("data/history.txt", "w") as file:
      for score in self.scores:
        file.write(f"{score.username:10} | {score.game_id:10} | {score.points:10} | {score.wins}\n")

  def play_game(self):
    if not self.recent_User:
      print("\nYou need to log in first to play the game.")
      return
    player_username = self.recent_User.username

    now = datetime.now()
    game_id = now.strftime("%d-%m %Y %H:%M:%S")
    recent_score = Score(self.recent_User.username, game_id)
    stage = 1

    while True:
      print("\n" + "=" * 30 + f" STAGE {stage} " + "=" * 30)
      user_score = 0
      CPU_score = 0
      rounds = 0

      while rounds <= 3:
        dice1 = randint(1,6) #users
        dice2 = randint(1,6) #CPU
        print(f"\n{player_username} rolled: {dice1}")
        print(f"CPU rolled: {dice2}")
        if dice1 > dice2:
          print(f"WINNER: {player_username}")
          user_score += 1
          recent_score.points += 1 
        elif dice1 < dice2:
          print("WINNER: CPU")
          CPU_score += 1
        else:
          print("It's a tie!")
        rounds += 1
      print("=" * 50)
        
      if user_score >=2:
        print(f"\n{player_username} won stage {stage}!")
        recent_score.points += 3
        recent_score.wins += 1
        choice = input("Enter any key to continue to next stage, and [0] to return: ")
        if choice == 0:
           break
        stage += 1
      else: 
        print("\nCPU won this stage.")
        break

    if recent_score.points > 0 and recent_score.wins > 0:
      self.scores.append(recent_score)
      self.save_scores()
      print(f"{player_username}, Your score has been recorded. ")
    else:
      print(f"{player_username} you didn't score any points in the previous game. ") 
    print(f"\n{player_username}:")
    print(f"\t Total Points: {recent_score.points}")
    print(f"\t Wins: {recent_score.wins}")      
    print("=" * 50) 

  def show_top_scores(self):
    sorted_scores = sorted(self.scores, key=lambda score: score.points, reverse=True)
    print("=" * 30 + " TOP 10 Scores " + "=" * 30)
    if not sorted_scores:
      print("No Record yet.")
    else:
      for i, score in enumerate(sorted_scores[:10]):
        print(f"{i+1}. {score.username:10} | {score.game_id:10} | Points: {score.points:10} | Wins: {score.wins:10}")
  
  def logout(self):
    if self.recent_User:
      print(f"\n{self.recent_User.username} logged out successfully.")
    self.recent_User = None
    self.main_menu()
  
  def show_register(self):
    while True:
      username = input("\nEnter a username (at least 4 characters, leave blank to return): ")
      if not username:
        return
      password = input("Enter a password (at least 8 characters, leave blank to return): ")
      if not password:
        return
      if self.user_manager.register(username, password):
        print(f"User {username} registered Successfully.")
        return
      else:
        print("Registration Failed. Username already taken or invalid.")

  def show_login(self):
    while True:
      username = input("\nEnter your username (at least 4 characters, leave blank to return): ")
      if not username:
        return
      password = input("Enter your password(at least 8 characters, leave blank to return): ")
      if not password:
        return
      if self.user_manager.login(username, password):
        self.recent_User = User(username, password)
        print(f"\n Welcome, {username}!")
        self.loogged_in_menu()
      else: 
        print(f"Login Failed. Incorrect credentials.")

  def loogged_in_menu(self):
    while True:
      print("\n" + "=" * 30 + f" User: {self.recent_User.username} " + "=" * 30)
      print("\n\t[1] Play Game")
      print("\t[2] Show Ranking")
      print("\t[3] Log out")
      print("=" * 70)
      choice = int(input("Enter your choice: "))
      while True:
        try:
          if choice == 1:
            self.play_game()
            break
          elif choice == 2:
            self.show_top_scores()
            break
          elif choice == 3:
            self.logout()
            break
          else:
            print("ERROR: Invalid Input. Please try again.")
        except ValueError:
          print("ERROR: Invalid input.")

  def main_menu(self):
    while True:
      print("\n" + "=" * 30 + " Welcome to Dice Game " + "=" * 30)
      print("\t[1] Register")
      print("\t[2] Log in")
      print("\t[3] Exit")
      print("=" * 80)
      choice = int(input("Enter your choice: "))
      while True:
        try:
          if choice == 1:
            self.show_register()
            break
          elif choice == 2:
            self.show_login()
            break
          elif choice == 3:
            print("Exiting the game... Thank you!...")
            exit()
          else:
            print("ERROR: Invalid input. Please try again.")
        except ValueError:
          print("ERROR: Invalid input.")
        
  def main_main_menu(self):
    if self.recent_User:
      self.loogged_in_menu()
    else:
      self.main_menu()





          

