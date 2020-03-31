
import scipy as sci
#Initialize
#Define number of rows and columns
n_rows=23
n_cols=6

#Calculate number of passengers
n_pass=n_rows*n_cols

#Create seat matrix




#Create function to assign seat number to each passenger
def AssignSeats(rq,cq,assign_type,n_pass=n_pass,n_rows=n_rows):
    if(assign_type=="SINP"):
        #Initialize initial and final positions
        i=0
        f=n_rows
        
        #Define column seating positions 
        c=[0,5,1,4,2,3]
        
        #Define iteratiion counter
        count=0
        
        #Assign queue
        while(f<=n_pass):
            rq[i:f]=list(reversed(range(0,n_rows)))
            cq[i:f]=[c[count]]*n_rows
            i+=n_rows
            f+=n_rows
            count+=1
        
    if(assign_type=="Random"):
        #Initialize possible row positions
        av_rows=sci.arange(0,n_rows,1)
        #Make as many copies of these positions as the number of columns
        av_rows=sci.tile(av_rows,(n_cols,1))
        av_rows=av_rows.T.flatten()
        
        #Initialize possible column positions
        av_cols=sci.arange(0,n_cols,1)
        #Make as many copies of these positions as the number of rows
        av_cols=sci.tile(av_cols,(n_rows,1)).flatten()
        
        #Create list of all possbile seat positions
        av_seats=sci.zeros((n_pass,2))
        for i in range(n_pass):
            av_seats[i]=[av_rows[i],av_cols[i]]
            
        #Randomize seat positions
        sci.random.shuffle(av_seats)
        rq=av_seats[:,0]
        cq=av_seats[:,1]
    
    if(assign_type=="BTF"):
        av_rows=sci.arange(0,n_rows,1)
        av_rows=sci.tile(av_rows,(n_cols,1))
        av_rows=av_rows.T.flatten()
        av_cols=sci.arange(0,n_cols,1)
        av_cols=sci.tile(av_cols,(n_rows,1)).flatten()
        av_seats=sci.zeros((n_pass,2))
        for i in range(n_pass):
            av_seats[i]=[av_rows[i],av_cols[i]]
            
        #Same as randomize except randomization is limited to specific groups
        group1=av_seats[:48]
        sci.random.shuffle(group1)
        group2=av_seats[48:96]
        sci.random.shuffle(group2)
        group3=av_seats[96:]
        sci.random.shuffle(group3)
        av_seats_final=sci.concatenate((group3,group2,group1))
        rq=av_seats_final[:,0]
        cq=av_seats_final[:,1]
   
    if(assign_type=="FTB"):
        av_rows=sci.arange(0,n_rows,1)
        av_rows=sci.tile(av_rows,(n_cols,1))
        av_rows=av_rows.T.flatten()
        av_cols=sci.arange(0,n_cols,1)
        av_cols=sci.tile(av_cols,(n_rows,1)).flatten()
        av_seats=sci.zeros((n_pass,2))
        for i in range(n_pass):
            av_seats[i]=[av_rows[i],av_cols[i]]
        group1=av_seats[:48]
        sci.random.shuffle(group1)
        group2=av_seats[48:96]
        sci.random.shuffle(group2)
        group3=av_seats[96:]
        sci.random.shuffle(group3)
        
        #Same as BTF except order of groups is swapped
        av_seats_final=sci.concatenate((group1,group2,group3))
        rq=av_seats_final[:,0]
        cq=av_seats_final[:,1]
    
    if(assign_type=="WMA"):
        window_1=sci.array([0]*n_rows)
        rows_1=sci.arange(0,n_rows,1)
        window_2=sci.array([5]*n_rows)
        rows_2=sci.arange(0,n_rows,1)
        window=sci.concatenate((window_1,window_2))
        rows=sci.concatenate((rows_1,rows_2))   
        av_seats_w=sci.column_stack((rows,window))
        sci.random.shuffle(av_seats_w)
        
        middle_1=sci.array([1]*n_rows)
        middle_2=sci.array([4]*n_rows)
        middle=sci.concatenate((middle_1,middle_2))
        av_seats_m=sci.column_stack((rows,middle))
        sci.random.shuffle(av_seats_m)
        
        aisle_1=sci.array([2]*n_rows)
        aisle_2=sci.array([3]*n_rows)
        aisle=sci.concatenate((aisle_1,aisle_2))
        av_seats_a=sci.column_stack((rows,aisle))
        sci.random.shuffle(av_seats_a)  
        av_seats=sci.concatenate((av_seats_w,av_seats_m,av_seats_a))
        rq=av_seats[:,0]
        cq=av_seats[:,1]
    
    if(assign_type=="Southwest"):
        #Make an array [0,5,0,5,...]
        window=sci.array([0,5]*n_rows)
       
        #Make an array [0,0,1,1,2,2,...]
        rows_1=sci.arange(0,n_rows,1)
        rows_2=sci.arange(0,n_rows,1)
        rows=sci.ravel(sci.column_stack((rows_1,rows_2)))
        
        w_seats=sci.column_stack((rows,window))

        w_group1=w_seats[:32,:]
        w_group2=w_seats[32:,:]
        
        aisle=sci.array([2,3]*n_rows)
        a_seats=sci.column_stack((rows,aisle))
        a_group1=a_seats[:32,:]
        a_group2=a_seats[32:,:]
        
        mega_group1=sci.concatenate((w_group1,a_group1))
        sci.random.shuffle(mega_group1)
        mega_group2=sci.concatenate((w_group2,a_group2))
        sci.random.shuffle(mega_group2)
        
        w_and_a=sci.concatenate((mega_group1,mega_group2))
        
        middle=sci.array([1,4]*n_rows)
        m_seats=sci.column_stack((rows,middle))
        m_group1=m_seats[:32,:]
        sci.random.shuffle(m_group1)
        m_group2=m_seats[32:,:]
        sci.random.shuffle(m_group2)
        
        av_seats=sci.concatenate((w_and_a,m_group1,m_group2))
        rq=av_seats[:,0]
        cq=av_seats[:,1]
        
    return rq,cq


