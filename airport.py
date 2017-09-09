#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May  6 08:54:53 2017

@author: amyyin
"""

from flask import Flask, render_template, request, session, url_for, redirect
#from flask.ext.hashing import Hashing
import pymysql.cursors
import hashlib
from hashlib import md5
import datetime
import sys


app = Flask(__name__)
#hashing = Hashing(app)

#Configure MySQL
conn = pymysql.connect(host = 'localhost',
                       user = 'root',
                       password = '',
                       db = 'airport',
                       charset = 'utf8mb4',
                       cursorclass = pymysql.cursors.DictCursor)

#Define route for home page
@app.route('/')
def home():
    return render_template('home.html')
    
#Logged out search
@app.route('/search', methods=['GET', 'POST'])
def search():
    return render_template('search.html')
    
#View search results
@app.route('/search_results', methods = ['GET', 'POST'])
def searchResults():
    #Form info
    departure_time = request.form['departure_time']
    #departure_city = request.form['departure_city']
    departure_airport = request.form['departure_airport']
    #arrival_city = request.form['arrival_city']
    arrival_airport = request.form['arrival_airport']
    

    #cursor to send queries
    cursor = conn.cursor()

    #execute query
    #query = 'SELECT * FROM flight, airport WHERE ((flight.departure_airport = airport.airport_name) AND (flight.departure_airport = %s OR airport.airport_city = %s)) AND ((flight.arrival_airport = airport.airport_name) AND (flight.arrival_airport = %s OR airport.airport_city = %s)) OR flight.departure_time = %s'
    #cursor.execute(query, (departure_airport, departure_city, arrival_airport, arrival_city, departure_time))
    query = 'SELECT * FROM flight WHERE departure_airport = %s AND arrival_airport = %s AND CAST(departure_time AS DATE) = %s'
    cursor.execute(query, (departure_airport, arrival_airport, departure_time))
    
    data2 = cursor.fetchall()
    
    #session['data'] = data

    print(data2)
    
    return render_template('search_results.html', data=data2)
        
    
#Logged out flight status
@app.route('/status', methods=['GET', 'POST'])
def status():
    return render_template('status.html')
   
#All user flights status
@app.route('/status_results', methods=['GET', 'POST'])
def statusResults():    
    #Form info
    flight_num = request.form['flight_num']
    arrival_time = request.form['arrival_time']
    departure_time = request.form['departure_time']
        
    #cursor to send queries
    cursor = conn.cursor()
        
    #execute query
    query = 'SELECT * FROM flight WHERE flight_num = %s AND CAST(departure_time AS DATE) = %s AND CAST(arrival_time AS DATE) = %s'
    cursor.execute(query, (flight_num, departure_time, arrival_time))
        
    data3 = cursor.fetchall()
            
    print(data3)
    
    return render_template('status_results.html', data=data3)
    
#Define route for login
@app.route('/login')
def login():
    return render_template('login.html')

#Login booking agent
@app.route('/booking_agent_login', methods=['GET', 'POST'])
def bookingAgentLogin():
    return render_template('booking_agent_login.html') 

#Login airline staff
@app.route('/airline_staff_login', methods=['GET', 'POST'])
def airlineStaffLogin():
    return render_template('airline_staff_login.html') 
    
#Login customer
@app.route('/customer_login', methods=['GET', 'POST'])
def customerLogin():
    return render_template('customer_login.html') 

#Authenticate the login
@app.route('/loginAuthAirlineStaff', methods=['GET', 'POST'])
def loginAuthAirlineStaff():
    #Form info
    username = request.form['username']
    password = request.form['password']
    password = password.encode('utf-8')

    #cursor to send queries
    cursor = conn.cursor()
    
    #execute query
    query = 'SELECT * FROM airline_staff WHERE (airline_staff.username = %s and airline_staff.password = %s)'
    cursor.execute(query, (username, hashlib.md5(password).hexdigest()))
    
    #stores the results in variable
    #use fetchall() if needed
    data = cursor.fetchone()
    
    cursor.close()
        
    if(data):
        #creates a session for the user
        session['username'] = username
        #return redirect(url_for(usertype+'_home'))
        return redirect(url_for('airline_staff_home'))
    else:
        #returns error to html page
        error = 'Invalid login or username'
        return render_template('airline_staff_login.html', error=error)
  
@app.route('/loginAuthBookingAgent', methods=['GET', 'POST'])
def loginAuthBookingAgent():
    #Form info
    username = request.form['username']
    password = request.form['password']
    password = password.encode('utf-8')

    #cursor to send queries
    cursor = conn.cursor()
    
    #execute query
    query = 'SELECT * FROM booking_agent WHERE (booking_agent.username = %s and booking_agent.password = %s)'
    cursor.execute(query, (username, hashlib.md5(password).hexdigest()))
    
    #stores the results in variable
    #use fetchall() if needed
    data = cursor.fetchone()
    
    cursor.close()
        
    if(data):
        #creates a session for the user
        session['username'] = username
        #return redirect(url_for(usertype+'_home'))
        return redirect(url_for('booking_agent_home'))
    else:
        #returns error to html page
        error = 'Invalid login or username'
        return render_template('booking_agent_login.html', error=error)
    
@app.route('/loginAuthCustomer', methods=['GET', 'POST'])
def loginAuthCustomer():
    #Form info
    username = request.form['username']
    password = request.form['password']
    password = password.encode('utf-8')

    #cursor to send queries
    cursor = conn.cursor()
    
    #execute query
    query = 'SELECT * FROM customer WHERE (customer.username = %s and customer.password = %s)'
    cursor.execute(query, (username, hashlib.md5(password).hexdigest()))
    
    #stores the results in variable
    #use fetchall() if needed
    data = cursor.fetchone()
    
    cursor.close()
        
    if(data):
        #creates a session for the user
        session['username'] = username
        #return redirect(url_for(usertype+'_home'))
        return redirect(url_for('customer_home'))
    else:
        #returns error to html page
        error = 'Invalid login or username'
        return render_template('customer_login.html', error=error)
    
    
#Different homepages
@app.route('/airline_staff_home')
def airline_staff_home():
    return render_template('airline_staff_home.html')
    
@app.route('/booking_agent_home')
def booking_agent_home():
    return render_template('booking_agent_home.html')
    
@app.route('/customer_home')
def customer_home():
    return render_template('customer_home.html')


#Register home page
@app.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('register.html')
    
#Register booking agent
@app.route('/booking_agent_register', methods=['GET', 'POST'])
def bookingAgentRegister():
    return render_template('booking_agent_register.html') 

#Register airline staff
@app.route('/airline_staff_register', methods=['GET', 'POST'])
def airlineStaffRegister():
    return render_template('airline_staff_register.html') 
    
#Register customer
@app.route('/customer_register', methods=['GET', 'POST'])
def customerRegister():
    return render_template('customer_register.html') 

#Authenticate the register for Booking Agent    
@app.route('/registerAuthBookingAgent', methods=['GET', 'POST'])
def registerAuthBookingAgent():
    #Form info
    username = request.form['username']
    password = request.form['password']
    booking_agent_id = request.form['booking_agent_id']
    password = password.encode('utf-8')

    #cursor to send queries
    cursor = conn.cursor()
    
    #execute query
    query = 'SELECT * FROM booking_agent WHERE (booking_agent.username = %s)'
    cursor.execute(query, (username))
    
    #stores the results in variable
    #use fetchall() if needed
    data = cursor.fetchone()

    if(data):
        #user exists
        error = "This user already exists"
        cursor.close()
        return render_template('booking_agent_register.html', error=error)
    else:
        ins = 'INSERT INTO booking_agent VALUES(%s, %s, %s)'
        cursor.execute(ins, (username, hashlib.md5(password).hexdigest(), booking_agent_id))
        #commit changes
        conn.commit()
        cursor.close()
        return render_template('home.html')
        
#Authenticate the register for Airline Staff      
@app.route('/registerAuthAirlineStaff', methods=['GET', 'POST'])
def registerAuthAirlineStaff():
    #Form info
    username = request.form['username']
    password = request.form['password']
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    date_of_birth = request.form['date_of_birth']
    airline_name = request.form['airline_name']
    password = password.encode('utf-8')

    #cursor to send queries
    cursor = conn.cursor()
    
    #execute query
    query = 'SELECT * FROM airline_staff WHERE (airline_staff.username = %s)'
    cursor.execute(query, (username))
    
    #stores the results in variable
    #use fetchall() if needed
    data = cursor.fetchone()
    
    if(data):
        #user exists
        error = "This user already exists"
        cursor.close()
        return render_template('airline_staff_register.html', error=error)
    else:
        ins = 'INSERT INTO airline_staff VALUES(%s, %s, %s, %s, %s, %s)'
        cursor.execute(ins, (username, hashlib.md5(password).hexdigest(), first_name, last_name, date_of_birth, airline_name))
        #commit changes
        conn.commit()
        cursor.close()
        return render_template('home.html')
        
#Authenticate the register for Customer    
@app.route('/registerAuthCustomer', methods=['GET', 'POST'])
def registerAuthCustomer():
    #Form info
    username = request.form['username']
    password = request.form['password']
    name = request.form['name']
    building_number = request.form['building_number']
    street = request.form['street']
    city = request.form['city']
    state = request.form['state']
    phone_number = request.form['phone_number']
    passport_number = request.form['passport_number']
    passport_expiration = request.form['passport_expiration']
    passport_country = request.form['passport_country']
    date_of_birth = request.form['date_of_birth']
    password = password.encode('utf-8')

    #cursor to send queries
    cursor = conn.cursor()
    
    #execute query
    query = 'SELECT * FROM customer WHERE (customer.username = %s)'
    cursor.execute(query, (username))
    
    #stores the results in variable
    #use fetchall() if needed
    data = cursor.fetchone()
    
    if(data):
        #user exists
        error = "This user already exists"
        cursor.close()
        return render_template('customer_register.html', error=error)
    else:
        ins = 'INSERT INTO customer VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
        cursor.execute(ins, (username, name, hashlib.md5(password).hexdigest(), building_number, street, city, state, phone_number, passport_number, passport_expiration, passport_country, date_of_birth))
        #commit changes
        conn.commit()
        cursor.close()
        return render_template('home.html')
    
    
#Logout
@app.route('/logout')
def logout():
    return render_template('logout.html')


#Define route for logged in users home page
@app.route('/:typeuser/home')
def userhome(typeuser, user_name):
    return render_template('home_'+typeuser+'.html', username = user_name)


#View flights for each user
@app.route('/airline_staff_view_flights', methods=['GET', 'POST'])
def viewFLightsAirlineStaff():
    return render_template('airline_staff_view_flights.html')
 
@app.route('/airline_staff_view_flights_results', methods=['GET', 'POST'])
def viewFlightsAirlineStaffResults():
    user_name = session['username']
    #airport_city = request.form['airport_city']
    #departure_airport = request.form['departure_airport']
    
    cursor = conn.cursor()
    #query = 'SELECT * FROM flight, airport WHERE flight.departure_airport = %s AND airport.airport_city = %s'
    #cursor.execute(query, (departure_airport, airport_city))
    query = 'SELECT * FROM flight'
    cursor.execute(query)
    #query = 'SELECT * FROM flight WHERE airline_name = %s AND flight_num = %s AND departure_airport = %s AND CAST(departure_time AS DATE) = %s AND arrival_airport = %s AND CAST(arrival_time AS DATE) = %s AND status = %s AND airplane_id = %s'
    #cursor.execute(query, (user_name, airline_name, flight_num, departure_airport, departure_time, arrival_airport, arrival_time, status, airplane_id))
    #query = 'SELECT flight.flight_id from flight, airline_staff where airline_staff.username = %s and airline_staff.airline_name = flight.airline_name'
    #cursor.execute(query, (user_name))   
        
    data2 = cursor.fetchall()
        
    print(data2)
        
    return render_template('airline_staff_view_flights_results.html', data = data2)

@app.route('/booking_agent_view_flights', methods=['GET', 'POST'])
def viewFLightsBookingAgent():
    return render_template('booking_agent_view_flights.html')

@app.route('/booking_agent_view_flights_results', methods=['GET', 'POST'])
def viewFlightsBookingAgentResults():
    user_name = session['username']
    booking_agent_id = request.form['booking_agent_id']
    customer_email = request.form['customer_email']
    airline_name = request.form['airline_name']
    flight_num = request.form['flight_num']

    cursor = conn.cursor()
    query = 'SELECT * FROM purchases, flight WHERE purchases.booking_agent_id = %s AND purchases.customer_email = %s AND flight.airline_name = %s AND flight.flight_num = %s'
    cursor.execute(query, (booking_agent_id, customer_email, airline_name, flight_num))
    
    data2 = cursor.fetchall()
        
    print(data2)
        
    return render_template('booking_agent_view_flights_results.html', data = data2)

@app.route('/customer_view_flights', methods=['GET', 'POST'])
def viewFLightsCustomer():
    return render_template('customer_view_flights.html')

@app.route('/customer_view_flights_results', methods=['GET', 'POST'])
def viewFlightsCustomerResults():
    user_name = session['username']
    ticket_id = request.form['ticket_id']
    customer_email = request.form['customer_email']
    
    cursor = conn.cursor()
    query = 'SELECT * FROM purchases, flight WHERE purchases.ticket_id = %s AND purchases.customer_email = %s'
    cursor.execute(query, (ticket_id, customer_email))
    
    data2 = cursor.fetchall()
        
    print(data2)
        
    return render_template('customer_view_flights_results.html', data = data2)
    

#Customer and Booking Agent
#Purchase tickets
@app.route('/purchase_tickets')
def purchaseTickets():
    return render_template('purchase_tickets.html') 

#Process purchase
@app.route('/process_purchase', methods=['GET','POST'])    
def processPurchase():
    user_name = session['username']
    
    #Form info
    ticket_id = request.form['ticket_id']
    customer_email = request.form['customer_email']
    booking_agent_id = request.form['booking_agent_id']
    purchase_date = request.form['purchase_date']

    #cursor to send queries
    cursor = conn.cursor()
    
    #execute query
    query = 'INSERT INTO Purchases VALUES (%s, %s, %s, %s)'
    cursor.execute(query, (ticket_id, customer_email, booking_agent_id, purchase_date));  
    
    #stores the results in variable
    #use fetchall() if needed
    data = cursor.fetchone()
    
    #if(not data):
        #flight exists
        #error = "Invalid purchase"
        #cursor.close()
        #return render_template('purchase_tickets.html', error=error)
    #else:
        #commit changes
    conn.commit()
    cursor.close()
    return redirect(url_for('customerSuccess')) 
    

#Customer and Booking Agent
#Search for flights
@app.route('/customer_search_flights')
def customerSearchFlights():    
    return render_template('customer_search_flights.html')

@app.route('/customer_search_flights_results', methods=['GET', 'POST'])
def customerSearchFlightsResults():
    user_name = session['username']
    departure_airport = request.form['departure_airport']
    arrival_airport = request.form['arrival_airport']
    departure_time = request.form['departure_time']
    
    cursor = conn.cursor()

    query = 'SELECT * FROM flight WHERE departure_airport = %s AND arrival_airport = %s AND CAST(departure_time AS DATE) = %s'
    cursor.execute(query, (departure_airport, arrival_airport, departure_time))
    
    data2 = cursor.fetchall()

    print(data2)
    
    return render_template('customer_search_flights_results.html', data=data2)

@app.route('/booking_agent_search_flights')
def bookingAgentSearchFlights():    
    return render_template('booking_agent_search_flights.html')

@app.route('/booking_agent_search_flights_results', methods=['GET', 'POST'])
def bookingAgentSearchFlightsResults():
    user_name = session['username']
    departure_airport = request.form['departure_airport']
    arrival_airport = request.form['arrival_airport']
    departure_time = request.form['departure_time']
    
    cursor = conn.cursor()

    query = 'SELECT * FROM flight WHERE departure_airport = %s AND arrival_airport = %s AND CAST(departure_time AS DATE) = %s'
    cursor.execute(query, (departure_airport, arrival_airport, departure_time))
    
    data2 = cursor.fetchall()

    print(data2)
    
    return render_template('booking_agent_search_flights_results.html', data=data2)
    
    
#Booking Agent Only
@app.route('/view_commission')
def viewCommission():
    return render_template('view_commission.html')
    
@app.route('/view_commission_results', methods=['GET','POST'])
def viewCommissionResults():
    username = session['username']
    booking_agent_id = request.form['booking_agent_id']

    #cursor to send queries
    cursor = conn.cursor() 

    query = 'SELECT price, ticket_id FROM booking_agent, flight NATURAL JOIN ticket WHERE booking_agent_id = %s'
    cursor.execute(query, (booking_agent_id))
    
    data2 = cursor.fetchall()

    print(data2)
    
    return render_template('view_commission_results.html', data=data2)
   
#==============================================================================
#     #stores the results in variable
#     #use fetchall() if needed
#     data = cursor.fetchone()
#    
#     cursor.close()
#    
#     if(not data):
#         return 0
#         
#     return render_template('view_commission.html', username = user_name)
#==============================================================================


#Airline staff only
#Create new flight
@app.route('/create_flight', methods=['GET', 'POST'])
def createFlight():
    return render_template('create_flight.html')
   
#Create new flight auth
@app.route('/create_flight_auth', methods=['GET', 'POST'])
def createFlightAuth():        
    username = session['username']

    #cursor to send queries
    cursor = conn.cursor() 

    #verify user 
    query = 'SELECT username FROM airline_staff WHERE username = %s'
    cursor.execute(query, (username))
   
    #stores the results in variable
    #use fetchall() if needed
    data = cursor.fetchall()
   
    cursor.close
   
    if(not data):
        return 0
    
    #Form info
    airline_name = request.form['airline_name']
    flight_num = request.form['flight_num']
    departure_airport = request.form['departure_airport']
    departure_time = request.form['departure_time']
    arrival_airport = request.form['arrival_airport']
    arrival_time = request.form['arrival_time'] 
    price = request.form['price']
    status = request.form['status']
    airplane_id = request.form['airplane_id']  
    print("Hi")
    print(airline_name + ", " + flight_num + ", " + departure_airport + ", " + departure_time + ", " + arrival_airport)

    #cursor to send queries
    cursor = conn.cursor()
    
    #execute query
    query = 'SELECT * FROM flight WHERE airline_name = %s and flight_num = %s'
    cursor.execute(query, (airline_name, flight_num))  
    
    #stores the results in variable
    #use fetchall() if needed
    data = cursor.fetchone()
    
    if(data):
        #flight exists
        error = "This flight already exists"
        cursor.close()
        return render_template('create_flight.html', error=error)
    else:
        ins = 'INSERT INTO flight(airline_name, flight_num, departure_airport, departure_time, arrival_airport, arrival_time, price, status, airplane_id) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)'
        cursor.execute(ins, (airline_name, flight_num, departure_airport, departure_time, arrival_airport, arrival_time, price, status, airplane_id))
        #commit changes
        conn.commit()
        cursor.close()
        return redirect(url_for('airlineStaffSuccess'))

#Change flight status
@app.route('/change_status', methods=['GET', 'POST'])
def changeStatus():
    return render_template('change_status.html')

#Change flight status auth
@app.route('/change_status_auth', methods=['GET', 'POST'])
def changeStatusAuth():    
    username = session['username']

    #cursor to send queries
    cursor = conn.cursor() 

    #verify user 
    query = 'SELECT username FROM airline_staff WHERE username = %s'
    cursor.execute(query, (username))
   
    #stores the results in variable
    #use fetchall() if needed
    data = cursor.fetchone()
   
    cursor.close
   
    if(not data):
        return 0
    
    #Form info
    airline_name = request.form['airline_name']
    flight_num = request.form['flight_num']
    status = request.form['status']

    #cursor to send queries
    cursor = conn.cursor()
    
    #execute query
    query = 'SELECT * FROM flight WHERE airline_name = %s and flight_num = %s'
    cursor.execute(query, (airline_name, flight_num))  
    
    #stores the results in variable
    #use fetchall() if needed
    data = cursor.fetchone()
    
    if(not data):
        #flight exists
        error = "This flight does not exist"
        cursor.close()
        return render_template('create_flight.html', error=error)
    else:    
        upd = 'UPDATE flight SET status = %s WHERE airline_name = %s and flight_num = %s'
        cursor.execute(upd,  (status, airline_name, flight_num))
        #commit changes
        conn.commit()
        cursor.close()
        return redirect(url_for('airlineStaffSuccess'))
        

#Add airplane
@app.route('/add_airplane', methods=['GET', 'POST'])
def addAirplane():
    return render_template('add_airplane.html')
    
#Add airplane auth
@app.route('/add_airplane_auth', methods=['GET', 'POST'])
def addAirplaneAuth():
    username = session['username']

    #cursor to send queries
    cursor = conn.cursor() 

    #verify user 
    query = 'SELECT username FROM airline_staff WHERE username = %s'
    cursor.execute(query, (username))
   
    #stores the results in variable
    #use fetchall() if needed
    data = cursor.fetchone()
   
    cursor.close
   
    if(not data):
        return 0
    
    #Form info
    airline_name = request.form['airline_name']
    airplane_id = request.form['airplane_id']
    seats = request.form['seats']

    #cursor to send queries
    cursor = conn.cursor()
    
    #execute query
    query = 'SELECT * FROM airplane WHERE airline_name = %s and airplane_id = %s'
    cursor.execute(query, (airline_name, airplane_id))  
    
    #stores the results in variable
    #use fetchall() if needed
    data = cursor.fetchone()
    
    if(data):
        #airplane exists
        error = "This airplane already exists"
        cursor.close()
        return render_template('airline_staff_home.html', error=error)
    else:    
        ins = 'INSERT INTO airplane VALUES(%s, %s, %s)'
        cursor.execute(ins, (airline_name, airplane_id, seats))
        #commit changes
        conn.commit()
        cursor.close()
        return redirect(url_for('airlineStaffSuccess'))
        
#Add airport
@app.route('/add_airport', methods=['GET', 'POST'])
def addAirport():
    return render_template('add_airport.html')
    
#Add airport auth
@app.route('/add_airport_auth', methods=['GET', 'POST'])
def addAirportAuth():    
    username = session['username']

    #cursor to send queries
    cursor = conn.cursor() 

    #verify user 
    query = 'SELECT username FROM airline_staff WHERE username = %s'
    cursor.execute(query, (username))
   
    #stores the results in variable
    #use fetchall() if needed
    data = cursor.fetchone()
   
    cursor.close
   
    if(not data):
        return 0
    
    #Form info
    airport_name = request.form['airport_name']
    airport_city = request.form['airport_city']

    #cursor to send queries
    cursor = conn.cursor()
    
    #execute query
    query = 'SELECT * FROM airport WHERE airport_name = %s'
    cursor.execute(query, (airport_name))  
    
    #stores the results in variable
    #use fetchall() if needed
    data = cursor.fetchone()
    
    if(data):
        #airport exists
        error = "This airport already exists"
        cursor.close()
        return render_template('airline_staff_home.html', error=error)
    else:    
        ins = 'INSERT INTO airport VALUES(%s, %s)'
        cursor.execute(ins, (airport_name, airport_city))
        #commit changes
        conn.commit()
        cursor.close()
        return render_template('airline_staff_success.html')
        
#View all booking agents
@app.route('/view_booking_agents')
def viewAgents():
    username = session['username']

    #cursor to send queries
    cursor = conn.cursor() 

    #verify user 
    query = 'SELECT username FROM airline_staff WHERE username = %s'
    cursor.execute(query, (username))
   
    #stores the results in variable
    #use fetchall() if needed
    data = cursor.fetchone()
   
    cursor.close
   
    if(not data):
        return 0
       
    #cursor to send queries
    cursor = conn.cursor()
    
    #execute query
    #PAST MONTH
    #PAST YEAR
    query = 'SELECT TOP 5 booking_agent.email, sum(purchases) FROM booking_agent, purchases WHERE purchases.booking_agent_id = booking_agent.booking_agent_id GROUP BY booking_agent.email'
    cursor.execute(query)  
    
    #stores the results in variable
    #use fetchall() if needed
    data1 = cursor.fetchall()
    
    cursor.close()
    
    #cursor to send queries
    cursor = conn.cursor()
    
    #execute query
    #ASK HOW TO CALCULATE COMMISSION
    #PAST YEAR
    query = 'SELECT TOP 5 booking_agent.email, sum(flight.price) FROM booking_agent, purchases, flight, ticket WHERE purchases.booking_agent_id = booking_agent.booking_agent_id and purchases.ticket_id = ticket.ticket_id and ticket.airline_name = flight.airline_name and ticket.flight_num = flight.flight_num GROUP BY booking_agent.email'
    cursor.execute(query)  
    
    #stores the results in variable
    #use fetchall() if needed
    data2 = cursor.fetchall()
    
    cursor.close()
    
    
    return render_template('view_booking_agents.html', agentList1 = data1, agentList2 = data2)
    
#View frequent customers
@app.route('/frequent_customers', methods=['GET', 'POST'])
def freqCust():    
    username = session['username']

    #cursor to send queries
    cursor = conn.cursor() 

    #verify user 
    query = 'SELECT username FROM airline_staff WHERE username = %s'
    cursor.execute(query, (username))
   
    #stores the results in variable
    #use fetchall() if needed
    data = cursor.fetchone()
   
    cursor.close
   
    if(not data):
        return 0
   
    #execute query
    #PAST YEAR
    #query = 'SELECT max(sum(purchases)), customer.email FROM customer, purchases WHERE purchases.customer_email = customer.email GROUP BY customer.email'
    query = 'SELECT customer.email, COUNT(*) FROM customer, purchases WHERE purchases.customer_email = customer.email GROUP BY purchases.customer_email'    
    cursor.execute(query)  
   
    #stores the results in variable
    #use fetchall() if needed
    data1 = cursor.fetchall()
        
    cursor.close()
   
    #cursor to send queries
    cursor = conn.cursor()
    
    #find airline staff airline
    query = 'SELECT airline_name FROM airline_staff where username = %s'
    cursor.execute(query, (username))
    
    airline = cursor.fetchone()
    
    #execute query
    #flights on airline
    query = 'SELECT ticket.flight_num FROM ticket, purchases WHERE purchases.customer_email = data1 AND ticket.ticket_id = purchases.ticket_id AND ticket.airline_name = %s GROUP BY purchases.email'
    cursor.execute(query, (data1, airline))  
    
    #stores the results in variable
    #use fetchall() if needed
    data2 = cursor.fetchall()
    
    cursor.close()
    
    
    return render_template('frequent_customers.html', data1 = data1, data2 = data2)
    
#View reports
@app.route('/view_reports', methods=['GET', 'POST'])
def viewReports():
    username = session['username']

    #cursor to send queries
    cursor = conn.cursor() 

    #verify user 
    query = 'SELECT username FROM airline_staff WHERE username = %s'
    cursor.execute(query, (username))
   
    #stores the results in variable
    #use fetchall() if needed
    data = cursor.fetchone()
   
    cursor.close
   
    if(not data):
        return 0
        
    #cursor to send queries
    cursor = conn.cursor()
    
    #execute query
    #flights on airline
    query = 'SELECT sum(purchases) FROM purchases GROUP BY purchase_date'
    cursor.execute(query)  
    
    #stores the results in variable
    #use fetchall() if needed
    data2 = cursor.fetchall()
    
    cursor.close()
    
    return render_template('reports.html', data2 = data2)
        

#Success
@app.route('/airline_staff_success', methods = ['GET', 'POST'])
def airlineStaffSuccess():
    return render_template('airline_staff_success.html') 

@app.route('/booking_agent_success', methods = ['GET', 'POST'])
def bookingAgentSuccess():
    return render_template('booking_agent_success.html') 

@app.route('/customer_success', methods = ['GET', 'POST'])
def customerSuccess():
    return render_template('customer_success.html') 
#==============================================================================
#     if request.method == 'GET':
#         return render_template('success.html')
#     
#     usertype = session['usertype']
#     return render_template(usertype+'_home.html')
#==============================================================================
    
        
app.secret_key = 'secret'    
    
#Run the app on localhost prot 5000
if __name__ == "__main__":
    app.run('127.0.0.1', 5000, debug = True)    
