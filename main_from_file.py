from collections import OrderedDict
import matplotlib.pyplot as plt

# The Geometry class contains common geometric operations and constants
class Geometry:
    # Tolerance value for geometric calculations
    TOLERANCE = 1e-10

    # Static method to calculate the Euclidean distance between two points
    @staticmethod
    def distance(point1, point2):
        return ((point1.x - point2.x) ** 2 + (point1.y - point2.y) ** 2) ** 0.5

    # Static method to check if a point lies on a given line segment
    @staticmethod
    def on_line(point, line):
        x, y = point.x, point.y
        x1, y1, x2, y2 = line

        # Check if the point coincides with either endpoint of the line
        if abs(x - x1) < Geometry.TOLERANCE and abs(y - y1) < Geometry.TOLERANCE:
            return True
        if abs(x - x2) < Geometry.TOLERANCE and abs(y - y2) < Geometry.TOLERANCE:
            return True

        # Check if the point is within a certain tolerance of the line
        if (x1 <= x <= x2 or x2 <= x <= x1) and (y1 <= y <= y2 or y2 <= y <= y1):
            # Calculate the perpendicular distance from the point to the line
            distance = abs((x2 - x1) * (y1 - y) - (x1 - x) * (y2 - y1)) / ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
            return distance < Geometry.TOLERANCE

        return False

class Point:
    # Represents a point in 2D space
    def __init__(self, x, y):
        # Initialize a point with x and y coordinates
        self.x = x
        self.y = y

class Polygon(Geometry):
    def __init__(self, points):
        # Initialize a polygon with a list of points
        self.points = points
        self.mbr = None  # Minimum Bounding Rectangle (MBR) for the polygon

    def create_mbr(self):
        # Create the Minimum Bounding Rectangle (MBR) of the polygon
        x_coords, y_coords = zip(*[(point.x, point.y) for point in self.points])
        min_x, max_x = min(x_coords), max(x_coords)
        min_y, max_y = min(y_coords), max(y_coords)
        # Define MBR as a list of four points
        return [Point(min_x, min_y), Point(max_x, min_y), Point(max_x, max_y), Point(min_x, max_y)]

    def point_in_mbr(self, point):
        # Check if a point is inside the MBR of the polygon
        x, y = point.x, point.y
        # Unpack MBR coordinates
        min_x, min_y, max_x, max_y = self.mbr[0].x, self.mbr[0].y, self.mbr[2].x, self.mbr[2].y
        return min_x <= x <= max_x and min_y <= y <= max_y

    def point_on_edge(self, point, edge):
        # Check if a point is on the edge of the polygon
        return Geometry.on_line(point, edge)

    def point_in_polygon(self, point):
        # Check if a point is inside the polygon, on the boundary, or outside
        x, y = point.x, point.y
        n = len(self.points)
        intersect_count = 0

        for i in range(n):
            x1, y1 = self.points[i].x, self.points[i].y
            x2, y2 = self.points[(i + 1) % n].x, self.points[(i + 1) % n].y

            # Check if the point is on the edge
            if self.point_on_edge(point, (x1, y1, x2, y2)):
                return "boundary"

            # Check for potential intersection
            if min(y1, y2) < y <= max(y1, y2):
                try:
                    # Use the Ray-Casting Algorithm to count intersections (RCA)
                    if x1 + (y - y1) / (y2 - y1) * (x2 - x1) < x + Geometry.TOLERANCE:
                        intersect_count += 1
                except ZeroDivisionError:
                    pass

        return "inside" if intersect_count % 2 == 1 else "outside"

    def classify_point_using_mbr_and_rca(self, point):
        # Classify a point using MBR and the Ray-Casting Algorithm (RCA)
        # Create MBR
        self.mbr = self.create_mbr()

        if self.point_in_mbr(point):
            # If the point is inside the MBR, further classify using the Ray-Casting Algorithm
            return self.point_in_polygon(point)
        else:
            # If the point is outside the MBR, classify as "outside"
            return "outside"

# I have used ChatGPT (Open AI, https://openai.com/) as a generative AI tool to effectively structure certain code segments related to RCA.

