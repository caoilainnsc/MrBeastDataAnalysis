"""
    CS051P Lab Assignments: PPM Processing

    Name: Caoilainn Christensen

    Date: May 8th, 2024

    The final project for CSCI51P - analyzing a data set of Mr. Beast videos and statistics related to them. The
    questions this project is trying to answer are:
    - Do longer videos have higher comment counts (possibly because there is more to talk about)?
    - Over time how has the length of Mr. Beast’s videos changed? Is there any close correlation with view count, or do
      both just change over time unrelated to each other?
    - Do videos that have “$” in the title have higher view counts? How about “win”, “!”, "vs", or "survive"?

    The plots that will be created to answer these questions are:
    - For the first question it will be a graph comparing the comment counts to the duration in seconds
    - For the second question it would be a graph of length in seconds and publish time and also a graph with time and
      view count. Comparing the two graphs to see if there is any similarity would be the main goal
    - For the third question it would be a bar graph comparing the average view count to videos where the title contains
      “$”, “win”, “!”, "vs", and "survive"

    For the additional libraries I used numpy to get the correlation coefficients and scipy to be able to produce error
    bars.
"""
import matplotlib.pyplot as plt
import numpy as np
import scipy as sp


def process_file(filename):
    """
    Takes a csv file and returns a list of list. Each list is a line with each element being one element in the line
    :param filename: (str) the name of the file to read
    :return: (lst) the list of lists with the file's elements
    """
    # Opens the file to read
    file_in = open(filename, "r")
    # Makes a list for the lists and a list (that will be reset) for each line
    file_list = []
    line_list = []
    # Makes a variable to hold the current element
    current_elem = ""
    # Makes a variable to hold the element when it is in the description
    desc = ""
    # A variable to determine if it is in the description (so new lines and commas will stay part of the same element)
    in_desc = False

    # Goes through each line and each character
    for line in file_in:
        for char in line:

            # For all characters not in the description
            if not in_desc:

                # If it is a new line it finishes the current list and adds it to the file list. It also resets the line
                # and current element
                if char == "\n":
                    line_list.append(current_elem)
                    file_list.append(line_list)
                    line_list = []
                    current_elem = ""

                # If the character is a quotation mark, it marks the beginning of the description, it adds the current
                # element and resets the holder
                elif char == '"':
                    in_desc = True

                # If it is any other element that isn't a comma, it adds it to the current element variable
                elif char != ",":
                    current_elem += char

                # If it is a comma, it adds that element to the line list and resets the element variable
                else:
                    line_list.append(current_elem)
                    current_elem = ""
                    desc = ""

            # For all characters in the description
            else:

                # If it is a quotation mark, it signifies the end of the description, it adds the variable to the line
                # list and resets the description variable and current elem variable
                if char == '"':
                    in_desc = False

                # If it is any other character, it adds the char to the description variable
                else:
                    desc += char

    # Closes the file
    file_in.close()
    # Returns the file list
    return file_list


def make_list_smaller(file_list):
    """
    Takes a file list and makes it 1/3 of the size
    :param file_list: (str) the file list of lists
    :return: (lst) a list containing every third list from the file given
    """
    # Makes a list to hold every third element
    small_list = []

    # Goes through each element and appends every third one to the small_list
    for i in range(0, len(file_list), 3):
        small_list.append(file_list[i])

    # Returns the list
    return small_list


def len_com_dict(file_list):
    """
    Takes a file list and makes a dictionary with the keys as the duration and the number of comments as the values
    :param file_list: (lst) a file list to go through
    :return: (dict) the dictionary with the durations and comment counts
    """
    # Creates a dictionary to hold values in
    len_com = {}

    # Goes through each element in the file list (each line)
    for elem in file_list:
        # If both the duration and comment count aren't empty, then it adds them to the dictionary
        if elem[5] != "" and elem[8] != "" and int(elem[5]) < 1000:
            len_com[int(elem[5])] = int(elem[8])

    # Returns the dictionary
    return len_com


def date_list(date_str):
    """
    Takes the date in the format given from the csv file and turns it into a tuple that can be more easily read
    :param date_str: (str) the string in the format given
    :return: (tup) a tuple with the values year, day, and month
    """
    # Puts the first four characters (the year) into the year variable
    year = int(date_str[0:4])

    # If the month starts with zero it only uses the second number for the month variable and if not it uses both
    if date_str[5] == 0:
        month = int(date_str[6])
    else:
        month = int(date_str[5:7])

    # If the day starts with zero it only uses the second number for the day variable and if not it uses both
    if date_str[8] == 0:
        day = int(date_str[9])
    else:
        day = int(date_str[8:10])

    # Returns a tuple the year, month, and day
    return (year * 100) + month + (day / 10)


