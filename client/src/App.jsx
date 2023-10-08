import './App.css';
import { LoginForm } from './LoginForm';
import { UserContext } from './UserContext';
import { useState, useCallback, useMemo, useContext, useEffect } from 'react';
import { User } from "./User.jsx";
import { Watchlist } from "./Watchlist";


function Search() {
  const [search, setSearch] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetch('http://localhost:8000/v1/securities/search?q=albert', {
      method: 'GET',
      headers: { 'Content-Type': 'application/json' }
    })
    .then((response) => response.json())
    .then((data) => {
      setSearch(data);
      console.info('Search loaded successfully');
    })
    .catch((error) => {
      console.error('Unable to load search', error);
    });
  }, []);

  return (
    <div className='search'>
      <h3>Search</h3>
      {("search" in search) && (search["search"] && search["search"].length)
      ? search["search"].map((stock,index) => (
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
