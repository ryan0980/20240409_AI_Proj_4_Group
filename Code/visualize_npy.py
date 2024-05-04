import numpy as np
import matplotlib.pyplot as plt

# Loop to load and process files from q-table1.npy to q-table10.npy
for i in range(7, 8):  # Loop from 1 to 10
    #file_path = f'Code/q-table{i}.npy'  # Construct file path
    file_path = 'Code\q-table6.npy'
    data = np.load(file_path)  # Load the numpy file

    # Calculate the average of the four action values across the third dimension
    combined_data = np.mean(data, axis=2)

    # Reshape the combined data into a 40x40 grid
    grid_40x40 = combined_data.reshape((40, 40))

    # Plotting the 40x40 grid
    plt.figure(figsize=(10, 10))
    plt.imshow(grid_40x40, cmap='viridis', interpolation='none')
    plt.colorbar()  # Show color scale
    plt.title(f"Visualization of the 40x40 Grid from q-table{i}")
    plt.show()
