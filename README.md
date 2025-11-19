# Dynamic Time Handling For Traffic Optimization

This project aims to make traffic lights smarter! Instead of fixed timings, it uses a computer model (specifically, a Random Forest model) to predict the best green light duration for each direction at an intersection (Fourway or threeway) based on how much traffic there is. The goal is to reduce traffic jams and make traffic flow smoother.

We use a traffic simulator called **SUMO** to create a virtual road network and test how well the predicted signal times work.

## Working

1.  **Dataset:** We need data that shows different traffic situations (e.g., 50 cars North, 30 cars East...) and the ideal green light time for each situation. This data is used to teach the computer model.
2.  **Training:** We use the data and the `RandomForest_model.ipynb` notebook to train the Random Forest model.
3.  **Prediction:** Once trained, you can give the model new traffic numbers (e.g., "Now there are 60 cars North, 25 cars East"). The model will predict the best green light times based on what it learned.
4.  **Simulation:** We can take these predicted times and update the traffic light settings in the SUMO simulation to see how well they work in a virtual environment.

## How to Use

1.  **Run Frontend Web Interface:**

    - If you have a simple web server script (like one using Flask) set up to use `templates/index.html` and the trained model:
      - Run the server script (e.g., `python app.py`).
      - Open your web browser to the specified address (usually `http://127.0.0.1:5000`).
      - Enter traffic numbers to get predictions.

2.  **Run the SUMO Simulation:**

    - Open your terminal, navigate to the project folder.
    - Launch the simulation with the graphical interface:
      ```bash
      sumo-gui -c ace1.sumocfg
      ```
    - You can watch the virtual cars move according to the rules defined in the files. The traffic lights will operate based on the timings set in the configuration.

3.  **Explore the Model (Optional) :**
    - Open the Jupyter Notebook:
      ```bash
      jupyter lab RandomForest_model.ipynb
      ```
    - Run the cells in the notebook to see how the data is loaded, how the model is trained, and how its accuracy is checked.

## Results

<img width="500" alt="Image" src="https://github.com/user-attachments/assets/cc3b64b7-12d3-41bd-a07e-0cb12c2ff0f6" />

## Output

<img width="500" alt="Image" src="https://github.com/user-attachments/assets/8822beb9-d9df-4483-8352-d8bc2cabaee6" />
