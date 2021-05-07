import { Route, Redirect } from 'react-router-dom';
import { getPath } from 'routes';

import isAuth from 'services/security/isAuth';
import hasRoles from 'services/security/hasRoles';

function MyRoute({ component: Component, needAuth, authAccess, roles, path }) {

  return (
    <Route
      path={path}
      exact={true}
      render={props =>
        needAuth ? (
          isAuth() ? (
            hasRoles(roles) ? (
              <Component {...props} />
            ) : (
              <Redirect to={getPath('dashboard')} />
            )
          ) : (
            <Redirect to={getPath('login')} />
          )
        ) : (
          !authAccess && isAuth() ? (
            <Redirect to={getPath('dashboard')} />
          ) : (
            <Component {...props} />
          )
        )
      }
    />
  );
}

export default MyRoute;