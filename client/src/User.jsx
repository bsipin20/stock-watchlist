import { useContext} from 'react';
import { UserContext } from "./UserContext.jsx";

export function User() {
  const { user, logout } = useContext(UserContext);

  if (!user) return null;

  return (
    <div className='user'>
      <h3>
        Welcome, {
          (user.username)
            ? `${user.name}` 
            : user.email
        }!
      </h3>
      <button onClick={ logout }>Logout</button>
    </div>
  );
}
