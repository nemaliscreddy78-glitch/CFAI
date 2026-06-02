import random




import random


class ExamSeatingSystem:

    # =====================================================
    # CO1: Class-based state representation
    # Agent stores environment information
    # =====================================================
    def __init__(self):

        # State representation using dictionary
        # {hall_id: {'rows': r, 'cols': c, 'streams': {}, 'grid': [[]]}}
        self.halls = {}

    # =====================================================
    # CO1: Functions + Problem Formulation
    # Creates a hall environment
    # =====================================================
    def create_hall(self):

        print("\n--- Create New Exam Hall ---")

        hall_id = input("Enter a unique Hall ID (e.g., LH-01, Hall-A): ").strip().upper()

        # Constraint validation
        if hall_id in self.halls:
            print(f"Error: Hall ID '{hall_id}' already exists.")
            return

        rows = int(input("Enter number of rows: "))
        cols = int(input("Enter number of columns: "))

        # CO1: Matrix/Grid representation using nested lists
        self.halls[hall_id] = {
            'rows': rows,
            'cols': cols,
            'streams': {},
            'grid': [["Empty" for _ in range(cols)] for _ in range(rows)]
        }

        print(f"Success: Hall '{hall_id}' created with {rows * cols} capacity.")

    # =====================================================
    # CO1 + CO3
    # Stream data collection and constraint setup
    # =====================================================
    def update_stream_data(self, hall_id):

        print(f"\n--- Updating Stream Data for {hall_id} ---")

        num_streams = int(input("How many streams are participating in this hall? "))

        streams = {}
        total_students = 0

        # CO1: Looping and dictionary insertion
        for _ in range(num_streams):
            name = input("Stream Name (e.g., CSE, ECE): ").upper()
            count = int(input(f"Number of students in {name}: "))

            streams[name] = count
            total_students += count

        hall = self.halls[hall_id]

        # CO3: Constraint checking
        if total_students > (hall['rows'] * hall['cols']):
            print("Warning: Number of students exceeds hall capacity!")

        self.halls[hall_id]['streams'] = streams

        print(f"Stream data updated for {hall_id}.")

    # =====================================================
    # CO2 + CO3
    # Heuristic Search + CSP-based seating arrangement
    # =====================================================
    def generate_plan(self, hall_id):

        hall = self.halls[hall_id]

        rows, cols = hall['rows'], hall['cols']
        streams_dict = hall['streams']

        if not streams_dict:
            print("Error: No stream data found for this hall. Update streams first.")
            return

        # =================================================
        # CO1: Dictionary and list processing
        # =================================================
        stream_lists = {s: [s] * c for s, c in streams_dict.items()}

        stream_names = list(stream_lists.keys())

        # Randomized ordering
        # CO2: Tie-breaking strategy intuition
        random.shuffle(stream_names)

        # Reset grid state
        new_grid = [["Empty" for _ in range(cols)] for _ in range(rows)]

        stream_idx = 0

        # =================================================
        # CO2: State-space traversal using nested loops
        # =================================================
        for r in range(rows):
            for c in range(cols):

                # =============================================
                # Single Stream Case
                # Checkerboard placement heuristic
                # =============================================
                if len(stream_names) == 1:
                    s_name = stream_names[0]

                    if (r + c) % 2 == 0 and stream_lists[s_name]:
                        new_grid[r][c] = stream_lists[s_name].pop()

                # =============================================
                # Multiple Streams
                # Constraint Satisfaction Logic
                # =============================================
                else:
                    attempts = 0

                    # =========================================
                    # CO3: Forward checking intuition
                    # CO2: Heuristic-guided search
                    # =========================================
                    while attempts < len(stream_names):

                        current_s = stream_names[stream_idx]

                        # Neighbor checking
                        left = new_grid[r][c - 1] if c > 0 else None
                        top = new_grid[r - 1][c] if r > 0 else None

                        # =====================================
                        # CO3: CSP Constraint Validation
                        # Avoid adjacent same-stream students
                        # =====================================
                        if stream_lists[current_s] and current_s != left and current_s != top:
                            new_grid[r][c] = stream_lists[current_s].pop()
                            break

                        # =====================================
                        # CO2: Search exploration
                        # =====================================
                        stream_idx = (stream_idx + 1) % len(stream_names)
                        attempts += 1

                    # Move to next stream
                    stream_idx = (stream_idx + 1) % len(stream_names)

        # Final seating state
        self.halls[hall_id]['grid'] = new_grid

        print(f"\nPlan generated for {hall_id}.")

        # Display result
        self.view_hall(hall_id)

    # =====================================================
    # CO1: Grid visualization
    # CO3: Timetabling / scheduling visualization
    # =====================================================
    def view_hall(self, hall_id):

        hall = self.halls[hall_id]

        print(f"\n--- Seating Plan: {hall_id} ({hall['rows']}x{hall['cols']}) ---")
        print("=" * (hall['cols'] * 10))

        for row in hall['grid']:
            print(" | ".join(f"{s:^7}" for s in row))

        print("=" * (hall['cols'] * 10))

    # =====================================================
    # CO1: Dictionary deletion operation
    # =====================================================
    def remove_hall(self):

        hid = input("Enter Hall ID to remove: ").upper()

        if hid in self.halls:
            del self.halls[hid]
            print(f"Hall {hid} deleted.")
        else:
            print("Hall ID not found.")


# =========================================================
# Main Menu Driver
# CO1: Functions and Control Statements
# =========================================================
def main_menu():

    system = ExamSeatingSystem()

    while True:

        print("\n===== MULTI-HALL EXAM MANAGER =====")
        print(f"Total Halls Managed: {len(system.halls)}")

        print("1. Add New Hall")
        print("2. Manage Hall (Update Streams & Generate Plan)")
        print("3. View Specific Hall Plan")
        print("4. Remove a Hall")
        print("5. Exit")

        choice = input("Select an option: ")

        if choice == '1':
            system.create_hall()

        elif choice == '2':
            hid = input("Enter Hall ID to manage: ").upper()

            if hid in system.halls:
                system.update_stream_data(hid)
                system.generate_plan(hid)
            else:
                print("Hall ID not found.")

        elif choice == '3':
            hid = input("Enter Hall ID to view: ").upper()

            if hid in system.halls:
                system.view_hall(hid)
            else:
                print("Hall ID not found.")

        elif choice == '4':
            system.remove_hall()

        elif choice == '5':
            print("System shutting down. Goodbye!")
            break

        else:
            print("Invalid input.")


# =========================================================
# Program Entry Point
# =========================================================
if __name__ == "__main__":
    main_menu()
