from utils.user import User
import os

class UserManager:
  def __init__(self):
    self.users = {}
    self.load_users()

  def load_users(self):
    if not os.path.exists("data"):
      os.makedirs("data")

    try:
      with open("data/users.txt", 'r') as file:
        for line in file:
          username, password = line.strip().split("|")
          self.users[username] = password
    except FileNotFoundError:
      return None
    except ValueError:
      return None

  def save_users(self):
    try:
      with open("data/users.txt", 'w') as file:
        for username, password in self.users.items():
          file.write(f"{username:10} | {password}\n")
    except IOError:
      print("ERROR: Unable to save users")

  def validate_username(self, username):
    if len(username) < 4:
      return False
    if username in self.users:
      return False
    return True
  
  def validate_password(self, password):
    if len(password) < 8:
      return False
    return True
  
  def register(self, username, password):
    if not self.validate_username(username):
      return False
    if not self.validate_password(password):
      return False
    
    new_user = User(username, password)
    self.users[username] = new_user
    self.users[username] = password
    self.save_users()
    return True

  def login(self, username, password):
    if username not in self.users:
      return False
    user_pass = self.users[username]
    if user_pass != password:
      return False
    return True
