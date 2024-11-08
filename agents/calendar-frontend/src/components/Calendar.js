// src/components/Calendar.js
import React, { useEffect, useState } from 'react';
import axios from 'axios';
import Day from './Day';
import './Calendar.css';

const Calendar = () => {
  const [schedules, setSchedules] = useState([]);
  const [showForm, setShowForm] = useState(false);
  const [currentMonth, setCurrentMonth] = useState(new Date().getMonth());
  const [newSchedule, setNewSchedule] = useState({
    sid: "",
    name: "",
    content: "",
    category: "Business",
    level: 1,
    status: 0.0,
    creation_time: "",
    start_time: "",
    end_time: ""
  });

  // Fetch schedules when the component mounts or the month changes
  useEffect(() => {
    fetchSchedules();
  }, [currentMonth]);

  // Function to fetch schedules from the backend
  const fetchSchedules = () => {
    axios.get('http://127.0.0.1:8000/schedules')
      .then((response) => {
        setSchedules(response.data);
      })
      .catch((error) => {
        console.error('Error fetching schedules:', error);
      });
  };

  // Handle month navigation
  const handleMonthChange = (increment) => {
    setCurrentMonth((prev) => (prev + increment + 12) % 12);
  };

  // Handle form input changes
  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setNewSchedule((prev) => ({ ...prev, [name]: value }));
  };

  // Handle form submission
  const handleFormSubmit = async (e) => {
    e.preventDefault();

    // Automatically set the creation_time to the current date and time
    const currentDateTime = new Date().toISOString().slice(0, 19).replace('T', ' ');

    // Prepare the schedule data with correct types
    const formattedSchedule = {
      ...newSchedule,
      creation_time: currentDateTime,
      status: parseFloat(newSchedule.status), // Ensure status is a float
      level: parseInt(newSchedule.level),     // Ensure level is an integer
    };

    try {
      const response = await axios.post('http://127.0.0.1:8000/schedules', formattedSchedule, {
        headers: {
          'Content-Type': 'application/json',
        },
      });
      setSchedules([...schedules, response.data]);
      setShowForm(false);
    } catch (error) {
      console.error('Error creating schedule:', error.response?.data || error.message);
    }
  };

  // Calculate the number of days in the current month
  const daysInMonth = new Date(2024, currentMonth + 1, 0).getDate();
  const daysArray = Array.from({ length: daysInMonth }, (_, i) => i + 1);

  return (
    <div>
      <h2>Schedule Calendar</h2>
      <div className="month-navigation">
        <button onClick={() => handleMonthChange(-1)}>Previous Month</button>
        <span>{new Date(2024, currentMonth).toLocaleString("default", { month: "long" })}</span>
        <button onClick={() => handleMonthChange(1)}>Next Month</button>
      </div>

      <button onClick={() => setShowForm(!showForm)}>
        {showForm ? "Close" : "Add New Schedule"}
      </button>

      {/* Schedule creation form */}
      {showForm && (
        <form onSubmit={handleFormSubmit} className="schedule-form">
          <input type="text" name="sid" placeholder="ID" onChange={handleInputChange} required />
          <input type="text" name="name" placeholder="Name" onChange={handleInputChange} required />
          <input type="text" name="content" placeholder="Content" onChange={handleInputChange} />
          <input type="datetime-local" name="start_time" onChange={handleInputChange} required />
          <input type="datetime-local" name="end_time" onChange={handleInputChange} required />
          <button type="submit">Create Schedule</button>
        </form>
      )}

      {/* Display the calendar */}
      <div className="calendar">
        {daysArray.map((day) => (
          <Day key={day} day={day} schedules={schedules.filter(schedule => {
            const scheduleDate = new Date(schedule.start_time);
            return (
              scheduleDate.getDate() === day &&
              scheduleDate.getMonth() === currentMonth
            );
          })} />
        ))}
      </div>
    </div>
  );
};

export default Calendar;
