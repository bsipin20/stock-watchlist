import './App.css';

import { LoginForm } from './LoginForm';
import { UserContext } from './UserContext';
import { useState, useCallback, useMemo, useContext, useEffect } from 'react';
import { User } from "./User.jsx";
import { Watchlist } from "./Watchlist";

function SearchResultStock(props) {
  const [ticker, setTicker] = useState(props.ticker); 
  const { user, logout } = useContext(UserContext);

  const updateWatchlist = async(event) => {
    event.preventDefault();
    try {
      const response = await fetch(`http://localhost:8000/v1/users/${user.userId}/watch_list/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ security_id: props.id }),
      }).then(() => {
        props.fetchWatchlist();
      })
      console.info('Added to watchlist successfully');
    } catch (error) {
      console.error('Error adding to watchlist', error);
    }
  }

  return (
    <div className='stock'>
      <h3>Sym: {props.ticker} Stock: {props.name}</h3>
      <button onClick={updateWatchlist}>Add to watchlist</button>  
    </div>
  )
}

function Search({fetchWatchlist}) {
  const { user, logout } = useContext(UserContext);
  const [query, setQuery] = useState('');
  const [searchResults, setSearchResults] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const handleInputChange = (event) => {
    setQuery(event.target.value);
  }

  const onRemoveTickerFromSearchResults = (ticker) => {
    const newSearchResults = searchResults["results"]["securities"].filter((stock) => stock.ticker !== ticker);
    setSearchResults(newSearchResults);
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
        <SearchResultStock key={stock.id} fetchWatchlist={fetchWatchlist} onRemoveTickerFromSearchResults= {onRemoveTickerFromSearchResults} ticker={stock.ticker} id={stock.id} /> 
      )) : <p>Empty search</p>}
    </div>
  )
}

function Content({watchlist, setWatchlist, fetchWatchlist}) {
 const {user} = useContext(UserContext);

  return(
    <section>
      <Watchlist watchlist={watchlist} fetchWatchlist={fetchWatchlist} setWatchlist={setWatchlist} />
    </section>
  )
}

function App() {
 const [user, setUser] = useState(null);

  const login = useCallback((u) => {
    setUser(u);
    localStorage.setItem('user', JSON.stringify(u));  // Save user to localStorage
  }, []);

  const logout = useCallback(() => {
    setUser(null);
    localStorage.removeItem('user');  // Remove user from localStorage on logout
  }, []);

  const [watchlist, setWatchlist] = useState([]);

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


  const userContextValue = useMemo(() => ({ user, login, logout }), [user, login, logout]);

  return (
    <UserContext.Provider value={userContextValue}>
      <div className="app">
        <LoginForm onLogin ={login}/>
        <header>
          <h1>Albert stock watch</h1>
          <User />
        </header>
        {user && (
          <section>
            <Search fetchWatchlist={fetchWatchlist} />
          </section>
        )}
        {user && <Content
                  watchlist={watchlist}
                  setWatchlist={setWatchlist}
                  fetchWatchlist={fetchWatchlist}
                  />}
      </div>
    </UserContext.Provider>
  );
}

export default App;