class Triangle(Geometry):
    def __init__(self, vertices):
        # Initialize a triangle with a list of vertices
        self.vertices = vertices
        self.mbr = None  # Minimum Bounding Rectangle (MBR) for the triangle

    @staticmethod
    def generate_fixed_triangle():
        # Define fixed vertices for a triangle and create a Triangle instance
        vertices = [Point(2, 2), Point(6, 2), Point(4, 6)]
        return Triangle(vertices)

    def create_mbr(self):
        # Create the Minimum Bounding Rectangle (MBR) of the triangle
        x_coords, y_coords = zip(*[(point.x, point.y) for point in self.vertices])
        min_x, max_x = min(x_coords), max(x_coords)
        min_y, max_y = min(y_coords), max(y_coords)
        # Define MBR as a list of four points
        return [Point(min_x, min_y), Point(max_x, min_y), Point(max_x, max_y), Point(min_x, max_y)]

    def point_in_mbr(self, point):
        # Check if a point is inside the MBR of the triangle
        min_x, min_y, max_x, max_y = self.create_mbr()
        return min_x <= point.x <= max_x and min_y <= point.y <= max_y

    def point_on_triangle_edge(self, point):
        # Check if a point is on any edge of the triangle
        for i in range(3):
            edge_start = self.vertices[i]
            edge_end = self.vertices[(i + 1) % 3]

            # Check if the point is on the current edge
            if Geometry.on_line(point, (edge_start.x, edge_start.y, edge_end.x, edge_end.y)):
                return True

        return False

    def point_in_triangle(self, point):
        # Check if a point is inside the triangle, on the boundary, or outside
        x, y = point.x, point.y
        x1, y1 = self.vertices[0].x, self.vertices[0].y
        x2, y2 = self.vertices[1].x, self.vertices[1].y
        x3, y3 = self.vertices[2].x, self.vertices[2].y

        # Calculate determinant of the matrix representing the triangle
        detT = (y2 - y3) * (x1 - x3) + (x3 - x2) * (y1 - y3)
        alpha = ((y2 - y3) * (x - x3) + (x3 - x2) * (y - y3)) / detT
        beta = ((y3 - y1) * (x - x3) + (x1 - x3) * (y - y3)) / detT
        gamma = 1 - alpha - beta

        # Check if the point is on the boundary
        if self.point_on_triangle_edge(point):
            return "boundary"

        # Check if the point is inside, considering tolerance
        if -Geometry.TOLERANCE <= alpha <= 1 + Geometry.TOLERANCE and \
           -Geometry.TOLERANCE <= beta <= 1 + Geometry.TOLERANCE and \
           -Geometry.TOLERANCE <= gamma <= 1 + Geometry.TOLERANCE:
            return "inside"
        else:
            return "outside"

    def classify_point_using_mbr_and_rca(self, point):
        # Classify a point using MBR and the Ray-Casting Algorithm (RCA)
        # Create MBR
        self.mbr = self.create_mbr()

        if self.point_in_mbr(point):
            # If the point is inside the MBR, further classify using the Triangle's point_in_triangle method
            return self.point_in_triangle(point)
        else:
            # If the point is outside the MBR, classify as "outside"
            return "outside"

class Square(Geometry):
    def __init__(self, side_length):
        # Initialize a square with a given side length and calculate the MBR
        self.side_length = side_length
        self.mbr = self.create_mbr()  # Initialize the MBR

    @staticmethod
    def generate_fixed_square():
        # Create a square with a fixed side length
        side_length = 4
        return Square(side_length)

    def create_mbr(self):
        # Create the Minimum Bounding Rectangle (MBR) of the square
        half_side = self.side_length / 2
        # Define MBR as a list of four points
        return [Point(-half_side, -half_side), Point(half_side, -half_side), Point(half_side, half_side),
                Point(-half_side, half_side)]

    def point_in_mbr(self, point):
        # Check if a point is inside the MBR of the square
        x, y = point.x, point.y
        # Unpack MBR coordinates
        min_x, min_y, max_x, max_y = self.mbr[0].x, self.mbr[0].y, self.mbr[2].x, self.mbr[2].y
        return min_x <= x <= max_x and min_y <= y <= max_y

    def point_on_edge(self, point, edge):
        # Check if a point is on the edge of the square
        return Geometry.on_line(point, edge)

    def point_in_square(self, point):
        # Check if a point is inside the square, on the boundary, or outside
        if not self.point_in_mbr(point):
            return "outside"

        half_side = self.side_length / 2
        x, y = point.x, point.y

        # Check if the point is on the boundary
        if abs(x) == half_side or abs(y) == half_side:
            return "boundary"

        # Check if the point is inside, considering tolerance
        if -half_side + Geometry.TOLERANCE <= x <= half_side - Geometry.TOLERANCE and \
                -half_side + Geometry.TOLERANCE <= y <= half_side - Geometry.TOLERANCE:
            return "inside"
        else:
            return "outside"

class Plotter(Geometry):
    def __init__(self, title="Polygon & File Points"):
        try:
            # Initialize the plot with a given title
            plt.figure()
            plt.title(title)
        except Exception as e:
            print(f"Error in Plotter initialization: {e}")

    def add_polygon(self, xs, ys):
        try:
            # Add a filled polygon to the plot
            plt.fill(xs, ys, 'lightgray', label='Polygon')
        except Exception as e:
            print(f"Error in add_polygon: {e}")

    def add_triangle(self, vertices):
        try:
            # Add a filled triangle to the plot
            xs, ys = zip(*[(point.x, point.y) for point in vertices])
            plt.fill(xs, ys, 'lightblue', label='Triangle')
        except Exception as e:
            print(f"Error in add_triangle: {e}")
    def add_square(self, mbr):
        try:
            # Add a filled square to the plot
            xs, ys = zip(*[(point.x, point.y) for point in mbr])
            plt.fill(xs, ys, 'lightblue', label='Square')
        except Exception as e:
            print(f"Errore in add_square: {e}")

    def add_point(self, x, y, kind=None):
        try:
            # Add a point to the plot with different markers based on classification
            if kind == 'outside':
                plt.plot(x, y, 'ro', label='Outside')
            elif kind == 'boundary':
                plt.plot(x, y, 'bo', label='Boundary')
            elif kind == 'inside':
                plt.plot(x, y, 'go', label='Inside')
            else:
                plt.plot(x, y, 'ko', label='Unclassified')
        except Exception as e:
            print(f"Error in add_point: {e}")

    def show(self):
        try:
            # Display the legend, set axis labels, and show the plot
            handles, labels = plt.gca().get_legend_handles_labels()
            by_label = OrderedDict(zip(labels, handles))
            plt.legend(by_label.values(), by_label.keys())
            plt.xlabel('X-axis')
            plt.ylabel('Y-axis')
            plt.show()
        except Exception as e:
            print(f"Error in show: {e}")

