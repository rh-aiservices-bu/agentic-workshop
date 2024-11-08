// src/components/Day.js
import React from 'react';
import './Day.css';

const Day = ({ day, schedules }) => {
  return (
    <div className="day">
      <h3>{day}</h3>
      <div className="schedule-list">
        {schedules.length > 0 ? (
          schedules.map((schedule) => (
            <div key={schedule.sid} className="schedule-item">
              <strong>{schedule.name}</strong>
              <p>{schedule.content}</p>
              <p>{new Date(schedule.start_time).toLocaleTimeString()} - {new Date(schedule.end_time).toLocaleTimeString()}</p>
            </div>
          ))
        ) : (
          <p className="no-schedule">No schedule</p>
        )}
      </div>
    </div>
  );
};

export default Day;
