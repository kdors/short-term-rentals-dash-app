## Short-Term Rentals in New Orleans App using Dash

This is an app I created using data on short-term rental permit applications in New Orleans found [here](https://data.nola.gov/Housing-Land-Use-and-Blight/Short-Term-Rental-Permit-Applications/en36-xvxg). I thought it would be useful if there was a map of the rental locations that allowed you to filter based on the current status of the application (if it's issued, denied, etc.), which was not possible using the map on data.nola.gov found [here](https://data.nola.gov/Housing-Land-Use-and-Blight/Map-of-Short-Term-Rental-Licenses/j5u3-2ueh).

I also added some visualizations to analyze some of the trends in the data. I hope to continue to work on this app as this is my first time using Dash, and I am really enjoying playing with it!

You can look at the rentals.ipynb file to see how I cleaned the data using the CSV file, or you can just click this [link](https://github.com/kdors/short-term-rentals-dash-app/blob/main/rentals.ipynb) to go right to the notebook.

To get the data, you can download the CSV file found by going to the link above. When creating the Dash app, I instead created an app token and called the API (also found using the link above). 

**Using the API resulted in a dataframe with slightly different column names, and the location column data is different as well, so the code to clean the data found in app.py is slightly different.**

![App Screenshot](/app-screenshot.png "App screenshot")

