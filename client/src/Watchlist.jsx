
import React, { useState, useEffect, useContext } from 'react'
import { UserContext } from './UserContext';
import { convertToLocaleTimeString } from './utils.js';

function Stock(props) {
  const {user} = useContext(UserContext);


  const onDeleteFromWatchlist = async() => {
    try {
      const response = await fetch(`http://localhost:8000/v1/users/${user.userId}/watch_list/${props.security_id}`, {
        method: 'DELETE',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ "security_id": props.security_id }),
    }).then(() => {
      props.fetchWatchlist();
    })
  } catch (error) {
      console.error('Error deleting from watchlist', error);
    }
  }
    return (
      <div className='stock'>
        <p>{props.ticker}, {props.name}, ${props.last_price}</p>
        <p>last_updated: {convertToLocaleTimeString(props.last_updated)}</p>
        <button onClick={onDeleteFromWatchlist}>Delete</button>
      </div>
    )
}

export function Watchlist({watchlist, fetchWatchlist}) {
    const {user} = useContext(UserContext);
    const [buttonStatus, setButtonStatus] = useState(false);
    const [message, setMessage] = useState("");
    const [messages, setMessages] = useState([]);
    const [currentPage, setCurrentPage] = useState(1);
    const itemsPerPage = 5;

    const indexOfLastItem = currentPage * itemsPerPage;
    const indexOfFirstItem = indexOfLastItem - itemsPerPage;

    const handleNextPage = () => {
      setCurrentPage(prevPage => prevPage + 1);
    };
    
    const handlePrevPage = () => {
      setCurrentPage(prevPage => Math.max(prevPage - 1, 1));
    };

    if (!user) return null;

    useEffect(() => {
      fetchWatchlist();
      const interval = setInterval(fetchWatchlist, 5000);
  
      // Clean up the interval to prevent memory leaks
      return () => clearInterval(interval);
    }, []);

    return (
      <div className='watchlist'>
        <h3>Watchlist</h3>
        {(watchlist && watchlist.length > 0)
        ? 
        watchlist
        .slice((currentPage - 1) * itemsPerPage, currentPage * itemsPerPage)
        .map((stock, index) => (
          <Stock key={index} ticker={stock.ticker} name={stock.name} fetchWatchlist={fetchWatchlist} security_id={stock.security_id} last_updated = {stock.last_updated} last_price={stock.last_price}/>
        )) 
        : <p>No stocks to search</p>}
         {/* Pagination controls */}
    <button onClick={handlePrevPage} disabled={currentPage === 1}>Previous</button>
    <span>Page {currentPage}</span>
    <button onClick={handleNextPage}>Next</button>
      </div>
    )
  }
