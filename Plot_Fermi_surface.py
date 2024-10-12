import numpy as np
import matplotlib.pyplot as plt
import math


def calculate_point_range(r):
    # It's obvious that, if we only care about the nine central reciprocal lattices, then we only have to care about a finite range of points that influences the center.
    max_distance = 1.5+r
    max_distance_rounded_up = math.ceil(max_distance)
    point_xlist = list(range(-max_distance_rounded_up, max_distance_rounded_up+1))
    point_ylist = list(range(-max_distance_rounded_up, max_distance_rounded_up+1))
    point_list = [(x, y) for x in point_xlist for y in point_ylist]
    return point_list

# Define the detection function to check how many circles a point is inside
def detect_num(detect_point, r, point_list):
    """
    detect_point: The coordinates of the point to detect (x, y)
    r: The radius of the circle, given detection range
    return: The number of circles the point is inside
    """
    overlap_num = 0  # Number of overlapping circles
    for point in point_list:
        # If the distance from the point to a lattice point is less than or equal to radius r, count it as overlapping
        if (point[0] - detect_point[0])**2 + (point[1] - detect_point[1])**2 <= r**2:
            overlap_num += 1
    return overlap_num

# Determine if a point is inside the n-th branch of the Fermi surface
def judge(detect_point, branch_index, r, point_list):
    """
    detect_point: The coordinates of the point to detect (x, y)
    branch_index: The index of the Fermi surface branch, indicating which branch
    r: The radius, defining the size of the circles
    return: Returns 1 if the point is inside n circles; otherwise returns 0
    """
    # If the number of overlapping circles is greater than or equal to branch_index, it belongs to the n-th branch of the Fermi surface
    if detect_num(detect_point, r, point_list) >= branch_index:
        return 1
    else:
        return 0

# Function to generate the grid in reciprocal space and calculate the Fermi surface determination results
def calculate_fermi_surface(branch_index, r, point_list,grid_size=500, grid_range=1.5):
    """
    branch_index: The index of the Fermi surface branch
    r: The radius of the circles
    grid_size: The number of divisions in the grid, default is 600
    grid_range: The size of the grid range, default is -3 to 3
    return: Returns the X, Y grid coordinates, and the calculated Z (Fermi surface distribution)
    """
    # Define the grid range in reciprocal space
    xrange = np.linspace(-grid_range, grid_range, grid_size)  # X-axis range
    yrange = np.linspace(-grid_range, grid_range, grid_size)  # Y-axis range
    X, Y = np.meshgrid(xrange, yrange)  # Generate 2D grid
    
    # Calculate the Fermi surface determination results
    Z = np.array([[judge((x, y), branch_index, r, point_list) for x in xrange] for y in yrange])
    
    return X, Y, Z

# Function to plot the Fermi surface
def plot_fermi_surface(X, Y, Z,branch_index,r,num_valence_electron):
    """
    X: The X coordinates of the grid
    Y: The Y coordinates of the grid
    Z: The determination results of the Fermi surface
    branch_index: The index of the Fermi surface branch
    r: The radius of the circles
    num_valence_electron:number of valence electrons
    """
    plt.figure(figsize=(8, 8))
    
    # Plot the filled contour for the Fermi surface, red indicates points on the Fermi surface
    plt.contourf(X, Y, Z, levels=[-0.5, 0.5, 1.5], colors=['white', 'red'], alpha=0.5)
    
    # Define boundary points for drawing dashed lines
    point_xlist_boundary = [-1.5, -0.5, 0.5, 1.5]
    point_ylist_boundary = [-1.5, -0.5, 0.5, 1.5]
    
    # Plot the lattice points in reciprocal space
    plt.scatter([x for x in [-1,-1,-1,0,0,0,1,1,1]], [y for  y in [-1,0,1,-1,0,1,-1,0,1]], facecolors='none', edgecolors='black', label='Reciprocal Space Lattice Points')
    
    # Add horizontal and vertical dashed lines to mark regions in reciprocal space
    for x in point_xlist_boundary:
        plt.axvline(x=x, color='gray', linestyle='--', linewidth=0.5, label='Edge of 1st BZ' if x == point_xlist_boundary[0] else "")
    for y in point_ylist_boundary:
        plt.axhline(y=y, color='gray', linestyle='--', linewidth=0.5)

    # Set the title and labels for the plot
    plt.title(f"Fermi Surface Plot (branch index = {branch_index},  num_valence_electron = {num_valence_electron},  r = {r:.2f})")
    plt.xlabel('kx-axis')
    plt.ylabel('ky-axis')
    plt.legend()
    plt.show()

# Main program to calculate and plot the Fermi surface
def main():
    """
    Main program to calculate and plot the specified branch of the Fermi surface
    """
    num_valence_electron = 18  # The number of valence electrons per unit cell
    r = np.sqrt(num_valence_electron / (2 * np.pi))  # Calculate the Fermi radius based on the Harrison method
    #print(f"Calculated Fermi radius r = {r:.4f} based on the number of valence electrons {num_valence_electron}")
    
    point_list = calculate_point_range(r)# Calculate the range of points to consider

    branch_index = 9  # Index of the Fermi surface branch
    
    # Calculate the X, Y grid and Z values for the Fermi surface
    X, Y, Z = calculate_fermi_surface(branch_index, r, point_list)
    
    # Plot the Fermi surface contour plot
    plot_fermi_surface(X, Y, Z, branch_index,r,num_valence_electron)

# Run the main program
if __name__ == "__main__":
    main()
