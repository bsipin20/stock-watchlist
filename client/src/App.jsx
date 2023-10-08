import './App.css';
import { LoginForm } from './LoginForm';
import { UserContext } from './UserContext';
import { useState, useCallback, useMemo, useContext, useEffect } from 'react';
import { User } from "./User.jsx";
import { Watchlist } from "./Watchlist";


function Search() {
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
      debugger;
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
      {("search" in searchResults) && (searchResults["search"] && searchResults["search"].length)
      ? searchResults["search"].map((stock,index) => (
        <Stock ticker={stock.ticker} last_price={stock.last_price} name={stock.name} />
      )) : <p>Empty search</p>}
    </div>
  )
}

function App() {
  const [user, setUser] = useState(null);
  const login = useCallback((u) => setUser(u), []);
  const logout = useCallback(() => setUser(null), []);
  const value = useMemo(() => ({ user, login, logout }), [user, login, logout]);
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
            <Search />
          </section>
        )}
        {user && (
          <section>
            <Watchlist />
          </section>
        )}
      </div>
    </UserContext.Provider>
  );
}

export default App;
