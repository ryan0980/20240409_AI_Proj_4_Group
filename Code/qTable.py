import numpy as np

# The filename where the Q-table will be saved
Q_TABLE_FILENAME = 'q-table4.npy'


def initialize_q_table():
    """ Initialize the [40][40][4] Q-table with zeros. """
    return np.zeros((40, 40, 4), dtype=float)


def save_q_table(q_table, filename=Q_TABLE_FILENAME):
    """ Save the Q-table to a file. """
    np.save(filename, q_table)


def load_q_table(filename=Q_TABLE_FILENAME):
    """ Load the Q-table from a file. """
    try:
        q_table = np.load(filename)
    except FileNotFoundError:
        print("File not found. Creating a new Q-table.")
        q_table = initialize_q_table()
    return q_table


# For demonstration purposes, let's use these functions
if __name__ == '__main__':
    # Initialize or load the Q-table
    q_table = load_q_table()

    # Here you can manipulate the Q-table as needed, for example:
    # q_table[0, 0, 0] = 1.0
    print(q_table[20][39][0])
    # Save the new or updated Q-table
    save_q_table(q_table)