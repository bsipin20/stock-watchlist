
import React, { useState, useEffect, useContext } from 'react'
import { UserContext } from './UserContext';

function Stock(props) {
  const {user} = useContext(UserContext);

  const onDeleteFromWatchlist = async() => {
    try {
      const response = await fetch(`http://localhost:8000/v1/users/${user.userId}/watch_list/`, {
        method: 'DELETE',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ "security_id": props.security_id }),
    });
      const data = await response.json();
  } catch (error) {
      console.error('Error deleting from watchlist', error);
    }
  }
    return (
      <div className='stock'>
        <h3>{props.ticker}</h3>
        <p>{props.last_price}</p>
        <p>last update: {props.last_updated}</p>
        <button onClick={onDeleteFromWatchlist}>Delete</button>
      </div>
    )
}

export function Watchlist({watchlist, setWatchlist}) {
    const {user} = useContext(UserContext);
    const [buttonStatus, setButtonStatus] = useState(false);
    const [message, setMessage] = useState("");
    const [messages, setMessages] = useState([]);

    if (!user) return null;

    const fetchWatchlist = () => {
      {
        fetch(`http://localhost:8000/v1/users/${user.userId}/watch_list`, {
          method: 'GET',
          headers: { 'Content-Type': 'application/json' }
        })
        .then((response) => response.json())
        .then((data) => {
          setWatchlist(data);
          console.info('Watchlist loaded successfully');
        })
        .catch((error) => {
          console.error('Unable to load watchlist', error);
        });
      }
    };

    useEffect(() => {
      setInterval(() => {
        fetchWatchlist();
      }, 5000);
    }, []); 


    return (
      <div className='watchlist'>
        <h3>Watchlist</h3>
        {("data" in watchlist) && (watchlist["data"] && watchlist["data"].length)
        ? 
        watchlist["data"].map((stock, index) => (
          <Stock ticker={stock.ticker} security_id = {stock.security_id} last_updated = {stock.last_updated} last_price={stock.last_price}/>
        )) : <p>No stocks in watchlist</p>}
      </div>
    )
  }
