from flask import Flask, render_template ,request, make_response,jsonify
from pulp import LpVariable, LpProblem, lpSum, value, LpMinimize
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/')
def index():
  print("Done /")
  return render_template('index.html')


@app.route("/solve-sudoku", methods = ['POST'])
def sudoku():


  print("******")
  print("YEAHHH")
  print("******")
  # input_data:
  jsonInput = request.get_json()
  puzzle = jsonInput['puzzle']
  print(puzzle)
  # solution = initialProblem
  
  # Initialize the problem
  prob = LpProblem("Sudoku Problem", LpMinimize)
  
  # Create the decision variables
  choices = LpVariable.dicts("Choice", (range(9), range(9), range(1, 10)), cat='Binary')
  
  # Add the objective function (not needed for solving Sudoku)
  prob += 0
  
  # Add the constraints
  for r in range(9):
      for c in range(9):
          prob += lpSum(choices[r][c][n] for n in range(1, 10)) == 1
          
  for r in range(9):
      for n in range(1, 10):
          prob += lpSum(choices[r][c][n] for c in range(9)) == 1
          
  for c in range(9):
      for n in range(1, 10):
          prob += lpSum(choices[r][c][n] for r in range(9)) == 1
          
  for br in range(3):
      for bc in range(3):
          for n in range(1, 10):
              prob += lpSum(choices[r+3*br][c+3*bc][n] for r in range(3) for c in range(3)) == 1
  
  # Set the initial values for the known cells
  known_values = [(r, c, puzzle[r][c]) for r in range(9) for c in range(9) if puzzle[r][c] != 0]
  for r, c, n in known_values:
      prob += choices[r][c][n] == 1
      
  # Solve the problem
  prob.solve()
  
  # Print the solution
  solution = [[0 for c in range(9)] for r in range(9)]
  for r in range(9):
      for c in range(9):
          for n in range(1, 10):
              if value(choices[r][c][n]) == 1:
                  solution[r][c] = n
  print(solution)
  

  res = make_response(jsonify(solution), 200)
  return res



@app.route("/rate", methods = ['POST'])
def rate():
    
    # Define the URL of the website you want to scrape
    
    url = "https://www.superfinanciera.gov.co/jsp/"
    # url = "https://www.banrep.gov.co/docum/buscador_series.html"
    
    # Send a GET request to the website
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'}
    response = requests.get(url, headers=headers)
    
    # response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, "html.parser")
        #print("*******************")
        divs = soup.find_all("div", class_="cont_Indicador")
    
        print("*******************")
        string_tmr = divs[0].text
        tmr = string_tmr[-8:]
        print(tmr)
        print("*******************")
    
    else:
        print("Failed to retrieve the web page TMR. ☹️")
    
    
    ## EUR / USD
    url2 = "https://www.xe.com/es/currencyconverter/convert/?Amount=1&From=EUR&To=USD"
    # Send a GET request to the website
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'}
    response = requests.get(url2, headers=headers)
    
    
    
    
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, "html.parser")
        # print("*******************")
        all_p = soup.find_all("p", class_="result__BigRate-sc-1bsijpp-1 iGrAod")
        
        string_rate = all_p[0].text
        rate = string_rate[:4]
        print("*******************")
        print(rate)
        print("*******************")
           
    else:
        print("Failed to retrieve the web page EUR-USD. ☹️")
    
    
    solution = {
        value_TMR:tmr,
        value_rate: rate
    }
    
    res1 = make_response(jsonify(solution), 200)
    return res1

if __name__ == '__main__':
  app.run(port=5000)
