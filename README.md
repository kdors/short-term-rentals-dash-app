## Short-Term Rentals in New Orleans App using Dash

This is an app using data on short-term rental permit applications in New Orleans found [here](https://data.nola.gov/Housing-Land-Use-and-Blight/Short-Term-Rental-Permit-Applications/en36-xvxg).

I first explored the data in Jupyter Notebook. It's called "rentals.ipynb", or you can just click this [link](https://github.com/kdors/short-term-rentals-dash-app/blob/main/rentals.ipynb) to go right to the notebook.

To get the data, you can download the CSV file found by going to the link above. For creating the Dash app, I instead created an app token and called the API (also found using the link above). If you want to run the file locally using a CSV you can just replace the code that calls the API (found in st_rentals.py) with `pd.read_csv(FileName)`.


 To run the app on your own computer:
 1. Clone this repo in a directory of choice
 2. Run  `pip install -r requirements.txt`
 3. Run `python app.py`