def date_len_dict(file_list):
    """
    Takes a file list and returns a dictionary with the day posted as the keys and the duration of the video as the
    values
    :param file_list: (lst) the file list to go through
    :return: (dict) the dictionary containing the dates and durations
    """
    # Makes a dictionary to hold the values in
    date_len = {}

    # Goes through each element (line) in the file and if neither value is blank it adds the date (as a tuple using
    # date_list and the duration
    for elem in file_list:
        if elem[3] != "" and elem[5] != "" and int(elem[5]) < 1000:
            date_len[date_list(elem[3])] = int(elem[5])

    # Returns the dictionary
    return date_len


def date_view_dict(file_list):
    """
    Takes a file list and returns a dictionary with the day posted as the keys and the view count of the video as the
    values
    :param file_list: (lst) the file list to go through
    :return: (dict) the dictionary containing the dates and view counts
    """
    # Makes a dictionary to hold the values in
    date_view = {}

    # Goes through each element (line) in the file and if neither value is blank it adds the date (as a tuple using
    # date_list and the duration
    for elem in file_list:
        if elem[3] != "" and elem[6] != "":
            date_view[date_list(elem[3])] = int(elem[6])

    # Returns the dictionary
    return date_view


def len_view_dict(file_list):
    """
    Takes a file list and returns a dictionary with the duration of the videos as the keys and the view count as the
    values
    :param file_list: (lst) the file list to go through
    :return: (dict) the dictionary containing the views and durations
    """
    # Makes a dictionary to hold the values in
    len_view = {}

    # Goes through each element (line) in the file and if neither value is blank it adds the date (as a tuple using
    # date_list and the duration
    for elem in file_list:
        if elem[5] != "" and elem[7] != "" and int(elem[5]) < 1000 and int(elem[7]) < 5000000:
            len_view[elem[5]] = int(elem[7])

    # Returns the dictionary
    return len_view


def avg_views_for_title_str(file_list, word):
    """
    Takes a file list and a character and returns the average number of views for each video with a title containing
    that character
    :param file_list: (lst) the file list to go through
    :param word: (str) the character to check if is in the title
    :return: (float) the average view count of each video with the char in the title
    """
    # Creates a counter for views in the videos and the number of videos included
    views = 0
    num = 0

    # Goes through the file list and if the character is in the title it adds the view count to views and adds one to
    # num
    for elem in file_list:
        if word.upper() in elem[1].upper() and elem[6] != "":
            views += int(elem[6])
            num += 1

    # If there were videos counted (it wouldn't divide by 0) it returns views/num (the average) and if not returns 0.0
    if num != 0:
        return views / num
    return 0.0


def avg_views(file_list):
    """
    Gets the average number of views in all of the videos
    :param file_list: (lst) the file list to go through
    :return: (float) the average number of views in all of the videos included
    """
    # Sets variables to hold total number of views and number of videos
    views = 0
    num = 0

    # Goes through the file list and adds the views (if included) to views and adds one to the number of videos
    for elem in file_list:
        if elem[6] != "":
            views += int(elem[6])
            num += 1

    # Returns views divided by num which is the average number of views
    return views / num


def plot_com_len(file_list):
    """
    Plots a scatterplot with the length being the x-axis and the number of comments being the y-axis
    :param file_list: (lst) the file list to get data from
    :return: (str) the correlation coefficient
    """
    # Creates a dictionary with the lengths as keys and the number of comments as values using len_com_dict
    len_com = len_com_dict(file_list)
    # Creates a list of just the durations and sorts the list
    seconds = list(len_com.keys())
    seconds.sort()
    # Creates a list to hold the sorted dictionary
    sorted_dict = {}

    # Goes through the sorted list of durations and adds each duration and its value in len_com (the number of comments
    # to sorted_dict
    for elem in seconds:
        sorted_dict[elem] = len_com[elem]

    # Creates a scatter plot with the keys and values in sorted_dict with labels to match, saves, and shows the plot
    plt.scatter(list(sorted_dict.keys()), list(sorted_dict.values()))
    plt.xlabel("Duration in Seconds")
    plt.ylabel("Average Number of Comments Per Video")
    plt.title("Number of Comments Compared to Duration of Video")
    plt.savefig("visualization1.png", bbox_inches="tight")
    plt.show()

    # Returns a string that has the correlation coefficient
    return ("The correlation coefficient of the number of comments to the duration of the video is " +
            str(np.corrcoef(list(sorted_dict.keys()), list(sorted_dict.values()))[0][1]) + ".")


