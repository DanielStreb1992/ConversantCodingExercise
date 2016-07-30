"""Test File."""

from csv import Sniffer, DictReader

import matplotlib.dates as dt
import matplotlib.pyplot as plt
import random

from matplotlib.dates import HourLocator, MinuteLocator, DateFormatter

# Take file name as raw string
test_file = r'Data(Relevant).csv'

# List of valid data centers
dataCenters = ('I', 'A', 'S')


def create_reader(csvfile=None):
    """
    Summary: Validates a csv file, returns a DictReader object.

    Description: Takes one argument: "data" (Should be a csv file)
    """
    # Determines the dialect of the csv file for processing
    file_dialect = Sniffer().sniff(csvfile.read(1024))

    # Resets the read/write pointer within the file
    csvfile.seek(0)

    # Checks to see that the csv file imported has a header row,
    # that will be used for later parsing.
    print("Header: {}".format(Sniffer().has_header(csvfile.read(1024))))
    print('Delimiter: "{}"'.format(file_dialect.delimiter))

    # Resets the read/write pointer within the file
    csvfile.seek(0)

    # Creates a DictReader object with the csvfile provided, and the
    # dialect object to define the parameters of the reader instance.
    reader = DictReader(csvfile, dialect=file_dialect)

    # Return DictReader object
    return reader


def valid_number(number):
    """
    Summary: Checks that value is a valid positive number.

    Description: Accepts positive whole and decimal numbers.
    """
    try:
        # Checking that entered value can be converted to a float.
        # Excludes letters and symbols.
        float(number)

        # Checking that validated number is nonnegative.
        if float(number) > 0:
            return True
        return False
    except ValueError:
        return False


def create_dc_dataset(reader=None, data_centers=None):
    """
    Summary: Creates a dataset of dcs and their respective times, values.

    Arguments: 'reader' defines a reader object used to read a csv file.
    'dataCenters' is a list containing data center names that are to be
    graphed.
    """
    dcs_to_graph = []
    ignored_records = []

    for dc in data_centers:
        dcs_to_graph.append({'Name': dc, 'Time_data': [], 'Value_data': []})

    for row in reader:
        # Checking that the 'DC' matches one defined in "dataCenters" list
        if row.get('DC') in dataCenters:
            # Validating DC's recorded value is a positive nonnegative number.
            if not valid_number(row.get('Value')):
                ignored_records.append(row)  # Archiving ignored records
            else:
                for data_cent in dcs_to_graph:
                    if data_cent['Name'] == row.get('DC'):
                        data_cent['Time_data'].append(float(row.get('Time')))
                        data_cent['Value_data'].append(float(row.get('Value')))

    return dcs_to_graph


def graph_dataset(dc_dataset_to_graph=None):
    """
    Summary: function that graphs data center dataset.

    Arguments: 'dc_dataset_to_graph' is a list containing dictionary
    instances holding specific datacenter attributes for value and time
    """
    # List to keep track of plotted data centers for legend creation
    plotted_dc = []

    hours = HourLocator(byhour=range(24), interval=2)
    minutes = MinuteLocator(byminute=range(60), interval=30)
    time_fmt = DateFormatter('%H:%M%p %x')
    fig, ax = plt.subplots()

    xmax = None
    ymax = None

    for dc in dc_dataset_to_graph:

        # Making an array of x values(time axis)
        x = [dt.epoch2num(time) for time in dc['Time_data']]
        xmax = random.choice(x)
        # Making an array of y values(value axis)
        y = dc['Value_data']
        ymax = max(y)

        ax.plot_date(x, y, xdate=True)

        plt.annotate(
            s=dc['Name'] + ' Max Value',
            xy=(xmax, ymax),
            xytext=(xmax + 0.1, ymax + 20),
            arrowprops=dict(facecolor='black', shrink=0.05),
        )

        # Adding data center name to plotted list for dynamic legend creation
        plotted_dc.append(dc['Name'])

    ax.xaxis.set_major_locator(hours)
    ax.xaxis.set_major_formatter(time_fmt)
    ax.xaxis.set_minor_locator(minutes)
    ax.autoscale_view()

    ax.fmt_xdata = DateFormatter('%A %b %d %H:%M%p')
    ax.grid(True)

    fig.autofmt_xdate()

    # Giving scatterplot a title
    plt.title("Data Centers(Value vs. Time)")
    # Making axis labels
    plt.xlabel('Time')
    plt.ylabel('Value')

    # Making a legend for the graph
    plt.legend(['Data Center: ' + dc for dc in plotted_dc])

    plt.show()

# Opening data binary file for reading, hence 'rb', as 'csvfile'.
with open(test_file, 'r') as csvfile:
    # Creates a reader object for later data manipulation
    reader = create_reader(csvfile)

    # Resetting read/write pointer to beginning of file
    csvfile.seek(0)

    # Creating list for graphing data center's dataset
    dcs_to_graph = create_dc_dataset(reader, dataCenters)

    # Graphing Data Center Data
    graph_dataset(dcs_to_graph)
