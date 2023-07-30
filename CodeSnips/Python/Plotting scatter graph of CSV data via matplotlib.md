```python
import pandas as pd
import matplotlib.pyplot as plt

# Read data from CSV file into a pandas DataFrame
data = pd.read_csv('data.csv')

# Extract x and y values from the DataFrame
x_values = data['x_values']
y_values = data['y_values']

# Create the scatter plot
plt.scatter(x_values, y_values)

# Set labels and title
plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.title('Scatter Plot')

# Show the plot
plt.show()
```
