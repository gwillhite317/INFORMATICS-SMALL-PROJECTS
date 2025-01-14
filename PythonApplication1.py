import csv
from csv import DictReader
import numpy as np

dict_names = {}
dict_sales = {}



#This is where we open the first csv file and identify it as names
#
with open("C:/Users/mowma/Downloads/snames _1_.csv", 'r') as names:
    head = names.readline().strip(",")
    for line in names:    
        #for every line (essentially every row / paired entry)
        lines = line.strip().split(',')    
        # strip all whitespace and commas 
        dict_names[lines[0]] = lines[1:]    
        # this creates key value pairs, the key being lines[0] the value being lines[1:] for every line then adding them to a dictionary
#This results in the dictionary "dict_names" containing all entries from the csv file 

#This is the same idea however the approach is a little different, the reason being threre can be multiple sale/donation entries for a single student
#another reason is that the formatting and data takes different forms (sales vs donations)
with open("C:/Users/mowma/Downloads/sales _1_.csv", 'r') as sales:   
    #open the file and read it in, refer to it as sales
    reader = csv.reader(sales) 
    #creating a csv reader object allows for easily traversing throught the lines
    next(reader) 
   # we are gonna skip the header row
    for line in reader:  
        #loop over each line in the csv
        student = line[0].strip()  
        #get the students name and strip whitespace
        sale = line[1].strip()  
        #get the sale or donation and strip whitespace
        if student in dict_sales:  
            #check if students name is already a key in dict_sales
            dict_sales[student].append(sale)  
            #if the student is already a key in the dictionary, append the new sale to their list of sales
        else:  
            #if not in the dictionary, add them with their sale into the dictionary
            dict_sales[student] = [sale]



#Q1
popcorn_count = 0
#set a count for our bags opf popcorn
for value in dict_sales.values():
    #for every value list (corresponding to a key)
    for item in value:
        #for item in list of values (because students can have multiple salues)
        if 'bags of popcorn' in item or 'bag of popcorn' in item:
            #here we are checking if the value was a sale (not a donation) by checking keywords
            num_bags = int(item.split()[0])
            #get the number of bags, taking the first integer (in every item entry the number of popcorn bags is at the first index)
            popcorn_count += num_bags   
            #add the number of bags determined by num_bags

print(f"Total bags of popcorn sold: {popcorn_count}")
#print to the screen


#Q2
#A
#In this section we are going to focus on using numpy which is an extremely useful python library
#we will specifically focus on using np.array which is a feature that allows us to turn lists or tuples into arrays
#once we have these arrays numpy has many built in functions that allows us to easily perform mathematical calculations

profit_list = []
#create an empty list to store our profits
for value in dict_sales.values():
    #for every value which is going to be a list of sales
    for item in value:
        # for each item in the list of sales (our value)
        if 'bags of popcorn' in item or 'bag of popcorn' in item:
            #same logic as above, checking if it is a sale or donation by checking keywords
                  bag_nums = int(item.split()[0])
                  #again same logic, taking number of bags
                  profit_list.append(bag_nums * 3)
                  #each bag yields $3 of profit, this could easily be changed if the price changes, just change the number
                  #add each value of bag_nums with the price adjustment to the profit list

profits_to_array = np.array(profit_list)
# here is where we use numpy to create an array
average_sale = np.mean(profits_to_array)
#calculate the average sale by using np.mean
print(f"Average sale : $ {average_sale:.2f}")
#print out our mean to the screen

#B

donation_list = []
#gonna be followiing a lot of the same logic here
for value in dict_sales.values():
    for item in value:
        #go through every item in list of sales
        if '$' in item:
            #check if its a donation, all donation entries begin with '$' then have an int following
            don_nums = int(item.strip("$"))
            #we can just strip the dollar sign here
            donation_list.append(don_nums)
            #then we append the int from the item to the list

donations_to_array = np.array(donation_list)
#create our array
average_donation = np.mean(donations_to_array)
#find average donation by finding the mean of all the values in the list
print(f"Average donation: $ {average_donation:.2f}")
#print our average donation

     
#C

#here we also could have just used the profits_to_array to calculate the total raised but for organizational reasons I just repeated the whole thing here
# would just be total_profits = np.sum(profits_to_array)

total_raised_popcorn = []
for value in dict_sales.values():
    for item in value:
        #all the above is the same logic, make a list and iterate through every value in sale
        if 'bags of popcorn' in item or 'bag of popcorn' in item:
            #check if its a sale
            corn_nums = int(item.split()[0])
            total_raised_popcorn.append(corn_nums * 3)
            #add profit amount

total_to_array = np.array(total_raised_popcorn)
#create our array
total_corn_sales = np.sum(total_to_array)
#use np.sum to add all values in array to get our total
print(f"Total Popcorn Profit: ${total_corn_sales:.2f} ")
#print to the screen


#D
#same as a bove we could have just used total_raised = np.sum(donations_to array)

total_raised_donations = []
for value in dict_sales.values():
    for item in value:
        if '$' in item:
            don_total_nums = int(item.strip('$'))
            total_raised_donations.append(don_total_nums)
            #this is all the same as question b