def read_coordinates_from_file(filename):
    try:
        coordinates = []
        with open(filename, 'r') as file:
            next(file)  # Skip the header line
            for id, line in enumerate(file, start=1):
                values = line.strip().split(',')

                try:
                    # Extract and convert x and y values from the line
                    x = float(values[1])
                    y = float(values[2])
                    coordinates.append(Point(x, y))
                except (ValueError, TypeError) as e:
                    # Handle errors during conversion, use default values (0, 0)
                    print(f"Error reading coordinates for id {id}: {e}. Using default values.")
                    coordinates.append(Point(0, 0))

        return coordinates
    except FileNotFoundError as e:
        # Handle file not found error
        print(f"Error in read_coordinates_from_file: {e}")
        return []


def write_results_to_file(filename, classifications):
    try:
        with open(filename, 'w') as file:
            file.write("id,category\n")
            for id, cls in enumerate(classifications, start=1):
                # Write ID and classification to the file
                file.write(f"{id},{cls}\n")
    except Exception as e:
        # Handle general writing error
        print(f"Error in write_results_to_file: {e}")

def main():
    try:
        # File names
        polygon_filename = 'polygon.csv'
        points_filename = 'input.csv'
        output_filename = 'output.csv'
        output2_filename = 'output_triangle.csv'
        output3_filename = 'output_square.csv'

        # Read polygon coordinates
        polygon_coordinates = read_coordinates_from_file(polygon_filename)
        if not polygon_coordinates:
            print("Error: Empty polygon coordinates.")
            return

        # Create a Polygon instance
        bounding_polygon_instance = Polygon(polygon_coordinates)

        # Read test points
        test_points = read_coordinates_from_file(points_filename)
        if not test_points:
            print("Error: Empty test points.")
            return

        # Classification for Polygon
        classifications = [bounding_polygon_instance.point_in_polygon(point) for point in test_points]
        write_results_to_file(output_filename, classifications)

        # Plot Polygon
        plotter = Plotter()
        bounding_polygon_instance.points.append(bounding_polygon_instance.points[0])
        polygon_xs, polygon_ys = zip(*[(point.x, point.y) for point in bounding_polygon_instance.points])
        plotter.add_polygon(polygon_xs, polygon_ys)

        # Add points to the plot
        for id, (point, classification) in enumerate(zip(test_points, classifications), start=1):
            plotter.add_point(point.x, point.y, kind=classification)

        # Show the plot
        plotter.show()

        # Classification for Triangle
        fixed_triangle = Triangle.generate_fixed_triangle()
        classifications_triangle = [fixed_triangle.point_in_triangle(point) for point in test_points]
        write_results_to_file(output2_filename, classifications_triangle)

        # Plot Triangle
        plotter_triangle = Plotter(title="Triangle & File Points")
        fixed_triangle.vertices.append(fixed_triangle.vertices[0])
        triangle_xs, triangle_ys = zip(*[(point.x, point.y) for point in fixed_triangle.vertices])
        plotter_triangle.add_triangle(fixed_triangle.vertices)

        # Add points to the plot
        for id, (point, classification) in enumerate(zip(test_points, classifications_triangle), start=1):
            plotter_triangle.add_point(point.x, point.y, kind=classification)

        # Show the plot
        plotter_triangle.show()

        # Classification for Square
        fixed_square = Square.generate_fixed_square()
        classifications_square = [fixed_square.point_in_square(point) for point in test_points]
        write_results_to_file(output3_filename, classifications_square)

        # Plot Square
        plotter_square = Plotter(title="Square & File Points")
        square_xs, square_ys = zip(*[(point.x, point.y) for point in fixed_square.create_mbr()])
        plotter_square.add_polygon(square_xs, square_ys)

        # Add points to the plot
        for id, (point, classification) in enumerate(zip(test_points, classifications_square), start=1):
            plotter_square.add_point(point.x, point.y, kind=classification)

        # Show the plot
        plotter_square.show()

    except Exception as e:
        print(f"Unexpected error in main: {e}")

# Execute main only if this script is run directly
if __name__ == "__main__":
    main()