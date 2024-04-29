from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from os import environ as env
import os
from dotenv import load_dotenv
import time
load_dotenv()

try:  # Add following vars to a .env file in the same directory as this script is in. 
    docker_username = env["docker_username"]    # For Oauth with docker, required by PWD.
    docker_password = env["docker_password"]
    tailscale_auth_key = env["tailscale_auth_key"]  # The API key with which tailscale exit node will be deployed. 
except KeyError:
    print(f"Please specify all the required env variables in a .env file in the script directory.")
    raise

driver = webdriver.Chrome()
driver.get("https://labs.play-with-docker.com/")

pwd_main_window = driver.window_handles[-1]     # Current, latest main window.
login_btn = driver.find_element(By.ID, "btnGroupDrop1")  # Login drop down button.
login_btn.click()

docker_oauth =  WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//a[@class="dropdown-item ng-binding ng-scope"]')))   # Docker login button in oauth drop down menu.
docker_oauth.click()

time.sleep(2)   # NEW WINDOW LOAD TIME.

docker_oauth_window = driver.window_handles[-1]
driver.switch_to.window(docker_oauth_window)

docker_username_field = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'username')))
docker_username_field.send_keys(docker_username)     # Fill username.

continue_btn = driver.find_element(By.NAME, 'action')
continue_btn.click()

password_field = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'password')))
password_field.send_keys(docker_password)   # Fill password.

continue_btn = driver.find_element(By.NAME, 'action')
continue_btn.click()


driver.switch_to.window(pwd_main_window)    # Switch to main window.
time.sleep(1)

session_start_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//a[@class="btn btn-lg btn-success" and text()="Start"]')))
session_start_button.click()    # Press start button, to start new session.

add_instance_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.md-primary.md-button.md-ink-ripple[ng-click="newInstance()"]')))
add_instance_button.click()  # create new VM instance in PWD.

terminal_cmd = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//div[@role="listitem" and text()="$ "]')))  # Selecting the exact element in HTML where linux commands are entered in web terminal.
time.sleep(3)
cmd = f" docker run -d \
         --name=tailscaled \
         -v /var/lib:/var/lib \
         -v /dev/net/tun:/dev/net/tun \
         --network=host \
         --cap-add=NET_ADMIN \
         --cap-add=NET_RAW \
         --env TS_AUTHKEY={tailscale_auth_key} \
         --env TS_EXTRA_ARGS=--advertise-exit-node \
         tailscale/tailscale"    # Command to deploy a tailscale container which authenticates with your tailscale auth_key, advertises exit node capabilities. [Refer read me to know how to create ts_auth_key, setup tailscale ACL to auto approve new exit nodes.]
terminal_cmd.send_keys(cmd, Keys.ENTER)     # Input above cmd, press enter in terminal to execute the deploy command.


close_session = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.md-warn.md-raised.md-button.md-ink-ripple[ng-click="closeSession()"]')))
try:
    time.sleep(60*60)   # 60 minutes * 60 seconds = 1 Hour
except KeyboardInterrupt:
    print("Manual Exit!")

close_session.click()  # ERROR : Some requests Error - Needs fix
time.sleep(5)   # wait for session close request to succeed.
driver.close()
