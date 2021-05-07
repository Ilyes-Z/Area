import { HashRouter as Router, Switch } from 'react-router-dom';
import { getRoutes } from 'routes';

import Header from 'components/Header/Header';
import Route from 'components/MyRoute/MyRoute';

function App() {

  return (
    <Router>
      <div className='app'>
        <div className='header'>
          <Header />
        </div>
        <div className='content'>
          <Switch>
            {getRoutes().map((route, index) => {
              return <Route exact {...route} key={index} />
            })}
          </Switch>
        </div>
      </div>
    </Router>
  );
}

export default App;