#Create function to move passengers into aircraft
    

def MoveToAisle(t,aisle_q,pass_q,sum_time):
    if(t>sum_time[0]):
        if(aisle_q[0]==-1):
            aisle_q[0]=pass_q[0].copy()
            pass_q=sci.delete(pass_q,0)
            sum_time=sci.delete(sum_time,0)
    return aisle_q,pass_q,sum_time
#Assign seating order
    


#Create array for times


def method(type):
#Create seat and speed dictionary
    seats=sci.zeros((n_rows,n_cols))
    seats[:,:]=-1
    
    #Create aisle array
    aisle_q=sci.zeros(n_rows)
    aisle_q[:]=-1
    
    #Create initial passenger number queue
    pass_q=[int(i) for i in range(n_pass)]
    pass_q=sci.array(pass_q)
    
    #Create array for seat nos
    row_q_init=sci.zeros(n_pass)
    col_q_init=sci.zeros(n_pass)
    
    #Let's create moveto arrays
    moveto_loc=sci.zeros(n_pass)
    moveto_time=sci.zeros(n_pass)
    
    moveto_loc_dict={i:j for i in pass_q for j in moveto_loc}
    moveto_time_dict={i:j for i in pass_q for j in moveto_time}
    pass_dict={}
    time_dict={}
    aisle_q=sci.zeros(n_rows)
    aisle_q[:]=-1
    mean_time=1.5
    stddev_time=0.5
    time_q=sci.random.normal(loc=mean_time,scale=stddev_time,size=n_pass)
    
    #Define multipliers (+2 for stowing luggage)
    empty_mult=1+2
    aisle_mult=4+2
    middle_mult=5+2
    aisle_middle_mult=7+2
    time=0
    time_step=0.1
    #Create initial passenger number queue
    pass_q=[int(i) for i in range(n_pass)]
    pass_q=sci.array(pass_q)

    
    row_q,col_q=AssignSeats(row_q_init,col_q_init,type)
    
    seat_nos=sci.column_stack((row_q,col_q))
    for i in range(n_pass):
        pass_dict[i]=seat_nos[i]
    
    for i in range(n_pass):
        time_dict[i]=time_q[i]
    
    #Create sum time array
    sum_time=sci.zeros(n_pass)
    for i in range(n_pass):
        sum_time[i]=sum(time_q[:i+1])
    
    #Let's define the boarding process in a while loop
    #Define initial conditions
    
    
    exit_sum=sci.sum(pass_q)
    pass_sum=sci.sum(seats)
    
    while(pass_sum!=exit_sum):
        #Try to move passenger inside the plane if passengers are left
        if(pass_q.size!=0):
            aisle_q,pass_q,sum_time=MoveToAisle(time,aisle_q,pass_q,sum_time)
        #Scan the aisle first for non-negative units (passengers)
        for passg in aisle_q:
            if(passg!=-1):
                #Store the row of passenger in aisle
                row=int(sci.where(aisle_q==passg)[0][0])
                #See if move has been assigned to passenger
                if(moveto_time_dict[passg]!=0):
                    #If move has been assigned check if it is time to move
                    if(time>moveto_time_dict[passg]):
                        #If it is time to move follow the procedure below
                        #Check if move is forward in aisle or to seat
                        if(moveto_loc_dict[passg]=="a"):
                            #If move is in the aisle, check if position ahead is empty
                            if(aisle_q[row+1]==-1):
                                #If position is empty move passenger ahead and free the position behind
                                aisle_q[row+1]=passg
                                aisle_q[row]=-1
                                #Set moves to 0 again
                                moveto_loc_dict[passg]=0
                                moveto_time_dict[passg]=0
                        elif(moveto_loc_dict[passg]=="s"):
                            #If move is to the seat,
                            #Find seat row and column of passenger
                            passg_row=int(pass_dict[passg][0])
                            passg_col=int(pass_dict[passg][1])
                            #Set seat matrix position to the passenger number
                            seats[passg_row,passg_col]=passg
                            #Free the aisle
                            aisle_q[row]=-1
                elif(moveto_time_dict[passg]==0):
                    #If move hasn't been assgined to passenger
                    #Check passenger seat location
                    passg_row=int(pass_dict[passg][0])
                    passg_col=int(pass_dict[passg][1])
                    if(passg_row==row):
                        #If passenger at the row where his/her seat is,
                        #Designate move type as seat
                        moveto_loc_dict[passg]="s"
                        #Check what type of seat: aisle, middle or window
                        #Depending upon seat type, designate when it is time to move
                        if(passg_col==0):
                            if(seats[passg_row,1]!=-1 and seats[passg_row,2]!=-1):
                                moveto_time_dict[passg]=time+aisle_middle_mult*time_dict[passg]
                            elif(seats[passg_row,1]!=-1):
                                moveto_time_dict[passg]=time+middle_mult*time_dict[passg]                                   
                            elif(seats[passg_row,2]!=-1):
                                moveto_time_dict[passg]=time+aisle_mult*time_dict[passg]
                            else:
                                moveto_time_dict[passg]=time+empty_mult*time_dict[passg]
                        elif(passg_col==5):
                            if(seats[passg_row,4]!=-1 and seats[passg_row,3]!=-1):
                                moveto_time_dict[passg]=time+aisle_middle_mult*time_dict[passg]
                            elif(seats[passg_row,4]!=-1):
                                moveto_time_dict[passg]=time+middle_mult*time_dict[passg]                                   
                            elif(seats[passg_row,3]!=-1):
                                moveto_time_dict[passg]=time+aisle_mult*time_dict[passg]
                            else:
                                moveto_time_dict[passg]=time+empty_mult*time_dict[passg]
                        elif(passg_col==1):
                            if(seats[passg_row,2]!=-1):
                                moveto_time_dict[passg]=time+aisle_mult*time_dict[passg] 
                            else:
                                moveto_time_dict[passg]=time+empty_mult*time_dict[passg]
                        elif(passg_col==4):
                            if(seats[passg_row,3]!=-1):
                                moveto_time_dict[passg]=time+aisle_mult*time_dict[passg]
                            else:
                                moveto_time_dict[passg]=time+empty_mult*time_dict[passg]
                        elif(passg_col==2 or passg_col==3):
                            moveto_time_dict[passg]=time+empty_mult*time_dict[passg]
                    elif(passg_row!=row):
                        #If passenger is not at the row where his/her seat is,
                        #Designate movement type as aisle
                        moveto_loc_dict[passg]="a"
                        #Designate time to move
                        moveto_time_dict[passg]=time+time_dict[passg]
    
        #Iteration timekeeping
        time+=time_step
        pass_sum=sci.sum(seats)
    return time 
  

#print("The time required to board is {0:.2f}".format(time))

from flask import Flask, escape, request
    
app = Flask(__name__)
@app.route("/")

def main():
    return "Welcome"

@app.route("/BTF")
def BTF(): 
    x="{0:.2f}".format(method("BTF"))
    return x

@app.route("/FTB")
def FTB():
    x="{0:.2f}".format(method("FTB"))
    return x

@app.route("/Random")
def Random():
    x="{0:.2f}".format(method("Random"))
    return x

@app.route("/SINP")
def SINP():
    x="{0:.2f}".format(method("SINP"))
    return x

@app.route("/Southwest")
def Southwest():
    x="{0:.2f}".format(method("Southwest"))
    return x

@app.route("/WMA")
def WMA():
    x="{0:.2f}".format(method("WMA"))
    return x


if __name__=="__main__":
    app.run(debug=True,host="0.0.0.0",port=8080) 