total_raised_array = np.array(total_raised_donations)
#create our array
total_raised = np.sum(total_raised_array)
#find total raised using np.sum
print(f"Total Donations: ${total_raised:.2f}")
#print to the screen

#E
total_amount_raised = np.add(total_raised, total_corn_sales)
#we can use np.add to add the two totals together
print(f"Total Amount Raised: $ {total_amount_raised:.2f}")
#print to the screen




#Question 3


unique_instruments = np.array(sorted(set(instrument[0] for instrument in dict_names.values())))
#here we are getting our array of distinct instruments, the innermost element extracts the instrument the student plays
#set removes duplicates, sorted sorts the list alphabetically, np.array gives us out numpy array

sales_matrix = np.zeros((len(dict_names), len(unique_instruments)))
#create a 2d matrix with each row representing a student and each coloumn is an instruement
#the matrix is initialized with zeroes
#defining our matrix size by using the length of names and distinct instruments, (number of coloumns is len(uniqueinstruments), number of rows is (len(dict_names)))

# This is where we fill our matrix
for student_band, (student, instrument_list) in enumerate(dict_names.items()):
    #for every student in the band
    #enumerate is very useful here because it gives the index(student_band), and the students name with the instrument they play
    if student in dict_sales:
        #here we get the instrument the student plays
        instrument = instrument_list[0]
        instrument_index = np.where(unique_instruments == instrument)[0][0]
        #the innermost part searches for the instrument in unique_instruments, creates a boolean array where elements that match instrument are marked as true
        #np.where returns the indices of the true values (where unique instrument matches index) 
        #the is now assigned to sales_matrix, identifying the coloumn where the sale should be recorded

        total_sales = 0
        #set sales equal to zero
        for sale in dict_sales[student]:
            #for every sale in list of sales for each student
            if 'bag' in sale or 'bags in sale' in sale:
                bags = int(sale.split()[0])
                total_sales += bags * 3  
                #  find profit using same logic as question 2a/2c
            elif '$' in sale:
                total_sales += float(sale.strip('$'))
                # find profit using same logic as 2b/2d
    
        sales_matrix[student_band, instrument_index] = total_sales
        #update the sales matrix with total sales for the student and their instrument

total_by_instrument = np.sum(sales_matrix, axis=0)
#calculate total sales for each instrument by summing up each coloumn (remember the coloumns are what contains the sale/donation amounts)
print("\nSales by Instrument:")
for i in range(len(unique_instruments)):
    #The logic here is that we are looping through every unique instrument and printing its name aswell as 
    #the total sales which is identified by the index of the index name
    print(f"{unique_instruments[i]}: ${total_by_instrument[i]:.2f}")





#Question 4

#now the majority of the heavy lifting for the next couple problems is done, but because I feel it is important for anyone reading this to be able to visualize the matrix
#we just created so I will explain it here,  Our matrix can be thought of as a dataframe, each row representing a student, each coloumn being a distinct instrument,
#and each value within the matrix being the total sales for the student corresponding to the instrument they play(each student plays one instrument)
#so that may raise the question, What about every value within the coloumns where the student in the row does not play an instrument? wouldnt they be empty? would that create problems?
#That is exactly why it is so important that we initialized our sales matrix with zeroes for every value, Zeroes vs persay an NA value permit us to do mathematical operations without interference 
#from data type errors,  hopefully that explains our sales matrix a little better and makes it easier to understand the following operations 


students_per_instrument = np.count_nonzero(sales_matrix, axis=0)
#the logic here is that we are counting per coloumn, how many values are not zero, (basically saying that there is a sale value) because zeroes represent that a student does not play the speicified instrument
average_per_person = np.divide(total_by_instrument, students_per_instrument)
#to find the average we take the total by instrument divided by the amount of students who play the instrument
sorted_indices = np.argsort(average_per_person)[::-1]
#sorting the data to show the average in descending order
print("\nInstruments Ranked by Average Amount Raised Per Person:")
for rank, i in enumerate(sorted_indices, 1):
    print(f"{rank}. {unique_instruments[i]}: ${average_per_person[i]:.2f} per person ({students_per_instrument[i]} students)")
    #here we use enumerate again which pairs each instrument’s index (from sorted_indices) with a rank starting from 1,
    #rank gives the position in the ranking, and i is the index of the instrument in unique_instruments.




#Question 5

student_totals = np.sum(sales_matrix, axis=1)
#calculates the sum of each row stored in sudent totals, the result is a 1 dimensional array
top_3 = np.argsort(student_totals)[-3:][::-1]
#sp.argsort sorts the index in an ascending order so we then take the last three indices, the [::1] reverses the order in which they appear
top_students = [list(dict_names.keys())[i] for i in top_3]
#here we get the names of the top 3 students by using the indices in top three
top_amounts = student_totals[top_3]
#retrieve the sales of the top three students
top_students_zip = zip(top_students, top_amounts)
#pairs each student name with their sales amount (tuples)

print("Three students that raised the most money: \n")
for rank, (student, amount) in enumerate(top_students_zip, 1):
    print(f"{student}: ${amount :.2f}")
    #Again we provide a rank starting from one and unpack each tuple into student name and amount
