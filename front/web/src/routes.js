import Home from 'scenes/Home/Home';

import Login from 'scenes/Auth/Login/Login';
import Register from 'scenes/Auth/Register/Register';
import Recuperation from 'scenes/Auth/Recuperation/Recuperation';

import Apk from 'scenes/Apk/Apk';

import Dashboard from 'scenes/Dashboard/Dashboard';
import Services from 'scenes/Services/Services';
import Areas from 'scenes/Areas/Areas';
import Profile from 'scenes/Profile/Profile';

import Admin from 'scenes/Admin/Admin';


const routes = [
  {
    'name': 'home',
    'path': '/',
    'component': Home,
    'needAuth': false,
    'authAccess': false,
  },
  {
    'path': '/auth',
    'routes': [
      {
        'name': 'login',
        'path': '/login',
        'component': Login,
        'needAuth': false,
        'authAccess': false,
      },
      {
        'name': 'register',
        'path': '/register',
        'component': Register,
        'needAuth': false,
        'authAccess': false,
      },
      {
        'name': 'recuperation',
        'path': '/recuperation',
        'component': Recuperation,
        'needAuth': false,
        'authAccess': false,
      },
    ],
  },
  {
    'name': 'apk',
    'path': '/apk',
    'component': Apk,
    'needAuth': false,
    'authAccess': true,
  },
  {
    'name': 'dashboard',
    'path': '/dashboard',
    'component': Dashboard,
    'needAuth': true,
  },
  {
    'name': 'services',
    'path': '/services',
    'component': Services,
    'needAuth': true,
  },
  {
    'name': 'areas',
    'path':'/areas',
    'component': Areas,
    'needAuth': true,
  },
  {
    'name': 'profile',
    'path':'/profile',
    'component': Profile,
    'needAuth': true,
  },
  {
    'name': 'admin',
    'path': '/admin',
    'component': Admin,
    'roles': ['ROLE_ADMIN'],
    'needAuth': true,
  },
]

const compile = (parentRoute, subRoutes) => {
  return subRoutes.flatMap(subRoute => {
    const newRoute = {
      name: subRoute.name,
      path: parentRoute.path + subRoute.path,
      component: subRoute.component,
      needAuth: subRoute.needAuth,
      authAccess: subRoute.authAccess,
      roles: (parentRoute.roles || []).concat((subRoute.roles || [])),
    };
    return (subRoute.routes) ? [...compile(newRoute, subRoute.routes)] : newRoute;
  });
}

const getRoutes = () => {
  return compile({ name: '', path: '' }, routes);
}

const getPath = (name, params) => {
  const routeFound = getRoutes().find(route => route.name === name);
  let path = routeFound ? routeFound.path : null;

  if (path && params) {
    Object.entries(params).forEach((key, value) => {
      path = path ? path.replace(`:${key}`, value) : '';
    });
  }
  return path;
}

export { getRoutes, getPath };