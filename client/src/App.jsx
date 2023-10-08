import './App.css';
import { LoginForm } from './LoginForm';
import { UserContext } from './UserContext';
import { useState, useCallback, useMemo, useContext, useEffect } from 'react';
import { User } from "./User.jsx";
import { Watchlist } from "./Watchlist";
import { on } from 'events';


function SearchResultStock(props) {

  const [ticker, setTicker] = useState(props.ticker); 
  const onAddToWatchlist = async(event) => {
    event.preventDefault();
    try {
      const response = await fetch(`http://localhost:8000/v1/users/1/watch_list/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ ticker: props.ticker }),
      });
      const data = await response.json();
      console.info('Added to watchlist successfully');
      props.onUpdate();
    } catch (error) {
      console.errog('Error adding to watchlist', error);
    }
  }

  return (
    <div className='stock'>
      <h3>Sym: {props.ticker} Stock: {props.name}</h3>
      <button onClick={onAddToWatchlist}>Add to watchlist</button>  
    </div>
  )
}

function Search({onUpdate}) {
  const [query, setQuery] = useState('');
  const [searchResults, setSearchResults] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const handleInputChange = (event) => {
    setQuery(event.target.value);
  }

  const handleSubmit = async(event) => {
    event.preventDefault();

    try {
      const response = await fetch(`http://localhost:8000/v1/securities/search?query=${query}`, {
        method: 'GET',
        headers: { 'Content-Type': 'application/json' }
      });
      const data = await response.json();
      setSearchResults(data);
      console.info('Search loaded successfully');
    } catch (error) {
      console.errog('Error loading search', error);
    }
  };

  return (
    <div className='search'>
      <form onSubmit={ handleSubmit }>
        <input
          type="text"
          id="search"
          placeholder="Search"
          value={query}
          onChange={handleInputChange}
          />
      </form>
      {("results" in searchResults) && (searchResults["results"] && searchResults["results"]["securities"].length > 0)
      ? searchResults["results"]["securities"].map((stock, index) => (
        <SearchResultStock onUpdate={onUpdate} ticker={stock.ticker} last_price={stock.last_price} name={stock.name} />
      )) : <p>Empty search</p>}
    </div>
  )
}

function App() {
  const [user, setUser] = useState(null);
  const [watchlist, setWatchlist] = useState([]);
  const login = useCallback((u) => setUser(u), []);
  const logout = useCallback(() => setUser(null), []);
  const value = useMemo(() => ({ user, login, logout }), [user, login, logout]);

  const fetchWatchlist = () => {
    {
      fetch('http://localhost:8000/v1/users/1/watch_list', {
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
    fetchWatchlist();
    setWatchlist(watchlist);
  }, []);

  const handleWatchlistUpdate = () => {
    setWatchlist(watchlist);
  }

  return (
    <UserContext.Provider value={value}>
      <div className="app">
        <LoginForm />
        <header>
          <h1>Albert stock watch</h1>
          <User />
        </header>
        {user && (
          <section>
            <Search onUpdate={fetchWatchlist}/>
          </section>
        )}
        {user && (
          <section>
            <Watchlist watchlist={watchlist}/>
          </section>
        )}
      </div>
    </UserContext.Provider>
  );
}

export default App;
