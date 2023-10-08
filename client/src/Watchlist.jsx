
import React, { useState, useEffect, useContext } from 'react'
import { UserContext } from './UserContext';

function Stock(props) {
    return (
      <div className='stock'>
        <h3>{props.ticker}</h3>
        <p>{props.name}</p>
        <p>{props.last_price}</p>
      </div>
    )
}

export function Watchlist({watchlist}) {
    const {user} = useContext(UserContext);
  
    if (!user) return null;
   // const [loading, setLoading] = useState(true);
   // const [error, setError] = useState(null);
  
    // useEffect(() => {
    //   fetch('http://localhost:8000/v1/users/1/watch_list', {
    //     method: 'GET',
    //     headers: { 'Content-Type': 'application/json' }
    //   })
    //   .then((response) => response.json())
    //   .then((data) => {
    //     handleUpdateWatchlist(data);
    //     console.info('Watchlist loaded successfully');
    //   })
    //   .catch((error) => {
    //     console.error('Unable to load watchlist', error);
    //   });
    // }, []);
  
    return (
      <div className='watchlist'>
        <h3>Watchlist</h3>
        {("watch_list" in watchlist) && (watchlist["watch_list"] && watchlist["watch_list"].length)
        ? watchlist["watch_list"].map((stock,index) => (
          <Stock ticker={stock.ticker} last_price={stock.last_price} name={stock.name} />
        )) : <p>Empty watchlist</p>}
      </div>
    )
  }
