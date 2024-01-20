import matplotlib.pyplot as plt

class Geometry:
    # Common geometric operations
    TOLERANCE = 1e-10  # A small value to handle floating-point precision issues

    @staticmethod
    def distance(point1, point2):
        # Calculate the Euclidean distance between two points
        return ((point1.x - point2.x) ** 2 + (point1.y - point2.y) ** 2) ** 0.5

    @staticmethod
    def on_line(point, line):
        # Check if a point is on a line segment
        x, y = point.x, point.y
        x1, y1, x2, y2 = line

        # Check if the point is one of the line's endpoints
        if abs(x - x1) < Geometry.TOLERANCE and abs(y - y1) < Geometry.TOLERANCE:
            return True
        if abs(x - x2) < Geometry.TOLERANCE and abs(y - y2) < Geometry.TOLERANCE:
            return True

        # Check if the point is within the bounding box of the line segment
        if (x1 <= x <= x2 or x2 <= x <= x1) and (y1 <= y <= y2 or y2 <= y <= y1):
            # Calculate the perpendicular distance from the point to the line
            try:
                distance = abs((x2 - x1) * (y1 - y) - (x1 - x) * (y2 - y1)) / ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
                return distance < Geometry.TOLERANCE
            except ZeroDivisionError:
                return False  # Handle division by zero error

        return False

class Point:
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

class Plotter(Geometry):
    def __init__(self, title=None, xlabel=None, ylabel=None):
        # Initialize a plot with optional title, xlabel, and ylabel
        plt.figure()
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)

    def add_polygon(self, xs, ys):
        # Add a filled polygon to the plot
        plt.fill(xs, ys, 'lightgray', label='Polygon')

    def add_point(self, x, y, kind=None):
        # Add a point to the plot with a specified kind (outside, boundary, inside, unclassified)
        if kind == 'outside':
            plt.plot(x, y, 'ro', label='Outside')
        elif kind == 'boundary':
            plt.plot(x, y, 'bo', label='Boundary')
        elif kind == 'inside':
            plt.plot(x, y, 'go', label='Inside')
        else:
            plt.plot(x, y, 'ko', label='Unclassified')

    def show(self):
        # Display the plot with legend
        handles, labels = plt.gca().get_legend_handles_labels()
        by_label = dict(zip(labels, handles))
        plt.legend(by_label.values(), by_label.keys())
        plt.show()

def get_user_test_point():
    # Get user input for the coordinates of a test point
    try:
        x = float(input("Enter the x-coordinate of the test point: "))
        y = float(input("Enter the y-coordinate of the test point: "))
        return Point(x, y)
    except (ValueError, TypeError):
        print("Invalid input. Please enter numerical values for coordinates.")
        return get_user_test_point()

print("Welcome to the 'Hit the Polygon' Game!")
print("Try to hit the target by classifying points as inside, on the boundary, or outside the polygon.")
print("Let's see how well you can 'Hit the Polygon'!\n")

if __name__ == "__main__":
    # Step 1: Read polygon coordinates and create a Polygon object
    polygon_filename = 'polygon.csv'
    try:
        with open(polygon_filename, 'r') as file:
            next(file)  # Skip the header line
            polygon_coordinates = [Point(float(line.split(',')[1]), float(line.split(',')[2])) for line in file]
    except FileNotFoundError:
        print(f"Error: The file '{polygon_filename}' is not found.")
        exit()

    polygon = Polygon(polygon_coordinates)

    # Initialize counters
    count_inside = 0
    count_boundary = 0
    count_outside = 0

    while True:
        # Read a point from the user for testing
        test_point = get_user_test_point()

        # Categorize the point and print the result
        try:
            classification = polygon.classify_point_using_mbr_and_rca(test_point)

            # Increment the appropriate counter
            if classification == "inside":
                count_inside += 1
            elif classification == "boundary":
                count_boundary += 1
            else:
                count_outside += 1

            # Output the classification based on the classification result
            if classification == "inside":
                print("Nice shot! Your point is safely inside the polygon!")
            elif classification == "boundary":
                print("You're walking the line! Your point is on the boundary of the polygon!")
            else:
                print("Oops! Your point is outside the polygon. Try again!")

        except Exception as e:
            print(f"Error during point classification: {e}")
            exit()

        # Plot the point and polygon
        plotter = Plotter(title="Polygon & User Point", xlabel="X-axis", ylabel="Y-axis")
        polygon.points.append(polygon.points[0])
        polygon_xs, polygon_ys = zip(*[(point.x, point.y) for point in polygon.points])
        plotter.add_polygon(polygon_xs, polygon_ys)
        plotter.add_point(test_point.x, test_point.y, kind=classification)
        plotter.show()

        # Print counters
        print("\nClassification Statistics:")
        print(f"Points inside the polygon: {count_inside}")
        print(f"Points on the boundary of the polygon: {count_boundary}")
        print(f"Points outside the polygon: {count_outside}")

        # Ask the user if they want to continue
        continue_process = input("Do you want to classify another point? (yes/no): ").lower()
        if continue_process != 'yes':
            print("Thank you for playing 'Hit the Polygon' Game!")
            break