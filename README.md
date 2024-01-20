# Point-in-Polygon-Test
# Point-in-Polygon Algorithm - University College London (UCL) project implementing a Python-based Point-in-Polygon algorithm. Features MBR and RCA components. Test the project with CSV data or user input.  Contact: Vittorio Zoccola - vittoriozoccola@gmail.com

This project was completed as part of the CEGE0096 course at University College London (UCL). The assignment focused on implementing a Point-in-Polygon (PiP) algorithm, a fundamental operation in Geographic Information Systems (GIS). The objective was to determine whether a given point lies inside or outside a polygon.

The project involves two main components: the Minimum Bounding Rectangle (MBR) algorithm and the Ray Casting Algorithm (RCA). The MBR serves as a preliminary check to quickly identify points outside the polygon, while the RCA is responsible for accurately categorizing points inside, outside, or on the boundary. The Point-in-Polygon (PiP) algorithm needs to be built without the use of external python packages.

The project is implemented in Python and utilizes classes such as Geometry, Polygon, Point, and Line. Two main programs, main_from_file.py and main_from_user.py, were created to read input data, categorize points, and visualize the results.

To run the project, follow these steps:
1) main_from_file.py

    Read x, y coordinates from a CSV file to create a polygon object (provided in clockwise order).
    Read x, y coordinates from another file to create a list of test points.
    Categorize these points (inside, outside, or boundary) and write the results to a file.
    Plot the points and polygon in a plot window.

2) main_from_user.py

    Read x, y coordinates from a CSV file to create a polygon object.
    Read a point from the user for testing.
    Categorize the point and print the result on the screen.
    Plot the point and polygon in a plot window.

Feel free to clone this repository and adapt the code for your needs. Ensure to follow the provided guidelines and give proper credit if adapting code from online sources.

Special thanks to Dr. Aldo Lipani, the module coordinator, for providing guidance throughout the course.
