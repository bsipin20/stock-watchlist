import { createContext } from 'react';

const defaultUserContext = {
    user: null,
    login: () => {},
    logout: () => {}
  };
  
export const UserContext = createContext(defaultUserContext);
  
