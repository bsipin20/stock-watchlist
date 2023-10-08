import './App.css';
import { LoginForm } from './LoginForm';
import { UserContext } from './UserContext';
import { useState, useCallback, useMemo, useContext, useEffect } from 'react';
import { User } from "./User.jsx";


function Stock(props) {
  return (
    <div className='stock'>
      <h3>{props.ticker}</h3>
      <p>{props.name}</p>
      <p>{props.last_price}</p>
    </div>
  )
}

function Watchlist(props) {
  const {user} = useContext(UserContext);

  if (!user) return null;
  const [watchlist, setWatchlist] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
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
  }, []);

  return (
    <div className='watchlist'>
      <h3>Watchlist</h3>
      {watchlist["watch_list"].length ? watchlist["watch_list"].map((stock,index) => (
        <Stock ticker={stock.ticker} last_price={stock.last_price} name={stock.name} />
      )) : <p>Empty watchlist</p>}
    </div>
  )
}


function App() {
  const [user, setUser] = useState(null);
  const login = useCallback((u) => setUser(u), []);
  const logout = useCallback(() => setUser(null), []);
  const value = useMemo(() => ({ user, login, logout }), [user, login, logout]);
  const stock_data = [
    { 'ticker': 'AAPL', 'last_price': 100.00, 'name': "Apple Inc." },
    { 'ticker': 'GOOG', 'last_price': 1000.00, 'name': "Alphabet Inc." },
    { 'ticker': 'MSFT', 'last_price': 200.00, 'name': "Microsoft Corporation" },
    { 'ticker': 'AMZN', 'last_price': 3000.00, 'name': "Amazon.com, Inc." }
  ]


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
            <Watchlist />
          </section>
        )}
      </div>
    </UserContext.Provider>
  );
}

export default App;
