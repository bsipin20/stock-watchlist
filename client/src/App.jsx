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
      });
      props.fetchWatchlist();
      console.info('Added to watchlist successfully');
    } catch (error) {
      console.error('Error adding to watchlist', error);
    }
  }

  return (
    <div className='stock'>
      <h3>Ticker: {props.ticker}: {props.name} </h3>
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
  const [currentPage, setCurrentPage] = useState(1);
  const itemsPerPage = 3;

  const indexOfLastItem = currentPage * itemsPerPage;
  const indexOfFirstItem = indexOfLastItem - itemsPerPage;
  const handleNextPage = () => {
    setCurrentPage(prevPage => prevPage + 1);
  };
  
  const handlePrevPage = () => {
    setCurrentPage(prevPage => Math.max(prevPage - 1, 1));
  };

  const handleInputChange = (event) => {
    setQuery(event.target.value);
  }

  const onRemoveTickerFromSearchResults = (ticker) => {
    const newSearchResults = searchResults["results"].filter((stock) => stock.ticker !== ticker);
    setSearchResults(newSearchResults);
  }

  const handleSubmit = async(event) => {
    event.preventDefault();

    try {
      const response = await fetch(`http://localhost:8000/v1/securities/search?query=${query}`, {
        method: 'GET',
        headers: { 'Content-Type': 'application/json' }
      });
      if (!response.ok) {
        const errorMessage = await response.json();
        setSearchResults([]);
        throw new Error(errorMessage["error"]);
      }
      setError(null);
      const data = await response.json();
      setSearchResults(data);

      console.info('Search loaded successfully');
    } catch (error) {
      setError(error.message);
    }
  };

  return (
    <div className='search'>
      {error && <p>Error: {error}</p>}
      <form onSubmit={ handleSubmit }>
        <input
          type="text"
          id="search"
          placeholder="Search"
          value={query}
          onChange={handleInputChange}
          />
      </form>
      {("results" in searchResults) && (searchResults["results"] && searchResults["results"].length > 0)
      ? searchResults["results"]
      .slice((currentPage - 1) * itemsPerPage, currentPage * itemsPerPage)
      .map((stock, index) => (
        <SearchResultStock key={stock.id} fetchWatchlist={fetchWatchlist} onRemoveTickerFromSearchResults= {onRemoveTickerFromSearchResults} name = {stock.name} ticker={stock.ticker} id={stock.id} /> 
      )) : <p>Empty search</p>}
          <button onClick={handlePrevPage} disabled={currentPage === 1}>Previous</button>
    <span>Page {currentPage}</span>
    <button onClick={handleNextPage}>Next</button>
    </div>
  )
}

function Content({fetchWatchlist, watchlist}) {
 const {user} = useContext(UserContext);

  useEffect(() => {
    fetchWatchlist();
  }, []);

  return(
    <section>
      <Watchlist watchlist={watchlist} fetchWatchlist={fetchWatchlist}/>
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
      .then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json();  // Parse the response as JSON
      })
      .then((data) => {
        setWatchlist(data['results']);
      })
      .catch((error) => {
        console.error('Unable to load watchlist', error);
      });
    }
  };

  useEffect(() => {
    const storedUser = JSON.parse(localStorage.getItem('user'));
    if (storedUser) {
      setUser(storedUser);
    }
  }, []);

  const userContextValue = useMemo(() => ({ user, login, logout }), [user, login, logout]);

  return (
    <UserContext.Provider value={userContextValue}>
      <div className="app">
        <LoginForm onLogin ={login}/>
        <header>
          <h1>Stock watch</h1>
          <User />
        </header>
        {user && (
          <section>
            <Search watchlist={watchlist} fetchWatchlist={fetchWatchlist} />
          </section>
        )}
        {user && <Content
                  watchlist={watchlist}
                  fetchWatchlist={fetchWatchlist}
                  />}
      </div>
    </UserContext.Provider>
  );
}

export default App;
