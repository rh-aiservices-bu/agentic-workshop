// src/components/Calendar.js
import React, { useEffect, useState } from 'react';
import axios from 'axios';
import Day from './Day';
import './Calendar.css';

const Calendar = () => {
  const [schedules, setSchedules] = useState([]);

  useEffect(() => {
    // Fetch schedules from the backend
    axios.get('http://127.0.0.1:8000/schedules')
      .then((response) => {
        setSchedules(response.data);
      })
      .catch((error) => {
        console.error('Error fetching schedules:', error);
      });
  }, []);

  // Generate days for a basic monthly calendar
  const daysInMonth = Array.from({ length: 30 }, (_, i) => i + 1);

  return (
    <div className="calendar">
      {daysInMonth.map((day) => (
        <Day key={day} day={day} schedules={schedules.filter(schedule => {
          const scheduleDate = new Date(schedule.start_time);
          return scheduleDate.getDate() === day;
        })} />
      ))}
    </div>
  );
};

export default Calendar;