def plot_time_len_views(file_list):
    """
    Takes a file list and makes 3 graphs: one of time vs duration, one of time vs views, and one of duration vs views
    :param file_list: (lst) the file list to get data from
    :return: (str) the correlation coefficient of duration vs views
    """
    # Creates a dictionary of the date made as keys and the duration of videos as the values and makes lists for x and y
    # to hold the values to plot
    len_date = date_len_dict(file_list)
    x = []
    y = []

    # Goes through dates in len_date and adds them to the x list, then sorts them
    for key in len_date.keys():
        x.append(key)
    x.sort()
    # For each element in x, it adds the y key to the y list
    for elem in x:
        y.append(len_date[elem])

    # It makes the x list a list of videos in order, so it is spaced directly over time
    for i in range(len(x)):
        x[i] = i

    # It plots the time vs duration graph with labels
    plt.scatter(x, y)
    plt.xlabel("Order of Video Posted (1 = first video posted)")
    plt.ylabel("Duration of Video")
    plt.title("Change in Duration of Videos Over Time")
    plt.savefig("visualization2.1.png", bbox_inches="tight")
    plt.show()

    # Creates a dictionary with the dates as keys and the number of views as values using date_view_dict and makes x
    # and y lists to hold values in to plot
    view_date = date_view_dict(file_list)
    x1 = []
    y1 = []

    # Goes through each date in view_date and adds it to the x list then sorts it
    for elem in view_date.keys():
        x1.append(elem)
    x1.sort()
    # For every element in the x list it adds the corresponding y value to the y list
    for elem in x1:
        y1.append(view_date[elem])

    # Makes each x value the order of the videos so that the spacing over time is correct
    for i in range(len(x1)):
        x1[i] = i

    # Creates a scatterplot of views over time with labels
    plt.scatter(x1, y1)
    plt.xlabel("Order of Video Posted (1 = first video posted)")
    plt.ylabel("Number of Views")
    plt.title("Change in Number of Views Over Time")
    plt.savefig("visualization2.2.png", bbox_inches="tight")
    plt.show()

    # Creates a dictionary with the duration of videos as keys and the number of views as values using len_view_dict
    # then makes x and y lists to hold values to plot
    len_view = len_view_dict(file_list)
    x2 = []
    y2 = []

    # Goes through each duration in len_view and adds it (as an int) to the x list and sorts it
    for elem in len_view.keys():
        x2.append(int(elem))
    x2.sort()
    # For each element it adds the corresponding view count in len_view to the y list
    for elem in x2:
        y2.append(len_view[str(elem)])

    # Creates a scatterplot of duration compared to number of views, saves it, and shows it
    plt.scatter(x2, y2)
    plt.xlabel("Duration of Video in Seconds")
    plt.ylabel("Number of Views")
    plt.title("Change in Number of Views Compared to the Duration")
    plt.savefig("visualization2.3.png", bbox_inches="tight")
    plt.show()

    # Returns a string that has the correlation coefficient of duration to view count
    return ("The correlation coefficient of the duration over time is " +
            str(np.corrcoef(x, y)[0][1]) + ".\nThe correlation coefficient of the views over time is " +
            str(np.corrcoef(x1, y1)[0][1])
            + ".\nThe correlation coefficient of the duration of the video to the number of views is " +
            str(np.corrcoef(x2, y2)[0][1]) + ".")


def plot_title_avgs(file_list):
    """
    Creates a bar graph of the average view count of
    :param file_list: (lst) the file list to get data from
    :return: (None) None
    """
    # Gets the averages of all videos and videos with $, !, win, vs, and survive
    all_vids_avg = avg_views(file_list)
    dollar_sign_avg = avg_views_for_title_str(file_list, "$")
    exclamation_point_avg = avg_views_for_title_str(file_list, "!")
    win_avg = avg_views_for_title_str(file_list, "win")
    vs_avg = avg_views_for_title_str(file_list, "vs")
    survive_avg = avg_views_for_title_str(file_list, "survive")

    # Creates the x and y values to be graphed and the labels for the x values and then plots it
    x = [0, 1, 2, 3, 4, 5]
    heights = [all_vids_avg, dollar_sign_avg, exclamation_point_avg, win_avg, vs_avg, survive_avg]
    x_labels = ["All", "$", "!", "WIN", "VS", "SURVIVE"]
    plt.bar(x, heights, tick_label=x_labels)

    # Labels the x and y axes and adds a title
    plt.xlabel("Word/Character Included in Title")
    plt.ylabel("Average Number of Views")
    plt.title("Average Number of Views of Videos Containing Certain Words/Characters in Title")
    # Creates error bars
    plt.errorbar(x, heights, yerr=sp.stats.sem(heights), ecolor="red", fmt="r.", capsize=5)

    # Saves the plot and shows the graph
    plt.savefig("visualization3.png", bbox_inches="tight")
    plt.show()


def main():
    """
    The code used to make the file MrBeastSmaller.csv

    smaller = make_list_smaller(process_file("MrBeastFile.csv")[1:])
    file_out = open("MrBeastSmaller.csv", "w")
    for line in smaller:
        line_holder = ""
        for elem in line:
            line_holder += elem + ","
        file_out.write(line_holder + "\n")
    file_out.close()
    """
    # Opens the smaller MrBeast file and turns it into a list
    file_in = open("MrBeastSmaller.csv", "r")
    smaller_list = []
    for line in file_in:
        smaller_list.append(line.split(",")[:-1])

    # Prints the two functions that have correlation coefficients (also running them) and runs the title vs average view
    # bar chart function
    print(plot_com_len(smaller_list))
    print(plot_time_len_views(smaller_list))
    plot_title_avgs(smaller_list)


if __name__ == '__main__':
    main()
